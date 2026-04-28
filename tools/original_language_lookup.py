from database.chroma_client import collection
from services.embeddings import embed_texts

def original_language_lookup(term: str, testament: str = "Both") -> str:
    """
    Search the scripture for verses that strongly embody an original Greek or Hebrew word concept.
    
    Args:
        term: The Hebrew or Greek word (e.g. 'Agape', 'Hesed', 'Shalom').
        testament: 'Old' for Hebrew concepts, 'New' for Greek concepts, or 'Both'.
    """
    try:
        # We craft a specific semantic anchor to look for verses embodying the original term's meaning.
        # Since the database is English, semantic search will map the underlying concept of the foreign word 
        # directly natively to the english verse that expresses it!
        prompt = f"Verses representing the deep biblical original language concept and meaning of the word '{term}'"
        query_embedding = embed_texts([prompt])
        
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=6
        )
        
        documents = results.get('documents', [[]])[0]
        metadatas = results.get('metadatas', [[]])[0]
        
        if not documents:
            return f"No verses found conceptually matching the original language term: '{term}'"
            
        formatted = f"**Top verses demonstrating the original concept of '{term}'**\n\n"
        
        for doc, meta in zip(documents, metadatas):
            ref = meta.get("reference", "Unknown Reference")
            formatted += f"- **{ref}**: {doc}\n"
            
        return formatted
    except Exception as e:
        return f"Error looking up original language term: {str(e)}"
