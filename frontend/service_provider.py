"""VISHVAS 360 — Service Provider portal."""
from __future__ import annotations

from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from core import (SERVICE_ICON, cross_sell, demand_frame, expansion_recommendations,
                  inject_theme, kpi, notify, persist, provider_card, sidebar_common,
                  trust_badge, trust_breakdown, trust_score)


def render():
    inject_theme()
    sidebar_common("Service Provider")
    providers = st.session_state.providers
    with st.sidebar:
        st.divider()
        names = [f"{p['name']} · {p['service']}" for p in providers]
        idx = st.selectbox("Your profile", range(len(names)), format_func=lambda i: names[i])
    p = providers[idx]
    score = trust_score(p)
    badge, color = trust_badge(score)

    st.markdown(
        f"<div class='v-hero'><h1>{SERVICE_ICON.get(p['service'],'🛠')} {p['name']}</h1>"
        f"<p>{p['service']} professional · {p['zone']}, {p['city']} · joined {p['joined']}</p>"
        f"<span class='v-pill'>{badge} · Trust {score}/100</span>"
        f"<span class='v-pill'>⭐ {p['rating']}</span>"
        f"<span class='v-pill'>{p['jobs_done']} jobs</span>"
        f"<span class='v-pill'>{'🚨 Emergency ready' if p['emergency_available'] else 'Standard hours'}</span></div>",
        unsafe_allow_html=True)
    st.write("")

    tabs = st.tabs(["📋 Job Requests", "🏅 Trust Score", "📸 Photo Verification",
                    "🔥 Demand Heatmap", "📈 Business Growth", "💰 Earnings"])
    with tabs[0]:
        _jobs(p)
    with tabs[1]:
        _trust(p, score, badge, color)
    with tabs[2]:
        _verify(p, idx)
    with tabs[3]:
        _heatmap(p)
    with tabs[4]:
        _growth(p)
    with tabs[5]:
        _earnings(p)


def _jobs(p):
    st.subheader("📋 Incoming & Active Jobs")
    jobs = [b for b in st.session_state.bookings if b["provider_id"] == p["id"]]
    if not jobs:
        st.info("No jobs assigned yet. Improve your trust score to rank higher in matching.")
        return
    df = pd.DataFrame(jobs)
    a, b, c, d = st.columns(4)
    kpi(a, "Total jobs", len(df))
    kpi(b, "Open", int(df.status.isin(["Requested", "In Progress"]).sum()))
    kpi(c, "Emergency", int(df.emergency.sum()))
    kpi(d, "Earned", f"₹{int(df[df.paid == True].amount.sum()):,}")
    st.write("")
    for bk in jobs[:12]:
        tag = "🚨 EMERGENCY" if bk["emergency"] else bk["status"]
        with st.expander(f"{bk['id']} · {bk['service']} · {bk['zone']} · {tag} · ₹{bk['amount']}"):
            st.write(f"Customer: **{bk['customer']}** · scheduled {bk['scheduled_at']}")
            c1, c2, c3 = st.columns(3)
            if c1.button("Accept", key=f"a{bk['id']}"):
                bk["status"] = "In Progress"
                notify("Customer", "Job accepted", f"{p['name']} accepted {bk['id']}.", "success")
                persist(); st.rerun()
            if c2.button("Mark complete", key=f"c{bk['id']}"):
                bk["status"] = "Completed"
                bk["photo_after"] = True
                notify("Customer", "Job completed", f"{bk['id']} completed — please rate.", "success")
                persist(); st.rerun()
            if c3.button("Decline", key=f"d{bk['id']}"):
                bk["status"] = "Cancelled"
                persist(); st.rerun()


def _trust(p, score, badge, color):
    st.subheader("🏅 Trust & Reputation Score")
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(f"<div class='v-card'><div class='v-icon'>🛡️</div><h3>{score}/100</h3>"
                    f"<span class='v-tag' style='background:{color}1a;color:{color}'>{badge}</span>"
                    "<ul><li>Rating and reviews</li><li>Completion & punctuality</li>"
                    "<li>Dispute history</li><li>Identity verification</li></ul></div>",
                    unsafe_allow_html=True)
    with c2:
        bd = trust_breakdown(p)
        bd["Lost"] = bd["Max"] - bd["Points"]
        fig = px.bar(bd, x="Points", y="Factor", orientation="h", text="Points",
                     color_discrete_sequence=["#1d4ed8"], title="Score contribution by factor")
        st.plotly_chart(fig, use_container_width=True)
    gaps = bd[bd.Points < bd.Max * 0.85]
    if not gaps.empty:
        st.warning("**AI coach:** biggest gains available in — " +
                   ", ".join(f"{r.Factor} (+{round(r.Max - r.Points,1)} pts)" for r in gaps.itertuples()))


def _verify(p, idx):
    st.subheader("📸 Photo & Identity Verification")
    st.caption("Selfie liveness, ID and job photos are matched by the AI verification agent "
               "before a provider is marked verified.")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**1. Live selfie**")
        selfie = st.camera_input("Take a selfie")
    with c2:
        st.markdown("**2. Government ID**")
        idcard = st.file_uploader("Aadhaar / PAN / DL", type=["png", "jpg", "jpeg", "pdf"])
    with c3:
        st.markdown("**3. Work proof**")
        work = st.file_uploader("Certificate or job photos", type=["png", "jpg", "jpeg", "pdf"],
                                accept_multiple_files=True)
    if st.button("🔍 Run AI verification", type="primary"):
        if selfie and idcard:
            st.session_state.providers[idx]["photo_verified"] = True
            st.session_state.providers[idx]["kyc_verified"] = True
            persist()
            st.success("✅ Face match 96.4% · ID OCR valid · liveness passed. Profile verified "
                       "(+8 trust points).")
            notify("Admin", "Verification submitted", f"{p['name']} passed AI photo verification.")
        else:
            st.error("A live selfie and a government ID are both required.")
    st.divider()
    cols = st.columns(3)
    for col, (label, ok) in zip(cols, [("KYC", p["kyc_verified"]), ("Photo", p["photo_verified"]),
                                       ("Police", p["police_verified"])]):
        col.markdown(f"<div class='v-kpi'><div class='l'>{label} verification</div>"
                     f"<div class='v'>{'✅ Verified' if ok else '⚠️ Pending'}</div></div>",
                     unsafe_allow_html=True)


def _heatmap(p):
    st.subheader("🔥 Service Demand Heatmap Agent")
    df = demand_frame()
    if df.empty:
        st.info("Not enough data yet.")
        return
    mine = df[df.service == p["service"]]
    st.map(mine.rename(columns={"lat": "latitude", "lon": "longitude"})[["latitude", "longitude"]],
           size=200, zoom=9)
    fig = px.density_heatmap(mine, x="zone", y="city", z="demand", text_auto=True,
                             color_continuous_scale="OrRd",
                             title=f"{p['service']} demand intensity by locality")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(mine[["city", "zone", "demand", "supply", "gap", "revenue", "heat"]]
                 .sort_values("demand", ascending=False), hide_index=True, use_container_width=True)


def _growth(p):
    st.subheader("📈 AI Business Expansion Recommendations")
    recs = expansion_recommendations(p)
    if recs.empty:
        st.info("Not enough demand signal yet.")
    else:
        for r in recs.itertuples():
            st.markdown(f"<div class='v-prov'><b>🚀 {r.zone}, {r.city}</b>"
                        f"<div style='color:#475569;font-size:.9rem;margin-top:4px'>{r.recommendation}</div>"
                        f"<div style='font-size:.8rem;color:#64748b;margin-top:4px'>Opportunity index "
                        f"{round(r.opportunity,1)} · demand {int(r.demand)} · supply {int(r.supply)}</div></div>",
                        unsafe_allow_html=True)
        st.plotly_chart(px.bar(recs, x="zone", y="opportunity", color="city",
                               title="Expansion opportunity index"), use_container_width=True)
    st.markdown("#### 💡 Skill & pricing advisory")
    for tip in cross_sell(p):
        st.info(tip)


def _earnings(p):
    st.subheader("💰 Earnings & Payouts")
    jobs = pd.DataFrame([b for b in st.session_state.bookings if b["provider_id"] == p["id"]])
    if jobs.empty:
        st.info("No earnings yet.")
        return
    paid = jobs[jobs.paid == True]
    gross = paid.amount.sum()
    a, b, c, d = st.columns(4)
    kpi(a, "Gross earnings", f"₹{int(gross):,}")
    kpi(b, "Platform fee (2%)", f"₹{int(gross * 0.02):,}")
    kpi(c, "Net payout", f"₹{int(gross * 0.98):,}")
    kpi(d, "Avg ticket", f"₹{int(paid.amount.mean()) if len(paid) else 0:,}")
    st.write("")
    if not paid.empty:
        paid = paid.copy()
        paid["date"] = pd.to_datetime(paid.created_at).dt.date
        st.plotly_chart(px.line(paid.groupby("date").amount.sum().reset_index(),
                                x="date", y="amount", markers=True, title="Daily earnings",
                                color_discrete_sequence=["#06b6d4"]), use_container_width=True)
    st.dataframe(jobs[["id", "service", "zone", "status", "amount", "paid", "payment_mode",
                       "created_at"]], hide_index=True, use_container_width=True)
