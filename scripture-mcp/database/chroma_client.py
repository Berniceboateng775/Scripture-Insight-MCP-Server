# ChromaDB setup
import chromadb
from chromadb.config import Settings

import os

# Point directly to the chroma_db folder inside the database directory
db_path = os.path.join(os.path.dirname(__file__), "chroma_db")

client = chromadb.PersistentClient(path=db_path)

collection = client.get_or_create_collection(
    name="bible_verses"
)