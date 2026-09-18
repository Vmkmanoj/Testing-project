from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[ChatMessage] = []
    mode: str = "leave"


class ChatResponse(BaseModel):
    reply: str
    intent: str | None = None