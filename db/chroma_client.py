import chromadb
from chromadb.utils import embedding_functions

client = chromadb.PersistentClient(path="./chroma_db")

embedding_function = embedding_functions.DefaultEmbeddingFunction()

collection = client.get_or_create_collection(
    name="chat_memory",
    embedding_function=embedding_function
)