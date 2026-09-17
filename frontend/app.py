"""
VISHVAS 360 — AI-Powered Trusted Local Service Marketplace
Home page with three role portals: Customer, Service Provider, Admin.

Run:  streamlit run app.py
"""
from __future__ import annotations

import streamlit as st

st.set_page_config(page_title="VISHVAS 360 — Trusted Local Services",
                   page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

from core import SERVICES, bootstrap, inject_theme, kpi, trust_score  # noqa: E402
import admin as admin_portal  # noqa: E402
import customer as customer_portal  # noqa: E402
import service_provider as provider_portal  # noqa: E402

bootstrap()
st.session_state.setdefault("role", None)

CARDS = [
    ("Service Provider", "🧑‍🔧", "#1d4ed8",
     "Grow your business with AI-driven jobs, trust scoring and expansion insights.",
     ["Live job requests & emergency dispatch", "Trust & reputation score with AI coaching",
      "Photo + KYC verification", "Service demand heatmap agent",
      "Business expansion recommendations", "Earnings & instant payouts"]),
    ("Customer", "👤", "#06b6d4",
     "Book verified local professionals by chat or voice — in your own language.",
     ["AI chatbot booking assistant", "Voice-based booking", "Multilingual interface",
      "🚨 Emergency service mode", "Secure payment gateway",
      "Reminders & real-time notifications"]),
    ("Admin", "🛡️", "#f59e0b",
     "Full marketplace control tower with analytics, moderation and payouts.",
     ["Live marketplace KPIs", "Provider verification queue", "Demand intelligence & supply gaps",
      "Booking and dispute oversight", "Revenue & payout ledger", "Broadcast notifications"]),
]


def home():
    inject_theme()
    st.markdown(
        "<div class='v-hero'><h1>🛡️ VISHVAS&nbsp;360</h1>"
        "<p>An AI-powered trusted local service marketplace — connecting customers with verified "
        "professionals through intelligent matching, text &amp; voice booking, multilingual support, "
        "emergency dispatch, secure payments and real-time notifications.</p>"
        "<span class='v-pill'>AI Chatbot</span><span class='v-pill'>Voice Booking</span>"
        "<span class='v-pill'>Multilingual</span><span class='v-pill'>Emergency Mode</span>"
        "<span class='v-pill'>Trust Score</span><span class='v-pill'>Demand Heatmap</span>"
        "<span class='v-pill'>Payments</span><span class='v-pill'>Photo Verification</span></div>",
        unsafe_allow_html=True)
    st.write("")

    providers = st.session_state.providers
    bookings = st.session_state.bookings
    a, b, c, d = st.columns(4)
    kpi(a, "Verified professionals", len(providers), "across 3 cities")
    kpi(b, "Services offered", len(SERVICES), "electrical to mechanical")
    kpi(c, "Jobs delivered", sum(1 for x in bookings if x["status"] == "Completed"))
    kpi(d, "Avg trust score",
        round(sum(trust_score(p) for p in providers) / max(len(providers), 1), 1), "out of 100")
    st.write("")
    st.markdown("### Choose your portal")

    cols = st.columns(3, gap="large")
    for col, (name, icon, color, tagline, feats) in zip(cols, CARDS):
        with col:
            items = "".join(f"<li>{f}</li>" for f in feats)
            st.markdown(
                f"""<div class='v-card'>
                <div class='v-icon'>{icon}</div>
                <h3>{name}</h3>
                <span class='v-tag' style='background:{color}1a;color:{color}'>Portal</span>
                <p style='color:#475569;font-size:.92rem;margin:.6rem 0 .2rem'>{tagline}</p>
                <ul>{items}</ul></div>""", unsafe_allow_html=True)
            st.write("")
            if st.button(f"Enter {name} Portal  →", key=f"go{name}",
                         use_container_width=True, type="primary"):
                st.session_state.role = name
                st.rerun()

    st.write("")
    st.markdown("### Services on the platform")
    cols = st.columns(8)
    for col, (s, ic) in zip(cols, SERVICES):
        col.markdown(f"<div class='v-kpi' style='text-align:center'><div style='font-size:1.7rem'>{ic}</div>"
                     f"<div style='font-size:.82rem;font-weight:600;color:#0f172a'>{s}</div></div>",
                     unsafe_allow_html=True)
    st.write("")
    st.caption("VISHVAS 360 · Trust-first local services · Demo build with simulated data.")


role = st.session_state.role
if role == "Customer":
    customer_portal.render()
elif role == "Service Provider":
    provider_portal.render()
elif role == "Admin":
    admin_portal.render()
else:
    home()
