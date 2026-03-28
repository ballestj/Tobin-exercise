# exercise2/run.py
# Full pipeline — loads and processes filings one at a time

import os
import pandas as pd
from exercise2.parse    import parse_filing
from exercise2.classify import process_company


def run(data_dir, output_path):

    files = [f for f in os.listdir(data_dir) if f.endswith(".txt")]
    print(f"Found {len(files)} filings. Processing...")

    results = []
    for i, fname in enumerate(files):
        filepath = os.path.join(data_dir, fname)
        company, text = parse_filing(filepath)

        if not text:
            continue

        result = process_company(fname, company, text)
        results.append(result)

        if (i + 1) % 50 == 0:
            print(f"  Processed {i+1}/{len(files)}...")

    df = pd.DataFrame(results)

    print(f"\n=== RESULTS ===")
    print(f"Companies processed   : {len(df)}")
    print(f"With climate passages : {(df.n_passages > 0).sum()}")
    print(f"Avg sentiment         : {df[df.avg_sentiment.notna()].avg_sentiment.mean():.3f}")
    print(f"Total physical        : {df.physical_passages.sum()}")
    print(f"Total transition      : {df.transition_passages.sum()}")

    print(f"\nTop 10 by exposure:")
    top = df[df.n_passages > 0].sort_values(
        "n_passages", ascending=False).head(10)
    print(top[["company", "n_passages", "avg_sentiment",
               "physical_passages", "transition_passages"]].to_string(index=False))

    df.to_csv(output_path, index=False)
    print(f"\nSaved to {output_path}")

    return df