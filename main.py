import uuid

from langchain.schema import AIMessage, BaseMessage, HumanMessage

from src.agentic.agents.researcher import researcher
from src.agentic.agents.state import State, create_initial_state
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
        stream_mode="values",
        config={"recursion_limit": 200, "configurable": {"thread_id": thread_id}},
    )
    final_state: State
    for chunk in result:
        last_message: BaseMessage = chunk["messages"][-1]
        if isinstance(last_message, AIMessage) or isinstance(
            last_message, HumanMessage
        ):
            last_message.pretty_print()
        final_state = State.model_validate(chunk)


if __name__ == "__main__":
    ask("DeerFlow 的 Deep Think 功能用的是推理模型？")
