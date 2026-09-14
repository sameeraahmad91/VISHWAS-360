import json
from groq import Groq

from .config import GROQ_API_KEY, MODEL_NAME
from .prompts import SYSTEM_PROMPT
from .schemas import ChatbotResponse


class VishvasChatbot:

    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = MODEL_NAME

    def process_message(
        self,
        user_message: str,
        conversation_history=None
    ):

        if conversation_history is None:
            conversation_history = []

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        # Add previous conversation context
        messages.extend(conversation_history)

        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })

        try:

            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                response_format={"type": "json_object"}
            )

            raw_response = completion.choices[0].message.content

            parsed_response = json.loads(raw_response)

            validated_response = ChatbotResponse(**parsed_response)

            return validated_response.model_dump()

        except Exception as e:

            print(f"Chatbot Error: {e}")

            return {
                "intent": "unknown",
                "response": "Sorry, I am having trouble understanding your request right now.",
                "service_category": None,
                "location": None,
                "urgency": "normal",
                "date": None,
                "time": None,
                "requires_backend_action": False
            }