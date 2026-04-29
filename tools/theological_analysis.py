from database.chroma_client import collection
from services.embeddings import embed_texts

def theological_analysis(reference: str, question: str) -> str:
    """
    Perform a deep theological analysis on a specific verse by gathering extensive biblical context.
    
    Args:
        reference: The exact Bible verse to analyze (e.g. 'Romans 8:28').
        question: The theological question or angle to analyze it from.
    """
    try:
        # fetch the primary verse text
        target = collection.get(where={"reference": reference})
        docs = target.get('documents', [])
        if not docs:
            return f"Could not find the reference '{reference}' for analysis. Please ensure it follows 'Book Chapter:Verse'."
            
        base_text = docs[0]
        
        prompt = f"Theological and doctrinal context answering '{question}' based on the verse: {base_text}"
        query_embedding = embed_texts([prompt])
        
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=7
        )
        
        cross_docs = results.get('documents', [[]])[0]
        cross_metas = results.get('metadatas', [[]])[0]
        
        formatted = f"**Raw Data for Theological Analysis of {reference}**\n\n"
        formatted += f"**Primary Text ({reference})**: {base_text}\n\n"
        formatted += "**Theological Context & Supporting Verses**:\n"
        
        for doc, meta in zip(cross_docs, cross_metas):
            cr_ref = meta.get("reference", "Unknown")
            if cr_ref != reference:
                formatted += f"- **{cr_ref}**: {doc}\n"
                
        formatted += "\n*System Instruction: Using the primary text and the supporting verses above, please synthesize a deep theological analysis answering the question. Include interpretation, doctrinal themes, and multiple viewpoints if applicable.*"
        
        return formatted
    except Exception as e:
        return f"Error performing theological analysis: {str(e)}"
