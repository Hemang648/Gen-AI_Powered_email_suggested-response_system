import os
import json
import time
import logging
from dotenv import load_dotenv
from tqdm import tqdm
import google.generativeai as genai

# -----------------------------
# Configuration
# -----------------------------

CURRENT_API_KEY = None
MODEL = None

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


REQUESTS_PER_MINUTE = 8
SECONDS_PER_REQUEST = 60 / REQUESTS_PER_MINUTE + 0.5
MAX_RETRIES = 3

# Use a relative path instead of an absolute Windows path
DATASET_PATH = os.path.join("dataset", "emails.json")
OUTPUT_PATH = os.path.join("Reply_generator", "generated", "generated_replies.json")


# ==========================================================
# Reusable Function
# ==========================================================



def generate_reply(
    email,
    tone,
    length="medium",
    additional_instruction="",
    api_key=None
):

    # Configure Gemini
    global CURRENT_API_KEY, MODEL

    key = api_key.strip() if api_key else os.getenv("GEMINI_API_KEY1_reply")

    if not key:
        return {
        "success": False,
        "error": "No Gemini API key provided."
         }

    if key != CURRENT_API_KEY:
        genai.configure(api_key=key)
        MODEL = genai.GenerativeModel("gemini-2.5-flash")
        CURRENT_API_KEY = key
    
    email = email.strip()
    additional_instruction = additional_instruction.strip()
    
    if length=="short":
        word_limit="40-60 words"

    elif length=="long":
        word_limit="150-200 words"

    else:
        word_limit="80-120 words"
    
    prompt = f"""

Reply to the email below.

Tone: {tone}
Extra instructions: {additional_instruction or "None"}

Requirements:

- Reply only
- Professional and natural
- Answer all questions
- Don't invent facts
- Ask for clarification if needed
- Keep the reply around {word_limit}

Email:
{email.strip()}

"""

    for attempt in range(MAX_RETRIES):

        try:
                
            response = MODEL.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                temperature=0.3,
                top_p=0.9,
                top_k=40
        
                                    )
                )
            # Check if Gemini returned an empty response
            if not response.text or not response.text.strip():
                return {
                        "success": False,
                        "error": "Gemini returned an empty response."
                    }
            
            return {
                "success": True,
                "reply": response.text.strip(),
                "model": "gemini-2.5-flash"
            }

        except Exception as e:

            error = str(e).lower()

            logging.error(error)

            # Invalid API key
            if (
                "api key" in error
                or "permission_denied" in error
                or "invalid" in error
                or "authentication" in error
            ):
                return {
                    "success": False,
                    "error": "Invalid Gemini API Key."
                }

            # Quota exceeded
            if (
                "429" in error
                or "quota" in error
                or "resource_exhausted" in error
                or "rate limit" in error
            ):
                return {
                    "success": False,
                    "error": "Gemini API quota exhausted."
                }

            # Retry only for temporary server issues
            if (
                "500" in error
                or "503" in error
                or "internal" in error
            ):
                wait = min(2 ** attempt, 10)
                print(f"Retrying in {wait}s...")
                time.sleep(wait)
                continue

            return {
                "success": False,
                "error": str(e)
            }

    return {
        "success": False,
        "error": "Maximum retries exceeded."
    }
# ==========================================================
# Standalone Script
# ==========================================================

if __name__ == "__main__":

    # -----------------------------
    # Load Dataset
    # -----------------------------

    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    # Resume support

    if os.path.exists(OUTPUT_PATH):

        with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
            generated = json.load(f)

        print(f"Loaded {len(generated)} existing replies.")

    else:

        generated = []

    completed_ids = {item["id"] for item in generated}

    # -----------------------------
# Generate Replies
# -----------------------------

    for item in tqdm(dataset):
    
        if item["id"] in completed_ids:
            continue
        
        result = generate_reply(
            email=item["incoming_email"],
            tone=item["tone"],
            length=item.get("length", "medium"),
            additional_instruction=item.get("additional_instruction", "")
)
    
        if not result["success"]:
            print(f"Reply {item['id']} failed: {result['error']}")
    
            if "quota" in result["error"].lower():
                print("\nGemini API quota exhausted. Stopping generation.")
                break
            
            continue
        
        reply = result["reply"]
    
        generated.append({
        
            "id": item["id"],
    
            "category": item["category"],
    
            "subject": item["subject"],
    
            "incoming_email": item["incoming_email"],
    
            "ideal_reply": item["ideal_reply"],
    
            "generated_reply": reply,
    
            "tone": item["tone"]
    
        })
    
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(generated, f, indent=4, ensure_ascii=False)
    
        print(f"Saved Reply {item['id']}")
    
        time.sleep(SECONDS_PER_REQUEST)
    
    print("\nFinished!")
    
    print(f"Generated Replies: {len(generated)}")
    
    print(f"Saved to: {OUTPUT_PATH}")
    
    
    
###################----------------------DID FOR TESTING----------------------------####################
    
# import os
# import json
# import time
# from dotenv import load_dotenv
# import pandas as pd
# from tqdm import tqdm
# from dotenv import load_dotenv
# import google.generativeai as genai

# # -----------------------------
# # Configuration
# # -----------------------------
# load_dotenv()

# genai.configure(api_key=os.getenv("GEMINI_API_KEY1_reply"))

# model = genai.GenerativeModel("gemini-2.5-flash")

# REQUESTS_PER_MINUTE = 8
# SECONDS_PER_REQUEST = 60 / REQUESTS_PER_MINUTE + 0.5
# MAX_RETRIES = 5

# DATASET_PATH = "E:\Gen-AI email suggested-response system\dataset\emails.json"
# OUTPUT_PATH = "generated/generated_replies.json"
# if __name__ =="__main__":
# # -----------------------------
# # Load Dataset
# # -----------------------------
#     with open(DATASET_PATH, "r", encoding="utf-8") as f:
#     dataset = json.load(f)
    
#     os.makedirs("generated", exist_ok=True)
    
#     # Resume if output already exists
#     if os.path.exists(OUTPUT_PATH):
#         with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
#             generated = json.load(f)
#         print(f"Loaded {len(generated)} existing replies.")
#     else:
#         generated = []
    
#     completed_ids = {item["id"] for item in generated}
    
#     # -----------------------------
#     # Reply Generator
#     # -----------------------------
#     # def generate_reply(email, tone, category, urgency, intent, subject):
    
#     #     prompt = f"""
#     # Here's a version I'd use:
    
#     # You are an expert business email assistant.
    
#     # Write a professional, helpful, and natural email reply.
    
#     # Context:
    
#     # Category: {category}
#     # Subject: {subject}
#     # Intent: {intent}
#     # Urgency: {urgency}
#     # Tone: {tone}
    
#     # Instructions:
    
#     # - Reply as a real support or business representative.
#     # - Address every question or concern.
#     # - Keep the response concise.
#     # - Maintain the requested tone.
#     # - If information is missing, politely ask for it instead of guessing.
#     # - End with an appropriate professional closing.
#     # - Return ONLY the email body without markdown or explanations.
    
#     # Incoming Email:
    
#     # {email}
#     # """
    
#     #     for attempt in range(MAX_RETRIES):
    
#     #         try:
    
#     #             response = model.generate_content(prompt)
    
#     #             return response.text.strip()
    
#     #         except Exception as e:
    
#     #             wait = (attempt + 1) * 10
    
#     #             print(f"Retrying in {wait}s...")
#     #             print(e)
    
#     #             time.sleep(wait)
    
#     #     return None
    
#     MAX_RETRIES = 5
    
#     def generate_reply(
#         email,
#         tone,
#         category="",
#         urgency="",
#         intent="",
#         subject="",
#         additional_instruction=""
#     ):
    
#         prompt = f"""
#     You are an expert business email assistant.
    
#     Write a professional, natural, and helpful reply.
    
#     Category:
#     {category}
    
#     Subject:
#     {subject}
    
#     Intent:
#     {intent}
    
#     Urgency:
#     {urgency}
    
#     Tone:
#     {tone}
    
#     Additional Instructions:
#     {additional_instruction}
    
#     Incoming Email:
    
#     {email}
    
#     Rules
    
#     - Answer every concern.
#     - Don't invent facts.
#     - Keep it concise.
#     - End professionally.
#     - Return ONLY the email.
#     """
    
#         for attempt in range(MAX_RETRIES):
        
#             try:
            
#                 response = model.generate_content(prompt)
    
#                 return response.text.strip()
    
#             except Exception as e:
            
#                 wait = (attempt + 1) * 10
    
#                 print(e)
    
#                 time.sleep(wait)
    
#         return None
    
#     # -----------------------------
#     # Generate Replies
#     # -----------------------------
#     for item in tqdm(dataset):
    
#         if item["id"] in completed_ids:
#             continue
        
#         reply = generate_reply(
#             item["incoming_email"],
#             item["tone"],
#             item["category"],
#             item["urgency"],
#             item["intent"],
#             item["subject"]
            
#         )
    
#         if reply is None:
#             continue
        
#         generated.append({
        
#             "id": item["id"],
    
#             "category": item["category"],
    
#             "subject": item["subject"],
    
#             "incoming_email": item["incoming_email"],
    
#             "ideal_reply": item["ideal_reply"],
    
#             "generated_reply": reply,
    
#             "tone": item["tone"]
    
#         })
    
#         with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
#             json.dump(generated, f, indent=4, ensure_ascii=False)
    
#         time.sleep(SECONDS_PER_REQUEST)
    
#     print(f"\nGenerated replies: {len(generated)}")
#     print(f"Saved to {OUTPUT_PATH}")
