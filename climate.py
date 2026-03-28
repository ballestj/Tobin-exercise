# exercise2/climate.py
# Identifies climate risk passages within 10-K text
# Adapted from event_classifier.py in LatAm Market Predictor

import re

# Keywords that indicate climate risk discussion
CLIMATE_KEYWORDS = [
    "climate", "climate change", "global warming", "greenhouse",
    "carbon", "emissions", "flood", "drought", "storm", "hurricane",
    "sea level", "wildfire", "extreme weather", "physical risk",
    "transition risk", "renewable", "sustainability", "environmental risk",
    "stranded asset", "carbon tax", "cap and trade", "paris agreement",
    "net zero", "decarbonization"
]

# Physical risk — direct impact of climate on assets and operations
PHYSICAL_KEYWORDS = [
    "flood", "drought", "storm", "hurricane", "wildfire",
    "sea level", "extreme weather", "precipitation",
    "water scarcity", "natural disaster", "coastal"
]

# Transition risk — policy, regulatory, and market shifts
TRANSITION_KEYWORDS = [
    "carbon", "emissions", "greenhouse", "regulation", "policy",
    "carbon tax", "cap and trade", "paris agreement", "net zero",
    "decarbonization", "renewable", "stranded asset",
    "legislation", "carbon price", "low carbon"
]


def find_passages(text, window=3):
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    passages  = []

    for i, sentence in enumerate(sentences):
        # Check if sentence contains any climate keyword
        if any(kw.lower() in sentence.lower() for kw in CLIMATE_KEYWORDS):
            # Grab surrounding context
            start   = max(0, i - window)
            end     = min(len(sentences), i + window + 1)
            passage = " ".join(sentences[start:end])
            passages.append(passage)

    return passages


def classify_passage(passage):
    # Classify each passage as physical, transition, both, or general
    p             = passage.lower()
    is_physical   = any(kw in p for kw in PHYSICAL_KEYWORDS)
    is_transition = any(kw in p for kw in TRANSITION_KEYWORDS)

    if is_physical and is_transition:
        return "both"
    elif is_physical:
        return "physical"
    elif is_transition:
        return "transition"
    else:
        return "general"
