from fastapi import FastAPI
from pydantic import BaseModel
from chromadb.utils import embedding_functions
from chromadb.config import Settings

import chromadb
import uuid

app = FastAPI()

# ✅ Persistent DB (IMPORTANT)
client = chromadb.Client(
    Settings(persist_directory="./chroma_db")
)

embedding_function = embedding_functions.DefaultEmbeddingFunction()

collection = client.get_or_create_collection(
    name="chat_memory",
    embedding_function=embedding_function
)

class Message(BaseModel):
    user_input: str

@app.post("/chat")
def chat(msg: Message):

    #  Generate unique ID
    message_id = str(uuid.uuid4())

    # Store message
    collection.add(
        documents=[msg.user_input],
        ids=[message_id]
    )

    #  Retrieve similar messages (top-k)
    results = collection.query(
        query_texts=[msg.user_input],
        n_results=3
    )

    similar = results["documents"][0] if results["documents"] else []

    #  ADAPTATION 
    response = f"You said: {msg.user_input}. "

    if similar:
        response += f"I remember you also talked about: {similar}"

   

    return {
        "response": response,
        "stored_messages_count": len(collection.get()["ids"]),
        "similar_messages": similar
    }