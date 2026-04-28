from database.chroma_client import collection

def get_passage(book: str, chapter: int, start_verse: int, end_verse: int) -> str:
    """
    Retrieve a contiguous range of verses from a specific book and chapter.
    
    Args:
        book: The name of the book (e.g. 'Genesis', 'John').
        chapter: The chapter number.
        start_verse: The starting verse number.
        end_verse: The ending verse number.
    """
    try:
        # We query the database using 'greater than or equal' and 'less than or equal' metadata operators
        results = collection.get(
            where={
                "$and": [
                    {"book": book},
                    {"chapter": int(chapter)},
                    {"verse": {"$gte": int(start_verse)}},
                    {"verse": {"$lte": int(end_verse)}}
                ]
            }
        )
        
        documents = results.get('documents', [])
        metadatas = results.get('metadatas', [])
        
        if not documents:
            return f"Passage not found: {book} {chapter}:{start_verse}-{end_verse}"
        
        # Combine docs and metadata so we can properly order them 
        combined = list(zip(documents, metadatas))
        
        # Sort by verse number sequentially (Chroma doesn't guarantee return order)
        combined.sort(key=lambda x: x[1].get("verse", 0))
        
        formatted = f"**{book} {chapter}:{start_verse}-{end_verse}**\n\n"
        for doc, meta in combined:
            verse_num = meta.get("verse", "?")
            formatted += f"[{verse_num}] {doc} "
            
        return formatted.strip()
    except Exception as e:
        return f"Error retrieving passage: {str(e)}"
