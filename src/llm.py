import re

import ollama

MODEL_NAME = "qwen3:1.7b"


def clean_response(content: str) -> str:
    """Remove leaked thinking content from the model response."""

    if "</think>" in content:
        content = content.split("</think>", 1)[1]

    content = re.sub(
        r"<think>.*?</think>",
        "",
        content,
        flags=re.DOTALL,
    )

    return content.strip()


def chat(messages: list[dict[str, str]]) -> str:
    """Send conversation messages to the local Ollama model."""

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=messages,
            think=False,
            stream=False,
        )

        return clean_response(response.message.content)

    except Exception as error:
        return f"LLM error: {error}"





# messages = [
#     {
#         "role": "user",
#         "content": "Reply with exactly: Study assistant ready",
#     }
# ]

# print(chat(messages))
