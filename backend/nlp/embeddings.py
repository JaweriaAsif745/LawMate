from backend.utils.config import EMBEDDING_MODEL
from sentence_transformers import SentenceTransformer
import numpy

_model = None

def load_embedding_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model

def embed_sentences(sentences):
    model = load_embedding_model()
    return model.encode(sentences, convert_to_numpy=True)