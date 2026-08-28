TASK_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new study task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Short title derived from the user's request.",
                    },
                    "description": {
                        "type": ["string", "null"],
                        "description": "Optional extra task details. Do not invent details.",
                    },
                    "due_date": {
                        "type": ["string", "null"],
                        "description": "Optional due date in YYYY-MM-DD format.",
                    },
                },
                "required": ["title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "Return all study tasks.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_task",
            "description": "Return a study task by its ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task.",
                    }
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a study task as completed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task to complete.",
                    }
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "reopen_task",
            "description": "Mark a completed study task as incomplete.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task to reopen.",
                    }
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update the title, description, or due date of a study task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task to update.",
                    },
                    "title": {
                        "type": ["string", "null"],
                        "description": "Optional new title.",
                    },
                    "description": {
                        "type": ["string", "null"],
                        "description": "Optional new description.",
                    },
                    "due_date": {
                        "type": ["string", "null"],
                        "description": "Optional new due date in YYYY-MM-DD format.",
                    },
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_task_due_date",
            "description": "Update or remove the due date of a study task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task.",
                    },
                    "due_date": {
                        "type": ["string", "null"],
                        "description": "New due date in YYYY-MM-DD format, or null to remove it.",
                    },
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a study task by its ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task to delete.",
                    }
                },
                "required": ["task_id"],
            },
        },
    },
]