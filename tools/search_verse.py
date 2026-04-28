from services.search_service import search_verses

def search_verse(query: str, translation: str = "BSB") -> str:
    """
    Find Bible verses by keyword, phrase, or theological theme using semantic search.
    
    Args:
        query: The keyword, phrase, or theme to search for (e.g. 'faith without works' or 'grace and truth').
        translation: The Bible translation to use (defaults to BSB).
    """
    try:
        results = search_verses(query)
        
        # formatting the raw database dictionary into a nice string for Claude to digest
        formatted = f"Search results for: '{query}' ({translation})\n\n"
        
        documents = results.get('documents', [[]])[0]
        metadatas = results.get('metadatas', [[]])[0]
        
        if not documents:
            return "No matching verses found."
            
        for doc, meta in zip(documents, metadatas):
            ref = meta.get("reference", "Unknown Reference")
            formatted += f"- {ref}: {doc}\n"
            
        return formatted
    except Exception as e:
        return f"Error performing search: {str(e)}"
