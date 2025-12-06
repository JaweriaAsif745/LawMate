import os

# Prefer environment variables for secrets
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", None)

# Model names (change if you prefer other models)
SUMMARIZER_MODEL = "sshleifer/distilbart-cnn-12-6"
QA_MODEL = "distilbert-base-cased-distilled-squad"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")
RULES_DIR = os.path.join(MODELS_DIR, "rules")