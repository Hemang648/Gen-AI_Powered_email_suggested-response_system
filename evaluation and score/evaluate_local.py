import os
import json
import pandas as pd
from tqdm import tqdm

from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer

from bert_score import score as bert_score



# -----------------------------
# Configuration
# -----------------------------

INPUT_FILE = "E:\Gen-AI email suggested-response system\Reply_generator\generated\generated_replies.json"

OUTPUT_FILE = "../results/local_scores.csv"

os.makedirs("../results", exist_ok=True)

# -----------------------------
# Load Data
# -----------------------------

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Loaded {len(data)} replies.")

# -----------------------------
# Initialize Metrics
# -----------------------------

smooth = SmoothingFunction().method1

rouge = rouge_scorer.RougeScorer(
    ["rougeL"],
    use_stemmer=True
)



results = []

# -----------------------------
# Evaluation
# -----------------------------

for item in tqdm(data):

    reference = item["ideal_reply"]

    generated = item["generated_reply"]

    # ---------------- BLEU ----------------

    bleu = sentence_bleu(
        [reference.split()],
        generated.split(),
        smoothing_function=smooth
    )

    # ---------------- ROUGE ----------------

    rouge_l = rouge.score(
        reference,
        generated
    )["rougeL"].fmeasure

    # ---------------- BERTScore ----------------

    P, R, F1 = bert_score(
        [generated],
        [reference],
        lang="en",
        verbose=False
    )

    bert = float(F1[0])

    # ---------------- Grammar ----------------

    grammar = 1.0

    # ---------------- Length ----------------

    ref_words = len(reference.split())

    gen_words = len(generated.split())

    length = 1 - abs(ref_words - gen_words) / max(
        ref_words,
        gen_words
    )

    # ---------------- Local Score ----------------

    local_score = (

    bleu * 0.20 +

    rouge_l * 0.25 +

    bert * 0.45 +

    length * 0.10

    ) * 100

    results.append({

        "id": item["id"],

        "category": item["category"],

        "BLEU": round(bleu, 4),

        "ROUGE_L": round(rouge_l, 4),

        "BERTScore": round(bert, 4),

        "Grammar": round(grammar, 4),

        "Length": round(length, 4),

        "LocalScore": round(local_score, 2)

    })

# -----------------------------
# Save
# -----------------------------

df = pd.DataFrame(results)

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print(df.head())

print("\n==========================")

print(f"Average BLEU       : {df.BLEU.mean():.4f}")

print(f"Average ROUGE-L    : {df.ROUGE_L.mean():.4f}")

print(f"Average BERTScore  : {df.BERTScore.mean():.4f}")

print(f"Average Grammar    : {df.Grammar.mean():.4f}")

print(f"Average LocalScore : {df.LocalScore.mean():.2f}")

print("==========================")