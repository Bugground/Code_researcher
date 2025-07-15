import os

from langchain_openai import ChatOpenAI

from src.llm_space.tracing import LocalTracer


def create_ark_model(model: str = "doubao-1-5-pro-32k-250115") -> ChatOpenAI:
    return ChatOpenAI(
        model=model,
        base_url="https://ark-cn-beijing.bytedance.net/api/v3",
        api_key=os.getenv("DOUBAO_API_KEY"),
        temperature=0,
        top_p=0,
        max_retries=3,
    )


def create_gpt4o_model(model: str = "gpt-4o-2024-11-20") -> ChatOpenAI:
    return ChatOpenAI(
        model=model,
        base_url="https://search.bytedance.net/gpt/openapi/online/v2/crawl/openai/deployments",
        default_query={"api-version": "2023-03-15-preview"},
        default_headers={"api-key": os.getenv("GPT_OPEN_API_KEY"), "caller": "sxy"},
        temperature=0,
        top_p=0,
        max_retries=3,
    )


def create_chat_model() -> ChatOpenAI:
    # return create_ark_model()
    model = create_gpt4o_model()
    model.callbacks = [LocalTracer("./logs")]
    return model


if __name__ == "__main__":
    chat_model = create_chat_model()
    print(chat_model.invoke("你好").content)
