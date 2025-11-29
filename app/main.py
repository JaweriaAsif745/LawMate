import os
import sys

# Get project root: D:/Jiya/Projects/LawMate
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add project root to Python path
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
from backend.utils.file_reader import read_file
from backend.nlp.clause_splitter import split_into_clauses
from backend.analysis.risk_detector import analyze_clauses_for_risk
from backend.analysis.summarizer import summarize_document
from backend.nlp.embeddings import embed_sentences, load_embedding_model
from app.components.highlights import highlight_clauses
from backend.analysis.qa_engine import answer_question_on_doc

st.set_page_config(page_title="LawMate Lite", layout="wide")
st.title("⚖️ LawMate Lite — Contract Summarizer & Clause Risk Highlighter")

uploaded = st.file_uploader("Upload a contract (PDF or DOCX)", type=["pdf", "docx", "txt"])
if uploaded:
    # save uploaded file to disk
    data_dir = os.path.join(os.getcwd(), "data", "uploads")
    os.makedirs(data_dir, exist_ok=True)
    file_path = os.path.join(data_dir, uploaded.name)
    with open(file_path, "wb") as f:
        f.write(uploaded.getbuffer())
    st.success("File saved. Processing...")

    # read
    text = read_file(file_path)
    st.header("Raw Extracted Text (preview)")
    st.write(text[:2000] + ("..." if len(text) > 2000 else ""))

    # clauses
    clauses = split_into_clauses(text)
    st.header("Detected Clauses")
    st.write(f"{len(clauses)} clauses detected.")
    # embed clauses (optional)
    try:
        embed_model = load_embedding_model()
        clause_embeddings = embed_sentences(clauses)
    except Exception:
        clause_embeddings = None

    # risk analysis
    clause_results = analyze_clauses_for_risk(clauses)
    st.header("Clause Risk Analysis")
    highlight_clauses(clause_results)

    # summarization
    st.header("Document Summary")
    with st.spinner("Generating summary..."):
        summary = summarize_document(text[:3000])  # short chunk for speed; in prod, chunk & combine
    st.markdown(summary)

    # QA
    st.header("Ask questions about this contract")
    q = st.text_input("Ask a question (e.g. 'What is the termination clause?')")
    if q:
        with st.spinner("Finding answer..."):
            ans = answer_question_on_doc(q, text, clauses, clause_embeddings)
        st.write(ans)
else:
    st.info("Upload a contract to get started.")
