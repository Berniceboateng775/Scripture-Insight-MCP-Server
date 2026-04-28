# ChromaDB setup
import chromadb
from chromadb.config import Settings

import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
db_path = os.path.join(BASE_DIR, "chroma_db")

client = chromadb.PersistentClient(path=db_path)

collection = client.get_or_create_collection(
    name="bible_verses"
)