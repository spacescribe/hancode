import json
from langchain.schema import HumanMessage, SystemMessage
from prompts.vocab_prompt import VOCAB_EXTRACTION_PROMPT

def extract_vocab(client, text):
    messages = [
        SystemMessage(content=VOCAB_EXTRACTION_PROMPT),
        HumanMessage(content=text)
    ]

    response = client.invoke(messages)

    try:
        vocab_items = json.loads(response.content)
        return vocab_items
    except Exception:
        return []
