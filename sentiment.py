# exercise2/sentiment.py
# Scores climate passages using VADER sentiment analysis
# Adapted from sentiment_scorer.py in LatAm Market Predictor

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize once — expensive to reinstantiate per passage
analyzer = SentimentIntensityAnalyzer()


def score_passage(passage):
    # Returns compound score between -1 (negative) and +1 (positive)
    return analyzer.polarity_scores(passage)["compound"]


def score_all(passages):
    # Score a list of passages and return average
    if not passages:
        return None
    scores = [score_passage(p) for p in passages]
    return round(sum(scores) / len(scores), 3)
