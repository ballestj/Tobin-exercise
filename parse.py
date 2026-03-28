# exercise2/parse.py
# Parses SEC EDGAR 10-K filings
# Extracts company name and clean text from the primary 10-K document block

import os
import re
from bs4 import BeautifulSoup


def parse_filing(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        raw = f.read()

    # Company name from SEC header
    company_match = re.search(r"COMPANY CONFORMED NAME:\s*(.+)", raw)
    company = company_match.group(1).strip() if company_match else "UNKNOWN"

    # Extract primary 10-K document block only
    doc_match = re.search(
        r"<TYPE>10-K.*?<TEXT>(.*?)</TEXT>",
        raw, re.DOTALL | re.IGNORECASE
    )

    if not doc_match:
        return company, ""

    html = doc_match.group(1)

    # Strip HTML tags
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text(separator=" ")

    # Clean whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return company, text


def extract_items(text):
    pattern = r"(Item\s+\d+[A-Z]?\.\s+[A-Z][^\n]{3,60})"
    splits  = re.split(pattern, text, flags=re.IGNORECASE)

    items = {}
    current_item = "HEADER"

    for chunk in splits:
        if re.match(pattern, chunk, re.IGNORECASE):
            current_item = chunk.strip()
        else:
            if current_item not in items:
                items[current_item] = ""
            items[current_item] += chunk

    return items


def load_all(data_dir):
    files   = [f for f in os.listdir(data_dir) if f.endswith(".txt")]
    results = []

    for fname in files:
        filepath = os.path.join(data_dir, fname)
        company, text = parse_filing(filepath)
        results.append((fname, company, text))

    return results
