"""Supabase connection used by the FastAPI service.

Only the backend may use the service-role key. Never put this key in Streamlit,
JavaScript, or a public repository.
"""
from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import Client, create_client

# Make local execution independent of the current working directory.
load_dotenv(Path(__file__).resolve().parents[1] / ".env")
load_dotenv()

SUPABASE_URL = (os.getenv("SUPABASE_URL") or "").strip().rstrip("/")
SUPABASE_KEY = (os.getenv("SUPABASE_SERVICE_ROLE_KEY") or "").strip()

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "Supabase is not configured. Create .env from .env.example and set "
        "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY before starting the API."
    )

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
