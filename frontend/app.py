"""API-backed VISHVAS 360 Streamlit frontend.

This UI deliberately has no fake session-state database. Every read and write is
performed through FastAPI, which persists to Supabase.
"""
import datetime as dt
import streamlit as st
from api_client import APIError, get, post, patch

st.set_page_config(page_title="VISHVAS 360", page_icon="🛡️", layout="wide")
st.title("🛡️ VISHVAS 360")
st.caption("Trusted local services — connected to Supabase")

if "auth" not in st.session_state: st.session_state.auth = None

def logout(): st.session_state.auth = None; st.rerun()

def auth_screen():
    st.info("Use a Supabase-backed account. No demo data is stored in this UI.")
    login, signup = st.tabs(["Log in", "Create account"])
    with login:
        with st.form("login"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Log in")
        if submitted:
            try: st.session_state.auth = post("/auth/login", {"email": email, "password": password}); st.rerun()
            except APIError as exc: st.error(str(exc))
    with signup:
        with st.form("signup"):
            name = st.text_input("Full name")
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Password", type="password", key="signup_password")
            role = st.selectbox("Account type", ["customer", "provider"])
            language = st.selectbox("Language", ["English", "Hindi", "Hinglish"])
            submitted = st.form_submit_button("Create account")
        if submitted:
            try:
                st.session_state.auth = post("/auth/signup", {"email": email, "password": password, "full_name": name, "role": role, "language": language}); st.rerun()
            except APIError as exc: st.error(str(exc))

if not st.session_state.auth:
    auth_screen(); st.stop()

user = st.session_state.auth["profile"]
st.sidebar.write(f"**{user['full_name']}** · {user['role']}")
if st.sidebar.button("Log out"): logout()

try:
    services = get("/services").get("services", [])
except APIError as exc:
    st.error(str(exc)); st.stop()

if user["role"] == "customer":
    page = st.sidebar.radio("Navigate", ["Book a service", "My bookings", "AI assistant", "Notifications"])
    if page == "Book a service":
        st.header("Book a verified provider")
        category = st.selectbox("Service", services, format_func=lambda x: x["name"])
        providers = get("/providers", service_id=category["id"]).get("providers", [])
        if not providers: st.warning("No approved providers currently offer this service.")
        for provider in providers:
            with st.container(border=True):
                st.subheader(provider.get("business_name") or provider.get("full_name"))
                st.write(f"Trust score: **{provider['trust_score']}/100** · Rating: **{provider.get('rating') or 'New'}**")
                with st.form(f"book_{provider['id']}"):
                    day = st.date_input("Date", min_value=dt.date.today())
                    time = st.time_input("Time")
                    address = st.text_input("Address")
                    description = st.text_area("Describe the issue")
                    emergency = st.checkbox("Emergency service")
                    if st.form_submit_button("Confirm booking"):
                        try:
                            result = post("/bookings", {"customer_id": user["id"], "service_id": category["id"], "provider_id": provider["id"], "booking_date": str(day), "booking_time": str(time), "address": address, "description": description, "is_emergency": emergency})
                            st.success(f"Booking #{result['booking'].get('id')} saved to Supabase.")
                        except APIError as exc: st.error(str(exc))
    elif page == "My bookings":
        st.header("My bookings")
        rows = get("/bookings", customer_id=user["id"]).get("bookings", [])
        st.dataframe(rows, use_container_width=True, hide_index=True)
    elif page == "AI assistant":
        st.header("AI booking assistant")
        message = st.text_area("Describe your requirement")
        if st.button("Analyze") and message:
            try: st.json(post("/assistant", {"message": message, "user_id": user["id"]}))
            except APIError as exc: st.error(str(exc))
    else:
        st.header("Notifications")
        st.dataframe(get(f"/notifications/{user['id']}").get("notifications", []), use_container_width=True, hide_index=True)
else:
    page = st.sidebar.radio("Navigate", ["Incoming bookings", "Profile", "Services"])
    provider_rows = get("/providers", verified_only=False).get("providers", [])
    provider = next((p for p in provider_rows if p.get("profile_id") == user["id"]), None)
    if not provider: st.warning("Your provider profile is pending setup."); st.stop()
    if page == "Incoming bookings":
        st.header("Incoming bookings")
        rows = get("/bookings", provider_id=provider["id"]).get("bookings", [])
        for row in rows:
            st.write(f"Booking #{row['id']} · **{row['status']}** · {row['address']}")
            next_status = {"pending": "accepted", "accepted": "on_the_way", "on_the_way": "in_progress", "in_progress": "completed"}.get(row["status"])
            if next_status and st.button(f"Mark {next_status}", key=f"status_{row['id']}"):
                try: patch(f"/bookings/{row['id']}/status", {"status": next_status}); st.rerun()
                except APIError as exc: st.error(str(exc))
    elif page == "Profile": st.json(provider)
    else: st.dataframe(provider.get("services", []), use_container_width=True)
