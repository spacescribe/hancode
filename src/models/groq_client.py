import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

def get_groq_client(model_name: str="llama-3.3-70b-versatile", temp: float=0.7):
    API_KEY=os.getenv("GROQ_API_KEY")
    if not API_KEY:
        raise ValueError("GROQ_API_KEY not found")

    return ChatGroq(
        model=model_name,
        temperature=temp
    )