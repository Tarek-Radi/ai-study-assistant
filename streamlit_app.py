from pathlib import Path

import streamlit as st

from src.llm import chat
from src.tools.task_tools import (
    add_task,
    complete_task,
    list_tasks,
    reopen_task,
)


SYSTEM_PROMPT = """
You are an AI Study Assistant.

Keep responses concise and focused unless the user asks for detail.
Do not invent references or sources.
If you are uncertain, say so clearly.
Use the conversation history to maintain context.

When the user asks for current or dynamic information that an available tool can provide,
you must use the appropriate tool instead of answering from memory.
""".strip()

KNOWLEDGE_DIR = Path("data/knowledge")


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 AI Study Assistant")
st.caption("Tools • PostgreSQL • Memory • RAG")


# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def get_message_value(message, key: str):
    """Read a value from either a dictionary or an Ollama message object."""

    if isinstance(message, dict):
        return message.get(key)

    return getattr(message, key, None)


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:
    st.header("Study Dashboard")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

        st.rerun()

    st.divider()

    # -----------------------------------------------------
    # Tasks
    # -----------------------------------------------------

    st.subheader("📝 Study Tasks")

    try:
        task_data = list_tasks()

        tasks = task_data["tasks"]

        if not tasks:
            st.caption("No study tasks yet.")

        for task in tasks:
            task_id = task["id"]
            completed = task["completed"]

            status = "✅" if completed else "⏳"

            st.markdown(
                f"{status} **{task['title']}**"
            )

            if task.get("due_date"):
                st.caption(
                    f"Due: {task['due_date']}"
                )

            if completed:
                if st.button(
                    "Reopen",
                    key=f"reopen_{task_id}",
                ):
                    reopen_task(task_id)
                    st.rerun()

            else:
                if st.button(
                    "Complete",
                    key=f"complete_{task_id}",
                ):
                    complete_task(task_id)
                    st.rerun()

    except Exception as error:
        st.error(
            f"Could not load tasks: {error}"
        )

    # -----------------------------------------------------
    # Add task
    # -----------------------------------------------------

    with st.expander("➕ Add Task"):
        task_title = st.text_input(
            "Title"
        )

        task_description = st.text_area(
            "Description"
        )

        if st.button("Add Task"):
            try:
                add_task(
                    title=task_title,
                    description=task_description or None,
                )

                st.success("Task added.")
                st.rerun()

            except Exception as error:
                st.error(str(error))

    st.divider()

    # -----------------------------------------------------
    # Knowledge Base
    # -----------------------------------------------------

    st.subheader("📚 Knowledge Base")

    uploaded_file = st.file_uploader(
        "Upload study notes",
        type=["txt"],
    )

    if uploaded_file is not None:
        if st.button("Add to Knowledge Base"):
            try:
                content = uploaded_file.getvalue().decode(
                    "utf-8"
                )

                if not content.strip():
                    raise ValueError(
                        "The uploaded file is empty."
                    )

                KNOWLEDGE_DIR.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                safe_filename = Path(
                    uploaded_file.name
                ).name

                destination = (
                    KNOWLEDGE_DIR / safe_filename
                )

                if destination.exists():
                    raise ValueError(
                        "A file with this name already exists."
                    )

                destination.write_text(
                    content,
                    encoding="utf-8",
                )

                st.success(
                    f"{safe_filename} added."
                )

            except Exception as error:
                st.error(str(error))

    st.caption(
        "Semantic retrieval is available, "
        "but agent RAG integration will be added later."
    )


# ---------------------------------------------------------
# Chat history
# ---------------------------------------------------------

for message in st.session_state.messages:
    role = get_message_value(
        message,
        "role",
    )

    content = get_message_value(
        message,
        "content",
    )

    if role not in ["user", "assistant"]:
        continue

    if not content:
        continue

    with st.chat_message(role):
        st.markdown(content)


# ---------------------------------------------------------
# Chat input
# ---------------------------------------------------------

user_input = st.chat_input(
    "Ask your study assistant..."
)

if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            assistant_response = chat(
                st.session_state.messages
            )

        if assistant_response.startswith(
            "LLM error:"
        ):
            st.error(assistant_response)

        else:
            st.markdown(
                assistant_response
            )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_response,
        }
    )