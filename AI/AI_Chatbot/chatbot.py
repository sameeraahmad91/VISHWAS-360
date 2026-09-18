"""Compatibility wrapper for the chatbot used by the API and CLI clients."""
from .intent_detector import detect_intent

class VishvasChatbot:
    def process_message(self, user_message: str, conversation_history=None):
        return detect_intent(user_message, conversation_history or [])
