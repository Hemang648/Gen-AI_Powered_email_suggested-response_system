# 📧 AI Email Suggested Response System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi)
![Gemini](https://img.shields.io/badge/Google-Gemini%202.5%20Flash-4285F4?style=for-the-badge&logo=google)
![Chrome Extension](https://img.shields.io/badge/Chrome-Extension-yellow?style=for-the-badge&logo=googlechrome)
![Machine Learning](https://img.shields.io/badge/NLP-LLM-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

Generate professional AI-powered email replies directly from a Chrome Extension using **Google Gemini 2.5 Flash**, **FastAPI**, and **Prompt Engineering**.

</div>

---

# 🚀 Project Overview

Writing professional email replies takes time, especially when handling customer support, HR communication, or business emails.

This project provides an AI-powered email assistant capable of generating natural, professional, and context-aware email replies based on:

- Email content
- Selected tone
- Additional user instructions
- Gemini AI

The project also includes a modern Chrome Extension so users can generate replies instantly without visiting another website.

---

# ✨ Features

- 🤖 AI-powered email reply generation
- ✨ Multiple reply tones
- 📌 Additional custom instructions
- 🔐 Bring Your Own Gemini API Key
- 💾 API key saved locally in Chrome Storage
- 📋 One-click copy reply
- ⚡ FastAPI backend
- 🌐 Deployable on Render
- 🔄 Retry mechanism for temporary API failures
- ⚠️ Proper handling of:
  - Invalid API Keys
  - API Quota Exhaustion
  - Network Errors

---

# 🛠 Tech Stack

## Backend

- Python
- FastAPI
- Google Gemini 2.5 Flash API
- Pydantic
- Uvicorn

## Frontend

- HTML
- CSS
- JavaScript

## Chrome Extension

- Manifest V3
- Chrome Storage API
- Fetch API

## Dataset & Evaluation

- JSON Dataset
- BLEU Score
- ROUGE-L Score
- LLM Judge Evaluation
- Local Quality Evaluation

---

# 📂 Project Structure

```text
AI-Email-Suggested-Response-System/

│
├── api/
│   └── app.py
│
├── dataset/
│   ├── emails.json
│   └── emails.csv
│
├── Reply_generator/
│   ├── generated/
│   └── reply_generater.py
│
├── evaluation and score/
│   ├── evaluate_old.py
│   ├── evaluate_local.py
│   ├── llm_judge.py
│   └── merge_scores.py
│
├── results/
│   ├── final_scores.csv
│   ├── llm_scores.csv
│   └── local_scores.csv
│
├── extension/
│   ├── popup.html
│   ├── popup.js
│   ├── style.css
│   └── manifest.json
│
├── requirements.txt
└── README.md
```

---

# 📊 Dataset Creation

A custom dataset was created consisting of realistic business emails.

Each sample contains:

- Email ID
- Subject
- Incoming Email
- Ideal Reply
- Category
- Tone
- Intent
- Urgency
- Difficulty

Example:

```json
{
"id":1,
"category":"Customer Support",
"tone":"Professional",
"intent":"Refund",
"incoming_email":"...",
"ideal_reply":"..."
}
```

---

# 🤖 Reply Generation Pipeline

The reply generator:

1. Loads dataset
2. Reads email information
3. Builds a dynamic prompt
4. Sends prompt to Gemini 2.5 Flash
5. Receives generated reply
6. Saves reply into JSON
7. Supports resume if generation stops

---

# 🧠 Prompt Engineering

The model receives:

- Email
- Tone
- Subject
- Intent
- Category
- Urgency
- Additional Instructions

The prompt ensures:

- Professional language
- Concise responses
- No hallucinations
- Proper closing
- Context-aware replies

---

# 📈 Evaluation

The generated replies were evaluated using multiple approaches.

### Traditional Metrics

- BLEU
- ROUGE-L

### Local Evaluation

- Grammar
- Readability
- Length

### LLM-as-a-Judge

Gemini evaluates generated replies on:

- Relevance
- Professionalism
- Helpfulness
- Tone
- Overall Quality

The individual scores are merged into a final evaluation report.

---

# 🌐 API

FastAPI exposes a REST API.

### POST

```
/generate
```

Example Request

```json
{
    "email":"...",
    "tone":"Professional",
    "additional_instruction":"Keep it short.",
    "api_key":"YOUR_GEMINI_KEY"
}
```

Example Response

```json
{
"success":true,
"reply":"..."
}
```

---

# 🧩 Chrome Extension

The project includes a Chrome Extension built using Manifest V3.

Features:

- Paste email
- Select tone
- Optional instructions
- Bring Your Own Gemini API Key
- Save API Key locally
- Generate reply
- Copy reply

---

# 🔑 Bring Your Own API Key

Users can use their own Gemini API Key.

The key is:

- Stored locally
- Never uploaded anywhere except Google's Gemini API
- Can be replaced anytime

Get your free Gemini API Key:

https://aistudio.google.com/apikey

---

# 🖥 Screenshots

## Extension Home



![Extension Home](IMAGES/HOME_INTERFACE.png)

---

## Generated Reply



![Generated Reply](IMAGES/AI_reply.png)

---

## API Key


![API Key](IMAGES/API_KEYS.png)

---

## Evaluation Results


![Evaluation](IMAGES/FINAL_SCORE_TABLE.png)

---

# ⚙ Installation

## 1 Clone Repository

```bash
git clone https://github.com/yourusername/AI-Email-Suggested-Response-System.git

cd AI-Email-Suggested-Response-System
```

---

## 2 Install Requirements

```bash
pip install -r requirements.txt
```

---

## 3 Start Backend

```bash
uvicorn api.app:app --reload
```

Backend runs at

```
http://127.0.0.1:8000
```

---

# 🧩 Load Chrome Extension

1. Download or clone this repository.

2. Open Chrome.

3. Navigate to:

```
chrome://extensions
```

4. Enable **Developer Mode**.

5. Click **Load Unpacked**.

6. Select the **extension** folder from this project.

7. Pin the extension.

8. Open the extension and enter your Gemini API Key.

9. Paste an email and generate professional AI replies instantly.

---

# 🚀 Deployment

The backend is currently deployed on **Render** using **FastAPI**, making it accessible over the internet for the Chrome Extension.

### Current Deployment

- ✅ Backend Hosting: **Render**
- ✅ Framework: **FastAPI**
- ✅ Public REST API Endpoint
- ✅ CORS Enabled for Chrome Extension Requests

### Keeping the Backend Alive

Render's free tier may put inactive services to sleep after a period of inactivity.

To minimize cold starts and keep the API responsive, a **Cron Job (Uptime Monitor)** periodically sends requests to the backend's health endpoint.

This ensures:

- 🚀 Faster response times
- ⏰ Reduced cold starts
- 🌐 Improved availability for extension users

### Health Check Endpoint

```
GET /
```

Example Response

```json
{
    "status": "running",
    "project": "Gen-AI Email Suggested Response System"
}
```

### Other Supported Deployment Platforms

Although this project is currently deployed on **Render**, it can also be deployed on:

- Railway
- Azure
- AWS
- Google Cloud Platform (GCP)

The Chrome Extension simply communicates with the deployed FastAPI endpoint, allowing users to generate AI-powered email replies from anywhere.
---

# 🔒 Error Handling

The application handles:

- Invalid API Key
- API Quota Exhausted
- Network Failure
- Server Errors
- Empty Input

---

# 📌 Future Improvements

- Gmail Integration
- Outlook Integration
- Reply History
- Multi-language Support
- One-click Email Sending
- Smart Email Classification
- Streaming Responses
- Reply Templates
- Dark/Light Themes
- User Authentication

---

# 👨‍💻 Developed By

**Hemang Joshi**

Computer Science Engineer

AI • Machine Learning • Software Engineer • Data Engineering

GitHub: https://github.com/Hemang648

LinkedIn: https://www.linkedin.com/in/hemangjoshi12/

---

# ⭐ If you like this project

Give this repository a ⭐ on GitHub.

It really helps!

---
