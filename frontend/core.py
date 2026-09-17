"""
VISHVAS 360 — shared core: data store, i18n, AI engine, trust scoring, payments,
notifications and reusable UI helpers.
"""
from __future__ import annotations

import json
import math
import os
import random
import uuid
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)

SERVICES = [
    ("Electrician", "⚡"), ("Plumber", "🚰"), ("AC Repair", "❄️"),
    ("Carpenter", "🪚"), ("Painter", "🎨"), ("Appliance Repair", "🔌"),
    ("Cleaning", "🧹"), ("Mechanic", "🔧"),
]
SERVICE_NAMES = [s for s, _ in SERVICES]
SERVICE_ICON = dict(SERVICES)

CITY_ZONES = {
    "Indore": [("Vijay Nagar", 22.7533, 75.8937), ("Palasia", 22.7244, 75.8839),
               ("Bhawarkua", 22.6890, 75.8680), ("Rau", 22.6470, 75.8080),
               ("Sudama Nagar", 22.6940, 75.8300)],
    "Bhopal": [("MP Nagar", 23.2330, 77.4340), ("Kolar", 23.1600, 77.4300),
               ("Arera Colony", 23.2100, 77.4300), ("Bairagarh", 23.2700, 77.3400)],
    "Pune": [("Kothrud", 18.5074, 73.8077), ("Hinjewadi", 18.5913, 73.7389),
             ("Viman Nagar", 18.5679, 73.9143), ("Hadapsar", 18.5089, 73.9260)],
}

LANGS = {
    "English": {
        "book": "Book a Service", "emergency": "Emergency Mode", "assistant": "AI Assistant",
        "my_bookings": "My Bookings", "pay": "Pay Now", "welcome": "Welcome back",
        "describe": "Describe your problem", "confirm": "Confirm Booking",
    },
    "हिन्दी": {
        "book": "सेवा बुक करें", "emergency": "आपातकालीन मोड", "assistant": "एआई सहायक",
        "my_bookings": "मेरी बुकिंग", "pay": "अभी भुगतान करें", "welcome": "पुनः स्वागत है",
        "describe": "अपनी समस्या बताएं", "confirm": "बुकिंग पक्की करें",
    },
    "मराठी": {
        "book": "सेवा बुक करा", "emergency": "आणीबाणी मोड", "assistant": "एआय सहाय्यक",
        "my_bookings": "माझ्या बुकिंग", "pay": "आता पैसे भरा", "welcome": "पुन्हा स्वागत",
        "describe": "तुमची समस्या सांगा", "confirm": "बुकिंग निश्चित करा",
    },
    "ગુજરાતી": {
        "book": "સેવા બુક કરો", "emergency": "કટોકટી મોડ", "assistant": "AI સહાયક",
        "my_bookings": "મારી બુકિંગ", "pay": "હમણાં ચૂકવો", "welcome": "ફરી સ્વાગત",
        "describe": "તમારી સમસ્યા જણાવો", "confirm": "બુકિંગ કન્ફર્મ કરો",
    },
    "தமிழ்": {
        "book": "சேவையை பதிவு செய்", "emergency": "அவசர பயன்முறை", "assistant": "AI உதவியாளர்",
        "my_bookings": "என் பதிவுகள்", "pay": "இப்போது செலுத்து", "welcome": "மீண்டும் வருக",
        "describe": "உங்கள் பிரச்சனையை கூறுங்கள்", "confirm": "பதிவை உறுதிசெய்",
    },
}


def t(key: str) -> str:
    lang = st.session_state.get("language", "English")
    return LANGS.get(lang, LANGS["English"]).get(key, LANGS["English"].get(key, key))


# ----------------------------------------------------------------------------
# Persistence
# ----------------------------------------------------------------------------
def _path(name: str) -> str:
    return os.path.join(DATA_DIR, f"{name}.json")


def load(name: str, default):
    try:
        with open(_path(name), "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return default


def save(name: str, payload) -> None:
    with open(_path(name), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False, default=str)


def new_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:6].upper()}"


# ----------------------------------------------------------------------------
# Seed data
# ----------------------------------------------------------------------------
FIRST = ["Ramesh", "Sunita", "Imran", "Ajay", "Priya", "Vikas", "Farhan", "Meena",
         "Rakesh", "Deepak", "Anita", "Sourav", "Kiran", "Nilesh", "Pooja", "Arjun"]
LAST = ["Sharma", "Verma", "Khan", "Patil", "Yadav", "Joshi", "Nair", "Chouhan",
        "Gupta", "Solanki", "Rathore", "Mishra"]


def seed_providers(n: int = 26):
    random.seed(11)
    rows = []
    for i in range(n):
        city = random.choice(list(CITY_ZONES))
        zone, lat, lon = random.choice(CITY_ZONES[city])
        jobs = random.randint(12, 480)
        rating = round(random.uniform(3.4, 5.0), 2)
        rows.append({
            "id": f"SP-{1000 + i}",
            "name": f"{random.choice(FIRST)} {random.choice(LAST)}",
            "service": random.choice(SERVICE_NAMES),
            "city": city, "zone": zone,
            "lat": lat + random.uniform(-0.02, 0.02),
            "lon": lon + random.uniform(-0.02, 0.02),
            "rating": rating,
            "jobs_done": jobs,
            "completion_rate": round(random.uniform(0.78, 0.99), 3),
            "on_time_rate": round(random.uniform(0.70, 0.99), 3),
            "dispute_rate": round(random.uniform(0.0, 0.09), 3),
            "years": random.randint(1, 18),
            "base_price": random.choice([249, 299, 349, 399, 499, 599]),
            "kyc_verified": random.random() > 0.15,
            "photo_verified": random.random() > 0.25,
            "police_verified": random.random() > 0.35,
            "emergency_available": random.random() > 0.5,
            "status": "Active",
            "languages": random.sample(list(LANGS), k=random.randint(1, 3)),
            "joined": (datetime.now() - timedelta(days=random.randint(30, 900))).strftime("%Y-%m-%d"),
        })
    return rows


def seed_bookings(providers, n: int = 60):
    random.seed(5)
    rows = []
    for i in range(n):
        p = random.choice(providers)
        created = datetime.now() - timedelta(days=random.randint(0, 45), hours=random.randint(0, 20))
        status = random.choices(["Completed", "In Progress", "Requested", "Cancelled"],
                                weights=[0.62, 0.14, 0.16, 0.08])[0]
        amount = p["base_price"] + random.choice([0, 100, 200, 350, 500])
        rows.append({
            "id": f"BK-{7000 + i}",
            "customer": f"{random.choice(FIRST)} {random.choice(LAST)}",
            "service": p["service"], "provider_id": p["id"], "provider": p["name"],
            "city": p["city"], "zone": p["zone"], "lat": p["lat"], "lon": p["lon"],
            "status": status,
            "emergency": random.random() > 0.85,
            "amount": amount,
            "paid": status == "Completed",
            "payment_mode": random.choice(["UPI", "Card", "Wallet", "Cash"]),
            "rating": round(random.uniform(3.0, 5.0), 1) if status == "Completed" else None,
            "created_at": created.strftime("%Y-%m-%d %H:%M"),
            "scheduled_at": (created + timedelta(hours=random.randint(2, 72))).strftime("%Y-%m-%d %H:%M"),
            "photo_before": random.random() > 0.4,
            "photo_after": status == "Completed" and random.random() > 0.3,
        })
    return rows


def bootstrap():
    """Load every dataset into session state exactly once."""
    if st.session_state.get("_booted"):
        return
    providers = load("providers", None) or seed_providers()
    bookings = load("bookings", None) or seed_bookings(providers)
    st.session_state.providers = providers
    st.session_state.bookings = bookings
    st.session_state.notifications = load("notifications", None) or []
    st.session_state.reminders = load("reminders", None) or []
    st.session_state.chat = []
    st.session_state.setdefault("language", "English")
    st.session_state.setdefault("emergency", False)
    st.session_state._booted = True
    persist()


def persist():
    save("providers", st.session_state.providers)
    save("bookings", st.session_state.bookings)
    save("notifications", st.session_state.notifications)
    save("reminders", st.session_state.reminders)


# ----------------------------------------------------------------------------
# Trust & reputation score
# ----------------------------------------------------------------------------
def trust_score(p: dict) -> int:
    """0-100 weighted trust score: quality, reliability, verification, tenure."""
    rating = (p["rating"] / 5) * 30
    completion = p["completion_rate"] * 20
    on_time = p["on_time_rate"] * 15
    disputes = (1 - min(p["dispute_rate"] / 0.1, 1)) * 10
    volume = min(p["jobs_done"] / 300, 1) * 10
    verify = (4 * p["kyc_verified"] + 4 * p["photo_verified"] + 4 * p["police_verified"])
    tenure = min(p["years"] / 10, 1) * 3
    return int(round(rating + completion + on_time + disputes + volume + verify + tenure))


def trust_badge(score: int) -> tuple[str, str]:
    if score >= 85:
        return "Platinum Trusted", "#16a34a"
    if score >= 72:
        return "Gold Trusted", "#ca8a04"
    if score >= 58:
        return "Silver Verified", "#64748b"
    return "Needs Review", "#dc2626"


def trust_breakdown(p: dict) -> pd.DataFrame:
    return pd.DataFrame({
        "Factor": ["Customer rating", "Completion rate", "On-time arrival",
                   "Low disputes", "Job volume", "Verification", "Tenure"],
        "Points": [round((p["rating"] / 5) * 30, 1), round(p["completion_rate"] * 20, 1),
                   round(p["on_time_rate"] * 15, 1),
                   round((1 - min(p["dispute_rate"] / 0.1, 1)) * 10, 1),
                   round(min(p["jobs_done"] / 300, 1) * 10, 1),
                   4 * p["kyc_verified"] + 4 * p["photo_verified"] + 4 * p["police_verified"],
                   round(min(p["years"] / 10, 1) * 3, 1)],
        "Max": [30, 20, 15, 10, 10, 12, 3],
    })


# ----------------------------------------------------------------------------
# AI engine (rule + scoring based; swap in an LLM by editing ai_reply)
# ----------------------------------------------------------------------------
INTENT_KEYWORDS = {
    "Electrician": ["light", "fan", "switch", "wiring", "current", "short circuit", "mcb", "बिजली", "पंखा"],
    "Plumber": ["tap", "leak", "pipe", "water", "drain", "toilet", "नल", "पानी", "लीक"],
    "AC Repair": ["ac", "air condition", "cooling", "gas refill", "एसी", "कूलिंग"],
    "Carpenter": ["door", "wood", "furniture", "hinge", "cupboard", "दरवाजा", "लकड़ी"],
    "Painter": ["paint", "wall", "putty", "whitewash", "पेंट", "दीवार"],
    "Appliance Repair": ["fridge", "washing machine", "microwave", "geyser", "tv", "फ्रिज"],
    "Cleaning": ["clean", "sofa", "deep clean", "bathroom", "सफाई"],
    "Mechanic": ["bike", "car", "engine", "puncture", "battery", "गाड़ी", "बाइक"],
}
URGENT_WORDS = ["urgent", "emergency", "immediately", "sparking", "flood", "smoke",
                "gas leak", "तुरंत", "आपात"]


def detect_service(text: str) -> tuple[str, float]:
    text_l = (text or "").lower()
    best, hits = SERVICE_NAMES[0], 0
    for service, words in INTENT_KEYWORDS.items():
        score = sum(1 for w in words if w in text_l)
        if score > hits:
            best, hits = service, score
    confidence = min(0.55 + 0.15 * hits, 0.98) if hits else 0.45
    return best, confidence


def is_urgent(text: str) -> bool:
    text_l = (text or "").lower()
    return any(w in text_l for w in URGENT_WORDS)


def haversine(lat1, lon1, lat2, lon2) -> float:
    r = 6371
    dlat, dlon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def match_providers(service: str, city: str, lat: float, lon: float,
                    emergency: bool = False, language: str | None = None, top: int = 5):
    """Intelligent matching: trust + proximity + price + emergency readiness."""
    out = []
    for p in st.session_state.providers:
        if p["service"] != service or p["status"] != "Active":
            continue
        if emergency and not p["emergency_available"]:
            continue
        dist = haversine(lat, lon, p["lat"], p["lon"])
        ts = trust_score(p)
        score = ts * 0.55 + max(0, 30 - dist * 2) * 1.2 + max(0, 600 - p["base_price"]) / 20
        if language and language in p["languages"]:
            score += 6
        if emergency and p["emergency_available"]:
            score += 10
        if p["city"] != city:
            score -= 25
        out.append({**p, "trust": ts, "distance_km": round(dist, 1),
                    "match_score": round(score, 1),
                    "eta_min": int(12 + dist * 4) if not emergency else int(8 + dist * 3)})
    return sorted(out, key=lambda r: r["match_score"], reverse=True)[:top]


def ai_reply(message: str, city: str, lat: float, lon: float) -> dict:
    """Returns an assistant turn: text + optional matched provider suggestions."""
    service, conf = detect_service(message)
    urgent = is_urgent(message)
    matches = match_providers(service, city, lat, lon, emergency=urgent,
                              language=st.session_state.get("language"))
    if urgent:
        head = (f"🚨 This sounds like an **emergency**. I have switched to Emergency Mode and "
                f"shortlisted **{service}** professionals who can reach you fastest.")
    else:
        head = (f"I understand you need a **{service}** ({int(conf * 100)}% confidence). "
                f"Here are the best-matched verified professionals near {city}.")
    if not matches:
        head += "\n\nNo provider is free in this zone right now — I can place you on priority standby."
    return {"role": "assistant", "text": head, "service": service, "urgent": urgent,
            "matches": matches}


# ----------------------------------------------------------------------------
# Demand heatmap agent + expansion recommendations
# ----------------------------------------------------------------------------
def demand_frame() -> pd.DataFrame:
    df = pd.DataFrame(st.session_state.bookings)
    if df.empty:
        return df
    grp = df.groupby(["city", "zone", "service"]).agg(
        demand=("id", "count"), revenue=("amount", "sum"),
        lat=("lat", "mean"), lon=("lon", "mean")).reset_index()
    supply = pd.DataFrame(st.session_state.providers).groupby(
        ["city", "zone", "service"]).size().reset_index(name="supply")
    merged = grp.merge(supply, on=["city", "zone", "service"], how="left").fillna({"supply": 0})
    merged["gap"] = merged["demand"] - merged["supply"] * 3
    merged["heat"] = (merged["demand"] / max(merged["demand"].max(), 1) * 100).round(1)
    return merged


def expansion_recommendations(provider: dict, limit: int = 5) -> pd.DataFrame:
    df = demand_frame()
    if df.empty:
        return df
    same = df[df["service"] == provider["service"]].copy()
    same["opportunity"] = same["gap"] * 6 + same["revenue"] / 400
    same["your_zone"] = same["zone"] == provider["zone"]
    same = same.sort_values("opportunity", ascending=False).head(limit)
    same["recommendation"] = same.apply(
        lambda r: (f"Expand into {r['zone']}, {r['city']} — {int(r['demand'])} requests vs "
                   f"{int(r['supply'])} providers. Potential monthly uplift ₹"
                   f"{int(max(r['gap'], 1) * provider['base_price'] * 1.4):,}."), axis=1)
    return same


def cross_sell(provider: dict) -> list[str]:
    pairs = {
        "Electrician": ["AC Repair", "Appliance Repair"], "Plumber": ["Cleaning", "Carpenter"],
        "AC Repair": ["Electrician", "Appliance Repair"], "Carpenter": ["Painter", "Cleaning"],
        "Painter": ["Cleaning", "Carpenter"], "Appliance Repair": ["Electrician", "AC Repair"],
        "Cleaning": ["Painter", "Plumber"], "Mechanic": ["Appliance Repair", "Electrician"],
    }
    tips = [f"Add **{s}** to your skill set — customers who book {provider['service']} "
            f"request it within 30 days." for s in pairs.get(provider["service"], [])]
    if provider["rating"] < 4.5:
        tips.append("Close the rating gap: ask every customer for a review right after job completion.")
    if not provider["police_verified"]:
        tips.append("Complete police verification to unlock +4 trust points and premium bookings.")
    if not provider["emergency_available"]:
        tips.append("Enable Emergency Mode — emergency jobs bill at 1.6× the standard rate.")
    return tips


# ----------------------------------------------------------------------------
# Payments, reminders, notifications
# ----------------------------------------------------------------------------
def process_payment(amount: float, mode: str, emergency: bool = False) -> dict:
    surge = 1.6 if emergency else 1.0
    gross = round(amount * surge, 2)
    fee = round(gross * 0.02, 2)
    return {"txn_id": new_id("TXN"), "gross": gross, "platform_fee": fee,
            "provider_payout": round(gross - fee, 2), "mode": mode,
            "status": "Success", "at": datetime.now().strftime("%Y-%m-%d %H:%M")}


def notify(audience: str, title: str, body: str, kind: str = "info"):
    st.session_state.notifications.insert(0, {
        "id": new_id("NT"), "audience": audience, "title": title, "body": body,
        "kind": kind, "at": datetime.now().strftime("%Y-%m-%d %H:%M"), "read": False})
    persist()


def add_reminder(booking_id: str, when: str, channel: str, text: str):
    st.session_state.reminders.insert(0, {
        "id": new_id("RM"), "booking_id": booking_id, "when": when,
        "channel": channel, "text": text, "status": "Scheduled"})
    persist()


# ----------------------------------------------------------------------------
# UI helpers
# ----------------------------------------------------------------------------
THEME_CSS = """
<style>
:root{--v-navy:#0b1f3a;--v-blue:#1d4ed8;--v-cyan:#06b6d4;--v-amber:#f59e0b;--v-ink:#0f172a;}
.stApp{background:linear-gradient(180deg,#f6f9ff 0%,#eef2fb 100%);}
#MainMenu,footer{visibility:hidden;}
.v-hero{background:linear-gradient(120deg,var(--v-navy) 0%,#123a6b 45%,var(--v-blue) 100%);
 border-radius:22px;padding:38px 42px;color:#fff;box-shadow:0 22px 48px -22px rgba(11,31,58,.75);}
.v-hero h1{font-size:2.6rem;margin:0;letter-spacing:-.02em;font-weight:800;}
.v-hero p{opacity:.88;margin:.5rem 0 0;font-size:1.03rem;max-width:760px;}
.v-pill{display:inline-block;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.25);
 padding:5px 13px;border-radius:999px;font-size:.78rem;margin:4px 6px 0 0;}
.v-card{background:#fff;border:1px solid #e4e9f2;border-radius:18px;padding:22px 24px;
 box-shadow:0 12px 30px -24px rgba(15,23,42,.65);min-height:470px;}
.v-card h3{margin:.2rem 0 .4rem;color:var(--v-ink);font-weight:750;}
.v-card ul{margin:.4rem 0 0 1rem;padding:0;color:#475569;font-size:.9rem;line-height:1.65;}
.v-icon{font-size:2.1rem;}
.v-tag{display:inline-block;padding:3px 10px;border-radius:999px;font-size:.72rem;font-weight:600;}
.v-kpi{background:#fff;border:1px solid #e4e9f2;border-radius:16px;padding:16px 18px;}
.v-kpi .l{color:#64748b;font-size:.78rem;text-transform:uppercase;letter-spacing:.06em;}
.v-kpi .v{font-size:1.6rem;font-weight:750;color:var(--v-ink);}
.v-prov{background:#fff;border:1px solid #e4e9f2;border-left:5px solid var(--v-blue);
 border-radius:14px;padding:14px 18px;margin-bottom:10px;}
.v-emg{background:#fee2e2;border-left:5px solid #dc2626;padding:12px 16px;border-radius:12px;color:#7f1d1d;font-weight:600;}
.stButton>button{border-radius:10px;font-weight:600;}
</style>
"""


def inject_theme():
    st.markdown(THEME_CSS, unsafe_allow_html=True)


def kpi(col, label, value, sub=""):
    col.markdown(
        f"<div class='v-kpi'><div class='l'>{label}</div><div class='v'>{value}</div>"
        f"<div style='color:#64748b;font-size:.78rem'>{sub}</div></div>", unsafe_allow_html=True)


def provider_card(p: dict, show_match: bool = True):
    badge, color = trust_badge(p.get("trust", trust_score(p)))
    verifs = " ".join(filter(None, [
        "✅ KYC" if p["kyc_verified"] else "⚠️ KYC pending",
        "📸 Photo verified" if p["photo_verified"] else "",
        "🛡️ Police verified" if p["police_verified"] else "",
    ]))
    extra = (f"<span style='color:#475569'>📍 {p.get('distance_km','–')} km · ⏱ ETA "
             f"{p.get('eta_min','–')} min · match {p.get('match_score','–')}</span>") if show_match else ""
    st.markdown(
        f"""<div class='v-prov'>
        <b style='font-size:1.05rem'>{SERVICE_ICON.get(p['service'],'🛠')} {p['name']}</b>
        <span class='v-tag' style='background:{color}1a;color:{color};margin-left:8px'>{badge} · {p.get('trust', trust_score(p))}</span>
        <div style='color:#475569;font-size:.9rem;margin-top:4px'>{p['service']} · {p['zone']}, {p['city']}
        · ⭐ {p['rating']} ({p['jobs_done']} jobs) · from ₹{p['base_price']}</div>
        <div style='font-size:.82rem;color:#64748b;margin-top:4px'>{verifs}</div>
        <div style='font-size:.82rem;margin-top:4px'>{extra}</div></div>""",
        unsafe_allow_html=True)


def sidebar_common(role: str):
    with st.sidebar:
        st.markdown("### 🛡️ VISHVAS 360")
        st.caption(f"Signed in as **{role}**")
        st.selectbox("🌐 Language / भाषा", list(LANGS), key="language")
        if st.button("🏠 Back to home", use_container_width=True):
            st.session_state.role = None
            st.rerun()
        st.divider()
        unread = [n for n in st.session_state.notifications
                  if n["audience"] in (role, "All")][:6]
        st.markdown(f"#### 🔔 Real-time notifications ({len(unread)})")
        if not unread:
            st.caption("No notifications yet.")
        for n in unread:
            st.info(f"**{n['title']}**\n\n{n['body']}\n\n`{n['at']}`")
