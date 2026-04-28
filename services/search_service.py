# Semantic search
from database.chroma_client import collection
from services.embeddings import embed_texts

def search_verses(query):
    query_embedding = embed_texts([query])

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=5
    )

    return results