import os
import json
import time
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
import google.generativeai as genai

# -----------------------------
# Configuration
# -----------------------------

load_dotenv()

genai.configure(api_key=os.getenv("LLM_JUDGE"))

model = genai.GenerativeModel("gemini-2.5-flash")

INPUT_FILE = "E:\Gen-AI email suggested-response system\Reply_generator\generated\generated_replies.json"

OUTPUT_FILE = "../results/llm_scores.csv"

REQUESTS_PER_MINUTE = 8
SECONDS_PER_REQUEST = 60 / REQUESTS_PER_MINUTE + 0.5

MAX_RETRIES = 5

os.makedirs("../results", exist_ok=True)

# -----------------------------
# Load replies
# -----------------------------

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Resume support
if os.path.exists(OUTPUT_FILE):
    existing = pd.read_csv(OUTPUT_FILE)
    completed = set(existing["id"].tolist())
    rows = existing.to_dict("records")
    print(f"Loaded {len(completed)} existing evaluations.")
else:
    completed = set()
    rows = []

# -----------------------------
# Judge Function
# -----------------------------

def judge_email(item):

    prompt = f"""
You are an expert evaluator of professional business emails.

Your job is to review an AI-generated email reply.

Evaluate ONLY the generated reply.

Incoming Email:

{item['incoming_email']}

--------------------------------------------------

Generated Reply:

{item['generated_reply']}

--------------------------------------------------

Score each category from 1 to 10.

Evaluation Criteria

1. Professionalism
2. Completeness
3. Helpfulness
4. Tone Match
5. Grammar
6. Conciseness

Return ONLY valid JSON.

Example:

{{
    "professionalism":9,
    "completeness":8,
    "helpfulness":10,
    "tone_match":9,
    "grammar":10,
    "conciseness":8,
    "overall":9.0,
    "feedback":"Excellent professional response."
}}

No markdown.
No explanation.
Only JSON.
"""

    for attempt in range(MAX_RETRIES):

        try:

            response = model.generate_content(prompt)

            text = response.text.strip()

            if text.startswith("```"):
                text = text.split("\n",1)[1]
                text = text.rsplit("```",1)[0]

            return json.loads(text)

        except Exception as e:

            wait = (attempt + 1) * 10

            print(f"Retry {attempt+1} after {wait}s")

            print(e)

            time.sleep(wait)

    return None

# -----------------------------
# Main Loop
# -----------------------------

for item in tqdm(data):

    if item["id"] in completed:
        continue

    result = judge_email(item)

    if result is None:
        continue

    rows.append({

        "id": item["id"],

        "Professionalism": result["professionalism"],

        "Completeness": result["completeness"],

        "Helpfulness": result["helpfulness"],

        "ToneMatch": result["tone_match"],

        "Grammar": result["grammar"],

        "Conciseness": result["conciseness"],

        "LLMScore": result["overall"],

        "Feedback": result["feedback"]

    })

    df = pd.DataFrame(rows)

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    time.sleep(SECONDS_PER_REQUEST)

print("\nFinished!")

print(pd.DataFrame(rows).head())