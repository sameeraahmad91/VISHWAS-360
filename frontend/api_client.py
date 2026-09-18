"""Small HTTP client for the Streamlit UI. Database writes go through FastAPI."""
from __future__ import annotations
import os
from pathlib import Path
import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")

class APIError(RuntimeError):
    pass

def api_request(method: str, path: str, **kwargs):
    try:
        response = requests.request(method, f"{API_BASE_URL}{path}", timeout=20, **kwargs)
        try: payload = response.json()
        except ValueError: payload = {"detail": response.text}
        if response.status_code >= 400:
            raise APIError(payload.get("detail", f"API error {response.status_code}"))
        return payload
    except requests.RequestException as exc:
        raise APIError(f"Cannot reach API at {API_BASE_URL}. Start FastAPI first: {exc}") from exc

def get(path, **params): return api_request("GET", path, params=params)
def post(path, payload): return api_request("POST", path, json=payload)
def patch(path, payload): return api_request("PATCH", path, json=payload)
