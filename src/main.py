from models.groq_client import get_groq_client
from prompts.basic_prompt import CHINESE_TUTOR_PROMPT
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_message_histories import ChatMessageHistory

history = ChatMessageHistory()

def main():
    client = get_groq_client()

    print("=== HanCode: AI Chinese tutor")
    print("Type 'quit' or 'exit' to exit.\n")

    start_msg = [
        SystemMessage(content=CHINESE_TUTOR_PROMPT),
        HumanMessage(content="Please start the conversation with a friendly greeting.")
    ]

    response = client.invoke(start_msg)
    print(f"Tutor: {response.content}")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["quit", "exit"]:
            print("Tutor: 再见\nZàijiàn\nGoodbye")
            break

        history.add_user_message(user_input)

        messages = [
            SystemMessage(content=CHINESE_TUTOR_PROMPT),
        ] + history.messages 

        response = client.invoke(messages)
        history.add_ai_message(response.content)
        print(f"Tutor: {response.content}")

if __name__=="__main__":
    main()