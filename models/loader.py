from transformers import (AutoTokenizer, AutoModelForSeq2SeqLM, AlbertForQuestionAnswering, AutoModelForSequenceClassification)

from functools import lru_cache

@lru_cache(maxsize=3)
def load_summarizer():
    model_name = "sshleifer/distilbart-cnn-12-6"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model

@lru_cache(maxsize=3)
def load_qa_model():
    model_name = "distilbert-base-cased-distilled-squad"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AlbertForQuestionAnswering.from_pretrained(model_name)
    return tokenizer, model

@lru_cache(maxsize=3)
def load_classifier():
    # Risk or clause classifier – uses general classifier
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    return tokenizer, model