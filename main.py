from fastapi import FastAPI
from models.request_models import Message
from services.memory_service import store_message, retrieve_memory
from services.llm_service import call_llm
from db.chroma_client import collection

app = FastAPI()

@app.post("/chat")
def chat(msg: Message):

    # Store
    store_message(msg.user_input, msg.user_id)

    # Retrieve
    similar = retrieve_memory(msg.user_input, msg.user_id)

    memory_text = " ".join(similar) if similar else ""

    # LLM
    response = call_llm(msg.user_input, memory_text)

    return {
        "response": response,
        "memory_used": similar,
        "stored_messages_count": len(collection.get()["ids"])
    }