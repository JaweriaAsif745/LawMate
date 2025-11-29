import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class SimpleSemanticSearch:
    def __init__(self, clause_texts, clause_embeddings):
        """
        clause_texts: list of clause strings
        clause_embeddings: numpy array of shape (n_clauses, embedding_dim)
        """
        self.clause_texts = clause_texts
        self.embeddings = clause_embeddings

    def query(self, q_emb, top_k=5):
        # Compute cosine similarity between query embedding and clause embeddings
        sims = cosine_similarity([q_emb], self.embeddings)[0]

        # Sort by highest similarity
        idxs = np.argsort(-sims)[:top_k]

        # Return (clause, similarity score)
        return [(self.clause_texts[i], float(sims[i])) for i in idxs]
