"""HTTP client for synchronising the Streamlit demo with the FastAPI backend."""
from __future__ import annotations

import os
from typing import Any

import requests


API_URL = os.getenv("VISHWAS_API_URL", "").rstrip("/")
TIMEOUT = float(os.getenv("VISHWAS_API_TIMEOUT", "8"))


def enabled() -> bool:
    return bool(API_URL)


def _url(path: str) -> str:
    return f"{API_URL}/{path.lstrip('/')}"


def pull_state() -> dict[str, Any] | None:
    """Return persisted marketplace state from FastAPI, or None when offline."""
    if not enabled():
        return None
    try:
        response = requests.get(_url("sync/state"), timeout=TIMEOUT)
        response.raise_for_status()
        payload = response.json()
        state = payload.get("state")
        return state if state and state.get("providers") is not None else None
    except (requests.RequestException, ValueError):
        return None


def push_state(state: dict[str, Any]) -> bool:
    """Persist the current Streamlit state through FastAPI/Supabase."""
    if not enabled():
        return False
    try:
        response = requests.put(_url("sync/state"), json={"state": state}, timeout=TIMEOUT)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False
