from backend.nlp.risk_rules import load_risk_keywords, detect_risk_in_clause

keywords = load_risk_keywords()

def analyze_clauses_for_risk(clauses):
    results = []
    for i, clause in enumerate(clauses):
        matches = detect_risk_in_clause(clause, keywords)
        results.append({
            "index" : i,
            "clause": clause,
            "matches": matches,
            "is_risky": len(matches) > 0
        })

    return results