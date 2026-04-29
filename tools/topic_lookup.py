from database.chroma_client import collection
from services.embeddings import embed_texts

def get_topic_verses(topic: str, num_results: int = 7) -> str:
    """
    Find verses throughout the Bible deeply related to a specific theological topic.
    
    Args:
        topic: The theological topic to look up (e.g. 'Grace', 'Salvation', 'Covenant', 'Marriage').
        num_results: The number of highly relevant verses to retrieve.
    """
    try:
        #wrapping the user's topic in a leading prompt string. 
        #This acts as an anchoring technique so the AI embedding model knows exactly what context 
        #to apply mathematically to the vector search
        query_embedding = embed_texts([f"Verses teaching about the core theological concept of {topic}"])
        
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=num_results
        )
        
        documents = results.get('documents', [[]])[0]
        metadatas = results.get('metadatas', [[]])[0]
        
        if not documents:
            return f"No verses found for the theological topic: '{topic}'"
            
        formatted = f"**Top Verses concerning the theology of '{topic}'**\n\n"
        
        for doc, meta in zip(documents, metadatas):
            ref = meta.get("reference", "Unknown Reference")
            formatted += f"- **{ref}**: {doc}\n"
            
        return formatted
    except Exception as e:
        return f"Error retrieving theological topic: {str(e)}"
