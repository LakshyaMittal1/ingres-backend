from fastapi import FastAPI
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware

# 1️⃣ Load .env before anything else
load_dotenv()

from app.api.chat import router as chat_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify: ["https://a08fb3a4-294c-4102-8c5d-6ef26499b295.lovableproject.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/chat")


""" from fastapi import FastAPI
from pydantic import BaseModel
import os
from groq import Groq
from app.core.prompt import SYSTEM_PROMPT

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    messages = [{"role": m.role, "content": m.content} for m in req.messages]
    messages.insert(0, {"role": "system", "content": SYSTEM_PROMPT})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        stream=False,  # <- important, no streaming
        temperature=0.7,
        max_tokens=1024,
    )

    return {"reply": response.choices[0].message.content}
 """