import json
import re

import ollama

from src.tools.basic_tools import (
    GET_CURRENT_DATE_TOOL,
    TOOL_REGISTRY as BASIC_TOOL_REGISTRY,
)

from src.tools.task_schemas import TASK_TOOLS

from src.tools.task_tools import (
    add_task,
    list_tasks,
    get_task,
    complete_task,
    reopen_task,
    update_task,
    update_task_due_date,
    delete_task,
)


MODEL_NAME = "qwen3:1.7b"
MAX_TOOL_ITERATIONS = 5


# ---------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------

TOOLS = [
    GET_CURRENT_DATE_TOOL,
    *TASK_TOOLS,
]


# ---------------------------------------------------------
# Tool registry
# ---------------------------------------------------------

TOOL_REGISTRY = {
    **BASIC_TOOL_REGISTRY,
    "add_task": add_task,
    "list_tasks": list_tasks,
    "get_task": get_task,
    "complete_task": complete_task,
    "reopen_task": reopen_task,
    "update_task": update_task,
    "update_task_due_date": update_task_due_date,
    "delete_task": delete_task,
}


# ---------------------------------------------------------
# Response cleaning
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# Agent loop
# ---------------------------------------------------------

def chat(messages: list[dict]) -> str:
    """Send messages to the LLM and handle tool calls."""

    try:
        for _ in range(MAX_TOOL_ITERATIONS):

            response = ollama.chat(
                model=MODEL_NAME,
                messages=messages,
                tools=TOOLS,
                think=False,
                stream=False,
            )

            tool_calls = response.message.tool_calls

            # No tool call means the LLM has produced its final answer.
            if not tool_calls:
                return clean_response(response.message.content)

            # Save the assistant message containing the tool call.
            messages.append(response.message)

            for tool_call in tool_calls:

                tool_name = tool_call.function.name
                tool_arguments = tool_call.function.arguments

                print(f"Tool name: {tool_name}")
                print(f"Tool arguments: {tool_arguments}")

                # Find the actual Python function.
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

                # Give the tool result back to the LLM.
                messages.append(
                    {
                        "role": "tool",
                        "content": json.dumps(
                            tool_result,
                            ensure_ascii=False,
                        ),
                    }
                )

        return "LLM error: maximum tool iterations reached."

    except Exception as error:
        return f"LLM error: {error}"