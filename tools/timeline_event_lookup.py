from database.chroma_client import collection
from services.embeddings import embed_texts

def timeline_event_lookup(event_name: str, num_results: int = 5) -> str:
    """
    Find verses that describe or detail major historical and redemptive biblical events.
    
    Args:
        event_name: The name of the biblical event (e.g. 'The Exodus', 'The Flood', 'Day of Pentecost', 'Destruction of the Temple').
        num_results: The number of historical verses to return.
    """
    try:
        prompt = f"Historical, narrative, and chronological verses recording the major biblical event of {event_name}"
        query_embedding = embed_texts([prompt])
        
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=num_results
        )
        
        documents = results.get('documents', [[]])[0]
        metadatas = results.get('metadatas', [[]])[0]
        
        if not documents:
            return f"No historical verses found for the event: '{event_name}'"
            
        formatted = f"**Key Historical Verses for '{event_name}'**\n\n"
        
        for doc, meta in zip(documents, metadatas):
            ref = meta.get("reference", "Unknown Reference")
            formatted += f"- **{ref}**: {doc}\n"
            
        return formatted
    except Exception as e:
        return f"Error looking up historical event: {str(e)}"
