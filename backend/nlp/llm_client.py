import os
from backend.utils.config import OPENAI_API_KEY, SUMMARIZER_MODEL, QA_MODEL
import logging

# Try using OpenAI if key present; otherwise use local transformers
USE_OPENAI = OPENAI_API_KEY is not None

if USE_OPENAI:
    import openai
    openai.api_key = OPENAI_API_KEY
else:
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForQuestionAnswering

# Summarize
def summarize_with_openai(text, max_tokens=256):
    prompt = f"Summarize the following legal text in plain language, with short bullet points:\n\n{text}"
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini" if "gpt-4o-mini" in openai.Model.list() else "gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.1
    )
    return resp.choices[0].message.content.strip()

# Local fallback summarizer
_local_summarizer = None
_local_summarizer_tokenizer = None

def load_local_summarizer():
    global _local_summarizer, _local_summarizer_tokenizer
    if _local_summarizer is None:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        _local_summarizer_tokenizer = AutoTokenizer.from_pretrained(SUMMARIZER_MODEL)
        _local_summarizer = AutoModelForSeq2SeqLM.from_pretrained(SUMMARIZER_MODEL)
    return _local_summarizer_tokenizer, _local_summarizer

def summarize_local(text, max_length=150):
    tok, model = load_local_summarizer()
    inputs = tok([text], truncation=True, max_length=1024, return_tensors="pt")
    outs = model.generate(**inputs, max_length=max_length)
    return tok.decode(outs[0], skip_special_tokens=True)

def summarize(text):
    if USE_OPENAI:
        try:
            return summarize_with_openai(text)
        except Exception as e:
            logging.warning("OpenAI summarization failed, falling back: %s", e)
    return summarize_local(text)

# QA: openai or local (very minimal)
def answer_question_with_openai(context, question):
    prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer in concise plain language."
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":prompt}],
        max_tokens=256,
        temperature=0.0
    )
    return resp.choices[0].message.content.strip()

# Local QA is nontrivial; so we provide a minimal fallback that returns best matching clause
def answer_question_local(question, clauses, embeddings, embedder, top_k=3):
    q_emb = embedder.encode([question], convert_to_numpy=True)[0]
    from sklearn.metrics.pairwise import cosine_similarity
    sims = cosine_similarity([q_emb], embeddings)[0]
    idxs = sims.argsort()[::-1][:top_k]
    answers = []
    for i in idxs:
        answers.append({"clause": clauses[i], "score": float(sims[i])})
    return answers

def answer_question(context_text, question, clauses=None, clause_embeddings=None, embedder=None):
    if USE_OPENAI:
        try:
            return answer_question_with_openai(context_text, question)
        except Exception as e:
            pass
    # fallback: semantic retrieval from clauses
    if clauses and clause_embeddings is not None and embedder is not None:
        return answer_question_local(question, clauses, clause_embeddings, embedder)
    return "Sorry, cannot answer right now."
