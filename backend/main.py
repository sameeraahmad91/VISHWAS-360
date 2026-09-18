"""VISHVAS 360 backend API.

The API is intentionally thin: Supabase remains the source of truth while this
module owns validation, matching, notifications, and AI fallbacks.
"""
from datetime import date, datetime, timezone
from math import asin, cos, radians, sin, sqrt
from typing import Any, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

try:
    from .supabase_client import supabase
except ImportError:
    from supabase_client import supabase

try:
    from AI.AI_Chatbot.intent_detector import detect_intent
except ImportError:
    from AI.AI_Chatbot.intent_detector import detect_intent

app = FastAPI(title="VISHVAS 360 API", description="Trusted local service marketplace", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

ALLOWED_STATUSES = {"pending", "accepted", "rejected", "on_the_way", "in_progress", "completed", "cancelled"}
NEXT_STATUSES = {
    "pending": {"accepted", "rejected", "cancelled"},
    "accepted": {"on_the_way", "cancelled"},
    "on_the_way": {"in_progress", "cancelled"},
    "in_progress": {"completed", "cancelled"},
}

class BookingIn(BaseModel):
    customer_id: str
    service_id: int
    provider_id: Optional[int] = None
    booking_date: date
    booking_time: str
    address: str = Field(min_length=3)
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)
    description: Optional[str] = None
    is_emergency: bool = False
    estimated_price: Optional[float] = Field(default=None, ge=0)

    @field_validator("booking_date")
    @classmethod
    def not_in_past(cls, value: date) -> date:
        if value < date.today():
            raise ValueError("booking_date cannot be in the past")
        return value

class StatusIn(BaseModel):
    status: str

class AssistantIn(BaseModel):
    message: str = Field(min_length=2, max_length=2000)
    user_id: Optional[str] = None
    history: list[dict[str, str]] = Field(default_factory=list)

class ReviewIn(BaseModel):
    booking_id: int
    customer_id: str
    provider_id: Optional[int] = None
    rating: int = Field(ge=1, le=5)
    review_text: Optional[str] = None

class PaymentIn(BaseModel):
    booking_id: int
    customer_id: str
    amount: float = Field(gt=0)
    payment_method: str = "upi"

class ComplaintIn(BaseModel):
    booking_id: Optional[int] = None
    customer_id: str
    provider_id: Optional[int] = None
    subject: str = Field(min_length=3)
    description: str = Field(min_length=5)

def db(table: str):
    return supabase.table(table)

def notify(user_id: str, title: str, message: str, kind: str = "booking") -> None:
    db("notifications").insert({"user_id": user_id, "title": title, "message": message,
                                  "notification_type": kind, "is_read": False}).execute()

def distance_km(a_lat: float | None, a_lon: float | None, b_lat: float | None, b_lon: float | None) -> float:
    if None in (a_lat, a_lon, b_lat, b_lon):
        return float("inf")
    p1, p2 = radians(a_lat), radians(b_lat)
    dphi, dlambda = radians(b_lat - a_lat), radians(b_lon - a_lon)
    h = sin(dphi / 2) ** 2 + cos(p1) * cos(p2) * sin(dlambda / 2) ** 2
    return 6371 * 2 * asin(sqrt(h))

def trust_score(provider_id: int) -> int:
    provider = db("service_providers").select("verification_status,experience_years").eq("id", provider_id).single().execute().data or {}
    reviews = db("reviews").select("rating").eq("provider_id", provider_id).execute().data or []
    completed = db("bookings").select("id", count="exact").eq("provider_id", provider_id).eq("status", "completed").execute().count or 0
    complaints = db("complaints").select("id", count="exact").eq("provider_id", provider_id).execute().count or 0
    verified = 25 if provider.get("verification_status") == "approved" else 8
    rating = (sum(r["rating"] for r in reviews) / len(reviews) / 5 * 30) if reviews else 18
    jobs = min(completed / 50, 1) * 20
    experience = min((provider.get("experience_years") or 0) / 10, 1) * 10
    conduct = max(0, 15 - complaints * 3)
    return round(min(100, verified + rating + jobs + experience + conduct))

def enrich_provider(provider: dict[str, Any]) -> dict[str, Any]:
    reviews = db("reviews").select("rating").eq("provider_id", provider["id"]).execute().data or []
    profile = db("profiles").select("full_name,phone").eq("id", provider["profile_id"]).single().execute().data or {}
    services = db("provider_services").select("service_id,price").eq("provider_id", provider["id"]).execute().data or []
    return {**provider, **profile, "rating": round(sum(r["rating"] for r in reviews) / len(reviews), 1) if reviews else None,
            "review_count": len(reviews), "trust_score": trust_score(provider["id"]), "services": services}

@app.get("/")
def home():
    return {"name": "VISHVAS 360", "status": "running", "version": app.version, "utc": datetime.now(timezone.utc)}

@app.get("/health")
def health():
    try:
        db("service_categories").select("id").limit(1).execute()
        return {"status": "healthy", "database": "connected"}
    except Exception as exc:
        return {"status": "degraded", "database": "unavailable", "detail": str(exc)}

@app.get("/services")
def get_services():
    return {"success": True, "services": db("service_categories").select("*").order("name").execute().data or []}

@app.get("/providers")
def get_providers(service_id: int | None = None, verified_only: bool = True,
                  latitude: float | None = Query(default=None, ge=-90, le=90),
                  longitude: float | None = Query(default=None, ge=-180, le=180),
                  radius_km: float = Query(default=50, gt=0, le=500)):
    query = db("service_providers").select("*")
    if verified_only:
        query = query.eq("verification_status", "approved")
    providers = query.execute().data or []
    if service_id:
        ids = {x["provider_id"] for x in (db("provider_services").select("provider_id").eq("service_id", service_id).execute().data or [])}
        providers = [p for p in providers if p["id"] in ids]
    result = []
    for provider in providers:
        item = enrich_provider(provider)
        item["distance_km"] = distance_km(latitude, longitude, provider.get("latitude"), provider.get("longitude"))
        if item["distance_km"] <= radius_km or latitude is None:
            result.append(item)
    return {"success": True, "providers": sorted(result, key=lambda p: (p["distance_km"], -p["trust_score"]))}

@app.get("/providers/{provider_id}")
def get_provider(provider_id: int):
    row = db("service_providers").select("*").eq("id", provider_id).single().execute().data
    if not row:
        raise HTTPException(404, "Provider not found")
    return {"success": True, "provider": enrich_provider(row)}

@app.get("/bookings")
def list_bookings(customer_id: str | None = None, provider_id: int | None = None):
    query = db("bookings").select("*").order("created_at", desc=True)
    if customer_id: query = query.eq("customer_id", customer_id)
    if provider_id: query = query.eq("provider_id", provider_id)
    return {"success": True, "bookings": query.execute().data or []}

@app.post("/bookings")
def create_booking(payload: BookingIn):
    data = payload.model_dump(mode="json")
    if not data["provider_id"]:
        candidates = get_providers(service_id=payload.service_id, verified_only=True)["providers"]
        if candidates: data["provider_id"] = candidates[0]["id"]
    result = db("bookings").insert(data).execute()
    booking = result.data[0] if result.data else data
    notify(payload.customer_id, "Booking placed", f"Request #{booking.get('id')} has been placed.")
    if booking.get("provider_id"):
        provider = db("service_providers").select("profile_id").eq("id", booking["provider_id"]).single().execute().data
        if provider: notify(provider["profile_id"], "New booking request", f"A customer requested service (#{booking.get('id')}).", "new_booking")
    return {"success": True, "booking": booking}

@app.patch("/bookings/{booking_id}/status")
def update_status(booking_id: int, payload: StatusIn):
    if payload.status not in ALLOWED_STATUSES: raise HTTPException(400, "Invalid booking status")
    current = db("bookings").select("*").eq("id", booking_id).single().execute().data
    if not current: raise HTTPException(404, "Booking not found")
    if payload.status not in NEXT_STATUSES.get(current["status"], set()): raise HTTPException(409, "Invalid status transition")
    result = db("bookings").update({"status": payload.status}).eq("id", booking_id).execute()
    notify(current["customer_id"], f"Booking {payload.status.replace('_', ' ')}", f"Booking #{booking_id} is now {payload.status.replace('_', ' ')}.", "status_update")
    return {"success": True, "booking": result.data[0] if result.data else {**current, "status": payload.status}}

@app.get("/notifications/{user_id}")
def get_notifications(user_id: str):
    rows = db("notifications").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(50).execute().data or []
    return {"success": True, "notifications": rows}

@app.patch("/notifications/{notification_id}/read")
def mark_read(notification_id: int):
    db("notifications").update({"is_read": True}).eq("id", notification_id).execute()
    return {"success": True}

@app.post("/payments")
def create_payment(payload: PaymentIn):
    if payload.payment_method not in {"upi", "card", "netbanking", "wallet", "cash"}: raise HTTPException(400, "Unsupported payment method")
    data = payload.model_dump() | {"payment_status": "success", "paid_at": datetime.now(timezone.utc).isoformat(), "transaction_id": f"TXN-{int(datetime.now().timestamp())}"}
    result = db("payments").insert(data).execute()
    notify(payload.customer_id, "Payment received", f"₹{payload.amount:.0f} paid for booking #{payload.booking_id}.", "payment")
    return {"success": True, "payment": result.data[0] if result.data else data}

@app.post("/reviews")
def create_review(payload: ReviewIn):
    booking = db("bookings").select("customer_id,provider_id,status").eq("id", payload.booking_id).single().execute().data
    if not booking or booking["status"] != "completed": raise HTTPException(400, "Reviews are allowed only for completed bookings")
    if booking["customer_id"] != payload.customer_id: raise HTTPException(403, "Booking does not belong to customer")
    data = payload.model_dump(); data["provider_id"] = booking["provider_id"]
    result = db("reviews").insert(data).execute()
    return {"success": True, "review": result.data[0] if result.data else data}

@app.post("/complaints")
def create_complaint(payload: ComplaintIn):
    result = db("complaints").insert(payload.model_dump()).execute()
    return {"success": True, "complaint": result.data[0] if result.data else payload.model_dump()}

@app.post("/assistant")
def assistant(payload: AssistantIn):
    result = detect_intent(payload.message, payload.history)
    service = result.get("service_category")
    providers = []
    if service:
        categories = db("service_categories").select("id").eq("name", service).execute().data or []
        if categories: providers = get_providers(service_id=categories[0]["id"])["providers"]
    result["provider_count"] = len(providers)
    return {"success": True, **result}

@app.get("/admin/stats")
def admin_stats():
    def count(table: str): return db(table).select("id", count="exact").execute().count or 0
    payments = db("payments").select("amount").eq("payment_status", "success").execute().data or []
    return {"success": True, "stats": {"customers": count("profiles"), "providers": count("service_providers"), "bookings": count("bookings"), "revenue": sum(float(p["amount"]) for p in payments), "open_complaints": db("complaints").select("id", count="exact").eq("status", "open").execute().count or 0}}
