"""FastAPI AI, heatmap, and expansion endpoints backed by Supabase state."""
from __future__ import annotations

import os
import tempfile
from datetime import datetime, timezone
from typing import Any

from fastapi import File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field

try:
    from .main import app
    from .supabase_client import supabase
except ImportError:
    from main import app
    from supabase_client import supabase


class StatePayload(BaseModel):
    state: dict[str, Any] = Field(default_factory=dict)


class UnderstandPayload(BaseModel):
    text: str
    channel: str = "text"


INTENTS = {
    "Electrician": ["light", "fan", "switch", "wiring", "current", "बिजली", "पंखा"],
    "Plumber": ["tap", "leak", "pipe", "water", "drain", "toilet", "नल", "पानी", "लीक"],
    "AC Repair": ["ac", "air condition", "cooling", "gas refill", "एसी", "कूलिंग"],
    "Carpenter": ["door", "wood", "furniture", "hinge", "cupboard", "दरवाजा", "लकड़ी"],
    "Painter": ["paint", "wall", "putty", "whitewash", "पेंट", "दीवार"],
    "Appliance Repair": ["fridge", "washing machine", "microwave", "geyser", "tv", "फ्रिज"],
    "Cleaning": ["clean", "sofa", "deep clean", "bathroom", "सफाई"],
    "Mechanic": ["bike", "car", "engine", "puncture", "battery", "गाड़ी", "बाइक"],
}
URGENT = ["urgent", "emergency", "immediately", "sparking", "flood", "smoke", "gas leak", "तुरंत", "आपात"]


def classify(text: str):
    lowered = (text or "").lower()
    scores = {service: sum(word in lowered for word in words) for service, words in INTENTS.items()}
    service, hits = max(scores.items(), key=lambda item: item[1])
    confidence = min(0.55 + 0.12 * hits, 0.98) if hits else 0.45
    urgent = any(word in lowered for word in URGENT)
    return service, confidence, urgent


@app.get("/sync/state")
def get_sync_state():
    result = supabase.table("app_state").select("payload, updated_at").eq("state_key", "streamlit").limit(1).execute()
    row = (result.data or [None])[0]
    return {"success": True, "state": row.get("payload") if row else None, "updated_at": row.get("updated_at") if row else None}


@app.put("/sync/state")
def put_sync_state(payload: StatePayload):
    if not payload.state.get("providers") or payload.state.get("bookings") is None:
        raise HTTPException(422, "state must contain providers and bookings")
    now = datetime.now(timezone.utc).isoformat()
    record = {"state_key": "streamlit", "payload": payload.state, "updated_at": now}
    result = supabase.table("app_state").upsert(record, on_conflict="state_key").execute()
    return {"success": True, "updated_at": now, "state": result.data[0] if result.data else record}


@app.post("/ai/understand")
def understand(payload: UnderstandPayload):
    service, confidence, urgent = classify(payload.text)
    reply = f"I identified this as a {service} request ({confidence:.0%} confidence)."
    if urgent: reply = f"🚨 This is urgent. I identified a {service} request and prioritised emergency-ready professionals."
    return {"success": True, "service": service, "confidence": confidence, "urgent": urgent, "channel": payload.channel, "reply": reply}


@app.post("/voice/transcribe")
def voice_transcribe(audio: UploadFile = File(...), language: str = Form("")):
    """Transcribe uploaded audio with faster-whisper when installed on the API host."""
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise HTTPException(503, "Whisper is not installed on the API host") from exc
    suffix = os.path.splitext(audio.filename or "voice.webm")[1] or ".webm"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as target:
        target.write(audio.file.read()); path = target.name
    try:
        model = WhisperModel(os.getenv("WHISPER_MODEL", "small"), device="cpu", compute_type="int8")
        segments, info = model.transcribe(path, language=language or None)
        transcript = " ".join(segment.text.strip() for segment in segments).strip()
        return {"success": True, "transcript": transcript, "language": getattr(info, "language", language)}
    finally:
        try: os.remove(path)
        except OSError: pass
