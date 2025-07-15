import json
import os

from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import BaseMessage
from langchain_core.messages import convert_to_openai_messages


class LocalTracer(BaseCallbackHandler):
    id_counter = 0
    _storage_path: str

    def __init__(self, storage_path: str):
        self._storage_path = os.path.abspath(storage_path)
        os.makedirs(self._storage_path, exist_ok=True)

    def next_id(self):
        self.id_counter += 1
        return self.id_counter

    def on_chat_model_start(
        self, serialized: dict, message_lists: list[list[BaseMessage]], **kwargs
    ):
        params: dict = kwargs["invocation_params"]
        for message_list in message_lists:
            chat_completion_params = params.copy()
            chat_completion_params["messages"] = convert_to_openai_messages(
                message_list
            )
            self.log_chat_completion(chat_completion_params)

    def log_chat_completion(self, chat_completion_params: dict):
        file_name = os.path.join(
            self._storage_path,
            f"chat-completion-{self.next_id():03d}.json",
        )
        with open(file_name, "w") as f:
            json.dump(chat_completion_params, f, indent=2, ensure_ascii=False)
        print(f"********** Saved in {file_name} **********\n\n\n\n")
