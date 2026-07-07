import os
import json
import time
import random
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

CATEGORIES = [
    "Customer Complaint",
    "Refund Request",
    "Technical Support",
    "Interview Invitation",
    "Meeting Scheduling",
    "Leave Request",
    "Sales Inquiry",
    "Partnership Proposal",
    "Feature Request",
    "Order Delay",
    "Subscription Cancellation",
    "Password Reset",
    "Internal Team Communication",
    "HR Query",
    "Finance Query",
    "General Inquiry",
    "Thank You",
    "Follow-up",
    "Job Application",
    "Product Feedback"
]

TONES = [
    "Professional",
    "Friendly",
    "Formal",
    "Empathetic",
    "Confident"
]

DIFFICULTY = [
    "Easy",
    "Medium",
    "Hard"
]


def generate_batch(category, tone, difficulty):

    prompt = f"""
Generate {BATCH_SIZE} UNIQUE realistic business email examples.

Every email must differ in:

- company
- sender
- context
- writing style
- urgency
- subject
- intent

Category:
{category}

Reply Tone:
{tone}

Difficulty:
{difficulty}

Return ONLY a JSON array.

Example:

[
 {{
    "subject":"",
    "sender_name":"",
    "incoming_email":"",
    "ideal_reply":"",
    "intent":"",
    "sentiment":"",
    "urgency":"",
    "tone":"{tone}"
 }},
 ...
]

Rules

Generate {BATCH_SIZE} completely different emails.

Different subjects.

Different names.

Different companies.

Different scenarios.

No markdown.

No explanation.

Return ONLY JSON.
"""

    for attempt in range(MAX_RETRIES):

        try:

            response = model.generate_content(prompt)

            text = response.text.strip()

            if text.startswith("```"):
                text = text.split("\n",1)[1]
                text = text.rsplit("```",1)[0]

            data = json.loads(text)

            if isinstance(data, list):
                return data

        except Exception as e:

            print(e)

            wait = 10 * (attempt + 1)

            print(f"Retrying in {wait} sec...")

            time.sleep(wait)

    return []



TOTAL = 100
BATCH_SIZE = 10
# Free-tier safe settings
REQUESTS_PER_MINUTE = 8      # Conservative
SECONDS_PER_REQUEST = 60 / REQUESTS_PER_MINUTE + 0.5
MAX_RETRIES = 10



os.makedirs("dataset", exist_ok=True)

json_file = "dataset/emails.json"
csv_file = "dataset/emails.csv"

# Resume if dataset already exists
if os.path.exists(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        dataset = json.load(f)
    print(f"Loaded {len(dataset)} existing samples.")
else:
    dataset = []
    

while len(dataset) < TOTAL:

    category = random.choice(CATEGORIES)

    tone = random.choice(TONES)

    difficulty = random.choice(DIFFICULTY)

    print(f"\nGenerating batch... Current size = {len(dataset)}")

    batch = generate_batch(category, tone, difficulty)

    if not batch:

        print("Failed batch.")

        continue

    for item in batch:

        if len(dataset) >= TOTAL:
            break

        duplicate = any(
            d["incoming_email"].strip().lower()
            == item["incoming_email"].strip().lower()
            for d in dataset
        )

        if duplicate:
            continue

        item["id"] = len(dataset) + 1
        item["category"] = category
        item["difficulty"] = difficulty

        dataset.append(item)

    with open(json_file, "w", encoding="utf-8") as f:

        json.dump(dataset, f, indent=4, ensure_ascii=False)

    pd.DataFrame(dataset).to_csv(
        csv_file,
        index=False,
        encoding="utf-8"
    )

    print(f"Saved {len(dataset)} examples.")

    time.sleep(SECONDS_PER_REQUEST)
    
    
print(f"\nFinished! Total samples: {len(dataset)}")
print("Dataset saved successfully.")