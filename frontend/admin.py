"""VISHVAS 360 — Admin control tower."""
from __future__ import annotations

from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from core import (SERVICE_NAMES, demand_frame, inject_theme, kpi, notify, persist,
                  sidebar_common, trust_badge, trust_score)

ADMIN_PIN = "1234"


def render():
    inject_theme()
    if not st.session_state.get("admin_ok"):
        _login()
        return
    sidebar_common("Admin")
    st.markdown(
        "<div class='v-hero'><h1>🛡️ Admin Control Tower</h1>"
        "<p>Marketplace health, provider verification queue, demand intelligence, payouts "
        "and platform-wide broadcasts.</p>"
        "<span class='v-pill'>Live KPIs</span><span class='v-pill'>Verification Queue</span>"
        "<span class='v-pill'>Demand Heatmap</span><span class='v-pill'>Payout Ledger</span></div>",
        unsafe_allow_html=True)
    st.write("")
    tabs = st.tabs(["📊 Overview", "🧑‍🔧 Providers", "🗂️ Bookings", "🔥 Demand Intelligence",
                    "🛡️ Verification Queue", "💳 Revenue", "📢 Broadcast"])
    with tabs[0]:
        _overview()
    with tabs[1]:
        _providers()
    with tabs[2]:
        _bookings()
    with tabs[3]:
        _demand()
    with tabs[4]:
        _queue()
    with tabs[5]:
        _revenue()
    with tabs[6]:
        _broadcast()


def _login():
    st.markdown("<div class='v-hero'><h1>🛡️ Admin Access</h1>"
                "<p>Restricted area — enter the administrator PIN to continue.</p></div>",
                unsafe_allow_html=True)
    st.write("")
    c = st.columns([1, 1, 1])[1]
    with c:
        pin = st.text_input("Admin PIN", type="password", placeholder="Demo PIN: 1234")
        if st.button("Sign in", type="primary", use_container_width=True):
            if pin == ADMIN_PIN:
                st.session_state.admin_ok = True
                st.rerun()
            else:
                st.error("Invalid PIN.")
        if st.button("⬅ Back to home", use_container_width=True):
            st.session_state.role = None
            st.rerun()


def _overview():
    bk = pd.DataFrame(st.session_state.bookings)
    pv = pd.DataFrame(st.session_state.providers)
    pv["trust"] = [trust_score(p) for p in st.session_state.providers]
    a, b, c, d, e = st.columns(5)
    kpi(a, "Bookings", len(bk))
    kpi(b, "Providers", len(pv), f"{int(pv.kyc_verified.sum())} KYC verified")
    kpi(c, "GMV", f"₹{int(bk[bk.paid == True].amount.sum()):,}")
    kpi(d, "Avg trust", round(pv.trust.mean(), 1))
    kpi(e, "Emergency jobs", int(bk.emergency.sum()))
    st.write("")
    c1, c2 = st.columns(2)
    c1.plotly_chart(px.pie(bk, names="status", hole=.55, title="Booking status mix"),
                    use_container_width=True)
    c2.plotly_chart(px.bar(bk.groupby("service").size().reset_index(name="count"),
                           x="service", y="count", title="Demand by service category",
                           color_discrete_sequence=["#1d4ed8"]), use_container_width=True)
    bk2 = bk.copy()
    bk2["date"] = pd.to_datetime(bk2.created_at).dt.date
    st.plotly_chart(px.area(bk2.groupby("date").size().reset_index(name="bookings"),
                            x="date", y="bookings", title="Daily booking volume",
                            color_discrete_sequence=["#06b6d4"]), use_container_width=True)


def _providers():
    pv = pd.DataFrame(st.session_state.providers)
    pv["trust"] = [trust_score(p) for p in st.session_state.providers]
    pv["badge"] = [trust_badge(t)[0] for t in pv.trust]
    c1, c2, c3 = st.columns(3)
    svc = c1.multiselect("Service", SERVICE_NAMES, default=SERVICE_NAMES)
    city = c2.multiselect("City", pv.city.unique().tolist(), default=pv.city.unique().tolist())
    mintrust = c3.slider("Min trust score", 0, 100, 0)
    view = pv[pv.service.isin(svc) & pv.city.isin(city) & (pv.trust >= mintrust)]
    st.dataframe(view[["id", "name", "service", "city", "zone", "rating", "jobs_done",
                       "trust", "badge", "kyc_verified", "photo_verified", "status"]]
                 .sort_values("trust", ascending=False), hide_index=True, use_container_width=True)
    st.plotly_chart(px.histogram(view, x="trust", nbins=20, title="Trust score distribution",
                                 color_discrete_sequence=["#f59e0b"]), use_container_width=True)
    st.markdown("#### Moderation")
    c1, c2 = st.columns(2)
    pid = c1.selectbox("Provider", view.id.tolist() if not view.empty else [])
    action = c2.selectbox("Action", ["Activate", "Suspend", "Flag for review"])
    if st.button("Apply action", type="primary", disabled=view.empty):
        for p in st.session_state.providers:
            if p["id"] == pid:
                p["status"] = {"Activate": "Active", "Suspend": "Suspended",
                               "Flag for review": "Under Review"}[action]
                notify("Service Provider", "Account update",
                       f"Your account status is now {p['status']}.", "warning")
        persist()
        st.success(f"{pid} → {action}")


def _bookings():
    bk = pd.DataFrame(st.session_state.bookings)
    c1, c2 = st.columns(2)
    stat = c1.multiselect("Status", bk.status.unique().tolist(), default=bk.status.unique().tolist())
    only_emg = c2.toggle("Emergency only")
    view = bk[bk.status.isin(stat)]
    if only_emg:
        view = view[view.emergency]
    st.dataframe(view, hide_index=True, use_container_width=True)
    st.download_button("⬇ Export CSV", view.to_csv(index=False), "vishvas360_bookings.csv")


def _demand():
    df = demand_frame()
    if df.empty:
        st.info("No demand data.")
        return
    st.plotly_chart(px.density_heatmap(df, x="zone", y="service", z="demand", text_auto=True,
                                       color_continuous_scale="OrRd",
                                       title="Demand heatmap — locality × service"),
                    use_container_width=True)
    st.map(df.rename(columns={"lat": "latitude", "lon": "longitude"})[["latitude", "longitude"]],
           size=180, zoom=8)
    gaps = df.sort_values("gap", ascending=False).head(10)
    st.markdown("#### 🚀 Supply gaps — recruit providers here")
    st.dataframe(gaps[["city", "zone", "service", "demand", "supply", "gap", "revenue"]],
                 hide_index=True, use_container_width=True)
    for r in gaps.head(4).itertuples():
        st.info(f"**{r.service} in {r.zone}, {r.city}** — {int(r.demand)} requests against "
                f"{int(r.supply)} providers. Onboard ~{max(int(r.gap // 3), 1)} more to cut ETA.")


def _queue():
    pending = [p for p in st.session_state.providers
               if not (p["kyc_verified"] and p["photo_verified"] and p["police_verified"])]
    st.markdown(f"#### {len(pending)} providers pending verification")
    for p in pending[:15]:
        with st.expander(f"{p['name']} · {p['service']} · {p['zone']}, {p['city']} "
                         f"· trust {trust_score(p)}"):
            c1, c2, c3 = st.columns(3)
            c1.write(f"KYC: {'✅' if p['kyc_verified'] else '⚠️ pending'}")
            c2.write(f"Photo: {'✅' if p['photo_verified'] else '⚠️ pending'}")
            c3.write(f"Police: {'✅' if p['police_verified'] else '⚠️ pending'}")
            a, b = st.columns(2)
            if a.button("Approve all", key=f"ap{p['id']}"):
                p.update(kyc_verified=True, photo_verified=True, police_verified=True)
                notify("Service Provider", "Verification approved",
                       f"{p['name']} is now fully verified.", "success")
                persist(); st.rerun()
            if b.button("Reject", key=f"rj{p['id']}"):
                p["status"] = "Under Review"
                persist(); st.rerun()


def _revenue():
    bk = pd.DataFrame(st.session_state.bookings)
    paid = bk[bk.paid == True]
    gmv = paid.amount.sum()
    a, b, c, d = st.columns(4)
    kpi(a, "GMV", f"₹{int(gmv):,}")
    kpi(b, "Platform revenue (2%)", f"₹{int(gmv * 0.02):,}")
    kpi(c, "Provider payouts", f"₹{int(gmv * 0.98):,}")
    kpi(d, "Avg order value", f"₹{int(paid.amount.mean()) if len(paid) else 0:,}")
    st.write("")
    c1, c2 = st.columns(2)
    c1.plotly_chart(px.bar(paid.groupby("payment_mode").amount.sum().reset_index(),
                           x="payment_mode", y="amount", title="Revenue by payment mode",
                           color_discrete_sequence=["#16a34a"]), use_container_width=True)
    c2.plotly_chart(px.bar(paid.groupby("city").amount.sum().reset_index(),
                           x="city", y="amount", title="Revenue by city",
                           color_discrete_sequence=["#1d4ed8"]), use_container_width=True)


def _broadcast():
    st.markdown("#### 📢 Real-time notification broadcast")
    c1, c2 = st.columns(2)
    audience = c1.selectbox("Audience", ["All", "Customer", "Service Provider"])
    kind = c2.selectbox("Type", ["info", "success", "warning"])
    title = st.text_input("Title", "Monsoon surge — extra jobs available")
    body = st.text_area("Message", "Demand for plumbing and electrical work is up 40% this week.")
    if st.button("Send broadcast", type="primary"):
        notify(audience, title, body, kind)
        st.success(f"Broadcast delivered to {audience}.")
    st.divider()
    if st.session_state.notifications:
        st.dataframe(pd.DataFrame(st.session_state.notifications), hide_index=True,
                     use_container_width=True)
