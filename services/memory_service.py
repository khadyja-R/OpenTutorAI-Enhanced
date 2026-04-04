import uuid
import time
from db.chroma_client import collection

def store_message(user_input, user_id):
    message_id = str(uuid.uuid4())

    collection.add(
        documents=[user_input],
        ids=[message_id],
        metadatas=[{
            "user_id": user_id,
            "timestamp": time.time()
        }]
    )

def retrieve_memory(user_input, user_id):
    results = collection.query(
        query_texts=[user_input],
        n_results=3,
        where={"user_id": user_id}
    )

    return results["documents"][0] if results["documents"] else []