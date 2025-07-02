import textwrap
import nltk
import fitz
import re
from sklearn.metrics.pairwise import cosine_similarity
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
    # Create a DataFrame with columns for Id, Chunk and Characters
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


def split_into_sentences(text):
    """Splits text into sentences, removes newlines, and fixes hyphenated words split across lines."""

    # Step 1: Fix hyphenated words broken by newlines (e.g., "new-\nline" → "newline")
    text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)

    # Step 2: Replace all newlines with spaces (after fixing hyphens)
    text = text.replace("\n", " ")

    # Step 3: Tokenize into sentences
    sentences = nltk.tokenize.sent_tokenize(text)

    return sentences


def create_chunks(sentences, nlp, min_words=40, max_words=70, similarity_threshold=0.9):
    """
    Groups sentences into chunks based on word count:
    - Each chunk has min_words to max_words.
    - Sentences that are semantically related are grouped together.
    """
    chunks = []
    current_chunk = []
    current_word_count = 0

    for i, sentence in enumerate(sentences):
        sentence_word_count = len(sentence.split())
        current_chunk.append(sentence)
        current_word_count += sentence_word_count

        # If we've reached at least min_words, consider splitting
        if current_word_count >= min_words:
            if i + 1 < len(sentences):
                next_sentence = sentences[i + 1]
                similarity = sentence_similarity(sentence, next_sentence, nlp)

                # Split if sentences are not semantically close
                if similarity < similarity_threshold:
                    chunks.append(" ".join(current_chunk))
                    current_chunk = []
                    current_word_count = 0

            # Always split if max_words is exceeded
            if current_word_count >= max_words:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_word_count = 0

    # Add any remaining sentences
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def sentence_similarity(sent1, sent2, nlp):  # Load spaCy's medium-sized English model for better sentence embeddings
    """Computes semantic similarity between two sentences using spaCy embeddings."""
    vec1 = nlp(sent1).vector.reshape(1, -1)
    vec2 = nlp(sent2).vector.reshape(1, -1)
    return cosine_similarity(vec1, vec2)[0][0]
