from models.groq_client import get_groq_client
from prompts.basic_prompt import CHINESE_TUTOR_PROMPT
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_message_histories import SQLChatMessageHistory
from pathlib import Path
from utils.vocab_extractor import extract_vocab
from db.vocab_db import init_db, save_vocab
import logging
from review import show_recent, quiz_mode

logger = logging.getLogger(__name__)

session_id = "persistent_session"

db_path = Path(__file__).parent.parent / "data" / "conversations.db"
print(f"[DEBUG] DB path: {db_path}")
db_path.parent.mkdir(parents=True, exist_ok=True)

memory = SQLChatMessageHistory(session_id=session_id, connection=f"sqlite:///{db_path}")

init_db()

def main():
    client = get_groq_client()

    print("=== HanCode: AI Chinese tutor")
    print("Type 'quit' or 'exit' to exit.\n")

    if len(memory.messages):
        print("=== Loaded previous conversation ===")
        for msg in memory.messages[-6:]:
            role = "You" if msg.type == "Human" else "Tutor"
            print(f"{role}: {msg.content}")
        print("=================================")

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

        if user_input.lower().startswith("/review"):
            parts = user_input.lower().split()
            if len(parts) == 1 or parts[1] == "week":
                show_recent(7)
            elif parts[1] == "today":
                show_recent(1)
            elif parts[1] == "quiz":
                quiz_mode()
            else:
                print("Usage: /review [today|week|quiz]")
            continue

        memory.add_user_message(user_input)

        messages = [
            SystemMessage(content=CHINESE_TUTOR_PROMPT),
        ] + memory.messages 

        response = client.invoke(messages)
        memory.add_ai_message(response.content)
        print(f"Tutor: {response.content}")

        vocab_items = extract_vocab(client, response.content)
        if vocab_items:
            save_vocab(vocab_items)
            logger.debug(f"Saved {len(vocab_items)} new words")

if __name__=="__main__":
    main()