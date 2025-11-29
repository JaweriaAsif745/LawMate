# backend/analysis/summarizer.py
import math
import logging
from backend.nlp.llm_client import summarize

# simple chunker by characters (safe heuristic). Adjust chunk_size as needed.
def _chunk_text(text, chunk_size=3000, overlap=200):
    """
    Splits text into chunks of approximately chunk_size characters with small overlap.
    Returns list of chunks.
    """
    if not text:
        return []
    chunks = []
    start = 0
    L = len(text)
    while start < L:
        end = min(start + chunk_size, L)
        chunk = text[start:end].strip()
        chunks.append(chunk)
        if end == L:
            break
        start = max(0, end - overlap)
    return chunks

def summarize_document(text):
    """
    Summarize by chunking: summarize each chunk then combine.
    Uses backend.nlp.llm_client.summarize (openai or local model).
    Note: local transformer summarizers can be slow for long input;
    if you have OPENAI_API_KEY set, OpenAI will usually be faster.
    """
    if not text:
        return ""

    # If text is short, summarize directly
    if len(text) <= 3000:
        try:
            return summarize(text)
        except Exception as e:
            logging.exception("Summarize failed on short text: %s", e)
            return "Summary unavailable."

    # For long docs, chunk and summarize each chunk
    chunks = _chunk_text(text, chunk_size=3000, overlap=200)
    summaries = []
    for i, c in enumerate(chunks):
        try:
            s = summarize(c)
            summaries.append(s.strip())
        except Exception as e:
            logging.exception("Chunk summarization failed for chunk %d: %s", i, e)
            # fallback: take first 500 chars
            summaries.append(c[:500] + "...")
    # combine chunk summaries and optionally summarize that
    combined = "\n\n".join(summaries)
    # final summarize of the combined (short)
    try:
        final = summarize(combined)
        return final
    except Exception:
        return combined
