from langchain.text_splitter import SpacyTextSplitter
import pandas as pd


# Get excel for each chapter
def get_excel_files(chapters):
    for chapter in chapters:
        chapter_name = chapter.title
        with open(chapter_name + ".txt", "r", encoding="utf-8") as f:
            text = f.read()

        chunks = langchain_text_splitter(text)
        extract_chunks_to_excel(chapter_name, chunks)


def extract_chunks_to_excel(chapter_name, chunks):
    # Create a DataFrame with columns for Id, Chunk and The Fellowship
    df = pd.DataFrame({
        'ID': range(1, len(chunks) + 1),
        'Chunk': chunks,
        'Fellowship': "Neutral"
    })

    # Save to Excel
    df.to_excel(chapter_name + ".xlsx", index=False)  # index=False removes the row numbers


def langchain_text_splitter(text):
    # Initialize the SpacyTextSplitter
    text_splitter = SpacyTextSplitter(
        chunk_size=500,  # Approximate max chars
        chunk_overlap=100  # Overlap in characters
    )

    # Your input text here
    chunks = text_splitter.split_text(text)

    # Now each chunk is sentence-aligned and context-preserving
    # for i, chunk in enumerate(chunks):
    # print(f"\n--- Chunk {i + 1}---{len(chunk)}---\n{chunk}")
    return chunks

