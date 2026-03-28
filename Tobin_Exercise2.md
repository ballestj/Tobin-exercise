---
title: "10-K Climate Risk Analysis"
author: "Jorge Ballestero"
date: "2026"
---

# Overview

This exercise analyzes 339 annual reports (Form 10-K) filed with the SEC 
to identify and score climate risk disclosures. The pipeline is adapted 
from a prior NLP project processing 18,000+ financial news articles for 
emerging market signal extraction. Results were validated against an 
independent Jupyter implementation, producing identical output across 
all 339 companies.

# Data & Parsing

Each filing is a multi-document SEC EDGAR submission containing the main 
10-K alongside exhibits and financial statements. I extract only the 
primary 10-K document block (`<TYPE>10-K`) to avoid processing irrelevant 
attachments, then strip HTML tags using BeautifulSoup to recover clean text.

# Item Extraction

Standard 10-K filings follow a prescribed structure: Item 1 (Business), 
Item 1A (Risk Factors), Item 7 (MD&A), and so on. I split the cleaned 
text on Item header patterns using regex to recover individual sections, 
enabling section-level analysis if needed.

# Climate Passage Identification

I identify climate-relevant passages by scanning each sentence for 
climate-related keywords: including "climate change", "carbon", 
"emissions", "flood", "drought", "paris agreement", and "net zero", 
among others. When a keyword is found, I extract a 7-sentence window 
centered on the hit to preserve context. This keyword approach is 
transparent and reproducible, though it will capture some boilerplate 
language alongside genuine disclosures, which is indeed a limitation.

# Sentiment Analysis

Each climate passage is scored using VADER (Valence Aware Dictionary 
and sEntiment Reasoner), a rule-based sentiment analyzer that returns 
a compound score between -1 (most negative) and +1 (most positive). 
Scores are averaged across all passages within a company to produce a 
company-level sentiment measure. VADER is appropriate as a baseline 
approach but has known limitations on formal regulatory text: it scores 
based on word polarity rather than financial context.

# Physical vs Transition Risk

Each passage is classified using two separate keyword lists:

- **Physical risk** — flood, drought, storm, hurricane, wildfire, 
sea level, extreme weather, water scarcity, coastal
- **Transition risk** — carbon, emissions, greenhouse, regulation, 
policy, carbon tax, paris agreement, net zero, decarbonization, 
renewable, stranded asset
- **Both** — passage contains keywords from both lists
- **General** — climate keyword present but neither list fires

# Results

## Coverage

311 of 339 companies (91.7%) contain at least one climate passage. 
The 28 companies with no climate passages tend to be smaller firms 
in sectors with limited direct environmental exposure.

## Sentiment

Average sentiment across climate passages is +0.155. which is slightly positive. 
This reflects the legal drafting conventions of 10-K filings, where risk 
disclosures are written to satisfy regulatory requirements while minimizing 
investor alarm. Companies frame climate risk as manageable rather than 
existential.

## Physical vs Transition Risk

| Risk Type  | Passages | Share |
|------------|----------|-------|
| Transition | 2,761    | 60%   |
| Physical   | 1,152    | 25%   |
| Both       | 578      | 13%   |

Transition risk passages outnumber physical risk passages by more than 
two to one. Companies are more concerned about regulatory and policy 
changes than direct physical impacts, which is consistent with the post-Paris 
Agreement regulatory environment in which these filings were prepared 
(fiscal year 2020).

## Top Exposed Companies

| Company | Passages | Sentiment | Physical | Transition |
|---------|----------|-----------|----------|------------|
| Entergy Corp | 179 | +0.421 | 104 | 48 |
| Southern Co | 136 | +0.600 | 36 | 81 |
| Par Pacific Holdings | 126 | +0.458 | 0 | 118 |
| MasTec Inc | 114 | +0.774 | 9 | 87 |
| Peabody Energy | 99 | +0.642 | 4 | 91 |

Energy and utility companies dominate. Their core assets are directly 
tied to fossil fuel infrastructure facing both physical and transition 
risk. Peabody Energy's high transition risk exposure reflects existential 
regulatory pressure on coal. Par Pacific (oil refining) shows exclusively 
transition risk (no physical passages) suggesting their disclosure 
focuses entirely on regulatory and policy exposure.

## Most Negative Sentiment

| Company | Passages | Sentiment |
|---------|----------|-----------|
| Fiserv Inc | 1 | -0.997 |
| LiveRamp Holdings | 2 | -0.995 |
| CoStar Group | 2 | -0.992 |
| Sirius XM Holdings | 2 | -0.992 |
| Dixie Group | 1 | -0.992 |

These are technology and media firms with minimal direct climate exposure. 
Their single climate passage is almost certainly boilerplate legal language 
flagging climate as a generic tail risk, which VADER scores as highly 
negative because risk disclosure language is inherently negative in tone. 
This illustrates a key limitation of lexicon-based sentiment on regulatory 
text.

# Limitations

Three limitations are worth noting. First, keyword matching captures 
some boilerplate language alongside genuine disclosures. Second, VADER 
is not calibrated for financial regulatory text and may misclassify 
formally written risk language. Third, the physical vs transition 
classification is keyword-based, as many real disclosures blend both 
risk types within a single paragraph, which our binary classification 
cannot fully capture.
