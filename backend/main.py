# from fastapi import FastAPI
# from supabase_client import supabase

# app = FastAPI(
#     title="VISHVAS 360 API",
#     description="AI-Powered Trusted Local Service Marketplace",
#     version="1.0.0"
# )


# @app.get("/")
# def home():
#     return {
#         "message": "Welcome to VISHVAS 360 API",
#         "status": "running"
#     }


# @app.get("/services")
# def get_services():

#     response = (
#         supabase
#         .table("service_categories")
#         .select("*")
#         .execute()
#     )

#     return {
#         "success": True,
#         "services": response.data
#     }

"""
VISHVAS 360 — FastAPI backend
Endpoints match exactly what app.py (Streamlit frontend) calls.

Run:
    uvicorn main:app --reload
"""

from datetime import date, datetime
from typing import Optional, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from supabase_client import supabase

app = FastAPI(
    title="VISHVAS 360 API",
    description="AI-Powered Trusted Local Service Marketplace",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# MODELS
# ============================================================

class BookingIn(BaseModel):
    customer_id: str
    service_id: int
    provider_id: Optional[int] = None
    booking_date: date
    booking_time: str
    address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None
    is_emergency: bool = False
    estimated_price: Optional[float] = None
    status: str = "pending"


class StatusIn(BaseModel):
    status: str


class ReviewIn(BaseModel):
    booking_id: int
    customer_id: str
    provider_id: Optional[int] = None
    rating: int
    review_text: Optional[str] = None


class PaymentIn(BaseModel):
    booking_id: int
    customer_id: str
    amount: float
    payment_method: str = "upi"


class ComplaintIn(BaseModel):
    booking_id: Optional[int] = None
    customer_id: str
    provider_id: Optional[int] = None
    subject: str
    description: str


class AssistantIn(BaseModel):
    message: str
    user_id: Optional[str] = None


# ============================================================
# HELPERS
# ============================================================

def trust_score(provider_id: int) -> int:
    """
    Computed, not stored. 0-100 from five factors:
      ID verification 20 · ratings 25 · completed jobs 20 · response 20 · complaints 15
    """
    prov = supabase.table("service_providers").select("verification_status") \
        .eq("id", provider_id).single().execute().data or {}
    reviews = supabase.table("reviews").select("rating").eq("provider_id", provider_id).execute().data or []
    done = supabase.table("bookings").select("id", count="exact") \
        .eq("provider_id", provider_id).eq("status", "completed").execute().count or 0
    complaints = supabase.table("complaints").select("id", count="exact") \
        .eq("provider_id", provider_id).execute().count or 0

    verification = 20 if prov.get("verification_status") == "verified" else 8
    avg = sum(r["rating"] for r in reviews) / len(reviews) if reviews else 0
    ratings = (avg / 5) * 25
    jobs = min(done / 50, 1) * 20
    response = 15  # replace with real accept-time telemetry
    conduct = max(0, 15 - complaints * 3)
    return int(round(verification + ratings + jobs + response + conduct))


def enrich_provider(p: dict) -> dict:
    reviews = supabase.table("reviews").select("rating").eq("provider_id", p["id"]).execute().data or []
    svc = supabase.table("provider_services").select("service_id, price") \
        .eq("provider_id", p["id"]).limit(1).execute().data or []
    service_name = None
    price = None
    if svc:
        price = svc[0].get("price")
        cat = supabase.table("service_categories").select("name") \
            .eq("id", svc[0]["service_id"]).single().execute().data or {}
        service_name = cat.get("name")
    profile = supabase.table("profiles").select("full_name, phone") \
        .eq("id", p["profile_id"]).single().execute().data or {}

    return {
        **p,
        "full_name": profile.get("full_name"),
        "service": service_name,
        "price": price,
        "rating": round(sum(r["rating"] for r in reviews) / len(reviews), 1) if reviews else None,
        "reviews": len(reviews),
        "trust_score": trust_score(p["id"]),
    }


def notify(user_id: str, title: str, message: str, kind: str = "booking"):
    supabase.table("notifications").insert({
        "user_id": user_id, "title": title, "message": message,
        "notification_type": kind, "is_read": False,
    }).execute()


# ============================================================
# ROUTES
# ============================================================

@app.get("/")
def home():
    return {"message": "Welcome to VISHVAS 360 API", "status": "running"}


@app.get("/services")
def get_services():
    res = supabase.table("service_categories").select("*").order("name").execute()
    return {"success": True, "services": res.data}


@app.get("/providers")
def get_providers(service_id: Optional[int] = None, verified_only: bool = False):
    q = supabase.table("service_providers").select("*")
    if verified_only:
        q = q.eq("verification_status", "verified")
    providers = q.execute().data or []

    if service_id:
        ids = {row["provider_id"] for row in
               (supabase.table("provider_services").select("provider_id")
                .eq("service_id", service_id).execute().data or [])}
        providers = [p for p in providers if p["id"] in ids]

    enriched = [enrich_provider(p) for p in providers]
    enriched.sort(key=lambda p: p["trust_score"], reverse=True)
    return {"success": True, "providers": enriched}


@app.get("/providers/{provider_id}")
def get_provider(provider_id: int):
    row = supabase.table("service_providers").select("*").eq("id", provider_id).single().execute().data
    if not row:
        raise HTTPException(404, "Provider not found")
    return {"success": True, "provider": enrich_provider(row)}


@app.get("/bookings")
def list_bookings(customer_id: Optional[str] = None, provider_id: Optional[int] = None):
    q = supabase.table("bookings").select("*").order("booking_date", desc=True)
    if customer_id:
        q = q.eq("customer_id", customer_id)
    if provider_id:
        q = q.eq("provider_id", provider_id)
    rows = q.execute().data or []

    cats = {c["id"]: c["name"] for c in
            (supabase.table("service_categories").select("id, name").execute().data or [])}
    out = []
    for b in rows:
        provider_name = None
        if b.get("provider_id"):
            sp = supabase.table("service_providers").select("profile_id") \
                .eq("id", b["provider_id"]).single().execute().data
            if sp:
                pr = supabase.table("profiles").select("full_name") \
                    .eq("id", sp["profile_id"]).single().execute().data or {}
                provider_name = pr.get("full_name")
        out.append({**b, "service": cats.get(b["service_id"]), "provider": provider_name})
    return {"success": True, "bookings": out}


@app.post("/bookings")
def create_booking(payload: BookingIn):
    data = payload.model_dump()
    data["booking_date"] = str(data["booking_date"])

    # Auto-match: highest trust score among providers offering this service.
    if not data.get("provider_id"):
        candidates = get_providers(service_id=data["service_id"], verified_only=True)["providers"]
        if candidates:
            data["provider_id"] = candidates[0]["id"]

    res = supabase.table("bookings").insert(data).execute()
    booking = res.data[0] if res.data else data

    notify(payload.customer_id, "Booking placed",
           f"Request #{booking.get('id')} sent. You'll be told as soon as a provider accepts.")
    return {"success": True, "booking": booking}


@app.patch("/bookings/{booking_id}/status")
def update_status(booking_id: int, payload: StatusIn):
    res = supabase.table("bookings").update({"status": payload.status}) \
        .eq("id", booking_id).execute()
    if not res.data:
        raise HTTPException(404, "Booking not found")
    b = res.data[0]
    notify(b["customer_id"], f"Booking {payload.status}",
           f"Booking #{booking_id} is now {payload.status}.")
    return {"success": True, "booking": b}


@app.get("/notifications/{user_id}")
def get_notifications(user_id: str):
    res = supabase.table("notifications").select("*") \
        .eq("user_id", user_id).order("created_at", desc=True).limit(30).execute()
    return {"success": True, "notifications": res.data}


@app.patch("/notifications/{notification_id}/read")
def mark_read(notification_id: int):
    supabase.table("notifications").update({"is_read": True}).eq("id", notification_id).execute()
    return {"success": True}


@app.post("/payments")
def create_payment(payload: PaymentIn):
    data = payload.model_dump()
    data.update({"payment_status": "paid", "paid_at": datetime.utcnow().isoformat(),
                 "transaction_id": f"TXN{int(datetime.utcnow().timestamp())}"})
    res = supabase.table("payments").insert(data).execute()
    notify(payload.customer_id, "Payment received",
           f"₹{payload.amount:.0f} paid for booking #{payload.booking_id}.", "payment")
    return {"success": True, "payment": res.data[0] if res.data else data}


@app.post("/reviews")
def create_review(payload: ReviewIn):
    data = payload.model_dump()
    if not data.get("provider_id"):
        b = supabase.table("bookings").select("provider_id") \
            .eq("id", data["booking_id"]).single().execute().data or {}
        data["provider_id"] = b.get("provider_id")
    res = supabase.table("reviews").insert(data).execute()
    return {"success": True, "review": res.data[0] if res.data else data}


@app.post("/complaints")
def create_complaint(payload: ComplaintIn):
    res = supabase.table("complaints").insert(payload.model_dump()).execute()
    return {"success": True, "complaint": res.data[0] if res.data else payload.model_dump()}


@app.get("/demand")
def get_demand(service_id: Optional[int] = None):
    q = supabase.table("demand_data").select("*")
    if service_id:
        q = q.eq("service_id", service_id)
    rows = q.execute().data or []

    merged = {}
    for r in rows:
        key = r["area_name"]
        m = merged.setdefault(key, {"area_name": key, "latitude": r.get("latitude"),
                                    "longitude": r.get("longitude"),
                                    "total_requests": 0, "completed_requests": 0})
        m["total_requests"] += r.get("total_requests") or 0
        m["completed_requests"] += r.get("completed_requests") or 0
    return {"success": True, "demand": list(merged.values())}


@app.get("/business-insights")
def business_insights():
    rows = supabase.table("business_insights").select("*") \
        .order("unmet_requests", desc=True).limit(20).execute().data or []
    cats = {c["id"]: c["name"] for c in
            (supabase.table("service_categories").select("id, name").execute().data or [])}
    return {"success": True,
            "insights": [{**r, "service": cats.get(r.get("service_id"))} for r in rows]}


@app.post("/agent/expansion")
def expansion_agent():
    """Rule-based demand agent. Swap the body for an LLM call when you're ready."""
    demand = get_demand()["demand"]
    insights: List[str] = []
    for area in sorted(demand, key=lambda d: d["total_requests"] - d["completed_requests"], reverse=True)[:4]:
        gap = area["total_requests"] - area["completed_requests"]
        total = area["total_requests"]
        if total and gap / total > 0.2:
            pct = gap / total
            insights.append(
                f'{area["area_name"]}: {gap} of {total} requests went unserved '
                f'({pct:.0%}). Add providers here first.')
        else:
            insights.append(f'{area["area_name"]}: supply is keeping up with {area["total_requests"]} requests.')
    return {"success": True, "insights": insights}


@app.get("/admin/stats")
def admin_stats():
    def count(table, **filters):
        q = supabase.table(table).select("id", count="exact")
        for k, v in filters.items():
            q = q.eq(k, v)
        return q.execute().count or 0

    payments = supabase.table("payments").select("amount") \
        .eq("payment_status", "paid").execute().data or []

    return {"success": True, "stats": {
        "customers": count("profiles", role="customer"),
        "providers": count("service_providers"),
        "bookings_today": count("bookings", booking_date=str(date.today())),
        "revenue_month": float(sum(p["amount"] for p in payments)),
        "verified_providers": count("service_providers", verification_status="verified"),
        "open_complaints": count("complaints", status="open"),
    }}


@app.post("/assistant")
def assistant(payload: AssistantIn):
    """
    Keyword router today; drop in an LLM (with the service list as context)
    to handle Hinglish and free-form descriptions properly.
    """
    text = payload.message.lower()
    rules = {
        "AC Repair": ["ac", "cooling", "एसी", "air conditioner"],
        "Plumber": ["tap", "leak", "pipe", "water", "नल", "पानी"],
        "Electrician": ["light", "wiring", "switch", "current", "बिजली", "fan"],
        "Mechanic": ["bike", "car", "scooter", "गाड़ी", "engine"],
        "Carpenter": ["door", "furniture", "wood", "लकड़ी"],
        "Cleaning": ["clean", "सफाई", "tank", "sofa"],
        "Painter": ["paint", "पेंट", "wall"],
        "Appliance Repair": ["fridge", "washing", "tv", "microwave"],
    }
    matched = next((svc for svc, words in rules.items() if any(w in text for w in words)), None)

    if matched:
        providers = supabase.table("service_categories").select("id").eq("name", matched).execute().data
        sid = providers[0]["id"] if providers else None
        available = get_providers(service_id=sid, verified_only=True)["providers"] if sid else []
        reply = (f"That sounds like a {matched} job. "
                 f"{len(available)} verified providers cover your area — shall I book the earliest slot?")
    else:
        reply = ("Tell me a little more — what stopped working, and since when? "
                 "I'll pick the right category and find someone verified nearby.")
    return {"success": True, "reply": reply, "service": matched}