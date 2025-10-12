from models.groq_client import get_groq_client
from prompts.basic_prompt import CHINESE_TUTOR_PROMPT
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_message_histories import SQLChatMessageHistory
from pathlib import Path
import time

session_id = f"hancode_{int(time.time())}"

db_path = Path(__file__).parent.parent / "data" / "conversations.db"
print(f"[DEBUG] DB path: {db_path}")
db_path.parent.mkdir(parents=True, exist_ok=True)

memory = SQLChatMessageHistory(session_id=session_id, connection=f"sqlite:///{db_path}")

def main():
    client = get_groq_client()

    print("=== HanCode: AI Chinese tutor")
    print("Type 'quit' or 'exit' to exit.\n")

    start_msg = [
        SystemMessage(content=CHINESE_TUTOR_PROMPT),
        HumanMessage(content="Please start the conversation with a friendly greeting.")
    ]

    response = client.invoke(start_msg)
    memory.add_ai_message(response.content)
    print(f"Tutor: {response.content}")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["quit", "exit"]:
            print("Tutor: 再见\nZàijiàn\nGoodbye")
            break

        memory.add_user_message(user_input)

        messages = [
            SystemMessage(content=CHINESE_TUTOR_PROMPT),
        ] + memory.messages 

        response = client.invoke(messages)
        memory.add_ai_message(response.content)
        print(f"Tutor: {response.content}")

if __name__=="__main__":
    main()