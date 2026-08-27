import json
import re

import ollama

from tools.basic_tools import GET_CURRENT_DATE_TOOL, TOOL_REGISTRY


MODEL_NAME = "qwen3:1.7b"
MAX_TOOL_ITERATIONS = 5


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
    """Send messages to the LLM and handle tool calls."""

    tools = [GET_CURRENT_DATE_TOOL]

    try:
        for _ in range(MAX_TOOL_ITERATIONS):
            response = ollama.chat(
                model=MODEL_NAME,
                messages=messages,
                tools=tools,
                think=False,
                stream=False,
            )

            tool_calls = response.message.tool_calls

            if not tool_calls:
                return clean_response(response.message.content)

            messages.append(response.message)

            for tool_call in tool_calls:
                tool_name = tool_call.function.name
                tool_arguments = tool_call.function.arguments

                print(f"Tool name: {tool_name}")
                print(f"Tool arguments: {tool_arguments}")

                tool_function = TOOL_REGISTRY.get(tool_name)

                if tool_function is None:
                    tool_result = {
                        "success": False,
                        "error": f"Unknown tool: {tool_name}",
                    }

                else:
                    try:
                        result = tool_function(**tool_arguments)

                        tool_result = {
                            "success": True,
                            "result": result,
                        }

                    except Exception as tool_error:
                        tool_result = {
                            "success": False,
                            "error": str(tool_error),
                        }

                print(f"Tool result: {tool_result}")

                messages.append(
                    {
                        "role": "tool",
                        "content": json.dumps(tool_result),
                    }
                )

        return "LLM error: maximum tool iterations reached."

    except Exception as error:
        return f"LLM error: {error}"