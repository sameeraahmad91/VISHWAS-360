"""Customer portal with AI chatbot and voice-booking gateway integration."""
from __future__ import annotations

from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st

from api_client import transcribe as api_transcribe, understand as api_understand
from core import (CITY_ZONES, SERVICE_ICON, SERVICE_NAMES, add_reminder, ai_reply,
                  detect_service, inject_theme, is_urgent, kpi, match_providers, new_id,
                  notify, persist, process_payment, provider_card, sidebar_common, t,
                  trust_badge, trust_score)


def _understand(text: str, city: str, zone: tuple, channel: str):
    remote = api_understand(text, channel=channel)
    if remote and remote.get("service"):
        service = remote["service"]
        urgent = bool(remote.get("urgent"))
        confidence = float(remote.get("confidence", 0.75))
        reply = remote.get("reply", f"I identified a {service} request.")
        return {"role": "assistant", "text": reply, "service": service, "urgent": urgent,
                "confidence": confidence,
                "matches": match_providers(service, city, zone[1], zone[2], urgent,
                                            st.session_state.get("language"))}
    result = ai_reply(text, city, zone[1], zone[2])
    result["confidence"] = result.get("confidence", 0.75)
    return result


def render():
    inject_theme(); sidebar_common("Customer")
    st.markdown("<div class='v-hero'><h1>👤 Customer Portal</h1><p>Book verified local professionals by chat or voice, in your language — with emergency dispatch, secure payments and live updates.</p><span class='v-pill'>AI Chatbot</span><span class='v-pill'>Voice Booking</span><span class='v-pill'>Multilingual</span><span class='v-pill'>Emergency Mode</span><span class='v-pill'>Secure Payments</span></div>", unsafe_allow_html=True)
    with st.sidebar:
        st.divider(); st.markdown("#### 📍 Your location")
        city = st.selectbox("City", list(CITY_ZONES))
        zone_name = st.selectbox("Locality", [z[0] for z in CITY_ZONES[city]])
        zone = next(z for z in CITY_ZONES[city] if z[0] == zone_name)
        st.session_state.cust_city, st.session_state.cust_zone = city, zone
        st.session_state.emergency = st.toggle(f"🚨 {t('emergency')}", value=st.session_state.get("emergency", False))
    if st.session_state.emergency:
        st.markdown("<div class='v-emg'>🚨 EMERGENCY MODE ACTIVE — only emergency-ready, trust-verified professionals are shown. Priority surge 1.6× applies.</div>", unsafe_allow_html=True)
    tabs = st.tabs([f"🤖 {t('assistant')}", "🎙️ Voice Booking", f"🛠️ {t('book')}", f"📒 {t('my_bookings')}", "💳 Payments", "⏰ Reminders"])
    with tabs[0]: _chatbot(city, zone)
    with tabs[1]: _voice(city, zone)
    with tabs[2]: _catalog(city, zone)
    with tabs[3]: _bookings()
    with tabs[4]: _payments()
    with tabs[5]: _reminders()


def _chatbot(city, zone):
    st.subheader(f"🤖 {t('assistant')}")
    st.caption("Requests are sent to FastAPI's AI gateway when configured, with the local multilingual matcher as a safe fallback.")
    if not st.session_state.chat:
        st.session_state.chat = [{"role": "assistant", "text": f"Namaste! 🙏 {t('describe')} — e.g. *Kitchen tap is leaking badly* or *AC not cooling since morning*.", "matches": []}]
    for turn in st.session_state.chat:
        with st.chat_message("user" if turn["role"] == "user" else "assistant"):
            st.markdown(turn["text"])
            for match in turn.get("matches", [])[:3]: provider_card(match)
    prompt = st.chat_input(t("describe"))
    if prompt:
        st.session_state.chat.append({"role": "user", "text": prompt, "matches": []})
        reply = _understand(prompt, city, zone, "chat")
        if reply["urgent"]: st.session_state.emergency = True
        st.session_state.chat.append(reply); st.session_state.last_service = reply["service"]
        st.rerun()
    if len(st.session_state.chat) > 1 and st.session_state.chat[-1].get("matches"):
        best = st.session_state.chat[-1]["matches"][0]
        if st.button("⚡ Book the top match now", type="primary"):
            _create_booking(best, st.session_state.chat[-1]["service"], city, zone, "AI Chatbot", st.session_state.emergency)


def _voice(city, zone):
    st.subheader("🎙️ Voice-Based AI Booking")
    st.caption("Record a request, transcribe it through the optional Whisper backend, then send the transcript through the same AI intent and matching pipeline.")
    c1, c2 = st.columns([1, 1])
    with c1:
        try: audio = st.audio_input("Record your request")
        except Exception: audio = st.file_uploader("Upload a voice note", type=["wav", "mp3", "m4a", "webm"])
        if audio:
            st.audio(audio)
            if st.button("🎧 Transcribe with Whisper", key="voice_transcribe"):
                transcript = api_transcribe(audio, st.session_state.get("language"))
                if transcript:
                    st.session_state.voice_transcript = transcript
                    st.success("Voice transcribed by the backend AI service.")
                else:
                    st.warning("Whisper is unavailable. Enter or edit the transcript manually.")
    with c2:
        transcript = st.text_area("Transcript (editable)", value=st.session_state.get("voice_transcript", ""), key="voice_transcript_editor", placeholder="e.g. Mere ghar ka geyser kaam nahi kar raha, urgent chahiye", height=120)
        if st.button("🧠 Understand voice request", type="primary", disabled=not transcript):
            result = _understand(transcript, city, zone, "voice")
            result["urgent"] = result["urgent"] or st.session_state.emergency
            st.session_state.voice_result = result
    result = st.session_state.get("voice_result")
    if result:
        st.divider(); a, b, c = st.columns(3)
        kpi(a, "Detected service", f"{SERVICE_ICON[result['service']]} {result['service']}")
        kpi(b, "Intent confidence", f"{int(result.get('confidence', .75) * 100)}%")
        kpi(c, "Urgency", "🚨 Emergency" if result["urgent"] else "Standard")
        for match in result.get("matches", [])[:4]:
            provider_card(match)
            if st.button(f"Book {match['name']}", key=f"voice-book-{match['id']}"):
                _create_booking(match, result["service"], city, zone, "Voice AI", result["urgent"])


def _catalog(city, zone):
    st.subheader(f"🛠️ {t('book')}")
    cols = st.columns(4)
    for i, service_name in enumerate(SERVICE_NAMES):
        if cols[i % 4].button(f"{SERVICE_ICON[service_name]}  {service_name}", use_container_width=True, key=f"sv{service_name}"): st.session_state.sel_service = service_name
    service = st.session_state.get("sel_service", SERVICE_NAMES[0])
    c1, c2, c3 = st.columns(3)
    service = c1.selectbox("Service", SERVICE_NAMES, index=SERVICE_NAMES.index(service))
    when = c2.selectbox("When", ["Within 1 hour", "Today", "Tomorrow", "Pick a slot"])
    if when == "Pick a slot": c3.time_input("Preferred time")
    notes = st.text_input("Describe the issue (optional)")
    matches = match_providers(service, city, zone[1], zone[2], st.session_state.emergency, st.session_state.language, top=6)
    st.markdown(f"**{len(matches)} verified professionals matched** — ranked by trust, distance, price and language fit.")
    for match in matches:
        provider_card(match); cc1, cc2 = st.columns([1, 5])
        if cc1.button("Book", key=f"b{match['id']}", type="primary"): _create_booking(match, service, city, zone, "Catalog", st.session_state.emergency, notes)
        with cc2.expander("Trust score breakdown"):
            from core import trust_breakdown
            st.dataframe(trust_breakdown(match), hide_index=True, use_container_width=True)


def _create_booking(p, service, city, zone, channel, emergency, notes=""):
    now = datetime.now()
    booking = {"id": new_id("BK"), "customer": st.session_state.get("cust_name", "You"), "service": service, "provider_id": p["id"], "provider": p["name"], "city": city, "zone": zone[0], "lat": zone[1], "lon": zone[2], "status": "Requested", "emergency": bool(emergency), "amount": p["base_price"], "paid": False, "payment_mode": "-", "rating": None, "notes": notes, "channel": channel, "created_at": now.strftime("%Y-%m-%d %H:%M"), "scheduled_at": (now + timedelta(minutes=p.get("eta_min", 45))).strftime("%Y-%m-%d %H:%M"), "photo_before": False, "photo_after": False}
    st.session_state.bookings.insert(0, booking)
    notify("Customer", "Booking requested", f"{p['name']} ({service}) will arrive by {booking['scheduled_at']}.", "success")
    notify("Service Provider", "🚨 New emergency job" if emergency else "New job request", f"{service} in {zone[0]}, {city} — ₹{p['base_price']}.", "warning")
    notify("Admin", "Booking created", f"{booking['id']} · {service} · {zone[0]}")
    add_reminder(booking["id"], (now + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M"), "WhatsApp", f"Your {service} professional arrives soon.")
    persist(); st.success(f"✅ Booking {booking['id']} confirmed with {p['name']}. The analytics heatmap has been updated."); st.balloons()


def _bookings():
    st.subheader(f"📒 {t('my_bookings')}"); df = pd.DataFrame(st.session_state.bookings)
    if df.empty: st.info("No bookings yet."); return
    a, b, c, d = st.columns(4); kpi(a, "Total bookings", len(df)); kpi(b, "Completed", int((df.status == "Completed").sum())); kpi(c, "Active", int(df.status.isin(["Requested", "In Progress"]).sum())); kpi(d, "Spend", f"₹{int(df[df.paid == True].amount.sum()):,}")
    status = st.multiselect("Filter status", df.status.unique().tolist(), default=df.status.unique().tolist()); view = df[df.status.isin(status)]
    st.dataframe(view[["id", "service", "provider", "zone", "status", "emergency", "amount", "paid", "scheduled_at"]], hide_index=True, use_container_width=True)


def _payments():
    st.subheader("💳 Secure Payment Gateway"); unpaid = [b for b in st.session_state.bookings if not b["paid"] and b["status"] != "Cancelled"]
    if not unpaid: st.success("All settled — no pending payments."); return
    opts = {f"{b['id']} · {b['service']} · ₹{b['amount']}": b for b in unpaid}; bk = opts[st.selectbox("Pending payment", list(opts))]; mode = st.radio("Payment method", ["UPI", "Card", "Net Banking", "Wallet", "Cash on completion"], horizontal=True); rec = process_payment(bk["amount"], mode, bk.get("emergency"))
    kpi(st.columns(3)[0], "Service charge", f"₹{bk['amount']}"); kpi(st.columns(3)[1], "Emergency surge", "1.6×" if bk.get("emergency") else "None"); kpi(st.columns(3)[2], "Payable", f"₹{rec['gross']:,.0f}")
    if st.button(f"🔒 {t('pay')}", type="primary"):
        bk.update(paid=True, payment_mode=mode, txn=rec["txn_id"], amount=rec["gross"]); notify("Customer", "Payment successful", f"₹{rec['gross']:,.0f} paid via {mode}. Txn {rec['txn_id']}.", "success"); notify("Service Provider", "Payout scheduled", f"₹{rec['provider_payout']:,.0f} for {bk['id']} (T+1).", "success"); persist(); st.success(f"Payment successful · Txn {rec['txn_id']}")


def _reminders():
    st.subheader("⏰ Reminders & Real-time Notifications"); ids = [b["id"] for b in st.session_state.bookings][:40]; bid = st.selectbox("Booking", ids) if ids else None; channel = st.selectbox("Channel", ["WhatsApp", "SMS", "Push", "Email", "Voice call"]); when = st.text_input("Send at", (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")); text = st.text_input("Message", "Reminder: your service visit is scheduled soon.")
    if st.button("Schedule reminder", type="primary", disabled=not bid): add_reminder(bid, when, channel, text); notify("Customer", "Reminder scheduled", f"{channel} at {when}"); st.success("Reminder scheduled.")
    if st.session_state.reminders: st.dataframe(pd.DataFrame(st.session_state.reminders), hide_index=True, use_container_width=True)
