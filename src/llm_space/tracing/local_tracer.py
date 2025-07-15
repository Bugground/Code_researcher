import json
import os
from uuid import UUID

from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import BaseMessage, LLMResult
from langchain_core.messages import convert_to_openai_messages


class LocalTracer(BaseCallbackHandler):
    id_counter = 0
    _storage_path: str

    def __init__(self, storage_path: str):
        self._storage_path = os.path.abspath(storage_path)
        os.makedirs(self._storage_path, exist_ok=True)

    def on_chat_model_start(
        self,
        serialized: dict,
        message_lists: list[list[BaseMessage]],
        *,
        run_id: UUID,
        **kwargs,
    ):
        params: dict = kwargs["invocation_params"]
        for message_list in message_lists:
            chat_completion_params = params.copy()
            chat_completion_params["messages"] = convert_to_openai_messages(
                message_list
            )
            self.log_chat_completion(run_id, chat_completion_params)

    def on_llm_end(
        self,
        response: LLMResult,
        *,
        run_id: UUID,
        **kwargs,
    ):
        message = response.generations[0][0].message
        converted_message = convert_to_openai_messages([message])[0]
        self.update_chat_completion_response(run_id, converted_message)

    def log_chat_completion(self, run_id: UUID, data: dict):
        file_name = os.path.join(
            self._storage_path,
            f"run-{run_id}.json",
        )
        with open(file_name, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f'Saved in "{file_name}"')

    def update_chat_completion_response(self, run_id: UUID, response_message: dict):
        file_name = os.path.join(
            self._storage_path,
            f"run-{run_id}.json",
        )
        with open(file_name, "r") as f:
            existing_data = json.load(f)
        existing_data["messages"].append(response_message)
        with open(file_name, "w") as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
