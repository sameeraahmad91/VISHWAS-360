from pydantic import BaseModel, Field
from typing import Optional, List


class ChatbotResponse(BaseModel):
    intent: str
    response: str

    service_category: Optional[str] = None
    location: Optional[str] = None
    urgency: str = "normal"

    date: Optional[str] = None
    time: Optional[str] = None

    requires_backend_action: bool = False