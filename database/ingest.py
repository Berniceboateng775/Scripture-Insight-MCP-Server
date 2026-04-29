import concurrent.futures
from database.chroma_client import collection 
from services.bible_api import get_books, get_chapter 
from services.embeddings import embed_texts

BATCH_SIZE = 100
MAX_WORKERS = 66  

def process_chapter(book_id, book_name, chapter_num):
    """Fetches a chapter and formats its verses for ingestion."""
    docs, metas, ids = [], [], []
    try:
        chapter_response = get_chapter("BSB", book_id, chapter_num)
        chapter = chapter_response.get("chapter", chapter_response)
        chapter_content = chapter.get("content", [])
        
        for item in chapter_content:
            if item.get("type") != "verse":
                continue
                
            verse_num = item.get("number")
            verse_parts = item.get("content", [])
            text_blocks = []
            
            for part in verse_parts:
                if isinstance(part, str):
                    text_blocks.append(part)
                elif isinstance(part, dict) and "text" in part:
                    text_blocks.append(part["text"])
                    
            text = " ".join(text_blocks).strip()
            if not text:
                continue
            
            ref = f"{book_name} {chapter_num}:{verse_num}"
            unique_id = f"{book_id}_{chapter_num}_{verse_num}"
            
            docs.append(text)
            metas.append({
                "reference": ref,
                "book": book_name,
                "chapter": chapter_num,
                "verse": verse_num,
                "translation": "BSB"
            })
            ids.append(unique_id)
            
        print(f"Fetched {book_name} {chapter_num}")
    except Exception as e:
        print(f"Error fetching {book_name} {chapter_num}: {e}")

    return docs, metas, ids

def main():
    print("Fetching books...")
    books = get_books("BSB")
    
    if isinstance(books, dict):
        books = books.get("data", books.get("bible", books.get("books", [])))

    if not books:
        print("No books found from API.")
        return

    #creating tasks for all chapters in these books
    tasks = []
    for book in books:
        book_id = book['id']
        book_name = book.get("name", book_id)
        num_chapters = book.get('numberOfChapters', 1)
        for chapter_num in range(1, num_chapters + 1):
            tasks.append((book_id, book_name, chapter_num))

    docs_batch, meta_batch, ids_batch = [], [], []

    print(f"Ingesting {len(tasks)} chapters using {MAX_WORKERS} parallel workers...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        
        future_to_chapter = {
            executor.submit(process_chapter, bid, bname, cnum): (bid, bname, cnum)
            for bid, bname, cnum in tasks
        }
        
        # Process results as they complete
        for future in concurrent.futures.as_completed(future_to_chapter):
            bid, bname, cnum = future_to_chapter[future]
            try:
                ch_docs, ch_metas, ch_ids = future.result()
                docs_batch.extend(ch_docs)
                meta_batch.extend(ch_metas)
                ids_batch.extend(ch_ids)
                
                # Whenever batch is large enough, process it
                while len(docs_batch) >= BATCH_SIZE:
                    # slice out BATCH_SIZE items
                    process_docs = docs_batch[:BATCH_SIZE]
                    process_metas = meta_batch[:BATCH_SIZE]
                    process_ids = ids_batch[:BATCH_SIZE]
                    
                    docs_batch = docs_batch[BATCH_SIZE:]
                    meta_batch = meta_batch[BATCH_SIZE:]
                    ids_batch = ids_batch[BATCH_SIZE:]
                    
                    # Embed and save
                    embeddings = embed_texts(process_docs)
                    collection.add(
                        documents=process_docs,
                        metadatas=process_metas,
                        ids=process_ids,
                        embeddings=embeddings
                    )
            except Exception as e:
                print(f"Exception while collecting results for {bname} {cnum}: {e}")

    # Process any remaining records
    if len(docs_batch) > 0:
        embeddings = embed_texts(docs_batch)
        collection.add(
            documents=docs_batch,
            metadatas=meta_batch,
            ids=ids_batch,
            embeddings=embeddings
        )

    print("Ingestion complete!")

if __name__ == "__main__":
    main()