import os
import pandas as pd

# ---------------------------------------------------
# Configuration
# ---------------------------------------------------

LOCAL_FILE = "../results/local_scores.csv"
LLM_FILE = "../results/llm_scores.csv"

OUTPUT_FILE = "../results/final_scores.csv"

# ---------------------------------------------------
# Load
# ---------------------------------------------------

if not os.path.exists(LOCAL_FILE):
    raise FileNotFoundError(f"{LOCAL_FILE} not found.")

if not os.path.exists(LLM_FILE):
    raise FileNotFoundError(f"{LLM_FILE} not found.")

local = pd.read_csv(LOCAL_FILE)
llm = pd.read_csv(LLM_FILE)

# ---------------------------------------------------
# Merge
# ---------------------------------------------------

df = local.merge(llm, on="id", how="inner")

# ---------------------------------------------------
# Normalize LLM score
# LLMScore is assumed to be out of 10
# ---------------------------------------------------

df["LLMScoreNorm"] = df["LLMScore"] / 10

# ---------------------------------------------------
# Final Weighted Score
# ---------------------------------------------------

df["FinalScore"] = (

    df["BLEU"] * 0.15 +

    df["ROUGE_L"] * 0.15 +

    df["BERTScore"] * 0.35 +

    df["LLMScoreNorm"] * 0.35

) * 100

df["FinalScore"] = df["FinalScore"].round(2)

# ---------------------------------------------------
# Rating
# ---------------------------------------------------

def rating(score):

    if score >= 90:
        return "Excellent"

    elif score >= 80:
        return "Very Good"

    elif score >= 70:
        return "Good"

    elif score >= 60:
        return "Fair"

    else:
        return "Needs Improvement"


df["Rating"] = df["FinalScore"].apply(rating)

# ---------------------------------------------------
# Save
# ---------------------------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False
)

# ---------------------------------------------------
# Summary
# ---------------------------------------------------

print("\n========== Evaluation Summary ==========\n")

print(f"Total Replies Evaluated : {len(df)}")

print(f"Average BLEU       : {df['BLEU'].mean():.4f}")
print(f"Average ROUGE-L    : {df['ROUGE_L'].mean():.4f}")
print(f"Average BERTScore  : {df['BERTScore'].mean():.4f}")
print(f"Average LLM Score  : {df['LLMScore'].mean():.2f}/10")
print(f"Average FinalScore : {df['FinalScore'].mean():.2f}/100")

print("\nRating Distribution\n")

print(df["Rating"].value_counts())

print("\nTop 5 Replies\n")

print(
    df[
        [
            "id",
            "FinalScore",
            "Rating",
            "Feedback"
        ]
    ]
    .sort_values(
        "FinalScore",
        ascending=False
    )
    .head()
)

print(f"\nSaved merged report to:\n{OUTPUT_FILE}")