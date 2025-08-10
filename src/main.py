from models.groq_client import get_groq_client
from prompts.basic_prompt import CHINESE_TUTOR_PROMPT
from langchain.schema import HumanMessage, SystemMessage

def main():
    client = get_groq_client()

    print("=== HanCode: AI Chinese tutor")
    print("Type 'quit' or 'exit' to exit.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["quit", "exit"]:
            print("Tutor: 再见\nZàijiàn\nGoodbye")
            break

        messages = [
            SystemMessage(content=CHINESE_TUTOR_PROMPT),
            HumanMessage(content=user_input)
        ]
        response = client.invoke(messages)
        print(f"Tutor: {response.content}")

if __name__=="__main__":
    main()