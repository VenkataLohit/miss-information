from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables
load_dotenv()

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Request schema
class ScanRequest(BaseModel):
    text: str

# Health check
@app.get("/")
def home():
    return {"message": "Backend running"}

# 🔥 EXACT ENDPOINT YOUR FRONTEND CALLS
@app.post("/analyze")
def analyze(data: ScanRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a misinformation detection assistant. "
                        "Analyze the claim and clearly state whether it is "
                        "true, false, misleading, or unverified. "
                        "Explain briefly."
                    )
                },
                {
                    "role": "user",
                    "content": data.text
                }
            ]
        )

        # 🔑 FRONTEND EXPECTS 'verdict'
        return {
            "verdict": response.choices[0].message.content
        }

    except Exception as e:
        # 🔑 FRONTEND EXPECTS 'error'
        return {
            "error": str(e)
        }
