"""HTTP client for AI and marketplace analytics."""
from __future__ import annotations

import os
from typing import Any

import requests

API_URL = os.getenv("VISHWAS_API_URL", "").rstrip("/")
TIMEOUT = float(os.getenv("VISHWAS_API_TIMEOUT", "12"))


def enabled() -> bool:
    return bool(API_URL)


def _url(path: str) -> str:
    return f"{API_URL}/{path.lstrip('/')}"


def pull_state() -> dict[str, Any] | None:
    if not enabled():
        return None
    try:
        response = requests.get(_url("sync/state"), timeout=TIMEOUT)
        response.raise_for_status()
        state = response.json().get("state")
        return state if state and state.get("providers") is not None else None
    except (requests.RequestException, ValueError):
        return None


def push_state(state: dict[str, Any]) -> bool:
    if not enabled():
        return False
    try:
        response = requests.put(_url("sync/state"), json={"state": state}, timeout=TIMEOUT)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False


def understand(text: str, *, channel: str = "text") -> dict[str, Any] | None:
    """Use the FastAPI AI gateway, returning None so the local engine can fall back."""
    if not enabled():
        return None
    try:
        response = requests.post(_url("ai/understand"), json={"text": text, "channel": channel}, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError):
        return None


def transcribe(audio: Any, language: str | None = None) -> str | None:
    """Send a recorded Streamlit UploadedFile to the optional Whisper service."""
    if not enabled() or audio is None:
        return None
    try:
        audio.seek(0)
        files = {"audio": (getattr(audio, "name", "voice.webm"), audio.read(), getattr(audio, "type", "audio/webm"))}
        data = {"language": language or ""}
        response = requests.post(_url("voice/transcribe"), files=files, data=data, timeout=60)
        response.raise_for_status()
        return response.json().get("transcript")
    except (requests.RequestException, ValueError, AttributeError):
        return None
