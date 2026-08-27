import datetime


def get_current_date() -> str:
    """Return the current date in ISO format."""
    return datetime.date.today().isoformat()


GET_CURRENT_DATE_TOOL = {
    "type": "function",
    "function": {
        "name": "get_current_date",
        "description": "Return the current date.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}


TOOL_REGISTRY = {
    "get_current_date": get_current_date,
}