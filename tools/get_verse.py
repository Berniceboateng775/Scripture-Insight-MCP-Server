from database.chroma_client import collection

def get_verse(book: str, chapter: int, verse: int) -> str:
    """
    Retrieve the exact text of a specific Bible verse.
    
    Args:
        book: The name of the book (e.g. 'Genesis', '1 Samuel').
        chapter: The chapter number.
        verse: The verse number.
    """
    try:
        #query the database using an exact metadata filter, rather than semantic similarity
        results = collection.get(
            where={
                "$and": [
                    {"book": book},
                    {"chapter": int(chapter)},
                    {"verse": int(verse)}
                ]
            }
        )
        
        documents = results.get('documents', [])
        
        if not documents:
            return f"Verse not found: {book} {chapter}:{verse}"
            
        return f"{book} {chapter}:{verse} - {documents[0]}"
    except Exception as e:
        return f"Error retrieving verse: {str(e)}"
