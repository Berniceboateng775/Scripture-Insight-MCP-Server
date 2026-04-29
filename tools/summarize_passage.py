from database.chroma_client import collection

def summarize_passage(book: str, chapter: int) -> str:
    """
    Fetch the complete text of a biblical chapter specifically to provide context for AI-driven summarization.
    
    Args:
        book: The name of the book (e.g. 'Genesis', 'Romans').
        chapter: The chapter number to fetch and summarize.
    """
    try:
        results = collection.get(
            where={
                "$and": [
                    {"book": book},
                    {"chapter": int(chapter)}
                ]
            }
        )
        
        documents = results.get('documents', [])
        metadatas = results.get('metadatas', [])
        
        if not documents:
            return f"No text found for {book} chapter {chapter}."
        
        #combine docs and metadata to order the verses sequentially
        combined = list(zip(documents, metadatas))
        combined.sort(key=lambda x: x[1].get("verse", 0))
        
        formatted = f"**Full Text of {book} {chapter} for Summarization**\n\n"
        for doc, meta in combined:
            verse_num = meta.get("verse", "?")
            formatted += f"[{verse_num}] {doc} "
            
        return formatted.strip()
    except Exception as e:
        return f"Error retrieving chapter for summarization: {str(e)}"
