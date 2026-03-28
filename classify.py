# exercise2/classify.py
# Aggregates passage-level results to company level

import numpy as np
from exercise2.climate   import find_passages, classify_passage
from exercise2.sentiment import score_passage


def process_company(fname, company, text):
    # Find all climate passages in the filing
    passages = find_passages(text)

    # No climate content — return zeros
    if not passages:
        return {
            "company":             company,
            "file":                fname,
            "n_passages":          0,
            "avg_sentiment":       None,
            "physical_passages":   0,
            "transition_passages": 0,
            "both_passages":       0,
            "general_passages":    0,
        }

    # Score sentiment and classify each passage
    sentiments = []
    physical   = 0
    transition = 0
    both       = 0
    general    = 0

    for passage in passages:
        sentiments.append(score_passage(passage))
        risk_type = classify_passage(passage)
        if risk_type == "physical":
            physical += 1
        elif risk_type == "transition":
            transition += 1
        elif risk_type == "both":
            both += 1
        else:
            general += 1

    return {
        "company":             company,
        "file":                fname,
        "n_passages":          len(passages),
        "avg_sentiment":       round(np.mean(sentiments), 3),
        "physical_passages":   physical,
        "transition_passages": transition,
        "both_passages":       both,
        "general_passages":    general,
    }
