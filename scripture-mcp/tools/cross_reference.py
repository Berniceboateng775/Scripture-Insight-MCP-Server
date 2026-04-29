from database.chroma_client import collection
from services.embeddings import embed_texts

def get_cross_references(reference: str, num_results: int = 5) -> str:
    """
    Find thematic cross-references for a specific Bible reference.
    
    Args:
        reference: The exact Bible verse to cross-reference (e.g. 'John 3:16' or '1 Samuel 2:4').
        num_results: How many highly related cross-references to return (default 5).
    """
    try:
        
        target = collection.get(
            where={"reference": reference}
        )
        
        docs = target.get('documents', [])
        if not docs:
            return f"Could not find the reference '{reference}' to cross-reference. Ensure it follows the format 'Book Chapter:Verse'."
            
        base_text = docs[0]
        
        #running a semantic query using the base verse text to find things mathematically similar in theme
        query_embedding = embed_texts([base_text])
        
        #querying for n_results + 1 because the #1 top result will obviously be the exact verse itself
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=num_results + 1
        )
        
        cross_docs = results.get('documents', [[]])[0]
        cross_metas = results.get('metadatas', [[]])[0]
        
        formatted = f"**Cross References for {reference}**\n*\"{base_text}\"*\n\n"
        
        found = 0
        for doc, meta in zip(cross_docs, cross_metas):
            cr_ref = meta.get("reference", "Unknown")
            
            # Skip the original verse to avoid circularly referencing itself
            if cr_ref == reference:
                continue
                
            formatted += f"- **{cr_ref}**: {doc}\n"
            found += 1
            if found >= num_results:
                break
                
        return formatted
    except Exception as e:
        return f"Error finding cross references: {str(e)}"
