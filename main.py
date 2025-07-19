import json
import uuid

from langchain.schema import AIMessage, BaseMessage, HumanMessage

from src.agentic.agents.researcher import researcher
from src.agentic.agents.state import State, create_initial_state
from src.agentic.agents.state_compressor import compress_state
from src.workspace.project import Project


def ask(question: str):
    thread_id = str(uuid.uuid4())
    print(f"Thread ID: {thread_id}")
    project = Project(work_dir="/Users/henry/workspaces/bytedance/deer-flow")
    initial_state = create_initial_state(project)
    initial_state.messages.append(
        HumanMessage(content=f"# User's Problem and Requirements\n\n{question}")
    )
    result = researcher.stream(
        input=initial_state,
        config={"recursion_limit": 200, "configurable": {"thread_id": thread_id}},
        stream_mode="values",
    )
    final_state: State
    for chunk in result:
        last_message: BaseMessage = chunk["messages"][-1]
        if isinstance(last_message, AIMessage) or isinstance(
            last_message, HumanMessage
        ):
            last_message.pretty_print()
        final_state = State.model_validate(chunk)
    with open(f"./.threads/{thread_id}/final_state.json", "w") as f:
        json.dump(final_state.model_dump(), f, indent=2, ensure_ascii=False)
    compressed_state = compress_state(final_state, thread_id)
    with open(f"./.threads/{thread_id}/compressed_state.json", "w") as f:
        json.dump(compressed_state.model_dump(), f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    ask(
        "今天收到白帽子安全团队发来的邮件，邮件内容如下：\n\n"
        "Dear DeerFlow Team,\n\n"
        "We have found a CORS security vulnerability in your project. Please fix it as soon as possible.\n\n"
        "src/server/app.py	Updates CORS middleware configuration to use environment variables and restricts allowed methods/headers\n\n"
        "Best regards,\n"
        "White Hat Security Team"
    )
