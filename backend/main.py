"""VISHVAS 360 production API: bookings, matching, trust, payments, AI and analytics."""
from __future__ import annotations
from datetime import date, datetime, timezone
from typing import Optional, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from .supabase_client import require_supabase
from .ml_models import classify

app = FastAPI(title="VISHVAS 360 API", version="2.0.0", description="Trusted local services marketplace")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class BookingIn(BaseModel):
    customer_id: str; service_id: int; provider_id: Optional[int] = None
    booking_date: date; booking_time: str; address: str = Field(min_length=3)
    latitude: Optional[float] = None; longitude: Optional[float] = None
    description: Optional[str] = None; is_emergency: bool = False
    estimated_price: Optional[float] = Field(default=None, ge=0)
class StatusIn(BaseModel): status: str
class ReviewIn(BaseModel):
    booking_id: int; customer_id: str; provider_id: Optional[int] = None
    rating: int = Field(ge=1, le=5); review_text: Optional[str] = None
class PaymentIn(BaseModel):
    booking_id: int; customer_id: str; amount: float = Field(gt=0)
    payment_method: str = "upi"
class ComplaintIn(BaseModel):
    booking_id: Optional[int] = None; customer_id: Optional[str] = None; provider_id: Optional[int] = None
    subject: str = Field(min_length=2); description: str = Field(min_length=2)
class AssistantIn(BaseModel): message: str = Field(min_length=1); user_id: Optional[str] = None

def db():
    try: return require_supabase()
    except RuntimeError as exc: raise HTTPException(503, str(exc)) from exc

def rows(table: str, columns: str = "*"):
    return db().table(table).select(columns).execute().data or []

def notify(user_id: str, title: str, message: str, kind: str = "booking"):
    db().table("notifications").insert({"user_id": user_id, "title": title, "message": message, "notification_type": kind}).execute()

def trust_score(provider_id: int) -> int:
    client = db(); provider = client.table("service_providers").select("verification_status,created_at").eq("id", provider_id).limit(1).execute().data
    if not provider: return 0
    p = provider[0]; reviews = rows("reviews", "rating")
    reviews = [r for r in reviews if r.get("provider_id") == provider_id]
    completed = len(client.table("bookings").select("id").eq("provider_id", provider_id).eq("status", "completed").execute().data or [])
    complaints = len(client.table("complaints").select("id").eq("provider_id", provider_id).execute().data or [])
    verification = 25 if p.get("verification_status") == "approved" else 8
    rating = (sum(r["rating"] for r in reviews) / len(reviews) / 5 * 30) if reviews else 12
    return max(0, min(100, round(verification + min(completed, 50) / 50 * 20 + 15 - min(complaints * 3, 15) + rating)))

def provider_view(p: dict) -> dict:
    client = db(); profile = client.table("profiles").select("full_name,language").eq("id", p["profile_id"]).limit(1).execute().data
    reviews = [r for r in rows("reviews", "provider_id,rating") if r.get("provider_id") == p["id"]]
    services = client.table("provider_services").select("service_id,price").eq("provider_id", p["id"]).execute().data or []
    return {**p, "full_name": profile[0].get("full_name") if profile else None, "language": profile[0].get("language") if profile else None,
            "services": services, "rating": round(sum(x["rating"] for x in reviews)/len(reviews), 1) if reviews else None,
            "review_count": len(reviews), "trust_score": trust_score(p["id"])}

@app.get("/")
def home(): return {"name": "VISHVAS 360", "status": "running", "version": app.version}
@app.get("/health")
def health(): return {"status": "ok", "database_configured": bool(__import__('backend.supabase_client', fromlist=['supabase']).supabase)}
@app.get("/services")
def services(): return {"success": True, "services": rows("service_categories")}
@app.get("/providers")
def providers(service_id: Optional[int] = None, verified_only: bool = True):
    client = db(); provider_rows = client.table("service_providers").select("*").execute().data or []
    if verified_only: provider_rows = [p for p in provider_rows if p.get("verification_status") == "approved"]
    if service_id:
        ids = {x["provider_id"] for x in client.table("provider_services").select("provider_id").eq("service_id", service_id).execute().data or []}
        provider_rows = [p for p in provider_rows if p["id"] in ids]
    return {"success": True, "providers": sorted([provider_view(p) for p in provider_rows], key=lambda x: x["trust_score"], reverse=True)}
@app.get("/providers/{provider_id}")
def provider(provider_id: int):
    data = db().table("service_providers").select("*").eq("id", provider_id).limit(1).execute().data
    if not data: raise HTTPException(404, "Provider not found")
    return {"success": True, "provider": provider_view(data[0])}
@app.get("/bookings")
def bookings(customer_id: Optional[str] = None, provider_id: Optional[int] = None):
    q = db().table("bookings").select("*").order("created_at", desc=True)
    if customer_id: q = q.eq("customer_id", customer_id)
    if provider_id: q = q.eq("provider_id", provider_id)
    return {"success": True, "bookings": q.execute().data or []}
@app.post("/bookings")
def create_booking(payload: BookingIn):
    data = payload.model_dump(); data["booking_date"] = str(data["booking_date"])
    if not data["provider_id"]:
        matches = providers(payload.service_id, True)["providers"]
        if matches: data["provider_id"] = matches[0]["id"]
    result = db().table("bookings").insert(data).execute(); booking = (result.data or [data])[0]
    notify(payload.customer_id, "Booking placed", f"Request #{booking.get('id')} has been created.")
    return {"success": True, "booking": booking}
@app.patch("/bookings/{booking_id}/status")
def update_booking(booking_id: int, payload: StatusIn):
    allowed = {"pending","accepted","rejected","on_the_way","in_progress","completed","cancelled"}
    if payload.status not in allowed: raise HTTPException(422, "Invalid booking status")
    result = db().table("bookings").update({"status": payload.status}).eq("id", booking_id).execute()
    if not result.data: raise HTTPException(404, "Booking not found")
    notify(result.data[0]["customer_id"], f"Booking {payload.status}", f"Booking #{booking_id} is now {payload.status}.")
    return {"success": True, "booking": result.data[0]}
@app.get("/notifications/{user_id}")
def notifications(user_id: str): return {"success": True, "notifications": db().table("notifications").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(50).execute().data or []}
@app.patch("/notifications/{notification_id}/read")
def read_notification(notification_id: int): db().table("notifications").update({"is_read": True}).eq("id", notification_id).execute(); return {"success": True}
@app.post("/payments")
def payment(payload: PaymentIn):
    if payload.payment_method not in {"upi","card","netbanking","wallet","cash"}: raise HTTPException(422, "Unsupported payment method")
    data = payload.model_dump() | {"payment_status":"success","paid_at":datetime.now(timezone.utc).isoformat(),"transaction_id":f"V360-{int(datetime.now().timestamp())}"}
    result = db().table("payments").insert(data).execute(); notify(payload.customer_id, "Payment received", f"₹{payload.amount:.2f} received.", "payment")
    return {"success": True, "payment": (result.data or [data])[0]}
@app.post("/reviews")
def review(payload: ReviewIn):
    data = payload.model_dump()
    if not data.get("provider_id"):
        booking = db().table("bookings").select("provider_id").eq("id", data["booking_id"]).limit(1).execute().data
        data["provider_id"] = booking[0].get("provider_id") if booking else None
    if not data.get("provider_id"): raise HTTPException(422, "Booking has no provider")
    result = db().table("reviews").insert(data).execute(); return {"success": True, "review": (result.data or [data])[0]}
@app.post("/complaints")
def complaint(payload: ComplaintIn):
    result = db().table("complaints").insert(payload.model_dump()).execute(); return {"success": True, "complaint": (result.data or [payload.model_dump()])[0]}
@app.get("/demand")
def demand(service_id: Optional[int] = None):
    data = rows("demand_data"); data = [x for x in data if service_id is None or x.get("service_id") == service_id]
    return {"success": True, "demand": data}
@app.get("/business-insights")
def insights(): return {"success": True, "insights": rows("business_insights")}
@app.post("/assistant")
def assistant(payload: AssistantIn):
    result = classify(payload.message); service = result["service"]
    reply = f"I identified a {service} request ({result['confidence']:.0%} confidence)."
    if result["urgent"]: reply = f"🚨 Emergency mode enabled. I identified {service} and will prioritise available verified professionals."
    return {"success": True, **result, "reply": reply}
@app.post("/ai/understand")
def understand(payload: dict[str, Any]): return {"success": True, **classify(str(payload.get("text", ""))), "channel": payload.get("channel", "text")}
