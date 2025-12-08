from backend.nlp.llm_client import answer_question
from backend.nlp.embeddings import load_embedding_model, embed_sentences

def answer_question_on_doc(question: str, full_text: str, clauses=None, clause_embeddings=None):
    """
    Returns either an LLM answer (if available) or a list of related clauses.
    """
    # If we have clauses+embeddings, use semantic retrieval fallback
    embedder = None
    if clauses is not None and clause_embeddings is not None:
        from sentence_transformers import SentenceTransformer
        embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return answer_question(full_text, question, clauses, clause_embeddings, embedder)