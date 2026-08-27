from llm import chat

SYSTEM_PROMPT = """
You are an AI Study Assistant.

Keep responses concise and focused unless the user asks for detail.
Do not invent references or sources.
If you are uncertain, say so clearly.
Use the conversation history to maintain context.
""".strip()

messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]

while True:
    user_input = input("You: ")

    if user_input.strip().lower() in ["exit", "quit"]:
        break

    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    assistant_response = chat(messages)

    messages.append(
        {
            "role": "assistant",
            "content": assistant_response
        }
    )

    print(f"Assistant: {assistant_response}")