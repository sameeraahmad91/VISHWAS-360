# """
# VISHVAS 360 — AI-Powered Trusted Local Service Marketplace
# Home page with three role portals: Customer, Service Provider, Admin.

# Run:  streamlit run app.py
# """
# from __future__ import annotations

# import streamlit as st

# st.set_page_config(page_title="VISHVAS 360 — Trusted Local Services",
#                    page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

# from core import SERVICES, bootstrap, inject_theme, kpi, trust_score  # noqa: E402
# import admin as admin_portal  # noqa: E402
# import customer as customer_portal  # noqa: E402
# import service_provider as provider_portal  # noqa: E402

# bootstrap()
# st.session_state.setdefault("role", None)

# CARDS = [
#     ("Service Provider", "🧑‍🔧", "#1d4ed8",
#      "Grow your business with AI-driven jobs, trust scoring and expansion insights.",
#      ["Live job requests & emergency dispatch", "Trust & reputation score with AI coaching",
#       "Photo + KYC verification", "Service demand heatmap agent",
#       "Business expansion recommendations", "Earnings & instant payouts"]),
#     ("Customer", "👤", "#06b6d4",
#      "Book verified local professionals by chat or voice — in your own language.",
#      ["AI chatbot booking assistant", "Voice-based booking", "Multilingual interface",
#       "🚨 Emergency service mode", "Secure payment gateway",
#       "Reminders & real-time notifications"]),
#     ("Admin", "🛡️", "#f59e0b",
#      "Full marketplace control tower with analytics, moderation and payouts.",
#      ["Live marketplace KPIs", "Provider verification queue", "Demand intelligence & supply gaps",
#       "Booking and dispute oversight", "Revenue & payout ledger", "Broadcast notifications"]),
# ]


# def home():
#     inject_theme()
#     st.markdown(
#         "<div class='v-hero'><h1>🛡️ VISHVAS&nbsp;360</h1>"
#         "<p>An AI-powered trusted local service marketplace — connecting customers with verified "
#         "professionals through intelligent matching, text &amp; voice booking, multilingual support, "
#         "emergency dispatch, secure payments and real-time notifications.</p>"
#         "<span class='v-pill'>AI Chatbot</span><span class='v-pill'>Voice Booking</span>"
#         "<span class='v-pill'>Multilingual</span><span class='v-pill'>Emergency Mode</span>"
#         "<span class='v-pill'>Trust Score</span><span class='v-pill'>Demand Heatmap</span>"
#         "<span class='v-pill'>Payments</span><span class='v-pill'>Photo Verification</span></div>",
#         unsafe_allow_html=True)
#     st.write("")

#     providers = st.session_state.providers
#     bookings = st.session_state.bookings
#     a, b, c, d = st.columns(4)
#     kpi(a, "Verified professionals", len(providers), "across 3 cities")
#     kpi(b, "Services offered", len(SERVICES), "electrical to mechanical")
#     kpi(c, "Jobs delivered", sum(1 for x in bookings if x["status"] == "Completed"))
#     kpi(d, "Avg trust score",
#         round(sum(trust_score(p) for p in providers) / max(len(providers), 1), 1), "out of 100")
#     st.write("")
#     st.markdown("### Choose your portal")

#     cols = st.columns(3, gap="large")
#     for col, (name, icon, color, tagline, feats) in zip(cols, CARDS):
#         with col:
#             items = "".join(f"<li>{f}</li>" for f in feats)
#             st.markdown(
#                 f"""<div class='v-card'>
#                 <div class='v-icon'>{icon}</div>
#                 <h3>{name}</h3>
#                 <span class='v-tag' style='background:{color}1a;color:{color}'>Portal</span>
#                 <p style='color:#475569;font-size:.92rem;margin:.6rem 0 .2rem'>{tagline}</p>
#                 <ul>{items}</ul></div>""", unsafe_allow_html=True)
#             st.write("")
#             if st.button(f"Enter {name} Portal  →", key=f"go{name}",
#                          use_container_width=True, type="primary"):
#                 st.session_state.role = name
#                 st.rerun()

#     st.write("")
#     st.markdown("### Services on the platform")
#     cols = st.columns(8)
#     for col, (s, ic) in zip(cols, SERVICES):
#         col.markdown(f"<div class='v-kpi' style='text-align:center'><div style='font-size:1.7rem'>{ic}</div>"
#                      f"<div style='font-size:.82rem;font-weight:600;color:#0f172a'>{s}</div></div>",
#                      unsafe_allow_html=True)
#     st.write("")
#     st.caption("VISHVAS 360 · Trust-first local services · Demo build with simulated data.")


# role = st.session_state.role
# if role == "Customer":
#     customer_portal.render()
# elif role == "Service Provider":
#     provider_portal.render()
# elif role == "Admin":
#     admin_portal.render()
# else:
#     home()


"""
VISHVAS 360 — AI-Powered Trusted Local Service Marketplace
Streamlit prototype covering Customer, Service Provider and Admin role
based functionality, built on the provided Postgres/Supabase schema.

This is a self-contained demo: all "database" tables are simulated in
st.session_state so it can be run instantly with `streamlit run`.
Swap the DATA_LAYER functions for real Supabase calls when wiring the
live backend described in the project schema.
"""

# import streamlit as st
# import pandas as pd
# import numpy as np
# import datetime as dt
# import uuid

# # ----------------------------------------------------------------------
# # PAGE CONFIG
# # ----------------------------------------------------------------------
# st.set_page_config(
#     page_title="VISHVAS 360 | Trusted Local Services",
#     page_icon="🛠️",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# # ----------------------------------------------------------------------
# # THEME / CSS — professional navy + teal palette, high-contrast text
# # ----------------------------------------------------------------------
# PRIMARY = "#0B3D62"      # deep navy
# ACCENT = "#0FA3A3"       # teal
# ACCENT_DARK = "#0C8484"
# BG = "#F4F7FA"
# CARD = "#FFFFFF"
# TEXT = "#12202E"
# MUTED = "#5B6B7A"
# DANGER = "#C0392B"
# WARN = "#B9770E"
# OK = "#1E8449"

# st.markdown(f"""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

# html, body, [class*="css"] {{
#     font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
#     color: {TEXT};
# }}

# .stApp {{
#     background-color: {BG};
# }}

# /* Headings */
# h1, h2, h3, h4 {{
#     color: {PRIMARY} !important;
#     font-weight: 800 !important;
# }}
# p, li, span, label, div {{
#     color: {TEXT};
# }}

# /* Sidebar */
# section[data-testid="stSidebar"] {{
#     background-color: {PRIMARY};
# }}
# section[data-testid="stSidebar"] * {{
#     color: #F4F7FA !important;
# }}
# section[data-testid="stSidebar"] .stButton>button {{
#     background-color: {ACCENT};
#     color: white !important;
#     border: none;
#     font-weight: 600;
# }}

# /* Buttons */
# .stButton>button {{
#     background-color: {ACCENT};
#     color: white;
#     border-radius: 8px;
#     border: none;
#     padding: 0.5rem 1.2rem;
#     font-weight: 600;
#     font-size: 0.95rem;
# }}
# .stButton>button:hover {{
#     background-color: {ACCENT_DARK};
#     color: white;
# }}

# /* Cards */
# .vh-card {{
#     background: {CARD};
#     border-radius: 14px;
#     padding: 1.25rem 1.4rem;
#     box-shadow: 0 2px 10px rgba(11,61,98,0.08);
#     border: 1px solid #E4EAF0;
#     margin-bottom: 1rem;
# }}
# .vh-badge {{
#     display:inline-block;
#     padding: 0.18rem 0.65rem;
#     border-radius: 999px;
#     font-size: 0.78rem;
#     font-weight: 700;
#     letter-spacing: .02em;
# }}
# .badge-ok {{ background:#E8F6EE; color:{OK}; }}
# .badge-warn {{ background:#FDF2E3; color:{WARN}; }}
# .badge-danger {{ background:#FBEAE8; color:{DANGER}; }}
# .badge-info {{ background:#E7F6F6; color:{ACCENT_DARK}; }}

# .vh-hero {{
#     background: linear-gradient(135deg, {PRIMARY} 0%, #124E7D 60%, {ACCENT} 130%);
#     padding: 2.4rem 2.2rem;
#     border-radius: 18px;
#     color: white;
#     margin-bottom: 1.6rem;
# }}
# .vh-hero h1 {{ color: white !important; margin-bottom: 0.3rem; }}
# .vh-hero p {{ color: #DCEAF5; font-size: 1.05rem; }}

# .metric-num {{ font-size: 1.9rem; font-weight: 800; color: {PRIMARY}; }}
# .metric-label {{ font-size: 0.85rem; color: {MUTED}; font-weight: 600; text-transform: uppercase; letter-spacing:.03em;}}

# hr {{ border-color: #E4EAF0; }}
# </style>
# """, unsafe_allow_html=True)

# # ----------------------------------------------------------------------
# # I18N — minimal multilingual label support (English / Hindi / Hinglish)
# # ----------------------------------------------------------------------
# LABELS = {
#     "welcome": {"English": "Welcome back", "Hindi": "वापसी पर स्वागत है", "Hinglish": "Welcome wapas"},
#     "book_service": {"English": "Book a Service", "Hindi": "सेवा बुक करें", "Hinglish": "Service Book Karein"},
#     "my_bookings": {"English": "My Bookings", "Hindi": "मेरी बुकिंग", "Hinglish": "Meri Bookings"},
#     "chat_placeholder": {
#         "English": "Describe your problem, e.g. 'My AC is making a strange noise and isn't cooling properly.'",
#         "Hindi": "अपनी समस्या बताएं, जैसे 'मेरा AC अजीब आवाज़ कर रहा है और ठंडा नहीं कर रहा।'",
#         "Hinglish": "Apni problem batao, jaise 'Mere ghar mein washing machine kharab hai.'",
#     },
# }
# def t(key, lang):
#     return LABELS.get(key, {}).get(lang, LABELS.get(key, {}).get("English", key))

# # ----------------------------------------------------------------------
# # SIMULATED DATABASE (st.session_state) — mirrors the Postgres schema
# # ----------------------------------------------------------------------
# def seed():
#     ss = st.session_state
#     ss.profiles = {
#         "admin-1": {"id": "admin-1", "full_name": "Platform Admin", "phone": "9990000000",
#                     "role": "admin", "language": "English", "password": "admin123"},
#         "cust-1": {"id": "cust-1", "full_name": "Anita Sharma", "phone": "9876500001",
#                    "role": "customer", "language": "English", "password": "pass123"},
#         "prov-1": {"id": "prov-1", "full_name": "Rahul Verma", "phone": "9876500002",
#                    "role": "provider", "language": "English", "password": "pass123"},
#     }

#     ss.service_categories = [
#         {"id": 1, "name": "Electrician", "description": "Wiring, switches, fittings"},
#         {"id": 2, "name": "Plumber", "description": "Pipes, taps, leakage"},
#         {"id": 3, "name": "AC Repair", "description": "Cooling, servicing, gas refill"},
#         {"id": 4, "name": "Carpenter", "description": "Furniture, doors, fittings"},
#         {"id": 5, "name": "Painter", "description": "Wall painting, touch-ups"},
#         {"id": 6, "name": "Appliance Repair", "description": "Washing machine, fridge, oven"},
#         {"id": 7, "name": "Cleaning", "description": "Home & office deep cleaning"},
#         {"id": 8, "name": "Mechanic", "description": "Two/four wheeler repair"},
#     ]

#     ss.service_providers = {
#         1: {"id": 1, "profile_id": "prov-1", "business_name": "Rahul Electrical & AC Services",
#             "experience_years": 6, "description": "Certified electrician & AC technician.",
#             "address": "Civil Lines, Muzaffarnagar", "latitude": 29.4727, "longitude": 77.7085,
#             "service_radius_km": 12, "verification_status": "approved",
#             "availability_status": "available", "profile_photo_url": None},
#     }
#     ss.next_provider_id = 2

#     ss.provider_services = [
#         {"provider_id": 1, "service_id": 1, "price": 350},
#         {"provider_id": 1, "service_id": 3, "price": 650},
#     ]

#     ss.bookings = []
#     ss.next_booking_id = 1
#     ss.payments = []
#     ss.next_payment_id = 1
#     ss.reviews = []
#     ss.complaints = []
#     ss.next_complaint_id = 1
#     ss.notifications = []
#     ss.verification = []
#     ss.next_verification_id = 1

#     ss.demand_data = [
#         {"area_name": "Civil Lines", "service": "Electrician", "lat": 29.4727, "lon": 77.7085, "total_requests": 58, "providers": 4},
#         {"area_name": "Sadar Bazar", "service": "Plumber", "lat": 29.4741, "lon": 77.7005, "total_requests": 41, "providers": 3},
#         {"area_name": "New Mandi", "service": "AC Repair", "lat": 29.4650, "lon": 77.7150, "total_requests": 73, "providers": 2},
#         {"area_name": "Khatauli", "service": "Mechanic", "lat": 29.2833, "lon": 77.7167, "total_requests": 22, "providers": 1},
#         {"area_name": "Indirapuram", "service": "AC Repair", "lat": 28.6469, "lon": 77.3672, "total_requests": 64, "providers": 1},
#     ]

#     ss.initialized = True

# if "initialized" not in st.session_state:
#     seed()

# ss = st.session_state
# ss.setdefault("current_user", None)
# ss.setdefault("current_role", None)
# ss.setdefault("nav", "Home")

# # ----------------------------------------------------------------------
# # HELPERS
# # ----------------------------------------------------------------------
# def category_name(cid):
#     for c in ss.service_categories:
#         if c["id"] == cid:
#             return c["name"]
#     return "Unknown"

# def provider_by_id(pid):
#     return ss.service_providers.get(pid)

# def profile_by_id(uid):
#     return ss.profiles.get(uid)

# def add_notification(user_id, title, message, ntype="general"):
#     ss.notifications.append({
#         "id": str(uuid.uuid4())[:8], "user_id": user_id, "title": title,
#         "message": message, "notification_type": ntype, "is_read": False,
#         "created_at": dt.datetime.now(),
#     })

# def signup(full_name, phone, password, role, language="English"):
#     uid = str(uuid.uuid4())[:8]
#     ss.profiles[uid] = {"id": uid, "full_name": full_name, "phone": phone,
#                          "role": role, "language": language, "password": password}
#     if role == "provider":
#         pid = ss.next_provider_id
#         ss.next_provider_id += 1
#         ss.service_providers[pid] = {
#             "id": pid, "profile_id": uid, "business_name": full_name,
#             "experience_years": 0, "description": "", "address": "",
#             "latitude": 29.4727, "longitude": 77.7085, "service_radius_km": 10,
#             "verification_status": "pending", "availability_status": "offline",
#             "profile_photo_url": None,
#         }
#     add_notification(uid, "Welcome to VISHVAS 360", "Your account has been created successfully.", "welcome")
#     return uid

# def login(phone, password):
#     for uid, p in ss.profiles.items():
#         if p["phone"] == phone and p["password"] == password:
#             return uid
#     return None

# def my_provider_record(profile_id):
#     for pid, p in ss.service_providers.items():
#         if p["profile_id"] == profile_id:
#             return p
#     return None

# def simple_intent_extraction(text):
#     """Very lightweight rule-based NLP standing in for the spaCy /
#     Sentence-Transformers pipeline described in the project spec."""
#     text_l = text.lower()
#     service_keywords = {
#         "Electrician": ["electric", "wiring", "switch", "fan", "short circuit", "bijli"],
#         "Plumber": ["pipe", "leak", "tap", "plumb", "paani", "water leak"],
#         "AC Repair": ["ac ", " ac", "cooling", "cooler", "gas refill", "airconditioner", "air conditioner"],
#         "Carpenter": ["furniture", "door", "carpenter", "wood", "almirah"],
#         "Painter": ["paint", "wall color", "whitewash"],
#         "Appliance Repair": ["washing machine", "fridge", "refrigerator", "oven", "microwave", "kharab"],
#         "Cleaning": ["clean", "safai", "deep cleaning"],
#         "Mechanic": ["bike", "scooter", "car", "engine", "mechanic"],
#     }
#     detected_service = None
#     for svc, kws in service_keywords.items():
#         if any(k in text_l for k in kws):
#             detected_service = svc
#             break
#     emergency_keywords = ["emergency", "urgent", "jaldi", "abhi", "asap", "immediately"]
#     priority = "Emergency" if any(k in text_l for k in emergency_keywords) else "Normal"
#     return {
#         "service": detected_service or "Not detected — please choose manually",
#         "problem": text.strip(),
#         "priority": priority,
#     }

# def trust_score(provider_id):
#     """Implements: 30% rating + 20% completed jobs + 15% repeat customers
#     + 15% response rate + 10% (100 - cancellation rate) + 10% verified experience."""
#     p = provider_by_id(provider_id)
#     if not p:
#         return 0
#     completed = [b for b in ss.bookings if b["provider_id"] == provider_id and b["status"] == "completed"]
#     cancelled = [b for b in ss.bookings if b["provider_id"] == provider_id and b["status"] == "cancelled"]
#     total = [b for b in ss.bookings if b["provider_id"] == provider_id]
#     prov_reviews = [r["rating"] for r in ss.reviews if r["provider_id"] == provider_id]
#     avg_rating = (sum(prov_reviews) / len(prov_reviews)) if prov_reviews else 4.0

#     customers = [b["customer_id"] for b in completed]
#     repeat_pct = 0
#     if customers:
#         from collections import Counter
#         counts = Counter(customers)
#         repeats = sum(1 for c in counts.values() if c > 1)
#         repeat_pct = (repeats / len(counts)) * 100

#     cancellation_rate = (len(cancelled) / len(total) * 100) if total else 0
#     response_rate = 96 if total else 90  # placeholder proxy signal
#     verified_exp = min(p.get("experience_years", 0) / 5, 1) * 100
#     completed_score = min(len(completed) / 150, 1) * 100

#     score = (
#         0.30 * (avg_rating / 5 * 100) +
#         0.20 * completed_score +
#         0.15 * repeat_pct +
#         0.15 * response_rate +
#         0.10 * (100 - cancellation_rate) +
#         0.10 * verified_exp
#     )
#     return round(score, 1), {
#         "verified": p["verification_status"] == "approved",
#         "completed_jobs": len(completed),
#         "avg_rating": round(avg_rating, 1),
#         "repeat_pct": round(repeat_pct, 1),
#         "cancellation_rate": round(cancellation_rate, 1),
#         "response_rate": response_rate,
#     }

# def demand_level(total_requests):
#     if total_requests >= 60:
#         return "high"
#     if total_requests >= 35:
#         return "medium"
#     return "low"

# def expansion_recommendation(provider_id):
#     p = provider_by_id(provider_id)
#     my_services = {category_name(ps["service_id"]) for ps in ss.provider_services if ps["provider_id"] == provider_id}
#     candidates = [d for d in ss.demand_data if d["service"] in my_services and d["providers"] <= 2]
#     if not candidates:
#         candidates = sorted(ss.demand_data, key=lambda d: d["total_requests"], reverse=True)
#     best = max(candidates, key=lambda d: d["total_requests"] / max(d["providers"], 1))
#     return best


# # ----------------------------------------------------------------------
# # UI — HOME / AUTH
# # ----------------------------------------------------------------------
# def render_home():
#     st.markdown("""
#     <div class="vh-hero">
#         <h1>🛠️ VISHVAS 360</h1>
#         <p>AI-Powered Trusted Local Service Marketplace — book verified electricians,
#         plumbers, AC technicians and more in seconds, by text or voice, in your own language.</p>
#     </div>
#     """, unsafe_allow_html=True)

#     col1, col2 = st.columns(2)
#     with col1:
#         st.markdown('<div class="vh-card">', unsafe_allow_html=True)
#         st.subheader("👤 I'm a Customer")
#         st.write("Find and book trusted local service providers near you.")
#         if st.button("Continue as Customer", key="pick_customer", use_container_width=True):
#             ss.portal = "customer"
#         st.markdown('</div>', unsafe_allow_html=True)
#     with col2:
#         st.markdown('<div class="vh-card">', unsafe_allow_html=True)
#         st.subheader("🧰 I'm a Service Provider")
#         st.write("Get bookings, grow your business, and build your trust score.")
#         if st.button("Continue as Provider", key="pick_provider", use_container_width=True):
#             ss.portal = "provider"
#         st.markdown('</div>', unsafe_allow_html=True)

#     st.markdown("---")
#     st.caption("Platform admin? Log in with your admin phone number below.")

#     portal = ss.get("portal")
#     if portal:
#         role_label = "Customer" if portal == "customer" else "Service Provider"
#         st.subheader(f"{role_label} Access")
#         tab_login, tab_signup = st.tabs(["Log In", "Sign Up"])

#         with tab_login:
#             with st.form("login_form"):
#                 phone = st.text_input("Phone number")
#                 pw = st.text_input("Password", type="password")
#                 submitted = st.form_submit_button("Log In", use_container_width=True)
#             if submitted:
#                 uid = login(phone, pw)
#                 if uid and ss.profiles[uid]["role"] in (portal, "admin"):
#                     ss.current_user = uid
#                     ss.current_role = ss.profiles[uid]["role"]
#                     st.success(f"Welcome back, {ss.profiles[uid]['full_name']}!")
#                     st.rerun()
#                 else:
#                     st.error("Invalid credentials, or this account isn't registered for this portal.")
#             st.caption("Demo logins — Customer: 9876500001 / pass123 · Provider: 9876500002 / pass123 · Admin: 9990000000 / admin123")

#         with tab_signup:
#             with st.form("signup_form"):
#                 full_name = st.text_input("Full name")
#                 phone_s = st.text_input("Phone number", key="signup_phone")
#                 pw_s = st.text_input("Password", type="password", key="signup_pw")
#                 lang = st.selectbox("Preferred language", ["English", "Hindi", "Hinglish"])
#                 submitted_s = st.form_submit_button("Create Account", use_container_width=True)
#             if submitted_s:
#                 if not full_name or not phone_s or not pw_s:
#                     st.error("Please fill in all fields.")
#                 elif any(p["phone"] == phone_s for p in ss.profiles.values()):
#                     st.error("An account with this phone number already exists.")
#                 else:
#                     uid = signup(full_name, phone_s, pw_s, portal, lang)
#                     ss.current_user = uid
#                     ss.current_role = portal
#                     st.success("Account created!")
#                     st.rerun()

# # ----------------------------------------------------------------------
# # UI — CUSTOMER PORTAL
# # ----------------------------------------------------------------------
# def render_customer():
#     profile = profile_by_id(ss.current_user)
#     lang = profile.get("language", "English")

#     st.sidebar.title("🛠️ VISHVAS 360")
#     st.sidebar.caption(f"{t('welcome', lang)}, {profile['full_name']}")
#     lang_choice = st.sidebar.selectbox("🌐 Language / भाषा", ["English", "Hindi", "Hinglish"],
#                                         index=["English", "Hindi", "Hinglish"].index(lang))
#     if lang_choice != lang:
#         ss.profiles[ss.current_user]["language"] = lang_choice
#         st.rerun()

#     page = st.sidebar.radio("Navigate", [
#         "🤖 AI Chatbot Booking", "📋 Browse & Book", t("my_bookings", lang),
#         "💳 Payments", "⭐ Reviews", "🔔 Notifications", "🚨 Report / Complaint",
#     ])
#     if st.sidebar.button("Log Out"):
#         ss.current_user = None
#         ss.current_role = None
#         ss.portal = None
#         st.rerun()

#     if page == "🤖 AI Chatbot Booking":
#         st.header("🤖 AI Chatbot — Natural-Language Service Discovery")
#         st.write("Type — or imagine speaking — your problem in plain language, in English, Hindi or Hinglish.")
#         text = st.text_area(t("chat_placeholder", lang), height=90)
#         c1, c2 = st.columns([1, 1])
#         with c1:
#             emergency_toggle = st.checkbox("🚨 This is an emergency")
#         with c2:
#             use_voice = st.checkbox("🎙️ Simulate voice input (same pipeline)")
#         if st.button("Analyze & Find Providers", type="primary"):
#             if not text.strip():
#                 st.warning("Please describe your problem first.")
#             else:
#                 result = simple_intent_extraction(text)
#                 if emergency_toggle:
#                     result["priority"] = "Emergency"
#                 st.markdown('<div class="vh-card">', unsafe_allow_html=True)
#                 st.markdown(f"**Service:** {result['service']}")
#                 st.markdown(f"**Problem:** {result['problem']}")
#                 badge_cls = "badge-danger" if result["priority"] == "Emergency" else "badge-info"
#                 st.markdown(f"**Priority:** <span class='vh-badge {badge_cls}'>{result['priority']}</span>", unsafe_allow_html=True)
#                 st.markdown('</div>', unsafe_allow_html=True)
#                 ss.chat_intent = result
#                 st.info("Scroll to **Browse & Book** to see matching providers, pre-filtered on this service.")

#     elif page == "📋 Browse & Book":
#         st.header("📋 Browse Services & Book a Provider")
#         cat_names = [c["name"] for c in ss.service_categories]
#         default_idx = 0
#         prefill = ss.get("chat_intent", {}).get("service")
#         if prefill in cat_names:
#             default_idx = cat_names.index(prefill)
#         service_name = st.selectbox("Service category", cat_names, index=default_idx)
#         service_id = next(c["id"] for c in ss.service_categories if c["name"] == service_name)

#         matches = [ps for ps in ss.provider_services if ps["service_id"] == service_id]
#         st.subheader(f"Providers offering {service_name}")
#         if not matches:
#             st.info("No providers listed yet for this service in the demo data.")
#         for ps in matches:
#             prov = provider_by_id(ps["provider_id"])
#             if not prov:
#                 continue
#             score = trust_score(prov["id"])[0] if ss.bookings or ss.reviews else 85.0
#             st.markdown('<div class="vh-card">', unsafe_allow_html=True)
#             cols = st.columns([3, 1, 1, 1])
#             cols[0].markdown(f"**{prov['business_name']}**  \n{prov['address']}  \n"
#                               f"Experience: {prov['experience_years']} yrs")
#             v_badge = "badge-ok" if prov["verification_status"] == "approved" else "badge-warn"
#             cols[1].markdown(f"<span class='vh-badge {v_badge}'>{prov['verification_status'].title()}</span>", unsafe_allow_html=True)
#             cols[2].markdown(f"**Trust Score**<br><span class='metric-num' style='font-size:1.3rem'>{score}/100</span>", unsafe_allow_html=True)
#             cols[3].markdown(f"**₹{ps['price']}**  \navailability: {prov['availability_status']}")
#             with st.expander("Book this provider"):
#                 with st.form(f"book_{prov['id']}_{service_id}"):
#                     b_date = st.date_input("Date", min_value=dt.date.today())
#                     b_time = st.time_input("Time")
#                     address = st.text_input("Your address", value=prov.get("address", ""))
#                     desc = st.text_area("Describe the issue", value=ss.get("chat_intent", {}).get("problem", ""))
#                     is_emergency = st.checkbox("Emergency booking", value=(ss.get("chat_intent", {}).get("priority") == "Emergency"))
#                     ok = st.form_submit_button("Confirm Booking", type="primary")
#                 if ok:
#                     bid = ss.next_booking_id
#                     ss.next_booking_id += 1
#                     ss.bookings.append({
#                         "id": bid, "customer_id": ss.current_user, "provider_id": prov["id"],
#                         "service_id": service_id, "booking_date": b_date, "booking_time": b_time,
#                         "address": address, "description": desc, "status": "pending",
#                         "is_emergency": is_emergency, "estimated_price": ps["price"],
#                         "created_at": dt.datetime.now(),
#                     })
#                     add_notification(prov["profile_id"], "New booking request",
#                                       f"{profile['full_name']} requested {service_name}.", "new_booking")
#                     add_notification(ss.current_user, "Booking placed",
#                                       f"Your {service_name} booking is pending provider confirmation.", "booking")
#                     st.success("Booking placed! Track it under 'My Bookings'.")
#             st.markdown('</div>', unsafe_allow_html=True)

#     elif page == t("my_bookings", lang):
#         st.header(f"📑 {t('my_bookings', lang)}")
#         my_b = [b for b in ss.bookings if b["customer_id"] == ss.current_user]
#         if not my_b:
#             st.info("No bookings yet — go to 'Browse & Book' to get started.")
#         for b in sorted(my_b, key=lambda x: x["created_at"], reverse=True):
#             prov = provider_by_id(b["provider_id"])
#             st.markdown('<div class="vh-card">', unsafe_allow_html=True)
#             cols = st.columns([3, 1, 1])
#             cols[0].markdown(f"**{category_name(b['service_id'])}** with {prov['business_name'] if prov else 'TBA'}  \n"
#                               f"{b['booking_date']} at {b['booking_time']}  \n{b['description']}")
#             status_map = {"pending": "badge-warn", "accepted": "badge-info", "on_the_way": "badge-info",
#                           "in_progress": "badge-info", "completed": "badge-ok",
#                           "rejected": "badge-danger", "cancelled": "badge-danger"}
#             cols[1].markdown(f"<span class='vh-badge {status_map.get(b['status'],'badge-info')}'>{b['status'].replace('_',' ').title()}</span>", unsafe_allow_html=True)
#             if b["status"] == "pending":
#                 if cols[2].button("Cancel", key=f"cancel_{b['id']}"):
#                     b["status"] = "cancelled"
#                     st.rerun()
#             if b["status"] == "completed":
#                 already_reviewed = any(r["booking_id"] == b["id"] for r in ss.reviews)
#                 if not already_reviewed:
#                     with st.expander("Leave a review"):
#                         with st.form(f"review_{b['id']}"):
#                             rating = st.slider("Rating", 1, 5, 5)
#                             text = st.text_area("Comments")
#                             sub = st.form_submit_button("Submit Review")
#                         if sub:
#                             ss.reviews.append({"booking_id": b["id"], "customer_id": ss.current_user,
#                                                 "provider_id": b["provider_id"], "rating": rating,
#                                                 "review_text": text, "created_at": dt.datetime.now()})
#                             st.success("Thanks for your feedback!")
#                             st.rerun()
#             st.markdown('</div>', unsafe_allow_html=True)

#     elif page == "💳 Payments":
#         st.header("💳 Payment Gateway")
#         payable = [b for b in ss.bookings if b["customer_id"] == ss.current_user
#                    and b["status"] in ("accepted", "completed")
#                    and not any(p["booking_id"] == b["id"] for p in ss.payments)]
#         if not payable:
#             st.info("No pending payments.")
#         for b in payable:
#             st.markdown('<div class="vh-card">', unsafe_allow_html=True)
#             st.write(f"**{category_name(b['service_id'])}** — Estimated: ₹{b['estimated_price']}")
#             method = st.selectbox("Payment method", ["upi", "card", "netbanking", "wallet"], key=f"pm_{b['id']}")
#             if st.button("Pay Now", key=f"pay_{b['id']}"):
#                 ss.payments.append({
#                     "id": ss.next_payment_id, "booking_id": b["id"], "customer_id": ss.current_user,
#                     "amount": b["estimated_price"], "payment_method": method,
#                     "payment_status": "success", "transaction_id": str(uuid.uuid4())[:10],
#                     "paid_at": dt.datetime.now(),
#                 })
#                 ss.next_payment_id += 1
#                 st.success("Payment successful (simulated).")
#                 add_notification(ss.current_user, "Payment successful", f"₹{b['estimated_price']} paid via {method}.", "payment")
#                 st.rerun()
#             st.markdown('</div>', unsafe_allow_html=True)

#         st.subheader("Payment history")
#         mine = [p for p in ss.payments if p["customer_id"] == ss.current_user]
#         if mine:
#             st.dataframe(pd.DataFrame(mine)[["id", "booking_id", "amount", "payment_method", "payment_status", "paid_at"]],
#                          use_container_width=True, hide_index=True)

#     elif page == "⭐ Reviews":
#         st.header("⭐ My Reviews")
#         mine = [r for r in ss.reviews if r["customer_id"] == ss.current_user]
#         if not mine:
#             st.info("You haven't left any reviews yet.")
#         for r in mine:
#             prov = provider_by_id(r["provider_id"])
#             st.markdown('<div class="vh-card">', unsafe_allow_html=True)
#             st.write(f"**{prov['business_name'] if prov else 'Provider'}** — {'⭐'*r['rating']}")
#             st.write(r["review_text"])
#             st.markdown('</div>', unsafe_allow_html=True)

#     elif page == "🔔 Notifications":
#         st.header("🔔 Notifications")
#         mine = [n for n in ss.notifications if n["user_id"] == ss.current_user]
#         for n in sorted(mine, key=lambda x: x["created_at"], reverse=True):
#             st.markdown('<div class="vh-card">', unsafe_allow_html=True)
#             st.write(f"**{n['title']}**  \n{n['message']}")
#             st.caption(n["created_at"].strftime("%d %b %Y, %I:%M %p"))
#             st.markdown('</div>', unsafe_allow_html=True)
#         if not mine:
#             st.info("No notifications yet.")

#     elif page == "🚨 Report / Complaint":
#         st.header("🚨 Raise a Complaint")
#         my_b = [b for b in ss.bookings if b["customer_id"] == ss.current_user]
#         with st.form("complaint_form"):
#             booking_choice = st.selectbox("Related booking (optional)",
#                                            ["None"] + [f"#{b['id']} — {category_name(b['service_id'])}" for b in my_b])
#             subject = st.text_input("Subject")
#             desc = st.text_area("Description")
#             sub = st.form_submit_button("Submit Complaint")
#         if sub:
#             booking_id = None
#             provider_id = None
#             if booking_choice != "None":
#                 bid = int(booking_choice.split("#")[1].split(" ")[0])
#                 booking_id = bid
#                 b = next(x for x in my_b if x["id"] == bid)
#                 provider_id = b["provider_id"]
#             ss.complaints.append({
#                 "id": ss.next_complaint_id, "booking_id": booking_id, "customer_id": ss.current_user,
#                 "provider_id": provider_id, "subject": subject, "description": desc,
#                 "status": "open", "created_at": dt.datetime.now(), "resolved_at": None,
#             })
#             ss.next_complaint_id += 1
#             st.success("Complaint submitted. Our admin team will review it shortly.")


# # ----------------------------------------------------------------------
# # UI — PROVIDER PORTAL
# # ----------------------------------------------------------------------
# def render_provider():
#     profile = profile_by_id(ss.current_user)
#     prov = my_provider_record(ss.current_user)

#     st.sidebar.title("🛠️ VISHVAS 360")
#     st.sidebar.caption(f"Provider · {profile['full_name']}")
#     page = st.sidebar.radio("Navigate", [
#         "🏠 Overview", "🧾 Profile & Verification", "🧰 My Services & Pricing",
#         "📥 Incoming Bookings", "⭐ Trust Score", "🗺️ Demand Heatmap",
#         "🚀 Business Expansion", "🔔 Notifications",
#     ])
#     if st.sidebar.button("Log Out"):
#         ss.current_user = None
#         ss.current_role = None
#         ss.portal = None
#         st.rerun()

#     if not prov:
#         st.error("No provider profile found for this account.")
#         return

#     if page == "🏠 Overview":
#         st.header(f"👋 Welcome, {prov['business_name']}")
#         my_bookings = [b for b in ss.bookings if b["provider_id"] == prov["id"]]
#         completed = [b for b in my_bookings if b["status"] == "completed"]
#         pending = [b for b in my_bookings if b["status"] == "pending"]
#         earnings = sum(p["amount"] for p in ss.payments if p["booking_id"] in [b["id"] for b in completed])
#         c1, c2, c3, c4 = st.columns(4)
#         for col, label, val in zip([c1, c2, c3, c4],
#                                     ["Total Bookings", "Completed Jobs", "Pending Requests", "Earnings (₹)"],
#                                     [len(my_bookings), len(completed), len(pending), f"{earnings:,.0f}"]):
#             col.markdown(f"<div class='vh-card'><div class='metric-label'>{label}</div>"
#                           f"<div class='metric-num'>{val}</div></div>", unsafe_allow_html=True)
#         status_badge = "badge-ok" if prov["verification_status"] == "approved" else "badge-warn"
#         st.markdown(f"Verification status: <span class='vh-badge {status_badge}'>{prov['verification_status'].title()}</span>",
#                     unsafe_allow_html=True)
#         avail = st.selectbox("Set your availability", ["available", "busy", "offline"],
#                               index=["available", "busy", "offline"].index(prov["availability_status"]))
#         if avail != prov["availability_status"]:
#             prov["availability_status"] = avail
#             st.success("Availability updated.")

#     elif page == "🧾 Profile & Verification":
#         st.header("🧾 Business Profile & Identity Verification")
#         with st.form("provider_profile"):
#             biz = st.text_input("Business name", value=prov["business_name"])
#             exp = st.number_input("Years of experience", min_value=0, max_value=50, value=prov["experience_years"])
#             desc = st.text_area("Description", value=prov["description"])
#             addr = st.text_input("Service address", value=prov["address"])
#             radius = st.slider("Service radius (km)", 1, 50, int(prov["service_radius_km"]))
#             saved = st.form_submit_button("Save Profile")
#         if saved:
#             prov.update({"business_name": biz, "experience_years": exp, "description": desc,
#                          "address": addr, "service_radius_km": radius})
#             st.success("Profile updated.")

#         st.subheader("🪪 Identity & Photo Verification")
#         st.caption("Document upload → OCR/data validation → selfie/photo match → admin approval "
#                    "(no raw ID numbers are stored, per UIDAI e-KYC guidance).")
#         with st.form("verification_form"):
#             id_doc = st.file_uploader("Government-approved ID document", type=["pdf", "png", "jpg", "jpeg"])
#             photo = st.file_uploader("Profile / selfie photo", type=["png", "jpg", "jpeg"])
#             cert = st.file_uploader("Optional service certificate", type=["pdf", "png", "jpg", "jpeg"])
#             submit_v = st.form_submit_button("Submit for Verification")
#         if submit_v:
#             if not id_doc or not photo:
#                 st.warning("Please upload both an ID document and a profile photo.")
#             else:
#                 ss.verification.append({
#                     "id": ss.next_verification_id, "provider_id": prov["id"],
#                     "identity_document_url": id_doc.name, "profile_photo_url": photo.name,
#                     "verification_status": "pending", "created_at": dt.datetime.now(),
#                 })
#                 ss.next_verification_id += 1
#                 prov["verification_status"] = "pending"
#                 st.success("Documents submitted. An admin will review your verification shortly.")

#     elif page == "🧰 My Services & Pricing":
#         st.header("🧰 Services You Offer")
#         offered_ids = {ps["service_id"] for ps in ss.provider_services if ps["provider_id"] == prov["id"]}
#         for cat in ss.service_categories:
#             existing = next((ps for ps in ss.provider_services if ps["provider_id"] == prov["id"] and ps["service_id"] == cat["id"]), None)
#             cols = st.columns([2, 1, 1])
#             cols[0].write(f"**{cat['name']}** — {cat['description']}")
#             checked = cols[1].checkbox("Offer this", value=existing is not None, key=f"off_{cat['id']}")
#             price = cols[2].number_input("Price (₹)", min_value=0, value=existing["price"] if existing else 0,
#                                           key=f"price_{cat['id']}")
#             if checked and not existing:
#                 ss.provider_services.append({"provider_id": prov["id"], "service_id": cat["id"], "price": price})
#             elif checked and existing:
#                 existing["price"] = price
#             elif not checked and existing:
#                 ss.provider_services.remove(existing)

#     elif page == "📥 Incoming Bookings":
#         st.header("📥 Incoming Bookings")
#         my_bookings = [b for b in ss.bookings if b["provider_id"] == prov["id"]]
#         if not my_bookings:
#             st.info("No bookings yet.")
#         next_status = {"pending": ("accepted", "rejected"), "accepted": ("on_the_way", None),
#                        "on_the_way": ("in_progress", None), "in_progress": ("completed", None)}
#         for b in sorted(my_bookings, key=lambda x: x["created_at"], reverse=True):
#             cust = profile_by_id(b["customer_id"])
#             st.markdown('<div class="vh-card">', unsafe_allow_html=True)
#             emo = "🚨 " if b["is_emergency"] else ""
#             st.markdown(f"{emo}**{category_name(b['service_id'])}** for {cust['full_name']}  \n"
#                         f"{b['booking_date']} at {b['booking_time']} — {b['address']}  \n{b['description']}")
#             st.markdown(f"Status: <span class='vh-badge badge-info'>{b['status'].replace('_',' ').title()}</span>", unsafe_allow_html=True)
#             fwd, rej = next_status.get(b["status"], (None, None))
#             c1, c2 = st.columns(2)
#             if fwd:
#                 if c1.button(f"Mark as {fwd.replace('_',' ').title()}", key=f"fwd_{b['id']}"):
#                     b["status"] = fwd
#                     add_notification(b["customer_id"], "Booking update",
#                                       f"Your booking is now '{fwd.replace('_',' ')}'.", "status_update")
#                     st.rerun()
#             if rej:
#                 if c2.button("Reject", key=f"rej_{b['id']}"):
#                     b["status"] = rej
#                     add_notification(b["customer_id"], "Booking rejected", "The provider is unavailable for this request.", "status_update")
#                     st.rerun()
#             st.markdown('</div>', unsafe_allow_html=True)

#     elif page == "⭐ Trust Score":
#         st.header("⭐ Serviora Trust Score")
#         score, details = trust_score(prov["id"])
#         c1, c2 = st.columns([1, 2])
#         c1.markdown(f"<div class='vh-card' style='text-align:center'><div class='metric-label'>Trust Score</div>"
#                     f"<div class='metric-num' style='font-size:2.6rem'>{score}/100</div></div>", unsafe_allow_html=True)
#         with c2:
#             st.markdown('<div class="vh-card">', unsafe_allow_html=True)
#             st.write(f"✅ Verified identity: **{'Yes' if details['verified'] else 'Pending'}**")
#             st.write(f"📦 Completed jobs: **{details['completed_jobs']}**")
#             st.write(f"⭐ Customer rating: **{details['avg_rating']}/5**")
#             st.write(f"🔁 Repeat customers: **{details['repeat_pct']}%**")
#             st.write(f"📉 Cancellation rate: **{details['cancellation_rate']}%**")
#             st.write(f"⚡ Response rate: **{details['response_rate']}%**")
#             st.markdown('</div>', unsafe_allow_html=True)
#         st.caption("Formula: 30% rating + 20% completed jobs + 15% repeat customers + "
#                    "15% response rate + 10% (100 − cancellation rate) + 10% verified experience.")

#     elif page == "🗺️ Demand Heatmap":
#         st.header("🗺️ Service Demand Heatmap")
#         df = pd.DataFrame(ss.demand_data)
#         svc_filter = st.multiselect("Filter by service", sorted(df["service"].unique()), default=list(df["service"].unique()))
#         df = df[df["service"].isin(svc_filter)]
#         df["demand"] = df["total_requests"].apply(demand_level)
#         color_map = {"high": [192, 57, 43], "medium": [185, 119, 14], "low": [30, 132, 73]}
#         df["color"] = df["demand"].map(color_map)
#         st.map(df.rename(columns={"lat": "latitude", "lon": "longitude"}), size=20, color="color")
#         st.dataframe(df[["area_name", "service", "total_requests", "providers", "demand"]],
#                      use_container_width=True, hide_index=True)
#         st.caption("🔴 High demand · 🟠 Medium demand · 🟢 Low demand")

#     elif page == "🚀 Business Expansion":
#         st.header("🚀 AI Business Expansion Recommendation")
#         best = expansion_recommendation(prov["id"])
#         st.markdown('<div class="vh-card">', unsafe_allow_html=True)
#         st.subheader("📍 Expansion Opportunity Detected")
#         st.write(f"**Recommended area:** {best['area_name']}")
#         st.write(f"**Service in demand:** {best['service']}")
#         st.write(f"**Demand level:** {demand_level(best['total_requests']).title()}")
#         st.write(f"**Current provider density:** {best['providers']}")
#         st.write(f"**Total recent requests:** {best['total_requests']}")
#         st.info(f"Expanding coverage to **{best['area_name']}** may provide higher booking opportunities, "
#                 f"given {best['providers']} active provider(s) against {best['total_requests']} recent requests.")
#         st.markdown('</div>', unsafe_allow_html=True)

#     elif page == "🔔 Notifications":
#         st.header("🔔 Notifications")
#         mine = [n for n in ss.notifications if n["user_id"] == ss.current_user]
#         for n in sorted(mine, key=lambda x: x["created_at"], reverse=True):
#             st.markdown('<div class="vh-card">', unsafe_allow_html=True)
#             st.write(f"**{n['title']}**  \n{n['message']}")
#             st.caption(n["created_at"].strftime("%d %b %Y, %I:%M %p"))
#             st.markdown('</div>', unsafe_allow_html=True)
#         if not mine:
#             st.info("No notifications yet.")

# # ----------------------------------------------------------------------
# # UI — ADMIN PORTAL
# # ----------------------------------------------------------------------
# def render_admin():
#     profile = profile_by_id(ss.current_user)
#     st.sidebar.title("🛠️ VISHVAS 360")
#     st.sidebar.caption(f"Admin · {profile['full_name']}")
#     page = st.sidebar.radio("Navigate", [
#         "📊 Platform Overview", "👥 Users", "🧰 Providers & Verification",
#         "📈 Services & Demand", "🚨 Complaints",
#     ])
#     if st.sidebar.button("Log Out"):
#         ss.current_user = None
#         ss.current_role = None
#         ss.portal = None
#         st.rerun()

#     if page == "📊 Platform Overview":
#         st.header("📊 Platform Overview")
#         total_bookings = len(ss.bookings)
#         total_revenue = sum(p["amount"] for p in ss.payments if p["payment_status"] == "success")
#         emergency = len([b for b in ss.bookings if b["is_emergency"]])
#         open_complaints = len([c for c in ss.complaints if c["status"] == "open"])
#         cols = st.columns(4)
#         for col, label, val in zip(cols, ["Total Bookings", "Revenue (₹)", "Emergency Requests", "Open Complaints"],
#                                     [total_bookings, f"{total_revenue:,.0f}", emergency, open_complaints]):
#             col.markdown(f"<div class='vh-card'><div class='metric-label'>{label}</div>"
#                           f"<div class='metric-num'>{val}</div></div>", unsafe_allow_html=True)

#         if ss.bookings:
#             df = pd.DataFrame(ss.bookings)
#             df["service"] = df["service_id"].apply(category_name)
#             st.subheader("Growth trend — bookings per day")
#             trend = df.groupby(df["created_at"].apply(lambda d: d.date())).size().reset_index(name="bookings")
#             st.line_chart(trend, x="created_at", y="bookings")
#             st.subheader("Bookings by status")
#             st.bar_chart(df["status"].value_counts())
#         else:
#             st.info("No bookings yet — data will appear here as customers book services.")

#     elif page == "👥 Users":
#         st.header("👥 Users")
#         rows = [{"ID": p["id"], "Name": p["full_name"], "Phone": p["phone"], "Role": p["role"],
#                  "Language": p["language"]} for p in ss.profiles.values()]
#         df = pd.DataFrame(rows)
#         role_filter = st.multiselect("Filter by role", sorted(df["Role"].unique()), default=list(df["Role"].unique()))
#         st.dataframe(df[df["Role"].isin(role_filter)], use_container_width=True, hide_index=True)

#     elif page == "🧰 Providers & Verification":
#         st.header("🧰 Providers & Verification")
#         for pid, prov in ss.service_providers.items():
#             profile_p = profile_by_id(prov["profile_id"])
#             score = trust_score(pid)[0]
#             st.markdown('<div class="vh-card">', unsafe_allow_html=True)
#             cols = st.columns([3, 1, 1, 1])
#             cols[0].markdown(f"**{prov['business_name']}**  \n{profile_p['full_name'] if profile_p else ''} · {prov['address']}")
#             v_badge = {"approved": "badge-ok", "pending": "badge-warn", "rejected": "badge-danger"}[prov["verification_status"]]
#             cols[1].markdown(f"<span class='vh-badge {v_badge}'>{prov['verification_status'].title()}</span>", unsafe_allow_html=True)
#             cols[2].markdown(f"Trust: **{score}/100**")
#             if prov["verification_status"] == "pending":
#                 if cols[3].button("Approve", key=f"appr_{pid}"):
#                     prov["verification_status"] = "approved"
#                     add_notification(prov["profile_id"], "Verification approved", "Your account is now verified!", "verification")
#                     st.rerun()
#                 if cols[3].button("Reject", key=f"rej_{pid}"):
#                     prov["verification_status"] = "rejected"
#                     add_notification(prov["profile_id"], "Verification rejected", "Please resubmit valid documents.", "verification")
#                     st.rerun()
#             st.markdown('</div>', unsafe_allow_html=True)

#     elif page == "📈 Services & Demand":
#         st.header("📈 Services & Demand Heatmap")
#         df = pd.DataFrame(ss.demand_data)
#         df["demand"] = df["total_requests"].apply(demand_level)
#         color_map = {"high": [192, 57, 43], "medium": [185, 119, 14], "low": [30, 132, 73]}
#         df["color"] = df["demand"].map(color_map)
#         st.map(df.rename(columns={"lat": "latitude", "lon": "longitude"}), size=20, color="color")
#         st.dataframe(df[["area_name", "service", "total_requests", "providers", "demand"]],
#                      use_container_width=True, hide_index=True)
#         most_requested = df.loc[df["total_requests"].idxmax()]
#         st.info(f"Most requested service right now: **{most_requested['service']}** in **{most_requested['area_name']}**.")

#     elif page == "🚨 Complaints":
#         st.header("🚨 Complaints")
#         if not ss.complaints:
#             st.info("No complaints filed.")
#         for c in sorted(ss.complaints, key=lambda x: x["created_at"], reverse=True):
#             cust = profile_by_id(c["customer_id"])
#             st.markdown('<div class="vh-card">', unsafe_allow_html=True)
#             st.write(f"**{c['subject']}** — filed by {cust['full_name'] if cust else 'Unknown'}")
#             st.write(c["description"])
#             status = st.selectbox("Status", ["open", "investigating", "resolved", "closed"],
#                                    index=["open", "investigating", "resolved", "closed"].index(c["status"]),
#                                    key=f"cstatus_{c['id']}")
#             if status != c["status"]:
#                 c["status"] = status
#                 if status in ("resolved", "closed"):
#                     c["resolved_at"] = dt.datetime.now()
#                 st.rerun()
#             st.markdown('</div>', unsafe_allow_html=True)

# # ----------------------------------------------------------------------
# # ROUTER
# # ----------------------------------------------------------------------
# if ss.current_user is None:
#     render_home()
# else:
#     role = ss.current_role
#     if role == "customer":
#         render_customer()
#     elif role == "provider":
#         render_provider()
#     elif role == "admin":
#         render_admin()



# """
# VISHVAS 360 — AI-Powered Trusted Local Service Marketplace
# Streamlit prototype covering Customer, Service Provider and Admin role
# based functionality, built on the provided Postgres/Supabase schema.

# This is a self-contained demo: all "database" tables are simulated in
# st.session_state so it can be run instantly with `streamlit run`.
# Swap the DATA_LAYER functions for real Supabase calls when wiring the
# live backend described in the project schema.
# """

import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import uuid
import math
from streamlit.components.v1 import html as st_html

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# ----------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="VISHVAS 360 | Trusted Local Services",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------
# CONFIG — replace with your own keys when wiring the real backend
# ----------------------------------------------------------------------
RAZORPAY_KEY_ID = "rzp_test_REPLACE_WITH_YOUR_KEY_ID"  # Razorpay test/live Key ID
FACE_MATCH_THRESHOLD = 0.85  # cosine similarity threshold for auto-verification
EXPANSION_RADIUS_KM = 100     # business-expansion search radius

# ----------------------------------------------------------------------
# THEME / CSS — professional navy + teal palette, high-contrast text
# ----------------------------------------------------------------------
PRIMARY = "#0B3D62"      # deep navy
ACCENT = "#0FA3A3"       # teal
ACCENT_DARK = "#0C8484"
BG = "#F4F7FA"
CARD = "#FFFFFF"
TEXT = "#12202E"
MUTED = "#5B6B7A"
DANGER = "#C0392B"
WARN = "#B9770E"
OK = "#1E8449"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: {TEXT};
}}

.stApp {{
    background-color: {BG};
}}

/* Headings */
h1, h2, h3, h4 {{
    color: {PRIMARY} !important;
    font-weight: 800 !important;
}}
p, li, span, label, div {{
    color: {TEXT};
}}

/* Sidebar */
section[data-testid="stSidebar"] {{
    background-color: {PRIMARY};
}}
section[data-testid="stSidebar"] * {{
    color: #F4F7FA !important;
}}
section[data-testid="stSidebar"] .stButton>button {{
    background-color: {ACCENT};
    color: white !important;
    border: none;
    font-weight: 600;
}}

/* Buttons */
.stButton>button {{
    background-color: {ACCENT};
    color: white;
    border-radius: 8px;
    border: none;
    padding: 0.5rem 1.2rem;
    font-weight: 600;
    font-size: 0.95rem;
}}
.stButton>button:hover {{
    background-color: {ACCENT_DARK};
    color: white;
}}

/* Cards */
.vh-card {{
    background: {CARD};
    border-radius: 14px;
    padding: 1.25rem 1.4rem;
    box-shadow: 0 2px 10px rgba(11,61,98,0.08);
    border: 1px solid #E4EAF0;
    margin-bottom: 1rem;
}}
.vh-badge {{
    display:inline-block;
    padding: 0.18rem 0.65rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: .02em;
}}
.badge-ok {{ background:#E8F6EE; color:{OK}; }}
.badge-warn {{ background:#FDF2E3; color:{WARN}; }}
.badge-danger {{ background:#FBEAE8; color:{DANGER}; }}
.badge-info {{ background:#E7F6F6; color:{ACCENT_DARK}; }}

.vh-hero {{
    background: linear-gradient(135deg, {PRIMARY} 0%, #124E7D 60%, {ACCENT} 130%);
    padding: 2.4rem 2.2rem;
    border-radius: 18px;
    color: white;
    margin-bottom: 1.6rem;
}}
.vh-hero h1 {{ color: white !important; margin-bottom: 0.3rem; }}
.vh-hero p {{ color: #DCEAF5; font-size: 1.05rem; }}

.metric-num {{ font-size: 1.9rem; font-weight: 800; color: {PRIMARY}; }}
.metric-label {{ font-size: 0.85rem; color: {MUTED}; font-weight: 600; text-transform: uppercase; letter-spacing:.03em;}}

hr {{ border-color: #E4EAF0; }}

/* ---- Visibility hardening: force readable colors on every Streamlit
   widget, regardless of the viewer's light/dark browser theme. ---- */
[data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
    background-color: {BG};
}}
.stTextInput input, .stNumberInput input, .stDateInput input, .stTimeInput input,
.stTextArea textarea, div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {{
    background-color: #FFFFFF !important;
    color: {TEXT} !important;
    border: 1px solid #C9D6E2 !important;
}}
div[data-baseweb="popover"] * , ul[data-baseweb="menu"] * {{
    color: {TEXT} !important;
    background-color: #FFFFFF !important;
}}
.stRadio label, .stCheckbox label, .stSlider label, .stSelectbox label,
.stTextInput label, .stTextArea label, .stNumberInput label, .stDateInput label,
.stTimeInput label, .stMultiSelect label, .stFileUploader label, .stFileUploader small {{
    color: {TEXT} !important;
    font-weight: 500;
}}
[data-testid="stWidgetLabel"] p {{
    color: {TEXT} !important;
    font-weight: 600 !important;
}}
.stTabs [data-baseweb="tab-list"] {{ gap: 4px; }}
.stTabs [data-baseweb="tab"] {{
    background-color: #EAF1F6;
    border-radius: 8px 8px 0 0;
    color: {TEXT} !important;
    font-weight: 600;
    padding: 0.5rem 1rem;
}}
.stTabs [aria-selected="true"] {{
    background-color: {ACCENT} !important;
    color: white !important;
}}
.stTabs [aria-selected="true"] p {{ color: white !important; }}
[data-testid="stExpander"] {{
    background-color: #FFFFFF;
    border: 1px solid #E4EAF0;
    border-radius: 10px;
}}
[data-testid="stExpander"] summary {{
    color: {PRIMARY} !important;
    font-weight: 700 !important;
}}
[data-testid="stDataFrame"] {{
    background-color: #FFFFFF;
}}
[data-testid="stFileUploaderDropzone"], [data-testid="stCameraInput"], [data-testid="stAudioInput"] {{
    background-color: #FFFFFF !important;
    border: 1.5px dashed #A9BCCB !important;
    border-radius: 10px;
}}
[data-testid="stAlert"] p {{ color: {TEXT} !important; font-weight: 500; }}
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{ color: {PRIMARY} !important; }}
section[data-testid="stSidebar"] .stRadio label p {{ color: #F4F7FA !important; font-weight: 600 !important; }}
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {{ color: #F4F7FA !important; }}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# I18N — minimal multilingual label support (English / Hindi / Hinglish)
# ----------------------------------------------------------------------
LABELS = {
    "welcome": {"English": "Welcome back", "Hindi": "वापसी पर स्वागत है", "Hinglish": "Welcome wapas"},
    "book_service": {"English": "Book a Service", "Hindi": "सेवा बुक करें", "Hinglish": "Service Book Karein"},
    "my_bookings": {"English": "My Bookings", "Hindi": "मेरी बुकिंग", "Hinglish": "Meri Bookings"},
    "chat_placeholder": {
        "English": "Describe your problem, e.g. 'My AC is making a strange noise and isn't cooling properly.'",
        "Hindi": "अपनी समस्या बताएं, जैसे 'मेरा AC अजीब आवाज़ कर रहा है और ठंडा नहीं कर रहा।'",
        "Hinglish": "Apni problem batao, jaise 'Mere ghar mein washing machine kharab hai.'",
    },
}
def t(key, lang):
    return LABELS.get(key, {}).get(lang, LABELS.get(key, {}).get("English", key))

# ----------------------------------------------------------------------
# LOCATION PRESETS — reused by customer / provider location pickers
# ----------------------------------------------------------------------
AREA_PRESETS = [
    {"area_name": "Civil Lines", "lat": 29.4727, "lon": 77.7085},
    {"area_name": "Sadar Bazar", "lat": 29.4741, "lon": 77.7005},
    {"area_name": "New Mandi", "lat": 29.4650, "lon": 77.7150},
    {"area_name": "Khatauli", "lat": 29.2833, "lon": 77.7167},
    {"area_name": "Indirapuram", "lat": 28.6469, "lon": 77.3672},
]

# ----------------------------------------------------------------------
# SIMULATED DATABASE (st.session_state) — mirrors the Postgres schema
# ----------------------------------------------------------------------
def seed():
    ss = st.session_state
    ss.profiles = {
        "admin-1": {"id": "admin-1", "full_name": "Platform Admin", "phone": "9990000000",
                    "role": "admin", "language": "English", "password": "admin123"},
        "cust-1": {"id": "cust-1", "full_name": "Anita Sharma", "phone": "9876500001",
                   "role": "customer", "language": "English", "password": "pass123"},
        "prov-1": {"id": "prov-1", "full_name": "Rahul Verma", "phone": "9876500002",
                   "role": "provider", "language": "English", "password": "pass123"},
    }

    ss.service_categories = [
        {"id": 1, "name": "Electrician", "description": "Wiring, switches, fittings"},
        {"id": 2, "name": "Plumber", "description": "Pipes, taps, leakage"},
        {"id": 3, "name": "AC Repair", "description": "Cooling, servicing, gas refill"},
        {"id": 4, "name": "Carpenter", "description": "Furniture, doors, fittings"},
        {"id": 5, "name": "Painter", "description": "Wall painting, touch-ups"},
        {"id": 6, "name": "Appliance Repair", "description": "Washing machine, fridge, oven"},
        {"id": 7, "name": "Cleaning", "description": "Home & office deep cleaning"},
        {"id": 8, "name": "Mechanic", "description": "Two/four wheeler repair"},
    ]

    ss.service_providers = {
        1: {"id": 1, "profile_id": "prov-1", "business_name": "Rahul Electrical & AC Services",
            "experience_years": 6, "description": "Certified electrician & AC technician.",
            "address": "Civil Lines, Muzaffarnagar", "latitude": 29.4727, "longitude": 77.7085,
            "service_radius_km": 12, "verification_status": "approved",
            "availability_status": "available", "profile_photo_url": None},
    }
    ss.next_provider_id = 2

    ss.provider_services = [
        {"provider_id": 1, "service_id": 1, "price": 350},
        {"provider_id": 1, "service_id": 3, "price": 650},
    ]

    ss.bookings = []
    ss.next_booking_id = 1
    ss.payments = []
    ss.next_payment_id = 1
    ss.reviews = []
    ss.complaints = []
    ss.next_complaint_id = 1
    ss.notifications = []
    ss.verification = []
    ss.next_verification_id = 1
    ss.customer_locations = {}

    ss.demand_data = [
        {"area_name": "Civil Lines", "service": "Electrician", "lat": 29.4727, "lon": 77.7085, "total_requests": 58, "providers": 4},
        {"area_name": "Sadar Bazar", "service": "Plumber", "lat": 29.4741, "lon": 77.7005, "total_requests": 41, "providers": 3},
        {"area_name": "New Mandi", "service": "AC Repair", "lat": 29.4650, "lon": 77.7150, "total_requests": 73, "providers": 2},
        {"area_name": "Khatauli", "service": "Mechanic", "lat": 29.2833, "lon": 77.7167, "total_requests": 22, "providers": 1},
        {"area_name": "Indirapuram", "service": "AC Repair", "lat": 28.6469, "lon": 77.3672, "total_requests": 64, "providers": 1},
    ]

    ss.initialized = True

if "initialized" not in st.session_state:
    seed()

ss = st.session_state
ss.setdefault("current_user", None)
ss.setdefault("current_role", None)
ss.setdefault("nav", "Home")
ss.setdefault("customer_locations", {})

# ----------------------------------------------------------------------
# RAZORPAY REDIRECT CALLBACK — picks up ?payment_success=1&booking_id=...
# from the browser after Razorpay Checkout completes (see
# razorpay_checkout_widget()). Runs once per script execution.
# ----------------------------------------------------------------------
_qp = st.query_params
if _qp.get("payment_success") == "1" and "booking_id" in _qp:
    try:
        _bid = int(_qp["booking_id"])
    except (TypeError, ValueError):
        _bid = None
    if _bid is not None and not any(p["booking_id"] == _bid for p in ss.payments):
        _booking = next((b for b in ss.bookings if b["id"] == _bid), None)
        if _booking:
            ss.payments.append({
                "id": ss.next_payment_id, "booking_id": _bid, "customer_id": _booking["customer_id"],
                "amount": _booking["estimated_price"], "payment_method": "razorpay",
                "payment_status": "success",
                "transaction_id": _qp.get("payment_id", str(uuid.uuid4())[:10]),
                "paid_at": dt.datetime.now(),
            })
            ss.next_payment_id += 1
            ss.notifications.append({
                "id": str(uuid.uuid4())[:8], "user_id": _booking["customer_id"],
                "title": "Payment successful",
                "message": f"₹{_booking['estimated_price']} paid via Razorpay.",
                "notification_type": "payment", "is_read": False, "created_at": dt.datetime.now(),
            })
    st.query_params.clear()

# ----------------------------------------------------------------------
# HELPERS
# ----------------------------------------------------------------------
def category_name(cid):
    for c in ss.service_categories:
        if c["id"] == cid:
            return c["name"]
    return "Unknown"

def provider_by_id(pid):
    return ss.service_providers.get(pid)

def profile_by_id(uid):
    return ss.profiles.get(uid)

def add_notification(user_id, title, message, ntype="general"):
    ss.notifications.append({
        "id": str(uuid.uuid4())[:8], "user_id": user_id, "title": title,
        "message": message, "notification_type": ntype, "is_read": False,
        "created_at": dt.datetime.now(),
    })

def signup(full_name, phone, password, role, language="English"):
    uid = str(uuid.uuid4())[:8]
    ss.profiles[uid] = {"id": uid, "full_name": full_name, "phone": phone,
                         "role": role, "language": language, "password": password}
    if role == "provider":
        pid = ss.next_provider_id
        ss.next_provider_id += 1
        ss.service_providers[pid] = {
            "id": pid, "profile_id": uid, "business_name": full_name,
            "experience_years": 0, "description": "", "address": "",
            "latitude": 29.4727, "longitude": 77.7085, "service_radius_km": 10,
            "verification_status": "pending", "availability_status": "offline",
            "profile_photo_url": None,
        }
    add_notification(uid, "Welcome to VISHVAS 360", "Your account has been created successfully.", "welcome")
    return uid

def login(phone, password):
    for uid, p in ss.profiles.items():
        if p["phone"] == phone and p["password"] == password:
            return uid
    return None

def my_provider_record(profile_id):
    for pid, p in ss.service_providers.items():
        if p["profile_id"] == profile_id:
            return p
    return None

def simple_intent_extraction(text):
    """Very lightweight rule-based NLP standing in for the spaCy /
    Sentence-Transformers pipeline described in the project spec."""
    text_l = text.lower()
    service_keywords = {
        "Electrician": ["electric", "wiring", "switch", "fan", "short circuit", "bijli"],
        "Plumber": ["pipe", "leak", "tap", "plumb", "paani", "water leak"],
        "AC Repair": ["ac ", " ac", "cooling", "cooler", "gas refill", "airconditioner", "air conditioner"],
        "Carpenter": ["furniture", "door", "carpenter", "wood", "almirah"],
        "Painter": ["paint", "wall color", "whitewash"],
        "Appliance Repair": ["washing machine", "fridge", "refrigerator", "oven", "microwave", "kharab"],
        "Cleaning": ["clean", "safai", "deep cleaning"],
        "Mechanic": ["bike", "scooter", "car", "engine", "mechanic"],
    }
    detected_service = None
    for svc, kws in service_keywords.items():
        if any(k in text_l for k in kws):
            detected_service = svc
            break
    emergency_keywords = ["emergency", "urgent", "jaldi", "abhi", "asap", "immediately"]
    priority = "Emergency" if any(k in text_l for k in emergency_keywords) else "Normal"
    return {
        "service": detected_service or "Not detected — please choose manually",
        "problem": text.strip(),
        "priority": priority,
    }

def trust_score(provider_id):
    """Implements: 30% rating + 20% completed jobs + 15% repeat customers
    + 15% response rate + 10% (100 - cancellation rate) + 10% verified experience."""
    p = provider_by_id(provider_id)
    if not p:
        return 0
    completed = [b for b in ss.bookings if b["provider_id"] == provider_id and b["status"] == "completed"]
    cancelled = [b for b in ss.bookings if b["provider_id"] == provider_id and b["status"] == "cancelled"]
    total = [b for b in ss.bookings if b["provider_id"] == provider_id]
    prov_reviews = [r["rating"] for r in ss.reviews if r["provider_id"] == provider_id]
    avg_rating = (sum(prov_reviews) / len(prov_reviews)) if prov_reviews else 4.0

    customers = [b["customer_id"] for b in completed]
    repeat_pct = 0
    if customers:
        from collections import Counter
        counts = Counter(customers)
        repeats = sum(1 for c in counts.values() if c > 1)
        repeat_pct = (repeats / len(counts)) * 100

    cancellation_rate = (len(cancelled) / len(total) * 100) if total else 0
    response_rate = 96 if total else 90  # placeholder proxy signal
    verified_exp = min(p.get("experience_years", 0) / 5, 1) * 100
    completed_score = min(len(completed) / 150, 1) * 100

    score = (
        0.30 * (avg_rating / 5 * 100) +
        0.20 * completed_score +
        0.15 * repeat_pct +
        0.15 * response_rate +
        0.10 * (100 - cancellation_rate) +
        0.10 * verified_exp
    )
    return round(score, 1), {
        "verified": p["verification_status"] == "approved",
        "completed_jobs": len(completed),
        "avg_rating": round(avg_rating, 1),
        "repeat_pct": round(repeat_pct, 1),
        "cancellation_rate": round(cancellation_rate, 1),
        "response_rate": response_rate,
    }

def demand_level(total_requests):
    if total_requests >= 60:
        return "high"
    if total_requests >= 35:
        return "medium"
    return "low"

def haversine(lat1, lon1, lat2, lon2):
    """Great-circle distance in km between two lat/lon points."""
    if None in (lat1, lon1, lat2, lon2):
        return float("inf")
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))

def live_bookings_near(lat, lon, service_name, radius_km=10):
    """Counts real bookings placed in this demo session near a point,
    for a given service — feeds the AI expansion agent alongside the
    seeded historical demand_data."""
    count = 0
    for b in ss.bookings:
        if b.get("latitude") is None or b.get("longitude") is None:
            continue
        if category_name(b["service_id"]) != service_name:
            continue
        if b["status"] in ("cancelled", "rejected"):
            continue
        if haversine(lat, lon, b["latitude"], b["longitude"]) <= radius_km:
            count += 1
    return count

def expansion_recommendation(provider_id, radius_km=EXPANSION_RADIUS_KM):
    """AI business-expansion agent: scans demand areas within `radius_km`
    of the provider's own base location, blends seeded historical demand
    with live bookings placed in this session for the provider's own
    services, and recommends the area with the best requests-per-provider
    ratio — i.e. highest unmet demand."""
    p = provider_by_id(provider_id)
    my_services = {category_name(ps["service_id"]) for ps in ss.provider_services if ps["provider_id"] == provider_id}
    lat0, lon0 = p.get("latitude"), p.get("longitude")

    scored = []
    for d in ss.demand_data:
        if my_services and d["service"] not in my_services:
            continue
        dist = haversine(lat0, lon0, d["lat"], d["lon"])
        if dist > radius_km:
            continue
        live = live_bookings_near(d["lat"], d["lon"], d["service"])
        effective_requests = d["total_requests"] + live
        scored.append({**d, "distance_km": round(dist, 1), "live_bookings": live,
                        "effective_requests": effective_requests})

    if not scored:
        # Nothing in range matching the provider's own services — widen to
        # any service within radius so the agent still has a recommendation.
        for d in ss.demand_data:
            dist = haversine(lat0, lon0, d["lat"], d["lon"])
            if dist <= radius_km:
                live = live_bookings_near(d["lat"], d["lon"], d["service"])
                scored.append({**d, "distance_km": round(dist, 1), "live_bookings": live,
                                "effective_requests": d["total_requests"] + live})

    if not scored:
        # Still nothing (provider has no location set) — fall back to the
        # single highest raw-demand area nationwide.
        best = max(ss.demand_data, key=lambda d: d["total_requests"] / max(d["providers"], 1))
        return {**best, "distance_km": None, "live_bookings": 0, "effective_requests": best["total_requests"]}

    best = max(scored, key=lambda d: d["effective_requests"] / max(d["providers"], 1))
    return best

def image_to_vector(uploaded_file, size=(64, 64)):
    """Turns an uploaded/captured image into a flattened, normalized
    grayscale feature vector for the AI verification agent's cosine-
    similarity face/ID match. A lightweight stand-in for a production
    face-embedding model (e.g. InsightFace/FaceNet)."""
    if not PIL_AVAILABLE or uploaded_file is None:
        return None
    try:
        uploaded_file.seek(0)
        img = Image.open(uploaded_file).convert("L").resize(size)
        arr = np.asarray(img, dtype=np.float32).flatten()
        norm = np.linalg.norm(arr)
        return arr / norm if norm > 0 else arr
    except Exception:
        return None

def cosine_similarity(v1, v2):
    if v1 is None or v2 is None:
        return 0.0
    n = min(len(v1), len(v2))
    v1, v2 = v1[:n], v2[:n]
    denom = np.linalg.norm(v1) * np.linalg.norm(v2)
    if denom == 0:
        return 0.0
    return float(np.clip(np.dot(v1, v2) / denom, -1.0, 1.0))

def razorpay_checkout_widget(amount_rupees, description, booking_id, customer_name, customer_phone):
    """Embeds the real Razorpay Checkout.js widget. On successful payment
    it redirects the top-level browser tab back to this app with
    ?payment_success=1&booking_id=...&payment_id=..., which the callback
    near the top of this script picks up and records as a payment.
    Replace RAZORPAY_KEY_ID at the top of this file with your own
    test/live Key ID from the Razorpay dashboard."""
    amount_paise = int(round(amount_rupees * 100))
    safe_desc = description.replace('"', "'")
    safe_name = customer_name.replace('"', "'")
    component_html = f"""
    <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
    <script>
    function openRazorpay_{booking_id}() {{
        var options = {{
            "key": "{RAZORPAY_KEY_ID}",
            "amount": "{amount_paise}",
            "currency": "INR",
            "name": "VISHVAS 360",
            "description": "{safe_desc}",
            "prefill": {{ "name": "{safe_name}", "contact": "{customer_phone}" }},
            "theme": {{ "color": "#0FA3A3" }},
            "handler": function (response) {{
                var base = (window.top.location.href).split('?')[0];
                window.top.location.href = base + "?payment_success=1&booking_id={booking_id}&payment_id=" + response.razorpay_payment_id;
            }}
        }};
        var rzp = new Razorpay(options);
        rzp.open();
    }}
    </script>
    <button onclick="openRazorpay_{booking_id}()"
        style="background:#0FA3A3;color:white;border:none;padding:0.65rem 1.4rem;
        border-radius:8px;font-weight:600;font-size:0.95rem;cursor:pointer;">
        💳 Pay ₹{amount_rupees:,.0f} with Razorpay
    </button>
    """
    st_html(component_html, height=64)


# ----------------------------------------------------------------------
# UI — HOME / AUTH
# ----------------------------------------------------------------------
def render_home():
    st.markdown("""
    <div class="vh-hero">
        <h1>🛠️ VISHVAS 360</h1>
        <p>AI-Powered Trusted Local Service Marketplace — book verified electricians,
        plumbers, AC technicians and more in seconds, by text or voice, in your own language.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="vh-card">', unsafe_allow_html=True)
        st.subheader("👤 I'm a Customer")
        st.write("Find and book trusted local service providers near you.")
        if st.button("Continue as Customer", key="pick_customer", use_container_width=True):
            ss.portal = "customer"
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="vh-card">', unsafe_allow_html=True)
        st.subheader("🧰 I'm a Service Provider")
        st.write("Get bookings, grow your business, and build your trust score.")
        if st.button("Continue as Provider", key="pick_provider", use_container_width=True):
            ss.portal = "provider"
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="vh-card">', unsafe_allow_html=True)
        st.subheader("🛡️ Platform Admin")
        st.write("Manage verification, complaints and platform-wide analytics.")
        if st.button("Continue as Admin", key="pick_admin", use_container_width=True):
            ss.portal = "admin"
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    portal = ss.get("portal")
    if portal:
        role_label = {"customer": "Customer", "provider": "Service Provider", "admin": "Platform Admin"}[portal]
        st.subheader(f"{role_label} Access")
        tab_login, tab_signup = st.tabs(["Log In", "Sign Up"])

        with tab_login:
            with st.form("login_form"):
                phone = st.text_input("Phone number")
                pw = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Log In", use_container_width=True)
            if submitted:
                uid = login(phone, pw)
                if uid and ss.profiles[uid]["role"] == portal:
                    ss.current_user = uid
                    ss.current_role = ss.profiles[uid]["role"]
                    st.success(f"Welcome back, {ss.profiles[uid]['full_name']}!")
                    st.rerun()
                else:
                    st.error("Invalid credentials, or this account isn't registered for this portal.")
            st.caption("Demo logins — Customer: 9876500001 / pass123 · Provider: 9876500002 / pass123 · Admin: 9990000000 / admin123")

        with tab_signup:
            if portal == "admin":
                st.warning("⚠️ In production, admin sign-up should be invite-only / restricted to authorized "
                           "staff. This demo allows self-signup so you can explore the admin portal.")
            with st.form("signup_form"):
                full_name = st.text_input("Full name")
                phone_s = st.text_input("Phone number", key="signup_phone")
                pw_s = st.text_input("Password", type="password", key="signup_pw")
                lang = st.selectbox("Preferred language", ["English", "Hindi", "Hinglish"])
                submitted_s = st.form_submit_button("Create Account", use_container_width=True)
            if submitted_s:
                if not full_name or not phone_s or not pw_s:
                    st.error("Please fill in all fields.")
                elif any(p["phone"] == phone_s for p in ss.profiles.values()):
                    st.error("An account with this phone number already exists.")
                else:
                    uid = signup(full_name, phone_s, pw_s, portal, lang)
                    ss.current_user = uid
                    ss.current_role = portal
                    st.success("Account created!")
                    st.rerun()

# ----------------------------------------------------------------------
# UI — CUSTOMER PORTAL
# ----------------------------------------------------------------------
def render_customer():
    profile = profile_by_id(ss.current_user)
    lang = profile.get("language", "English")

    st.sidebar.title("🛠️ VISHVAS 360")
    st.sidebar.caption(f"{t('welcome', lang)}, {profile['full_name']}")
    lang_choice = st.sidebar.selectbox("🌐 Language / भाषा", ["English", "Hindi", "Hinglish"],
                                        index=["English", "Hindi", "Hinglish"].index(lang))
    if lang_choice != lang:
        ss.profiles[ss.current_user]["language"] = lang_choice
        st.rerun()

    page = st.sidebar.radio("Navigate", [
        "🤖 AI Chatbot Booking", "📋 Browse & Book", t("my_bookings", lang),
        "💳 Payments", "⭐ Reviews", "🔔 Notifications", "🚨 Report / Complaint",
        "📍 My Location",
    ])
    if st.sidebar.button("Log Out"):
        ss.current_user = None
        ss.current_role = None
        ss.portal = None
        st.rerun()

    if page == "🤖 AI Chatbot Booking":
        st.header("🤖 AI Chatbot — Natural-Language Service Discovery")
        st.write("Describe your problem by **text or voice**, in English, Hindi or Hinglish, and the AI agent "
                 "will identify the service, the problem and the priority for you.")

        input_mode = st.radio("Input method", ["⌨️ Type", "🎙️ Record voice"], horizontal=True)

        text = ""
        if input_mode == "⌨️ Type":
            text = st.text_area(t("chat_placeholder", lang), height=90, key="chat_text_input")
        else:
            st.caption("Tap record, describe your problem out loud, then stop — this feeds the same "
                       "Speech-to-Text → NLP/LLM pipeline as the project spec (Whisper / Web Speech API in "
                       "production).")
            audio_val = st.audio_input("🎙️ Record your problem", key="chat_audio_input")
            if audio_val is not None:
                st.audio(audio_val)
                ss.setdefault("chat_voice_transcript", "")
                ss.chat_voice_transcript = st.text_area(
                    "📝 Transcribed text (edit if the AI mis-heard anything)",
                    value=ss.chat_voice_transcript, height=80, key="chat_voice_transcript_box")
                text = ss.chat_voice_transcript

        c1, c2 = st.columns([1, 1])
        with c1:
            emergency_toggle = st.checkbox("🚨 This is an emergency")
        with c2:
            st.write("")

        if st.button("Analyze & Find Providers", type="primary"):
            if not text.strip():
                st.warning("Please describe your problem first (by typing or recording voice).")
            else:
                result = simple_intent_extraction(text)
                if emergency_toggle:
                    result["priority"] = "Emergency"
                st.markdown('<div class="vh-card">', unsafe_allow_html=True)
                st.markdown(f"**Service:** {result['service']}")
                st.markdown(f"**Problem:** {result['problem']}")
                badge_cls = "badge-danger" if result["priority"] == "Emergency" else "badge-info"
                st.markdown(f"**Priority:** <span class='vh-badge {badge_cls}'>{result['priority']}</span>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                ss.chat_intent = result
                st.info("Go to **Browse & Book** to see matching providers, pre-filtered on this service.")

    elif page == "📋 Browse & Book":
        st.header("📋 Browse Services & Book a Provider")
        cat_names = [c["name"] for c in ss.service_categories]
        default_idx = 0
        prefill = ss.get("chat_intent", {}).get("service")
        if prefill in cat_names:
            default_idx = cat_names.index(prefill)
        service_name = st.selectbox("Service category", cat_names, index=default_idx)
        service_id = next(c["id"] for c in ss.service_categories if c["name"] == service_name)

        matches = [ps for ps in ss.provider_services if ps["service_id"] == service_id]
        st.subheader(f"Providers offering {service_name}")
        if not matches:
            st.info("No providers listed yet for this service in the demo data.")
        for ps in matches:
            prov = provider_by_id(ps["provider_id"])
            if not prov:
                continue
            score = trust_score(prov["id"])[0] if ss.bookings or ss.reviews else 85.0
            st.markdown('<div class="vh-card">', unsafe_allow_html=True)
            cols = st.columns([3, 1, 1, 1])
            cols[0].markdown(f"**{prov['business_name']}**  \n{prov['address']}  \n"
                              f"Experience: {prov['experience_years']} yrs")
            v_badge = "badge-ok" if prov["verification_status"] == "approved" else "badge-warn"
            cols[1].markdown(f"<span class='vh-badge {v_badge}'>{prov['verification_status'].title()}</span>", unsafe_allow_html=True)
            cols[2].markdown(f"**Trust Score**<br><span class='metric-num' style='font-size:1.3rem'>{score}/100</span>", unsafe_allow_html=True)
            cols[3].markdown(f"**₹{ps['price']}**  \navailability: {prov['availability_status']}")
            with st.expander("Book this provider"):
                my_loc = ss.customer_locations.get(ss.current_user, {})
                default_desc = ss.get("chat_intent", {}).get("problem", "")

                st.markdown("**🎙️ Optional: describe the issue by voice instead of typing**")
                voice_key = f"book_audio_{prov['id']}_{service_id}"
                book_audio = st.audio_input("Record your issue", key=voice_key)
                if book_audio is not None:
                    st.audio(book_audio)
                    transcript_key = f"book_transcript_{prov['id']}_{service_id}"
                    ss.setdefault(transcript_key, default_desc)
                    ss[transcript_key] = st.text_input(
                        "📝 Transcribed text (edit if needed)", value=ss[transcript_key], key=f"tt_{voice_key}")
                    default_desc = ss[transcript_key]

                with st.form(f"book_{prov['id']}_{service_id}"):
                    b_date = st.date_input("Date", min_value=dt.date.today())
                    b_time = st.time_input("Time")
                    address = st.text_input("Your address", value=my_loc.get("address") or prov.get("address", ""))
                    desc = st.text_area("Describe the issue", value=default_desc)
                    is_emergency = st.checkbox("Emergency booking", value=(ss.get("chat_intent", {}).get("priority") == "Emergency"))
                    with st.expander("📍 Advanced: exact coordinates (used by heatmap & expansion AI)"):
                        c1, c2 = st.columns(2)
                        b_lat = c1.number_input("Latitude", value=float(my_loc.get("lat", prov.get("latitude", 29.4727))), format="%.4f")
                        b_lon = c2.number_input("Longitude", value=float(my_loc.get("lon", prov.get("longitude", 77.7085))), format="%.4f")
                    ok = st.form_submit_button("Confirm Booking", type="primary")
                if ok:
                    bid = ss.next_booking_id
                    ss.next_booking_id += 1
                    ss.bookings.append({
                        "id": bid, "customer_id": ss.current_user, "provider_id": prov["id"],
                        "service_id": service_id, "booking_date": b_date, "booking_time": b_time,
                        "address": address, "latitude": b_lat, "longitude": b_lon,
                        "description": desc, "status": "pending",
                        "is_emergency": is_emergency, "estimated_price": ps["price"],
                        "created_at": dt.datetime.now(),
                    })
                    add_notification(prov["profile_id"], "New booking request",
                                      f"{profile['full_name']} requested {service_name}.", "new_booking")
                    add_notification(ss.current_user, "Booking placed",
                                      f"Your {service_name} booking is pending provider confirmation.", "booking")
                    st.success("Booking placed! Track it under 'My Bookings'.")
            st.markdown('</div>', unsafe_allow_html=True)

    elif page == t("my_bookings", lang):
        st.header(f"📑 {t('my_bookings', lang)}")
        my_b = [b for b in ss.bookings if b["customer_id"] == ss.current_user]
        if not my_b:
            st.info("No bookings yet — go to 'Browse & Book' to get started.")
        for b in sorted(my_b, key=lambda x: x["created_at"], reverse=True):
            prov = provider_by_id(b["provider_id"])
            st.markdown('<div class="vh-card">', unsafe_allow_html=True)
            cols = st.columns([3, 1, 1])
            cols[0].markdown(f"**{category_name(b['service_id'])}** with {prov['business_name'] if prov else 'TBA'}  \n"
                              f"{b['booking_date']} at {b['booking_time']}  \n{b['description']}")
            status_map = {"pending": "badge-warn", "accepted": "badge-info", "on_the_way": "badge-info",
                          "in_progress": "badge-info", "completed": "badge-ok",
                          "rejected": "badge-danger", "cancelled": "badge-danger"}
            cols[1].markdown(f"<span class='vh-badge {status_map.get(b['status'],'badge-info')}'>{b['status'].replace('_',' ').title()}</span>", unsafe_allow_html=True)
            if b["status"] == "pending":
                if cols[2].button("Cancel", key=f"cancel_{b['id']}"):
                    b["status"] = "cancelled"
                    st.rerun()
            if b["status"] == "completed":
                already_reviewed = any(r["booking_id"] == b["id"] for r in ss.reviews)
                if not already_reviewed:
                    with st.expander("Leave a review"):
                        with st.form(f"review_{b['id']}"):
                            rating = st.slider("Rating", 1, 5, 5)
                            text = st.text_area("Comments")
                            sub = st.form_submit_button("Submit Review")
                        if sub:
                            ss.reviews.append({"booking_id": b["id"], "customer_id": ss.current_user,
                                                "provider_id": b["provider_id"], "rating": rating,
                                                "review_text": text, "created_at": dt.datetime.now()})
                            st.success("Thanks for your feedback!")
                            st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    elif page == "💳 Payments":
        st.header("💳 Payment Gateway — Razorpay")
        if RAZORPAY_KEY_ID.endswith("REPLACE_WITH_YOUR_KEY_ID"):
            st.warning("⚠️ Demo mode: set `RAZORPAY_KEY_ID` at the top of the file to your real Razorpay "
                      "test/live Key ID to accept real payments. The button below will still open the "
                      "Razorpay Checkout widget, but the transaction won't complete until a valid key is set.")
        payable = [b for b in ss.bookings if b["customer_id"] == ss.current_user
                   and b["status"] in ("accepted", "completed")
                   and not any(p["booking_id"] == b["id"] for p in ss.payments)]
        if not payable:
            st.info("No pending payments.")
        for b in payable:
            st.markdown('<div class="vh-card">', unsafe_allow_html=True)
            st.write(f"**{category_name(b['service_id'])}** — Amount due: ₹{b['estimated_price']}")
            razorpay_checkout_widget(b["estimated_price"], f"{category_name(b['service_id'])} service (Booking #{b['id']})",
                                      b["id"], profile["full_name"], profile["phone"])
            with st.expander("Other payment options (offline demo simulation)"):
                method = st.selectbox("Payment method", ["upi", "card", "netbanking", "wallet"], key=f"pm_{b['id']}")
                if st.button("Pay Now (Simulate)", key=f"pay_{b['id']}"):
                    ss.payments.append({
                        "id": ss.next_payment_id, "booking_id": b["id"], "customer_id": ss.current_user,
                        "amount": b["estimated_price"], "payment_method": method,
                        "payment_status": "success", "transaction_id": str(uuid.uuid4())[:10],
                        "paid_at": dt.datetime.now(),
                    })
                    ss.next_payment_id += 1
                    st.success("Payment successful (simulated).")
                    add_notification(ss.current_user, "Payment successful", f"₹{b['estimated_price']} paid via {method}.", "payment")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        st.subheader("Payment history")
        mine = [p for p in ss.payments if p["customer_id"] == ss.current_user]
        if mine:
            st.dataframe(pd.DataFrame(mine)[["id", "booking_id", "amount", "payment_method", "payment_status", "paid_at"]],
                         use_container_width=True, hide_index=True)

    elif page == "⭐ Reviews":
        st.header("⭐ My Reviews")
        mine = [r for r in ss.reviews if r["customer_id"] == ss.current_user]
        if not mine:
            st.info("You haven't left any reviews yet.")
        for r in mine:
            prov = provider_by_id(r["provider_id"])
            st.markdown('<div class="vh-card">', unsafe_allow_html=True)
            st.write(f"**{prov['business_name'] if prov else 'Provider'}** — {'⭐'*r['rating']}")
            st.write(r["review_text"])
            st.markdown('</div>', unsafe_allow_html=True)

    elif page == "🔔 Notifications":
        st.header("🔔 Notifications")
        mine = [n for n in ss.notifications if n["user_id"] == ss.current_user]
        for n in sorted(mine, key=lambda x: x["created_at"], reverse=True):
            st.markdown('<div class="vh-card">', unsafe_allow_html=True)
            st.write(f"**{n['title']}**  \n{n['message']}")
            st.caption(n["created_at"].strftime("%d %b %Y, %I:%M %p"))
            st.markdown('</div>', unsafe_allow_html=True)
        if not mine:
            st.info("No notifications yet.")

    elif page == "🚨 Report / Complaint":
        st.header("🚨 Raise a Complaint")
        my_b = [b for b in ss.bookings if b["customer_id"] == ss.current_user]
        with st.form("complaint_form"):
            booking_choice = st.selectbox("Related booking (optional)",
                                           ["None"] + [f"#{b['id']} — {category_name(b['service_id'])}" for b in my_b])
            subject = st.text_input("Subject")
            desc = st.text_area("Description")
            sub = st.form_submit_button("Submit Complaint")
        if sub:
            booking_id = None
            provider_id = None
            if booking_choice != "None":
                bid = int(booking_choice.split("#")[1].split(" ")[0])
                booking_id = bid
                b = next(x for x in my_b if x["id"] == bid)
                provider_id = b["provider_id"]
            ss.complaints.append({
                "id": ss.next_complaint_id, "booking_id": booking_id, "customer_id": ss.current_user,
                "provider_id": provider_id, "subject": subject, "description": desc,
                "status": "open", "created_at": dt.datetime.now(), "resolved_at": None,
            })
            ss.next_complaint_id += 1
            st.success("Complaint submitted. Our admin team will review it shortly.")

    elif page == "📍 My Location":
        st.header("📍 My Location")
        st.write("Set your default address so it can pre-fill your bookings and help match you to nearby "
                 "verified providers.")
        loc = ss.customer_locations.get(ss.current_user, {})
        preset_names = [a["area_name"] for a in AREA_PRESETS] + ["Custom / Other"]
        default_idx = preset_names.index(loc["area"]) if loc.get("area") in preset_names else len(preset_names) - 1
        area_choice = st.selectbox("Choose your area", preset_names, index=default_idx)
        if area_choice != "Custom / Other":
            preset = next(a for a in AREA_PRESETS if a["area_name"] == area_choice)
            lat_default, lon_default = preset["lat"], preset["lon"]
        else:
            lat_default, lon_default = loc.get("lat", 29.4727), loc.get("lon", 77.7085)

        address = st.text_input("Full address", value=loc.get("address", ""))
        c1, c2 = st.columns(2)
        lat = c1.number_input("Latitude", value=float(lat_default), format="%.4f", key="cust_lat")
        lon = c2.number_input("Longitude", value=float(lon_default), format="%.4f", key="cust_lon")
        if st.button("Save Location", type="primary"):
            ss.customer_locations[ss.current_user] = {"area": area_choice, "address": address, "lat": lat, "lon": lon}
            add_notification(ss.current_user, "Location saved", f"Your default address is set to {address or area_choice}.", "location")
            st.success("Location saved — it will now pre-fill your bookings.")
            st.rerun()

        saved_loc = ss.customer_locations.get(ss.current_user)
        if saved_loc:
            st.map(pd.DataFrame([{"latitude": saved_loc["lat"], "longitude": saved_loc["lon"]}]), size=25)
        else:
            st.info("No location saved yet.")

# ----------------------------------------------------------------------
# UI — PROVIDER PORTAL
# ----------------------------------------------------------------------
def render_provider():
    profile = profile_by_id(ss.current_user)
    prov = my_provider_record(ss.current_user)

    st.sidebar.title("🛠️ VISHVAS 360")
    st.sidebar.caption(f"Provider · {profile['full_name']}")
    page = st.sidebar.radio("Navigate", [
        "🏠 Overview", "🧾 Profile & Verification", "🧰 My Services & Pricing",
        "📥 Incoming Bookings", "⭐ Trust Score", "🗺️ Demand Heatmap",
        "🚀 Business Expansion", "📍 My Location", "🔔 Notifications",
    ])
    if st.sidebar.button("Log Out"):
        ss.current_user = None
        ss.current_role = None
        ss.portal = None
        st.rerun()

    if not prov:
        st.error("No provider profile found for this account.")
        return

    if page == "🏠 Overview":
        st.header(f"👋 Welcome, {prov['business_name']}")
        my_bookings = [b for b in ss.bookings if b["provider_id"] == prov["id"]]
        completed = [b for b in my_bookings if b["status"] == "completed"]
        pending = [b for b in my_bookings if b["status"] == "pending"]
        earnings = sum(p["amount"] for p in ss.payments if p["booking_id"] in [b["id"] for b in completed])
        c1, c2, c3, c4 = st.columns(4)
        for col, label, val in zip([c1, c2, c3, c4],
                                    ["Total Bookings", "Completed Jobs", "Pending Requests", "Earnings (₹)"],
                                    [len(my_bookings), len(completed), len(pending), f"{earnings:,.0f}"]):
            col.markdown(f"<div class='vh-card'><div class='metric-label'>{label}</div>"
                          f"<div class='metric-num'>{val}</div></div>", unsafe_allow_html=True)
        status_badge = "badge-ok" if prov["verification_status"] == "approved" else "badge-warn"
        st.markdown(f"Verification status: <span class='vh-badge {status_badge}'>{prov['verification_status'].title()}</span>",
                    unsafe_allow_html=True)
        avail = st.selectbox("Set your availability", ["available", "busy", "offline"],
                              index=["available", "busy", "offline"].index(prov["availability_status"]))
        if avail != prov["availability_status"]:
            prov["availability_status"] = avail
            st.success("Availability updated.")

    elif page == "🧾 Profile & Verification":
        st.header("🧾 Business Profile & Identity Verification")
        with st.form("provider_profile"):
            biz = st.text_input("Business name", value=prov["business_name"])
            exp = st.number_input("Years of experience", min_value=0, max_value=50, value=prov["experience_years"])
            desc = st.text_area("Description", value=prov["description"])
            saved = st.form_submit_button("Save Profile")
        if saved:
            prov.update({"business_name": biz, "experience_years": exp, "description": desc})
            st.success("Profile updated.")
        st.caption("📍 Set your business address & coordinates under **My Location** in the sidebar.")

        st.markdown("---")
        st.subheader("🪪 AI-Powered Identity & Photo Verification")
        st.caption("Pipeline: capture/upload selfie + government ID → **AI agent extracts a facial feature "
                   "vector from each image and computes cosine similarity** to confirm they're the same "
                   "person → auto-approve on a strong match, or flag for admin review. Raw ID numbers are "
                   "never stored, per UIDAI e-KYC guidance.")

        if not PIL_AVAILABLE:
            st.error("Pillow (PIL) isn't installed in this environment — add `Pillow` to requirements.txt "
                     "to enable the AI face-match agent.")

        st.markdown("**Step 1 — Your photo**")
        selfie_tab_cam, selfie_tab_up = st.tabs(["📷 Live Camera Capture", "📁 Upload Photo"])
        with selfie_tab_cam:
            selfie_camera = st.camera_input("Take a real-time selfie", key="selfie_cam")
        with selfie_tab_up:
            selfie_upload = st.file_uploader("Upload a selfie / profile photo", type=["png", "jpg", "jpeg"], key="selfie_up")
        selfie_file = selfie_camera or selfie_upload

        st.markdown("**Step 2 — Government ID**")
        id_tab_up, id_tab_cam = st.tabs(["📁 Upload Government ID", "📷 Capture ID with Camera"])
        with id_tab_up:
            id_upload = st.file_uploader("Upload a government-approved ID (front side)", type=["png", "jpg", "jpeg"], key="id_up")
        with id_tab_cam:
            id_camera = st.camera_input("Capture your ID with the camera", key="id_cam")
        id_file = id_upload or id_camera

        cert = st.file_uploader("Optional service certificate / work portfolio", type=["pdf", "png", "jpg", "jpeg"], key="cert_up")

        if st.button("🤖 Run AI Verification Agent", type="primary"):
            if not selfie_file or not id_file:
                st.warning("Please provide both a selfie photo and a government ID photo.")
            elif not PIL_AVAILABLE:
                st.error("Cannot run the AI agent — Pillow isn't available.")
            else:
                v1 = image_to_vector(selfie_file)
                v2 = image_to_vector(id_file)
                similarity = cosine_similarity(v1, v2)
                auto_verified = similarity >= FACE_MATCH_THRESHOLD
                status = "approved" if auto_verified else "pending"
                ss.verification.append({
                    "id": ss.next_verification_id, "provider_id": prov["id"],
                    "identity_document_url": getattr(id_file, "name", "id_capture.png"),
                    "profile_photo_url": getattr(selfie_file, "name", "selfie_capture.png"),
                    "similarity_score": round(similarity, 4),
                    "verification_status": status, "created_at": dt.datetime.now(),
                })
                ss.next_verification_id += 1
                prov["verification_status"] = status
                prov["similarity_score"] = round(similarity, 4)

                st.markdown('<div class="vh-card">', unsafe_allow_html=True)
                st.metric("Cosine similarity (selfie ↔ ID photo)", f"{similarity*100:.1f}%")
                st.progress(min(max(similarity, 0.0), 1.0))
                if auto_verified:
                    st.success(f"✅ AI agent matched selfie and ID with {similarity*100:.1f}% similarity "
                              f"(≥ {FACE_MATCH_THRESHOLD*100:.0f}% threshold) — profile **auto-verified**!")
                else:
                    st.warning(f"⚠️ Similarity score {similarity*100:.1f}% is below the "
                              f"{FACE_MATCH_THRESHOLD*100:.0f}% auto-verification threshold — your "
                              f"documents have been sent to an admin for manual review.")
                st.markdown('</div>', unsafe_allow_html=True)

    elif page == "🧰 My Services & Pricing":
        st.header("🧰 Services You Offer")
        offered_ids = {ps["service_id"] for ps in ss.provider_services if ps["provider_id"] == prov["id"]}
        for cat in ss.service_categories:
            existing = next((ps for ps in ss.provider_services if ps["provider_id"] == prov["id"] and ps["service_id"] == cat["id"]), None)
            cols = st.columns([2, 1, 1])
            cols[0].write(f"**{cat['name']}** — {cat['description']}")
            checked = cols[1].checkbox("Offer this", value=existing is not None, key=f"off_{cat['id']}")
            price = cols[2].number_input("Price (₹)", min_value=0, value=existing["price"] if existing else 0,
                                          key=f"price_{cat['id']}")
            if checked and not existing:
                ss.provider_services.append({"provider_id": prov["id"], "service_id": cat["id"], "price": price})
            elif checked and existing:
                existing["price"] = price
            elif not checked and existing:
                ss.provider_services.remove(existing)

    elif page == "📥 Incoming Bookings":
        st.header("📥 Incoming Bookings")
        my_bookings = [b for b in ss.bookings if b["provider_id"] == prov["id"]]
        if not my_bookings:
            st.info("No bookings yet.")
        next_status = {"pending": ("accepted", "rejected"), "accepted": ("on_the_way", None),
                       "on_the_way": ("in_progress", None), "in_progress": ("completed", None)}
        for b in sorted(my_bookings, key=lambda x: x["created_at"], reverse=True):
            cust = profile_by_id(b["customer_id"])
            st.markdown('<div class="vh-card">', unsafe_allow_html=True)
            emo = "🚨 " if b["is_emergency"] else ""
            st.markdown(f"{emo}**{category_name(b['service_id'])}** for {cust['full_name']}  \n"
                        f"{b['booking_date']} at {b['booking_time']} — {b['address']}  \n{b['description']}")
            st.markdown(f"Status: <span class='vh-badge badge-info'>{b['status'].replace('_',' ').title()}</span>", unsafe_allow_html=True)
            fwd, rej = next_status.get(b["status"], (None, None))
            c1, c2 = st.columns(2)
            if fwd:
                if c1.button(f"Mark as {fwd.replace('_',' ').title()}", key=f"fwd_{b['id']}"):
                    b["status"] = fwd
                    add_notification(b["customer_id"], "Booking update",
                                      f"Your booking is now '{fwd.replace('_',' ')}'.", "status_update")
                    st.rerun()
            if rej:
                if c2.button("Reject", key=f"rej_{b['id']}"):
                    b["status"] = rej
                    add_notification(b["customer_id"], "Booking rejected", "The provider is unavailable for this request.", "status_update")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    elif page == "⭐ Trust Score":
        st.header("⭐ Serviora Trust Score")
        score, details = trust_score(prov["id"])
        c1, c2 = st.columns([1, 2])
        c1.markdown(f"<div class='vh-card' style='text-align:center'><div class='metric-label'>Trust Score</div>"
                    f"<div class='metric-num' style='font-size:2.6rem'>{score}/100</div></div>", unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="vh-card">', unsafe_allow_html=True)
            st.write(f"✅ Verified identity: **{'Yes' if details['verified'] else 'Pending'}**")
            st.write(f"📦 Completed jobs: **{details['completed_jobs']}**")
            st.write(f"⭐ Customer rating: **{details['avg_rating']}/5**")
            st.write(f"🔁 Repeat customers: **{details['repeat_pct']}%**")
            st.write(f"📉 Cancellation rate: **{details['cancellation_rate']}%**")
            st.write(f"⚡ Response rate: **{details['response_rate']}%**")
            st.markdown('</div>', unsafe_allow_html=True)
        st.caption("Formula: 30% rating + 20% completed jobs + 15% repeat customers + "
                   "15% response rate + 10% (100 − cancellation rate) + 10% verified experience.")

    elif page == "🗺️ Demand Heatmap":
        st.header("🗺️ Service Demand Heatmap")
        df = pd.DataFrame(ss.demand_data)
        svc_filter = st.multiselect("Filter by service", sorted(df["service"].unique()), default=list(df["service"].unique()))
        df = df[df["service"].isin(svc_filter)]
        df["demand"] = df["total_requests"].apply(demand_level)
        color_map = {"high": [192, 57, 43], "medium": [185, 119, 14], "low": [30, 132, 73]}
        df["color"] = df["demand"].map(color_map)
        st.map(df.rename(columns={"lat": "latitude", "lon": "longitude"}), size=20, color="color")
        st.dataframe(df[["area_name", "service", "total_requests", "providers", "demand"]],
                     use_container_width=True, hide_index=True)
        st.caption("🔴 High demand · 🟠 Medium demand · 🟢 Low demand")

    elif page == "🚀 Business Expansion":
        st.header("🚀 AI Business Expansion Recommendation")
        if prov.get("latitude") is None:
            st.info("Set your base location under **📍 My Location** for a distance-aware recommendation.")
        st.caption(f"The AI agent scans demand areas within **{EXPANSION_RADIUS_KM} km** of your business "
                   f"location, combining historical demand data with bookings actually placed on the "
                   f"platform for your services, and recommends the area with the highest unmet demand "
                   f"(requests per active provider).")
        best = expansion_recommendation(prov["id"])
        st.markdown('<div class="vh-card">', unsafe_allow_html=True)
        st.subheader("📍 Expansion Opportunity Detected")
        cols = st.columns(2)
        cols[0].write(f"**Recommended area:** {best['area_name']}")
        cols[0].write(f"**Service in demand:** {best['service']}")
        cols[0].write(f"**Demand level:** {demand_level(best['total_requests']).title()}")
        dist_txt = f"{best['distance_km']} km" if best.get("distance_km") is not None else "N/A"
        cols[1].write(f"**Distance from you:** {dist_txt}")
        cols[1].write(f"**Current provider density:** {best['providers']}")
        cols[1].write(f"**Live bookings on platform (this area):** {best.get('live_bookings', 0)}")
        st.write(f"**Total effective requests:** {best['effective_requests']}")
        st.info(f"Expanding coverage to **{best['area_name']}** (within {EXPANSION_RADIUS_KM} km) may provide "
                f"higher booking opportunities, given only {best['providers']} active provider(s) against "
                f"{best['effective_requests']} requests for {best['service']}.")
        st.markdown('</div>', unsafe_allow_html=True)

    elif page == "📍 My Location":
        st.header("📍 My Business Location")
        st.write("This is the centre point the AI expansion agent measures the 100 km radius from, and "
                 "what customers see when browsing providers.")
        preset_names = [a["area_name"] for a in AREA_PRESETS] + ["Custom / Other"]
        area_choice = st.selectbox("Choose your base area", preset_names, index=len(preset_names) - 1, key="prov_area_choice")
        if area_choice != "Custom / Other":
            preset = next(a for a in AREA_PRESETS if a["area_name"] == area_choice)
            lat_default, lon_default = preset["lat"], preset["lon"]
        else:
            lat_default = prov.get("latitude", 29.4727)
            lon_default = prov.get("longitude", 77.7085)

        address = st.text_input("Business address", value=prov.get("address", ""))
        c1, c2 = st.columns(2)
        lat = c1.number_input("Latitude", value=float(lat_default), format="%.4f", key="prov_lat")
        lon = c2.number_input("Longitude", value=float(lon_default), format="%.4f", key="prov_lon")
        radius = st.slider("Service radius (km)", 1, 100, int(prov["service_radius_km"]))
        if st.button("Save Location", type="primary"):
            prov.update({"address": address, "latitude": lat, "longitude": lon, "service_radius_km": radius})
            st.success("Location updated.")
            st.rerun()
        st.map(pd.DataFrame([{"latitude": prov.get("latitude", lat), "longitude": prov.get("longitude", lon)}]), size=25)

    elif page == "🔔 Notifications":
        st.header("🔔 Notifications")
        mine = [n for n in ss.notifications if n["user_id"] == ss.current_user]
        for n in sorted(mine, key=lambda x: x["created_at"], reverse=True):
            st.markdown('<div class="vh-card">', unsafe_allow_html=True)
            st.write(f"**{n['title']}**  \n{n['message']}")
            st.caption(n["created_at"].strftime("%d %b %Y, %I:%M %p"))
            st.markdown('</div>', unsafe_allow_html=True)
        if not mine:
            st.info("No notifications yet.")

# ----------------------------------------------------------------------
# UI — ADMIN PORTAL
# ----------------------------------------------------------------------
def render_admin():
    profile = profile_by_id(ss.current_user)
    st.sidebar.title("🛠️ VISHVAS 360")
    st.sidebar.caption(f"Admin · {profile['full_name']}")
    page = st.sidebar.radio("Navigate", [
        "📊 Platform Overview", "👥 Users", "🧰 Providers & Verification",
        "📈 Services & Demand", "🚨 Complaints",
    ])
    if st.sidebar.button("Log Out"):
        ss.current_user = None
        ss.current_role = None
        ss.portal = None
        st.rerun()

    if page == "📊 Platform Overview":
        st.header("📊 Platform Overview")
        total_bookings = len(ss.bookings)
        total_revenue = sum(p["amount"] for p in ss.payments if p["payment_status"] == "success")
        emergency = len([b for b in ss.bookings if b["is_emergency"]])
        open_complaints = len([c for c in ss.complaints if c["status"] == "open"])
        cols = st.columns(4)
        for col, label, val in zip(cols, ["Total Bookings", "Revenue (₹)", "Emergency Requests", "Open Complaints"],
                                    [total_bookings, f"{total_revenue:,.0f}", emergency, open_complaints]):
            col.markdown(f"<div class='vh-card'><div class='metric-label'>{label}</div>"
                          f"<div class='metric-num'>{val}</div></div>", unsafe_allow_html=True)

        if ss.bookings:
            df = pd.DataFrame(ss.bookings)
            df["service"] = df["service_id"].apply(category_name)
            st.subheader("Growth trend — bookings per day")
            trend = df.groupby(df["created_at"].apply(lambda d: d.date())).size().reset_index(name="bookings")
            st.line_chart(trend, x="created_at", y="bookings")
            st.subheader("Bookings by status")
            st.bar_chart(df["status"].value_counts())
        else:
            st.info("No bookings yet — data will appear here as customers book services.")

    elif page == "👥 Users":
        st.header("👥 Users")
        rows = [{"ID": p["id"], "Name": p["full_name"], "Phone": p["phone"], "Role": p["role"],
                 "Language": p["language"]} for p in ss.profiles.values()]
        df = pd.DataFrame(rows)
        role_filter = st.multiselect("Filter by role", sorted(df["Role"].unique()), default=list(df["Role"].unique()))
        st.dataframe(df[df["Role"].isin(role_filter)], use_container_width=True, hide_index=True)

    elif page == "🧰 Providers & Verification":
        st.header("🧰 Providers & Verification")
        for pid, prov in ss.service_providers.items():
            profile_p = profile_by_id(prov["profile_id"])
            score = trust_score(pid)[0]
            st.markdown('<div class="vh-card">', unsafe_allow_html=True)
            cols = st.columns([3, 1, 1, 1])
            sim = prov.get("similarity_score")
            sim_txt = f" · AI face-match: **{sim*100:.1f}%**" if sim is not None else ""
            cols[0].markdown(f"**{prov['business_name']}**  \n{profile_p['full_name'] if profile_p else ''} · {prov['address']}{sim_txt}")
            v_badge = {"approved": "badge-ok", "pending": "badge-warn", "rejected": "badge-danger"}[prov["verification_status"]]
            cols[1].markdown(f"<span class='vh-badge {v_badge}'>{prov['verification_status'].title()}</span>", unsafe_allow_html=True)
            cols[2].markdown(f"Trust: **{score}/100**")
            if prov["verification_status"] == "pending":
                if cols[3].button("Approve", key=f"appr_{pid}"):
                    prov["verification_status"] = "approved"
                    add_notification(prov["profile_id"], "Verification approved", "Your account is now verified!", "verification")
                    st.rerun()
                if cols[3].button("Reject", key=f"rej_{pid}"):
                    prov["verification_status"] = "rejected"
                    add_notification(prov["profile_id"], "Verification rejected", "Please resubmit valid documents.", "verification")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    elif page == "📈 Services & Demand":
        st.header("📈 Services & Demand Heatmap")
        df = pd.DataFrame(ss.demand_data)
        df["demand"] = df["total_requests"].apply(demand_level)
        color_map = {"high": [192, 57, 43], "medium": [185, 119, 14], "low": [30, 132, 73]}
        df["color"] = df["demand"].map(color_map)
        st.map(df.rename(columns={"lat": "latitude", "lon": "longitude"}), size=20, color="color")
        st.dataframe(df[["area_name", "service", "total_requests", "providers", "demand"]],
                     use_container_width=True, hide_index=True)
        most_requested = df.loc[df["total_requests"].idxmax()]
        st.info(f"Most requested service right now: **{most_requested['service']}** in **{most_requested['area_name']}**.")

    elif page == "🚨 Complaints":
        st.header("🚨 Complaints")
        if not ss.complaints:
            st.info("No complaints filed.")
        for c in sorted(ss.complaints, key=lambda x: x["created_at"], reverse=True):
            cust = profile_by_id(c["customer_id"])
            st.markdown('<div class="vh-card">', unsafe_allow_html=True)
            st.write(f"**{c['subject']}** — filed by {cust['full_name'] if cust else 'Unknown'}")
            st.write(c["description"])
            status = st.selectbox("Status", ["open", "investigating", "resolved", "closed"],
                                   index=["open", "investigating", "resolved", "closed"].index(c["status"]),
                                   key=f"cstatus_{c['id']}")
            if status != c["status"]:
                c["status"] = status
                if status in ("resolved", "closed"):
                    c["resolved_at"] = dt.datetime.now()
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------------------------
# ROUTER
# ----------------------------------------------------------------------
if ss.current_user is None:
    render_home()
else:
    role = ss.current_role
    if role == "customer":
        render_customer()
    elif role == "provider":
        render_provider()
    elif role == "admin":
        render_admin()