"""Optional backend-backed state synchronisation endpoints.

Run this application instead of backend.main when the Streamlit demo should use
Supabase for its local marketplace state:

    uvicorn backend.sync_api:app --reload
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import HTTPException
from pydantic import BaseModel, Field

try:  # package invocation: uvicorn backend.sync_api:app
    from .main import app
    from .supabase_client import supabase
except ImportError:  # direct invocation from backend/
    from main import app
    from supabase_client import supabase


class StatePayload(BaseModel):
    state: dict[str, Any] = Field(default_factory=dict)


@app.get("/sync/state")
def get_sync_state():
    """Load the Streamlit marketplace snapshot from the app_state table."""
    result = supabase.table("app_state").select("payload, updated_at").eq("state_key", "streamlit").limit(1).execute()
    row = (result.data or [None])[0]
    return {"success": True, "state": row.get("payload") if row else None, "updated_at": row.get("updated_at") if row else None}


@app.put("/sync/state")
def put_sync_state(payload: StatePayload):
    """Upsert a complete demo snapshot; mutations remain behind the API boundary."""
    if not payload.state.get("providers") or payload.state.get("bookings") is None:
        raise HTTPException(status_code=422, detail="state must contain providers and bookings")
    now = datetime.now(timezone.utc).isoformat()
    record = {"state_key": "streamlit", "payload": payload.state, "updated_at": now}
    result = supabase.table("app_state").upsert(record, on_conflict="state_key").execute()
    return {"success": True, "updated_at": now, "state": result.data[0] if result.data else record}
