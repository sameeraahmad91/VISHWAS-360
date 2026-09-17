"""
VISHVAS 360 — AI-Powered Trusted Local Service Marketplace.
Run with: streamlit run app.py
"""
from __future__ import annotations

import streamlit as st

import core as core_module
from api_client import pull_state, push_state
from core import SERVICES, bootstrap, inject_theme, kpi, trust_score
import admin as admin_portal
import customer as customer_portal
import service_provider as provider_portal

st.set_page_config(page_title="VISHVAS 360 — Trusted Local Services", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

# Pull once before bootstrap so a hosted API snapshot becomes the app's local working set.
remote_state = pull_state()
if remote_state:
    for name in ("providers", "bookings", "notifications", "reminders"):
        if name in remote_state:
            core_module.save(name, remote_state[name])

bootstrap()
st.session_state.setdefault("role", None)

# All existing portals call core.persist (some imported the symbol directly), so wrap
# both references and retain the offline JSON fallback when VISHWAS_API_URL is unset.
_local_persist = core_module.persist

def persist_with_backend():
    _local_persist()
    push_state({name: st.session_state.get(name, []) for name in ("providers", "bookings", "notifications", "reminders")})

core_module.persist = persist_with_backend
customer_portal.persist = persist_with_backend
provider_portal.persist = persist_with_backend
admin_portal.persist = persist_with_backend

CARDS = [
    ("Service Provider", "🧑‍🔧", "#1d4ed8", "Grow your business with AI-driven jobs, trust scoring and expansion insights.", ["Live job requests & emergency dispatch", "Trust & reputation score with AI coaching", "Photo + KYC verification", "Service demand heatmap agent", "Business expansion recommendations", "Earnings & instant payouts"]),
    ("Customer", "👤", "#06b6d4", "Book verified local professionals by chat or voice — in your own language.", ["AI chatbot booking assistant", "Voice-based booking", "Multilingual interface", "🚨 Emergency service mode", "Secure payment gateway", "Reminders & real-time notifications"]),
    ("Admin", "🛡️", "#f59e0b", "Full marketplace control tower with analytics, moderation and payouts.", ["Live marketplace KPIs", "Provider verification queue", "Demand intelligence & supply gaps", "Booking and dispute oversight", "Revenue & payout ledger", "Broadcast notifications"]),
]


def home():
    inject_theme()
    st.markdown("<div class='v-hero'><h1>🛡️ VISHVAS&nbsp;360</h1><p>An AI-powered trusted local service marketplace — connecting customers with verified professionals through intelligent matching, text &amp; voice booking, multilingual support, emergency dispatch, secure payments and real-time notifications.</p><span class='v-pill'>AI Chatbot</span><span class='v-pill'>Voice Booking</span><span class='v-pill'>Multilingual</span><span class='v-pill'>Emergency Mode</span><span class='v-pill'>Trust Score</span><span class='v-pill'>Demand Heatmap</span><span class='v-pill'>Payments</span><span class='v-pill'>Photo Verification</span></div>", unsafe_allow_html=True)
    st.write("")
    providers, bookings = st.session_state.providers, st.session_state.bookings
    a, b, c, d = st.columns(4)
    kpi(a, "Verified professionals", len(providers), "across 3 cities")
    kpi(b, "Services offered", len(SERVICES), "electrical to mechanical")
    kpi(c, "Jobs delivered", sum(1 for x in bookings if x["status"] == "Completed"))
    kpi(d, "Avg trust score", round(sum(trust_score(p) for p in providers) / max(len(providers), 1), 1), "out of 100")
    st.write("")
    st.markdown("### Choose your portal")
    cols = st.columns(3, gap="large")
    for col, (name, icon, color, tagline, feats) in zip(cols, CARDS):
        with col:
            items = "".join(f"<li>{f}</li>" for f in feats)
            st.markdown(f"<div class='v-card'><div class='v-icon'>{icon}</div><h3>{name}</h3><span class='v-tag' style='background:{color}1a;color:{color}'>Portal</span><p style='color:#475569;font-size:.92rem;margin:.6rem 0 .2rem'>{tagline}</p><ul>{items}</ul></div>", unsafe_allow_html=True)
            st.write("")
            if st.button(f"Enter {name} Portal  →", key=f"go{name}", use_container_width=True, type="primary"):
                st.session_state.role = name
                st.rerun()
    st.write("")
    st.markdown("### Services on the platform")
    cols = st.columns(8)
    for col, (service, icon) in zip(cols, SERVICES):
        col.markdown(f"<div class='v-kpi' style='text-align:center'><div style='font-size:1.7rem'>{icon}</div><div style='font-size:.82rem;font-weight:600;color:#0f172a'>{service}</div></div>", unsafe_allow_html=True)
    st.caption("VISHVAS 360 · Trust-first local services · API-connected demo when VISHWAS_API_URL is configured.")


role = st.session_state.role
if role == "Customer":
    customer_portal.render()
elif role == "Service Provider":
    provider_portal.render()
elif role == "Admin":
    admin_portal.render()
else:
    home()
