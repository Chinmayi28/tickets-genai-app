import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

if not api_key:
    raise RuntimeError("GROQ_API_KEY is not set")

client = Groq(api_key=api_key)

# 1. Models defined at top
class PromptRequest(BaseModel):
    prompt: str

class PromptResponse(BaseModel):
    response: str
    model: str

# 2. System Prompt defined before routes
SYSTEM_PROMPT = """
You are a technical assistant for a web application.
You are ONLY allowed to answer questions related to:
1. React
2. FastAPI
3. MongoDB
"""

# 3. Router setup
router = APIRouter()

@router.get("/")
def root():
    return {
        "message": "Groq FastAPI server is running",
        "model": model
    }

@router.post("/chat", response_model=PromptResponse)
def chat(request: PromptRequest):
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": request.prompt}
            ]
        )
        return PromptResponse(
            response=completion.choices[0].message.content,
            model=model
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Groq API error: {str(e)}")