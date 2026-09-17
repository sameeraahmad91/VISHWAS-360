"""VISHVAS 360 — Customer portal."""
from __future__ import annotations

from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st

from core import (CITY_ZONES, SERVICE_ICON, SERVICE_NAMES, add_reminder, ai_reply,
                  detect_service, inject_theme, is_urgent, kpi, match_providers, new_id,
                  notify, persist, process_payment, provider_card, sidebar_common, t,
                  trust_badge, trust_score)


def render():
    inject_theme()
    sidebar_common("Customer")
    st.markdown(
        "<div class='v-hero'><h1>👤 Customer Portal</h1>"
        "<p>Book verified local professionals by chat or voice, in your language — with "
        "emergency dispatch, secure payments and live updates.</p>"
        "<span class='v-pill'>AI Chatbot</span><span class='v-pill'>Voice Booking</span>"
        "<span class='v-pill'>Multilingual</span><span class='v-pill'>Emergency Mode</span>"
        "<span class='v-pill'>Secure Payments</span></div>", unsafe_allow_html=True)
    st.write("")

    with st.sidebar:
        st.divider()
        st.markdown("#### 📍 Your location")
        city = st.selectbox("City", list(CITY_ZONES))
        zone_name = st.selectbox("Locality", [z[0] for z in CITY_ZONES[city]])
        zone = next(z for z in CITY_ZONES[city] if z[0] == zone_name)
        st.session_state.cust_city, st.session_state.cust_zone = city, zone
        st.session_state.emergency = st.toggle(
            f"🚨 {t('emergency')}", value=st.session_state.get("emergency", False),
            help="Dispatch the nearest available professional at 1.6× priority rate.")

    if st.session_state.emergency:
        st.markdown("<div class='v-emg'>🚨 EMERGENCY MODE ACTIVE — only emergency-ready, "
                    "trust-verified professionals are shown. Priority surge 1.6× applies.</div>",
                    unsafe_allow_html=True)

    tabs = st.tabs([f"🤖 {t('assistant')}", "🎙️ Voice Booking", f"🛠️ {t('book')}",
                    f"📒 {t('my_bookings')}", "💳 Payments", "⏰ Reminders"])

    with tabs[0]:
        _chatbot(city, zone)
    with tabs[1]:
        _voice(city, zone)
    with tabs[2]:
        _catalog(city, zone)
    with tabs[3]:
        _bookings()
    with tabs[4]:
        _payments()
    with tabs[5]:
        _reminders()


# ---------------------------------------------------------------- AI chatbot
def _chatbot(city, zone):
    st.subheader(f"🤖 {t('assistant')}")
    st.caption("Describe the problem naturally — the assistant detects the service, urgency "
               "and shortlists trusted professionals.")
    if not st.session_state.chat:
        st.session_state.chat = [{"role": "assistant",
                                  "text": f"Namaste! 🙏 {t('describe')} — e.g. *'Kitchen tap is "
                                          "leaking badly'* or *'AC not cooling since morning'*.",
                                  "matches": []}]
    for turn in st.session_state.chat:
        with st.chat_message("user" if turn["role"] == "user" else "assistant"):
            st.markdown(turn["text"])
            for m in turn.get("matches", [])[:3]:
                provider_card(m)

    prompt = st.chat_input(t("describe"))
    if prompt:
        st.session_state.chat.append({"role": "user", "text": prompt, "matches": []})
        reply = ai_reply(prompt, city, zone[1], zone[2])
        if reply["urgent"]:
            st.session_state.emergency = True
        st.session_state.chat.append(reply)
        st.session_state.last_service = reply["service"]
        st.rerun()

    if len(st.session_state.chat) > 1 and st.session_state.chat[-1].get("matches"):
        st.divider()
        best = st.session_state.chat[-1]["matches"][0]
        st.success(f"Top match: **{best['name']}** · trust {best['trust']} · ETA {best['eta_min']} min")
        if st.button("⚡ Book the top match now", type="primary"):
            _create_booking(best, st.session_state.chat[-1]["service"], city, zone,
                            "AI Chatbot", st.session_state.emergency)


# -------------------------------------------------------------- Voice booking
def _voice(city, zone):
    st.subheader("🎙️ Voice-Based Booking")
    st.caption("Speak your request. The audio is transcribed, intent is detected, and a "
               "professional is matched automatically.")
    c1, c2 = st.columns([1, 1])
    with c1:
        try:
            audio = st.audio_input("Record your request")
        except Exception:
            audio = st.file_uploader("Upload a voice note (wav/mp3/m4a)", type=["wav", "mp3", "m4a"])
        if audio:
            st.audio(audio)
            st.info("🎧 Audio captured. Connect Whisper / Google STT in `transcribe()` for "
                    "production transcription.")
    with c2:
        transcript = st.text_area(
            "Transcript (auto-filled by speech-to-text; editable)",
            placeholder="e.g. Mere ghar ka geyser kaam nahi kar raha, urgent chahiye",
            height=120)
        if st.button("🧠 Understand & match", type="primary", disabled=not transcript):
            service, conf = detect_service(transcript)
            urgent = is_urgent(transcript) or st.session_state.emergency
            st.session_state.voice_result = {
                "service": service, "confidence": conf, "urgent": urgent,
                "matches": match_providers(service, city, zone[1], zone[2], urgent,
                                           st.session_state.language)}

    res = st.session_state.get("voice_result")
    if res:
        st.divider()
        a, b, c = st.columns(3)
        kpi(a, "Detected service", f"{SERVICE_ICON[res['service']]} {res['service']}")
        kpi(b, "Intent confidence", f"{int(res['confidence'] * 100)}%")
        kpi(c, "Urgency", "🚨 Emergency" if res["urgent"] else "Standard")
        st.write("")
        for m in res["matches"][:4]:
            provider_card(m)
            if st.button(f"Book {m['name']}", key=f"v{m['id']}"):
                _create_booking(m, res["service"], city, zone, "Voice", res["urgent"])


# ------------------------------------------------------------------- Catalog
def _catalog(city, zone):
    st.subheader(f"🛠️ {t('book')}")
    cols = st.columns(4)
    for i, s in enumerate(SERVICE_NAMES):
        if cols[i % 4].button(f"{SERVICE_ICON[s]}  {s}", use_container_width=True, key=f"sv{s}"):
            st.session_state.sel_service = s
    service = st.session_state.get("sel_service", SERVICE_NAMES[0])
    st.write("")
    c1, c2, c3 = st.columns(3)
    service = c1.selectbox("Service", SERVICE_NAMES, index=SERVICE_NAMES.index(service))
    when = c2.selectbox("When", ["Within 1 hour", "Today", "Tomorrow", "Pick a slot"])
    slot = c3.time_input("Preferred time") if when == "Pick a slot" else None
    notes = st.text_input("Describe the issue (optional)")

    matches = match_providers(service, city, zone[1], zone[2],
                              st.session_state.emergency, st.session_state.language, top=6)
    st.markdown(f"**{len(matches)} verified professionals matched** — ranked by trust score, "
                "distance, price and language fit.")
    for m in matches:
        provider_card(m)
        cc1, cc2 = st.columns([1, 5])
        if cc1.button("Book", key=f"b{m['id']}", type="primary"):
            _create_booking(m, service, city, zone, "Catalog", st.session_state.emergency, notes)
        with cc2.expander("Trust score breakdown"):
            from core import trust_breakdown
            st.dataframe(trust_breakdown(m), hide_index=True, use_container_width=True)


def _create_booking(p, service, city, zone, channel, emergency, notes=""):
    bk = {
        "id": new_id("BK"), "customer": st.session_state.get("cust_name", "You"),
        "service": service, "provider_id": p["id"], "provider": p["name"],
        "city": city, "zone": zone[0], "lat": zone[1], "lon": zone[2],
        "status": "Requested", "emergency": bool(emergency),
        "amount": p["base_price"], "paid": False, "payment_mode": "-",
        "rating": None, "notes": notes, "channel": channel,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "scheduled_at": (datetime.now() + timedelta(minutes=p.get("eta_min", 45))).strftime("%Y-%m-%d %H:%M"),
        "photo_before": False, "photo_after": False,
    }
    st.session_state.bookings.insert(0, bk)
    notify("Customer", "Booking requested",
           f"{p['name']} ({service}) will arrive by {bk['scheduled_at']}.", "success")
    notify("Service Provider", "🚨 New emergency job" if emergency else "New job request",
           f"{service} in {zone[0]}, {city} — ₹{p['base_price']}.", "warning")
    notify("Admin", "Booking created", f"{bk['id']} · {service} · {zone[0]}")
    add_reminder(bk["id"], (datetime.now() + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M"),
                 "WhatsApp", f"Your {service} professional arrives soon.")
    persist()
    st.success(f"✅ Booking {bk['id']} confirmed with {p['name']}. Live tracking is on.")
    st.balloons()


# ------------------------------------------------------------------ Bookings
def _bookings():
    st.subheader(f"📒 {t('my_bookings')}")
    df = pd.DataFrame(st.session_state.bookings)
    if df.empty:
        st.info("No bookings yet.")
        return
    a, b, c, d = st.columns(4)
    kpi(a, "Total bookings", len(df))
    kpi(b, "Completed", int((df.status == "Completed").sum()))
    kpi(c, "Active", int(df.status.isin(["Requested", "In Progress"]).sum()))
    kpi(d, "Spend", f"₹{int(df[df.paid == True].amount.sum()):,}")
    st.write("")
    status = st.multiselect("Filter status", df.status.unique().tolist(),
                            default=df.status.unique().tolist())
    view = df[df.status.isin(status)]
    st.dataframe(view[["id", "service", "provider", "zone", "status", "emergency",
                       "amount", "paid", "scheduled_at"]],
                 hide_index=True, use_container_width=True)

    st.markdown("#### ⭐ Rate a completed job")
    done = view[view.status == "Completed"]["id"].tolist()
    if done:
        bid = st.selectbox("Booking", done)
        stars = st.slider("Rating", 1.0, 5.0, 5.0, 0.5)
        review = st.text_input("Review")
        if st.button("Submit review"):
            for bk in st.session_state.bookings:
                if bk["id"] == bid:
                    bk["rating"] = stars
                    bk["review"] = review
            notify("Service Provider", "New review", f"{stars}★ on {bid}: {review}", "success")
            persist()
            st.success("Review submitted — it feeds directly into the provider trust score.")


# ------------------------------------------------------------------ Payments
def _payments():
    st.subheader("💳 Secure Payment Gateway")
    unpaid = [b for b in st.session_state.bookings if not b["paid"] and b["status"] != "Cancelled"]
    if not unpaid:
        st.success("All settled — no pending payments.")
    else:
        opts = {f"{b['id']} · {b['service']} · ₹{b['amount']}": b for b in unpaid}
        pick = st.selectbox("Pending payment", list(opts))
        bk = opts[pick]
        mode = st.radio("Payment method", ["UPI", "Card", "Net Banking", "Wallet", "Cash on completion"],
                        horizontal=True)
        rec = process_payment(bk["amount"], mode, bk.get("emergency"))
        c1, c2, c3 = st.columns(3)
        kpi(c1, "Service charge", f"₹{bk['amount']}")
        kpi(c2, "Emergency surge", "1.6×" if bk.get("emergency") else "None")
        kpi(c3, "Payable", f"₹{rec['gross']:,.0f}")
        if st.button(f"🔒 {t('pay')}", type="primary"):
            bk["paid"] = True
            bk["payment_mode"] = mode
            bk["txn"] = rec["txn_id"]
            bk["amount"] = rec["gross"]
            notify("Customer", "Payment successful",
                   f"₹{rec['gross']:,.0f} paid via {mode}. Txn {rec['txn_id']}.", "success")
            notify("Service Provider", "Payout scheduled",
                   f"₹{rec['provider_payout']:,.0f} for {bk['id']} (T+1).", "success")
            persist()
            st.success(f"Payment successful · Txn {rec['txn_id']} · escrow released on completion.")

    st.divider()
    df = pd.DataFrame([b for b in st.session_state.bookings if b["paid"]])
    if not df.empty:
        fig = px.bar(df.groupby("payment_mode").amount.sum().reset_index(),
                     x="payment_mode", y="amount", title="Your spend by payment method",
                     color_discrete_sequence=["#1d4ed8"])
        st.plotly_chart(fig, use_container_width=True)


# ----------------------------------------------------------------- Reminders
def _reminders():
    st.subheader("⏰ Reminders & Real-time Notifications")
    c1, c2, c3 = st.columns(3)
    ids = [b["id"] for b in st.session_state.bookings][:40]
    bid = c1.selectbox("Booking", ids) if ids else None
    channel = c2.selectbox("Channel", ["WhatsApp", "SMS", "Push", "Email", "Voice call"])
    when = c3.text_input("Send at", (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M"))
    text = st.text_input("Message", "Reminder: your service visit is scheduled soon.")
    if st.button("Schedule reminder", type="primary", disabled=not bid):
        add_reminder(bid, when, channel, text)
        notify("Customer", "Reminder scheduled", f"{channel} at {when}")
        st.success("Reminder scheduled.")
    st.write("")
    if st.session_state.reminders:
        st.dataframe(pd.DataFrame(st.session_state.reminders), hide_index=True,
                     use_container_width=True)
    else:
        st.caption("No reminders scheduled yet.")
