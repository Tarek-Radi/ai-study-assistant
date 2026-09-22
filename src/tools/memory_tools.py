from typing import Any

from src.memory.memory_store import (
    save_memory,
    get_memory,
    list_memories,
    delete_memory,
)


def save_user_memory(
    key: str,
    value: str,
) -> dict[str, Any]:
    """Save or update an important user memory."""

    cleaned_key = key.strip()
    cleaned_value = value.strip()

    if not cleaned_key:
        raise ValueError(
            "Memory key cannot be empty."
        )

    if not cleaned_value:
        raise ValueError(
            "Memory value cannot be empty."
        )

    memory = save_memory(
        key=cleaned_key,
        value=cleaned_value,
    )

    return {
        "memory": memory,
    }


def get_user_memory(
    key: str,
) -> dict[str, Any]:
    """Get one saved user memory."""

    cleaned_key = key.strip()

    if not cleaned_key:
        raise ValueError(
            "Memory key cannot be empty."
        )

    memory = get_memory(
        key=cleaned_key,
    )

    if memory is None:
        raise ValueError(
            f"Memory '{cleaned_key}' was not found."
        )

    return {
        "memory": memory,
    }


def list_user_memories() -> dict[str, Any]:
    """Return all saved user memories."""

    memories = list_memories()

    return {
        "count": len(memories),
        "memories": memories,
    }


def delete_user_memory(
    key: str,
) -> dict[str, Any]:
    """Delete one saved user memory."""

    cleaned_key = key.strip()

    if not cleaned_key:
        raise ValueError(
            "Memory key cannot be empty."
        )

    deleted = delete_memory(
        key=cleaned_key,
    )

    if not deleted:
        raise ValueError(
            f"Memory '{cleaned_key}' was not found."
        )

    return {
        "deleted": True,
        "key": cleaned_key,
    }


SAVE_USER_MEMORY_TOOL = {
    "type": "function",
    "function": {
        "name": "save_user_memory",
        "description": (
            "Save or update an important piece of information "
            "about the user that should persist across conversations."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "key": {
                    "type": "string",
                    "description": (
                        "A short stable identifier such as "
                        "'preferred_language'."
                    ),
                },
                "value": {
                    "type": "string",
                    "description": (
                        "The information to remember."
                    ),
                },
            },
            "required": [
                "key",
                "value",
            ],
        },
    },
}


GET_USER_MEMORY_TOOL = {
    "type": "function",
    "function": {
        "name": "get_user_memory",
        "description": (
            "Retrieve a specific saved memory about the user."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "key": {
                    "type": "string",
                    "description": (
                        "The memory key to retrieve."
                    ),
                },
            },
            "required": [
                "key",
            ],
        },
    },
}


LIST_USER_MEMORIES_TOOL = {
    "type": "function",
    "function": {
        "name": "list_user_memories",
        "description": (
            "List all saved long-term user memories."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
}


DELETE_USER_MEMORY_TOOL = {
    "type": "function",
    "function": {
        "name": "delete_user_memory",
        "description": (
            "Delete a saved user memory when the user asks "
            "to forget or remove it."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "key": {
                    "type": "string",
                    "description": (
                        "The memory key to delete."
                    ),
                },
            },
            "required": [
                "key",
            ],
        },
    },
}

if __name__ == "__main__":
    print(
        get_user_memory(
            key="preferred_language"
        )
    )

    print(
        list_user_memories()
    )

    print(
        delete_user_memory(
            key="preferred_language"
        )
    )