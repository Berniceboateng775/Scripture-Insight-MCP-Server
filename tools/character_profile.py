from database.chroma_client import collection
from services.embeddings import embed_texts

def character_profile(character: str, num_results: int = 6) -> str:
    """
    Search for key verses detailing the life, major actions, and profile of a specific biblical character.
    
    Args:
        character: The name of the biblical character (e.g. 'Moses', 'David', 'Paul', 'Ruth').
        num_results: The number of biographical verses to retrieve.
    """
    try:
        # We craft a prompt that specifically directs the semantic search to look for 
        # historical and biographical significance rather than a standard keyword match.
        prompt = f"Key biographical verses detailing the life, profile, and major actions of the biblical character {character}"
        query_embedding = embed_texts([prompt])
        
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=num_results
        )
        
        documents = results.get('documents', [[]])[0]
        metadatas = results.get('metadatas', [[]])[0]
        
        if not documents:
            return f"No verses found profiling the character: '{character}'"
            
        formatted = f"**Key Biographical Verses for '{character}'**\n\n"
        
        for doc, meta in zip(documents, metadatas):
            ref = meta.get("reference", "Unknown Reference")
            formatted += f"- **{ref}**: {doc}\n"
            
        return formatted
    except Exception as e:
        return f"Error looking up character profile: {str(e)}"
