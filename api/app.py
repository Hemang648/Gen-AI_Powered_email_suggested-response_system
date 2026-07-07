from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from Reply_generator.reply_generater import generate_reply

app = FastAPI(
    title="AI Email Reply API",
    description="Backend for AI Email Suggested Response System",
    version="1.0"
)

# -----------------------------------
# Allow Chrome Extension
# -----------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------
# Request Model
# -----------------------------------

class EmailRequest(BaseModel):

    email: str

    tone: str = "Professional"

    category: str = ""

    urgency: str = ""

    intent: str = ""

    subject: str = ""

    additional_instruction: str = ""

    api_key: str = ""
    
    


# -----------------------------------
# Health Check
# -----------------------------------

@app.get("/")
def home():

    return {

        "status": "running",

        "project": "Gen-AI Email Suggested Response System"

    }


# -----------------------------------
# Generate Reply
# -----------------------------------

@app.post("/generate")
def generate(req: EmailRequest):

    reply = generate_reply(

        email=req.email,

        tone=req.tone,

        category=req.category,

        urgency=req.urgency,

        intent=req.intent,

        subject=req.subject,

        additional_instruction=req.additional_instruction,

        api_key=req.api_key

    )

    return {

        "success": reply is not None,

        "reply": reply

    }