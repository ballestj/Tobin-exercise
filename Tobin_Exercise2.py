# Tobin_Exercise2.py
# 10-K Climate Risk Analysis — Jorge Ballestero
#
# Identifies and scores climate risk passages across 339 SEC 10-K filings.
# Separates physical risk (floods, storms, drought) from transition risk
# (carbon regulation, emissions policy, net zero commitments).
#
# Pipeline adapted from signal_extraction/ in LatAm Market Predictor:
# https://jorgedballestero.com/latin-markets.html
#
# Usage: python Tobin_Exercise2.py

from exercise2.run import run

DATA_DIR    = "data/10Ks"
OUTPUT_PATH = "output/exercise2_results_py.csv"

if __name__ == "__main__":
    run(DATA_DIR, OUTPUT_PATH)
