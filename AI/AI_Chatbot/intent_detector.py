"""Production-safe intent detection with an optional Groq enhancement.

The deterministic fallback keeps booking available when no LLM key is configured.
"""
from __future__ import annotations
import json
import os
import re
from typing import Any

SERVICES = {
    "Electrician": ("electric wiring switch fan short circuit bijli light current"),
    "Plumber": ("pipe leak tap plumber paani water nal drainage"),
    "AC Repair": (" ac cooling cooler gas refill air conditioner"),
    "Carpenter": ("furniture door carpenter wood almirah"),
    "Painter": ("paint wall colour color whitewash"),
    "Appliance Repair": ("washing machine fridge refrigerator oven microwave tv appliance"),
    "Cleaning": ("clean cleaning safai sofa house office"),
    "Mechanic": ("bike scooter car engine mechanic vehicle puncture"),
}
EMERGENCY = {"emergency", "urgent", "asap", "immediately", "abhi", "jaldi", "fire", "danger"}

def _fallback(message: str) -> dict[str, Any]:
    text = message.lower()
    service = next((name for name, words in SERVICES.items() if any(re.search(rf"\b{re.escape(word.strip())}\b", text) for word in words.split())), None)
    urgent = any(word in text for word in EMERGENCY)
    if service:
        response = f"This looks like a {service} request. I can find verified providers{\' urgently\' if urgent else \'\'} near you."
    else:
        response = "Please describe what needs fixing and your area; I will identify the right service and find a verified provider."
    return {"intent": "emergency_service" if urgent else ("find_service" if service else "unknown"), "response": response, "service_category": service, "location": None, "urgency": "high" if urgent else "normal", "date": None, "time": None, "requires_backend_action": bool(service)}

def detect_intent(message: str, history: list[dict[str, str]] | None = None) -> dict[str, Any]:
    fallback = _fallback(message)
    key = os.getenv("GROQ_API_KEY")
    if not key:
        return fallback
    try:
        from groq import Groq
        completion = Groq(api_key=key).chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
            temperature=0.1,
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": "Return JSON with intent,response,service_category,location,urgency,date,time,requires_backend_action. Never invent providers."}, *(history or [])[-6:], {"role": "user", "content": message}],
        )
        result = json.loads(completion.choices[0].message.content)
        return {**fallback, **result}
    except Exception:
        return fallback
