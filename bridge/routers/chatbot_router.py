from ninja import Router
from bridge.schemas.chatbot_schema import ChatRequest, ChatResponse
from bridge.services.chatbot_service import handle_chat
import os

router_chatbot = Router(tags=["Chatbot"])

@router_chatbot.post("/", response=ChatResponse)
def post_chatbot(request, payload: ChatRequest):
    reply = handle_chat(payload.message)
    return {"response": reply}

@router_chatbot.get("/check-openai-key/")
def check_openai_key(request):
    key = os.getenv("OPENAI_API_KEY")
    return {
        "key_found": bool(key),
        "starts_with": key[:5] + "..." if key else "❌ Not set"
    }
