from fastapi import APIRouter
from pydantic import BaseModel
import os
from groq import Groq
from app.core.prompt import SYSTEM_PROMPT
from app.db.conversations import create_conversation, get_conversations
from app.db.messages import add_message, get_messages

router = APIRouter()

# 1️⃣ Create Groq client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not found in environment")
client = Groq(api_key=GROQ_API_KEY)

# 2️⃣ Pydantic models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    conversation_id: str | None  # If None, we create a new conversation
    messages: list[Message]

# 3️⃣ Chat endpoint
@router.post("/")
async def chat_endpoint(req: ChatRequest):
    # 3a. Create a new conversation if no ID provided
    if not req.conversation_id:
        # conversation = create_conversation(title="New Chat")
        conversation = create_conversation(
            title=req.messages[-1].content[:60]
        )
        conversation_id = conversation["id"]
    else:
        conversation_id = req.conversation_id

    # 3b. Insert user messages into DB
    for msg in req.messages:
        add_message(conversation_id, role=msg.role, content=msg.content)

    # 3c. Prepare messages for Groq API
    messages_for_groq = [{"role": "system", "content": SYSTEM_PROMPT}]
    # Fetch previous messages if you want full context; for now, just the current user message
    messages_for_groq.extend([{"role": m.role, "content": m.content} for m in req.messages])

    # 3d. Call Groq
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages_for_groq,
        stream=False,
        temperature=0.7,
        max_tokens=1024,
    )
    assistant_reply = response.choices[0].message.content

    # 3e. Save assistant response
    add_message(conversation_id, role="assistant", content=assistant_reply)

    return {
        "conversation_id": conversation_id,
        "reply": assistant_reply
    }

# 5️⃣ Optional: fetch list of conversations
@router.get("/conversations")
async def list_conversations():
    return {"conversations": get_conversations()}

# 4️⃣ Endpoint to fetch chat history
@router.get("/{conversation_id}/messages")
async def fetch_messages(conversation_id: str):
    messages = get_messages(conversation_id)
    return {"messages": messages}

# # 5️⃣ Optional: fetch list of conversations
# @router.get("/conversations")
# async def list_conversations():
#     return {"conversations": get_conversations()}
