# backend/nlp/risk_rules.py
import json
import os
from typing import List, Dict
from backend.utils.config import RULES_DIR

def load_risk_keywords() -> Dict[str, List[str]]:
    path = os.path.join(RULES_DIR, "risk_keywords.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def detect_risk_in_clause(clause: str, keywords: Dict[str, List[str]]) -> List[Dict]:
    """
    Return a list of matches with severity and matched keyword.
    """
    clause_lower = clause.lower()
    matches = []
    for severity, words in keywords.items():
        for w in words:
            if w in clause_lower:
                matches.append({"severity": severity, "keyword": w})
    return matches
