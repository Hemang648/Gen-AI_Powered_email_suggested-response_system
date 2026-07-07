import json
import os

import pandas as pd
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer

INPUT_FILE = "E:\Gen-AI email suggested-response system\Reply_generator\generated\generated_replies.json"
OUTPUT_FILE = "scores.csv"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)

smooth = SmoothingFunction().method1

results = []

for item in data:

    reference = item["ideal_reply"]

    generated = item["generated_reply"]

    bleu = sentence_bleu(
        [reference.split()],
        generated.split(),
        smoothing_function=smooth
    )

    rouge = scorer.score(reference, generated)["rougeL"].fmeasure

    ref_len = len(reference.split())
    gen_len = len(generated.split())

    length_score = 1 - abs(ref_len - gen_len) / max(ref_len, gen_len)

    overall = (
        bleu * 0.40 +
        rouge * 0.40 +
        length_score * 0.20
    ) * 100

    results.append({

        "id": item["id"],

        "category": item["category"],

        "BLEU": round(bleu, 4),

        "ROUGE_L": round(rouge, 4),

        "LengthScore": round(length_score, 4),

        "OverallScore": round(overall, 2)

    })

df = pd.DataFrame(results)

df.to_csv(OUTPUT_FILE, index=False)

print(df.head())

print()

print("Average BLEU:", df["BLEU"].mean())

print("Average ROUGE:", df["ROUGE_L"].mean())

print("Average Overall:", df["OverallScore"].mean())