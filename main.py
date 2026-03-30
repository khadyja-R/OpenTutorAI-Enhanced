from fastapi import FastAPI
from pydantic import BaseModel
from chromadb.utils import embedding_functions

import chromadb
import uuid

app = FastAPI()

# Initialize ChromaDB
client = chromadb.Client()
embedding_function = embedding_functions.DefaultEmbeddingFunction()
collection = client.create_collection(
    name="chat_memory",
    embedding_function=embedding_function
)
class Message(BaseModel):
    user_input: str

@app.post("/chat")
def chat(msg: Message):

    # Generate unique ID
    message_id = str(uuid.uuid4())

    # Store message in ChromaDB
    collection.add(
        documents=[msg.user_input],
        ids=[message_id]
    )

    # Retrieve similar messages
    results = collection.query(
        query_texts=[msg.user_input],
        n_results=2
    )

    return {
        "response": "Message stored",
        "similar_messages": results["documents"]
    }
