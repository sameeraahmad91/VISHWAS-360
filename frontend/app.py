# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.express as px
# from datetime import datetime, timedelta
# import random

# # ============================================================
# # PAGE CONFIGURATION
# # ============================================================

# st.set_page_config(
#     page_title="VISHVAS 360",
#     page_icon="🛠️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ============================================================
# # CUSTOM CSS
# # ============================================================

# st.markdown("""
# <style>

# @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

# * {
#     font-family: 'Inter', sans-serif;
# }

# .main {
#     background-color: #f8fafc;
# }

# .block-container {
#     padding-top: 1.5rem;
#     padding-bottom: 2rem;
#     max-width: 1400px;
# }

# /* Sidebar */

# [data-testid="stSidebar"] {
#     background: linear-gradient(180deg, #0f172a 0%, #1e3a5f 100%);
# }

# [data-testid="stSidebar"] * {
#     color: white !important;
# }

# /* Hero */

# .hero {
#     background: linear-gradient(135deg, #dbeafe 0%, #eff6ff 50%, #ffffff 100%);
#     padding: 35px;
#     border-radius: 20px;
#     margin-bottom: 25px;
#     border: 1px solid #bfdbfe;
# }

# .hero-heading {
#     font-size: 42px;
#     font-weight: 800;
#     color: #0f172a;
#     letter-spacing: -1px;
# }

# .hero-subheading {
#     font-size: 20px;
#     font-weight: 600;
#     color: #2563eb;
#     margin-top: 8px;
# }

# .hero-text {
#     font-size: 16px;
#     color: #475569;
#     margin-top: 12px;
#     line-height: 1.7;
# }

# /* Cards */

# .service-card {
#     background: white;
#     padding: 20px;
#     border-radius: 15px;
#     border: 1px solid #e2e8f0;
#     margin-bottom: 10px;
#     text-align: center;
#     transition: 0.2s;
# }

# .service-card:hover {
#     border-color: #2563eb;
#     box-shadow: 0px 4px 15px rgba(37, 99, 235, 0.12);
# }

# .metric-card {
#     background: white;
#     padding: 22px;
#     border-radius: 15px;
#     border: 1px solid #e2e8f0;
#     text-align: center;
# }

# .metric-title {
#     font-size: 14px;
#     color: #64748b;
# }

# .metric-value {
#     font-size: 28px;
#     font-weight: 800;
#     color: #1e40af;
# }

# .metric-change {
#     font-size: 13px;
#     color: #16a34a;
# }

# /* Status badges */

# .badge-success {
#     background: #dcfce7;
#     color: #166534;
#     padding: 5px 10px;
#     border-radius: 20px;
#     font-size: 12px;
#     font-weight: 600;
# }

# .badge-warning {
#     background: #fef3c7;
#     color: #92400e;
#     padding: 5px 10px;
#     border-radius: 20px;
#     font-size: 12px;
#     font-weight: 600;
# }

# .badge-danger {
#     background: #fee2e2;
#     color: #991b1b;
#     padding: 5px 10px;
#     border-radius: 20px;
#     font-size: 12px;
#     font-weight: 600;
# }

# /* Chat */

# .chat-user {
#     background: #dbeafe;
#     padding: 12px 16px;
#     border-radius: 15px 15px 2px 15px;
#     margin: 8px 0;
#     margin-left: 20%;
# }

# .chat-bot {
#     background: #f1f5f9;
#     padding: 12px 16px;
#     border-radius: 15px 15px 15px 2px;
#     margin: 8px 0;
#     margin-right: 20%;
# }

# /* Emergency */

# .emergency-box {
#     background: linear-gradient(135deg, #fee2e2, #fff1f2);
#     border: 1px solid #fecaca;
#     padding: 20px;
#     border-radius: 15px;
# }

# /* Section titles */

# .section-title {
#     font-size: 24px;
#     font-weight: 700;
#     color: #0f172a;
#     margin-top: 20px;
#     margin-bottom: 15px;
# }

# </style>
# """, unsafe_allow_html=True)


# # ============================================================
# # SESSION STATE
# # ============================================================

# if "bookings" not in st.session_state:
#     st.session_state.bookings = []

# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = [
#         {
#             "role": "assistant",
#             "message": "Hello! 👋 I'm your VISHVAS 360 AI assistant. How can I help you today?"
#         }
#     ]

# if "notifications" not in st.session_state:
#     st.session_state.notifications = 3

# if "language" not in st.session_state:
#     st.session_state.language = "English"


# # ============================================================
# # SAMPLE DATA
# # ============================================================

# services = [
#     ("⚡", "Electrician", "Electrical repairs & installations"),
#     ("🔧", "Plumber", "Pipes, leakage & fittings"),
#     ("❄️", "AC Repair", "AC servicing & maintenance"),
#     ("🪚", "Carpenter", "Furniture & woodwork"),
#     ("🎨", "Painter", "Home & office painting"),
#     ("🔌", "Appliance Repair", "TV, washing machine & more"),
#     ("🧹", "Cleaning", "Home & office cleaning"),
#     ("🚗", "Mechanic", "Vehicle repair & servicing"),
# ]

# providers = [
#     {
#         "name": "Rajesh Kumar",
#         "service": "Electrician",
#         "rating": 4.9,
#         "jobs": 245,
#         "trust": 96,
#         "distance": "1.2 km",
#         "verified": True
#     },
#     {
#         "name": "Amit Sharma",
#         "service": "Plumber",
#         "rating": 4.8,
#         "jobs": 189,
#         "trust": 94,
#         "distance": "2.4 km",
#         "verified": True
#     },
#     {
#         "name": "Vikram Singh",
#         "service": "AC Repair",
#         "rating": 4.7,
#         "jobs": 156,
#         "trust": 91,
#         "distance": "3.1 km",
#         "verified": True
#     },
#     {
#         "name": "Suresh Verma",
#         "service": "Mechanic",
#         "rating": 4.6,
#         "jobs": 112,
#         "trust": 88,
#         "distance": "4.2 km",
#         "verified": False
#     }
# ]


# # ============================================================
# # SIDEBAR NAVIGATION
# # ============================================================

# with st.sidebar:

#     st.markdown("""
#     <div style="text-align:center; padding:15px 0 25px;">
#         <div style="font-size:42px;">🛠️</div>
#         <h1 style="font-size:24px; margin:5px 0;">VISHVAS 360</h1>
#         <p style="font-size:12px; color:#cbd5e1;">Trusted Local Services</p>
#     </div>
#     """, unsafe_allow_html=True)

#     st.markdown("---")

#     mode = st.radio(
#         "Select Mode",
#         [
#             "🏠 Customer Dashboard",
#             "🤖 AI Assistant",
#             "📅 My Bookings",
#             "👨‍🔧 Service Provider",
#             "📊 Admin Dashboard"
#         ]
#     )

#     st.markdown("---")

#     st.markdown("### Quick Actions")

#     if st.button("🚨 Emergency Service", use_container_width=True):
#         st.session_state.emergency = True

#     if st.button("🔔 Notifications", use_container_width=True):
#         st.info(f"You have {st.session_state.notifications} notifications.")

#     if st.button("🌐 Change Language", use_container_width=True):
#         st.session_state.language = "Hindi" if st.session_state.language == "English" else "English"

#     st.markdown("---")

#     st.caption("VISHVAS 360 v1.0")
#     st.caption("AI-Powered Trusted Local Service Marketplace")


# # ============================================================
# # HEADER
# # ============================================================

# st.markdown("""
# <div class="hero">
#     <div class="hero-heading">VISHVAS 360</div>
#     <div class="hero-subheading">AI-Powered Trusted Local Service Marketplace</div>
#     <div class="hero-text">
#         Connecting customers with verified local service providers through intelligent
#         matching, voice and text booking, multilingual support, emergency services,
#         secure payments, and real-time notifications.
#     </div>
# </div>
# """, unsafe_allow_html=True)


# # ============================================================
# # EMERGENCY SERVICE MODE
# # ============================================================

# if st.session_state.get("emergency", False):

#     st.markdown("""
#     <div class="emergency-box">
#         <h2 style="color:#b91c1c;">🚨 Emergency Service Mode</h2>
#         <p>Get immediate assistance from nearby verified service providers.</p>
#     </div>
#     """, unsafe_allow_html=True)

#     col1, col2, col3 = st.columns(3)

#     with col1:
#         st.metric("Nearby Providers", "12")

#     with col2:
#         st.metric("Average Response", "8 mins")

#     with col3:
#         st.metric("Emergency Fee", "₹99")

#     emergency_type = st.selectbox(
#         "Select Emergency Type",
#         [
#             "Electrical Failure",
#             "Water Leakage",
#             "AC Breakdown",
#             "Vehicle Breakdown",
#             "Other"
#         ]
#     )

#     location = st.text_input("Your Location", placeholder="Enter your location")

#     if st.button("🚨 Find Emergency Provider", type="primary"):
#         st.success("Emergency request sent! Matching with the nearest verified provider.")
#         st.session_state.emergency = False

#     if st.button("Close Emergency Mode"):
#         st.session_state.emergency = False

#     st.stop()


# # ============================================================
# # CUSTOMER DASHBOARD
# # ============================================================

# if mode == "🏠 Customer Dashboard":

#     # Top metrics

#     st.markdown('<div class="section-title">Welcome Back, Customer 👋</div>',
#                 unsafe_allow_html=True)

#     c1, c2, c3, c4 = st.columns(4)

#     with c1:
#         st.markdown("""
#         <div class="metric-card">
#             <div class="metric-title">Active Bookings</div>
#             <div class="metric-value">2</div>
#             <div class="metric-change">● In Progress</div>
#         </div>
#         """, unsafe_allow_html=True)

#     with c2:
#         st.markdown("""
#         <div class="metric-card">
#             <div class="metric-title">Completed Services</div>
#             <div class="metric-value">18</div>
#             <div class="metric-change">+3 this month</div>
#         </div>
#         """, unsafe_allow_html=True)

#     with c3:
#         st.markdown("""
#         <div class="metric-card">
#             <div class="metric-title">Saved Providers</div>
#             <div class="metric-value">6</div>
#             <div class="metric-change">Trusted contacts</div>
#         </div>
#         """, unsafe_allow_html=True)

#     with c4:
#         st.markdown("""
#         <div class="metric-card">
#             <div class="metric-title">Wallet Balance</div>
#             <div class="metric-value">₹850</div>
#             <div class="metric-change">Secure payments</div>
#         </div>
#         """, unsafe_allow_html=True)

#     st.markdown("---")

#     # Service Categories

#     st.markdown('<div class="section-title">What Service Do You Need?</div>',
#                 unsafe_allow_html=True)

#     cols = st.columns(4)

#     for i, (icon, name, description) in enumerate(services):

#         with cols[i % 4]:

#             st.markdown(f"""
#             <div class="service-card">
#                 <div style="font-size:35px;">{icon}</div>
#                 <h4 style="margin:8px 0;">{name}</h4>
#                 <p style="font-size:12px;color:#64748b;">{description}</p>
#             </div>
#             """, unsafe_allow_html=True)

#             if st.button(f"Book {name}", key=f"book_{name}", use_container_width=True):
#                 st.session_state.selected_service = name
#                 st.session_state.show_booking = True

#     # Booking section

#     if st.session_state.get("show_booking", False):

#         st.markdown("---")
#         st.markdown('<div class="section-title">Book a Service</div>',
#                     unsafe_allow_html=True)

#         selected_service = st.session_state.get("selected_service", "Electrician")

#         col1, col2 = st.columns(2)

#         with col1:

#             st.info(f"Selected Service: {selected_service}")

#             provider_choice = st.selectbox(
#                 "Choose Provider",
#                 [
#                     "Let AI Match Me Automatically",
#                     "Rajesh Kumar - Electrician ⭐4.9",
#                     "Amit Sharma - Plumber ⭐4.8",
#                     "Vikram Singh - AC Repair ⭐4.7"
#                 ]
#             )

#             address = st.text_area(
#                 "Service Address",
#                 placeholder="Enter complete address"
#             )

#         with col2:

#             service_date = st.date_input(
#                 "Preferred Date",
#                 datetime.today()
#             )

#             service_time = st.selectbox(
#                 "Preferred Time",
#                 [
#                     "Morning (8 AM - 11 AM)",
#                     "Afternoon (12 PM - 3 PM)",
#                     "Evening (4 PM - 7 PM)"
#                 ]
#             )

#             notes = st.text_area(
#                 "Additional Requirements",
#                 placeholder="Describe your problem..."
#             )

#         col1, col2, col3 = st.columns(3)

#         with col1:
#             if st.button("Confirm Booking", type="primary", use_container_width=True):

#                 booking = {
#                     "service": selected_service,
#                     "provider": provider_choice,
#                     "date": str(service_date),
#                     "time": service_time,
#                     "status": "Confirmed",
#                     "booking_id": f"V360{random.randint(1000,9999)}"
#                 }

#                 st.session_state.bookings.append(booking)
#                 st.success("Booking confirmed successfully! 🎉")
#                 st.balloons()

#         with col2:
#             if st.button("Cancel", use_container_width=True):
#                 st.session_state.show_booking = False
#                 st.rerun()

#         with col3:
#             if st.button("Find with AI", use_container_width=True):
#                 st.info("AI is analyzing provider ratings, distance, availability, and trust scores...")

#     # Recommended Providers

#     st.markdown("---")

#     st.markdown('<div class="section-title">Recommended Verified Providers</div>',
#                 unsafe_allow_html=True)

#     provider_cols = st.columns(4)

#     for i, provider in enumerate(providers):

#         with provider_cols[i]:

#             verified_badge = "✓ Verified" if provider["verified"] else "Pending Verification"

#             st.markdown(f"""
#             <div class="service-card" style="text-align:left;">
#                 <div style="font-size:35px;text-align:center;">👨‍🔧</div>
#                 <h4>{provider["name"]}</h4>
#                 <p style="color:#64748b;">{provider["service"]}</p>
#                 <p>⭐ {provider["rating"]} Rating</p>
#                 <p>📍 {provider["distance"]} away</p>
#                 <p>🛡️ Trust Score: <b>{provider["trust"]}/100</b></p>
#                 <span class="badge-success">{verified_badge}</span>
#             </div>
#             """, unsafe_allow_html=True)


# # ============================================================
# # AI ASSISTANT
# # ============================================================

# elif mode == "🤖 AI Assistant":

#     st.markdown('<div class="section-title">🤖 VISHVAS AI Assistant</div>',
#                 unsafe_allow_html=True)

#     st.info(
#         "Describe your problem naturally. Our AI assistant can help you identify "
#         "the right service, find providers, and create bookings."
#     )

#     # Quick suggestions

#     st.markdown("### Quick Suggestions")

#     suggestion_cols = st.columns(4)

#     suggestions = [
#         "My AC is not cooling",
#         "I need an electrician",
#         "Book emergency plumber",
#         "Find a nearby mechanic"
#     ]

#     for i, suggestion in enumerate(suggestions):
#         with suggestion_cols[i]:
#             if st.button(suggestion, use_container_width=True):
#                 st.session_state.chat_history.append(
#                     {"role": "user", "message": suggestion}
#                 )

#                 st.session_state.chat_history.append(
#                     {
#                         "role": "assistant",
#                         "message": f"I understand! I'll help you find the best service provider for: {suggestion}. "
#                                    "Would you like me to check nearby verified providers?"
#                     }
#                 )

#     st.markdown("---")

#     # Chat History

#     for chat in st.session_state.chat_history:

#         if chat["role"] == "user":

#             st.markdown(
#                 f'<div class="chat-user">👤 {chat["message"]}</div>',
#                 unsafe_allow_html=True
#             )

#         else:

#             st.markdown(
#                 f'<div class="chat-bot">🤖 {chat["message"]}</div>',
#                 unsafe_allow_html=True
#             )

#     user_message = st.chat_input("Type your message here...")

#     if user_message:

#         st.session_state.chat_history.append(
#             {"role": "user", "message": user_message}
#         )

#         # Demo AI response
#         response = (
#             f"Thanks for explaining! Based on your request, I recommend checking "
#             f"verified local service providers. I can help you book a suitable "
#             f"professional near your location."
#         )

#         st.session_state.chat_history.append(
#             {"role": "assistant", "message": response}
#         )

#         st.rerun()

#     st.markdown("---")

#     # Voice Booking UI

#     st.markdown("### 🎙️ Voice-Based Booking")

#     col1, col2 = st.columns([2, 1])

#     with col1:
#         st.write("Speak naturally to describe your service requirement.")

#         audio_value = st.audio_input("Record your voice request")

#         if audio_value:
#             st.success("Voice received! AI will process your request.")

#     with col2:
#         st.info("""
#         Supported Languages:
#         - English
#         - Hindi
#         - Hinglish
#         - Punjabi
#         - More languages coming soon
#         """)


# # ============================================================
# # MY BOOKINGS
# # ============================================================

# elif mode == "📅 My Bookings":

#     st.markdown('<div class="section-title">📅 My Service Bookings</div>',
#                 unsafe_allow_html=True)

#     # Sample active bookings

#     sample_bookings = [
#         {
#             "booking_id": "V3601024",
#             "service": "AC Repair",
#             "provider": "Vikram Singh",
#             "date": "2026-09-18",
#             "time": "Morning",
#             "status": "Confirmed"
#         },
#         {
#             "booking_id": "V3601025",
#             "service": "Electrician",
#             "provider": "Rajesh Kumar",
#             "date": "2026-09-20",
#             "time": "Afternoon",
#             "status": "Pending"
#         }
#     ]

#     all_bookings = sample_bookings + st.session_state.bookings

#     if len(all_bookings) == 0:
#         st.info("You don't have any bookings yet.")

#     for booking in all_bookings:

#         with st.container(border=True):

#             col1, col2, col3, col4 = st.columns([2, 2, 2, 1])

#             with col1:
#                 st.markdown(f"### {booking['service']}")
#                 st.caption(f"Booking ID: {booking['booking_id']}")

#             with col2:
#                 st.write(f"👨‍🔧 {booking['provider']}")
#                 st.write(f"📅 {booking['date']}")

#             with col3:
#                 st.write(f"⏰ {booking['time']}")

#                 if booking["status"] == "Confirmed":
#                     st.success("Confirmed")
#                 else:
#                     st.warning(booking["status"])

#             with col4:
#                 st.button("Track", key=f"track_{booking['booking_id']}")

#                 if st.button("Cancel", key=f"cancel_{booking['booking_id']}"):
#                     st.warning("Cancellation request submitted.")

#     st.markdown("---")

#     st.markdown("### 🔔 Real-Time Notifications")

#     notifications = [
#         "Your AC repair provider has accepted the booking.",
#         "Reminder: Electrician appointment tomorrow at 10 AM.",
#         "Payment of ₹499 completed successfully."
#     ]

#     for notification in notifications:
#         st.info(notification)


# # ============================================================
# # SERVICE PROVIDER DASHBOARD
# # ============================================================

# elif mode == "👨‍🔧 Service Provider":

#     st.markdown('<div class="section-title">👨‍🔧 Service Provider Dashboard</div>',
#                 unsafe_allow_html=True)

#     st.markdown("""
#     <div style="background:linear-gradient(135deg,#eff6ff,#ffffff);
#     padding:20px;border-radius:15px;border:1px solid #bfdbfe;">
#         <h3>Welcome, Service Professional!</h3>
#         <p>Manage your services, bookings, trust score, and business growth.</p>
#     </div>
#     """, unsafe_allow_html=True)

#     st.markdown("### Your Business Overview")

#     c1, c2, c3, c4 = st.columns(4)

#     with c1:
#         st.metric("Today's Jobs", "8", "+2")

#     with c2:
#         st.metric("Monthly Earnings", "₹42,500", "+12%")

#     with c3:
#         st.metric("Trust Score", "94/100", "+3")

#     with c4:
#         st.metric("Customer Rating", "4.8 ⭐", "+0.2")

#     st.markdown("---")

#     # Provider Profile

#     col1, col2 = st.columns(2)

#     with col1:

#         st.markdown("### 👤 Provider Profile")

#         provider_name = st.text_input("Full Name", "Rajesh Kumar")
#         provider_service = st.selectbox(
#             "Primary Service",
#             [x[1] for x in services]
#         )

#         experience = st.number_input(
#             "Years of Experience",
#             min_value=0,
#             max_value=50,
#             value=5
#         )

#         st.markdown("### 📸 Photo Verification")

#         uploaded_photo = st.file_uploader(
#             "Upload Identity / Profile Photo",
#             type=["jpg", "jpeg", "png"]
#         )

#         if uploaded_photo:
#             st.image(uploaded_photo, width=200)
#             st.success("Photo uploaded successfully. Verification pending.")

#     with col2:

#         st.markdown("### 🛡️ Trust & Reputation Score")

#         trust_score = 94

#         st.progress(trust_score / 100)

#         st.markdown(f"""
#         <div style="font-size:32px;font-weight:800;color:#2563eb;">
#             {trust_score}/100
#         </div>
#         """, unsafe_allow_html=True)

#         st.write("Trust Score Components:")

#         trust_data = pd.DataFrame({
#             "Factor": [
#                 "Identity Verification",
#                 "Customer Ratings",
#                 "Completed Jobs",
#                 "Response Time",
#                 "Customer Complaints"
#             ],
#             "Score": [20, 25, 20, 15, 14]
#         })

#         fig = px.bar(
#             trust_data,
#             x="Score",
#             y="Factor",
#             orientation="h",
#             title="Trust Score Breakdown"
#         )

#         st.plotly_chart(fig, use_container_width=True)

#     # Today's Bookings

#     st.markdown("---")
#     st.markdown("### 📅 Today's Service Requests")

#     provider_bookings = pd.DataFrame({
#         "Customer": ["Ananya Sharma", "Rahul Gupta", "Neha Verma", "Aman Jain"],
#         "Service": ["AC Repair", "Maintenance", "Installation", "Repair"],
#         "Time": ["10:00 AM", "12:30 PM", "3:00 PM", "5:30 PM"],
#         "Status": ["Accepted", "Pending", "Accepted", "Completed"]
#     })

#     st.dataframe(
#         provider_bookings,
#         use_container_width=True,
#         hide_index=True
#     )

#     # Business Expansion Recommendation

#     st.markdown("---")

#     st.markdown("### 💡 AI Business Expansion Recommendations")

#     st.success("""
#     Based on demand patterns and customer requests, expanding your service coverage
#     to nearby high-demand locations may help increase job opportunities.
#     """)

#     recommendation_data = pd.DataFrame({
#         "Recommendation": [
#             "Add AC Installation Service",
#             "Expand to Civil Lines Area",
#             "Offer Weekend Availability",
#             "Partner with Appliance Repair Providers"
#         ],
#         "Potential Demand": ["High", "High", "Medium", "Medium"],
#         "Estimated Growth": ["25%", "18%", "12%", "10%"]
#     })

#     st.dataframe(
#         recommendation_data,
#         use_container_width=True,
#         hide_index=True
#     )


# # ============================================================
# # ADMIN DASHBOARD
# # ============================================================

# elif mode == "📊 Admin Dashboard":

#     st.markdown('<div class="section-title">📊 Admin Control Center</div>',
#                 unsafe_allow_html=True)

#     st.info("Monitor marketplace activity, demand trends, providers, and platform performance.")

#     # Platform Metrics

#     c1, c2, c3, c4, c5 = st.columns(5)

#     with c1:
#         st.metric("Total Users", "12,450", "+8.2%")

#     with c2:
#         st.metric("Service Providers", "1,280", "+5.4%")

#     with c3:
#         st.metric("Daily Bookings", "342", "+14.3%")

#     with c4:
#         st.metric("Revenue", "₹2.4L", "+11.8%")

#     with c5:
#         st.metric("Trust Verified", "1,145", "+7.1%")

#     st.markdown("---")

#     # Demand Heatmap

#     st.markdown("### 🗺️ AI-Powered Service Demand Heatmap")

#     st.write(
#         "This map visualizes service demand across different locations. "
#         "In a production version, this data can come from booking history, "
#         "GPS coordinates, and real-time service requests."
#     )

#     # Demo demand data

#     np.random.seed(42)

#     locations = [
#         ("Civil Lines", 29.4727, 77.7085, 85),
#         ("Sadar Bazar", 29.4760, 77.7030, 65),
#         ("New Mandi", 29.4620, 77.7080, 72),
#         ("Jansath Road", 29.4500, 77.7200, 45),
#         ("Muzaffarnagar City", 29.4727, 77.7081, 95),
#         ("Rohana", 29.5200, 77.6500, 35),
#         ("Shahpur", 29.3500, 77.5500, 50),
#         ("Khatauli", 29.2800, 77.7300, 60),
#         ("Budhana", 29.2900, 77.4700, 42),
#         ("Purqazi", 29.5600, 77.8200, 38)
#     ]

#     demand_df = pd.DataFrame(
#         locations,
#         columns=["Area", "Latitude", "Longitude", "Demand"]
#     )

#     service_filter = st.selectbox(
#         "Filter by Service Category",
#         ["All Services"] + [x[1] for x in services]
#     )

#     if service_filter != "All Services":
#         demand_df["Demand"] = demand_df["Demand"] * np.random.uniform(0.7, 1.3, len(demand_df))
#         demand_df["Demand"] = demand_df["Demand"].round(0)

#     fig_map = px.scatter_mapbox(
#         demand_df,
#         lat="Latitude",
#         lon="Longitude",
#         size="Demand",
#         color="Demand",
#         hover_name="Area",
#         hover_data={"Demand": True},
#         zoom=10,
#         height=500,
#         color_continuous_scale="Turbo"
#     )

#     fig_map.update_layout(
#         mapbox_style="open-street-map",
#         margin={"r": 0, "t": 0, "l": 0, "b": 0}
#     )

#     st.plotly_chart(fig_map, use_container_width=True)

#     st.caption("Demo data shown for visualization. Connect real booking/GPS data for production heatmaps.")

#     # Demand Analytics

#     st.markdown("---")

#     st.markdown("### 📈 Service Demand Analytics")

#     col1, col2 = st.columns(2)

#     with col1:

#         service_demand = pd.DataFrame({
#             "Service": [
#                 "AC Repair",
#                 "Electrician",
#                 "Plumber",
#                 "Cleaning",
#                 "Mechanic",
#                 "Carpenter",
#                 "Appliance Repair",
#                 "Painter"
#             ],
#             "Requests": [420, 380, 310, 275, 240, 190, 175, 130]
#         })

#         fig = px.bar(
#             service_demand,
#             x="Service",
#             y="Requests",
#             title="Demand by Service Category"
#         )

#         st.plotly_chart(fig, use_container_width=True)

#     with col2:

#         monthly_data = pd.DataFrame({
#             "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
#                       "Jul", "Aug", "Sep"],
#             "Bookings": [1200, 1350, 1480, 1600, 1720, 1890, 2100, 2300, 2450]
#         })

#         fig2 = px.line(
#             monthly_data,
#             x="Month",
#             y="Bookings",
#             markers=True,
#             title="Monthly Booking Growth"
#         )

#         st.plotly_chart(fig2, use_container_width=True)

#     # Provider Management

#     st.markdown("---")

#     st.markdown("### 👨‍🔧 Provider Verification Management")

#     verification_data = pd.DataFrame({
#         "Provider": [
#             "Rajesh Kumar",
#             "Amit Sharma",
#             "Vikram Singh",
#             "Suresh Verma",
#             "Pankaj Yadav"
#         ],
#         "Service": [
#             "Electrician",
#             "Plumber",
#             "AC Repair",
#             "Mechanic",
#             "Carpenter"
#         ],
#         "Trust Score": [96, 94, 91, 88, 76],
#         "Verification": [
#             "Verified",
#             "Verified",
#             "Verified",
#             "Pending",
#             "Pending"
#         ]
#     })

#     st.dataframe(
#         verification_data,
#         use_container_width=True,
#         hide_index=True
#     )

#     # AI Expansion Agent

#     st.markdown("---")

#     st.markdown("### 🤖 AI Service Demand Agent")

#     st.write(
#         "The AI agent analyzes booking density, provider availability, customer complaints, "
#         "and service demand trends to recommend business expansion opportunities."
#     )

#     expansion_data = pd.DataFrame({
#         "Area": ["Civil Lines", "New Mandi", "Sadar Bazar", "Khatauli"],
#         "High Demand Service": ["AC Repair", "Electrician", "Plumber", "Mechanic"],
#         "Current Providers": [8, 5, 12, 3],
#         "Demand Level": ["Very High", "High", "High", "Medium"],
#         "Expansion Opportunity": ["Yes", "Yes", "Yes", "Monitor"]
#     })

#     st.dataframe(
#         expansion_data,
#         use_container_width=True,
#         hide_index=True
#     )

#     if st.button("Generate AI Business Expansion Report", type="primary"):

#         with st.spinner("AI Agent analyzing marketplace data..."):
#             import time
#             time.sleep(1)

#         st.success("Expansion analysis completed!")

#         st.markdown("""
#         #### AI Insights Generated:

#         - AC Repair demand is increasing in high-density residential areas.
#         - Civil Lines shows a shortage of verified service providers.
#         - Weekend demand is higher than weekday demand for home services.
#         - Adding 3–5 providers in high-demand zones may improve response times.
#         """)


# # ============================================================
# # FOOTER
# # ============================================================

# st.markdown("---")

# st.markdown("""
# <div style="text-align:center;color:#64748b;padding:20px;">
#     <b>VISHVAS 360</b> — Building Trust Between Customers and Local Service Providers
#     <br><br>
#     AI-Powered • Verified Professionals • Secure Services • Smart Marketplace
# </div>
# """, unsafe_allow_html=True)

"""
VISHVAS 360 — AI-Powered Trusted Local Service Marketplace
Streamlit frontend wired to the FastAPI backend (main.py) / Supabase schema.

Run:
    streamlit run app.py

Env:
    VISHVAS_API_URL   default http://127.0.0.1:8000
"""

import os
import random
from datetime import datetime, date, timedelta

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

API_BASE = os.getenv("VISHVAS_API_URL", "http://127.0.0.1:8000").rstrip("/")

st.set_page_config(
    page_title="VISHVAS 360",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# DESIGN SYSTEM
# ============================================================
# Ink navy + marigold accent + verified teal. Cards are left-edge
# accented rather than uniformly bordered so hierarchy reads fast.

INK = "#101233"
INK_SOFT = "#2A2F55"
MARIGOLD = "#F4A118"
TEAL = "#0F9E8E"
CORAL = "#E4572E"
PAPER = "#F6F5F1"

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Inter:wght@400;500;600;700&family=Noto+Sans+Devanagari:wght@500;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
h1, h2, h3, h4, .v-display { font-family: 'Sora', sans-serif; letter-spacing: -0.02em; }

.stApp { background: #F6F5F1; }
.block-container { padding-top: 1.2rem; padding-bottom: 3rem; max-width: 1380px; }

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] { background: #101233; border-right: 1px solid #23264d; }
[data-testid="stSidebar"] * { color: #EDEDF5 !important; }
[data-testid="stSidebar"] .stRadio label { font-size: 14px; }
[data-testid="stSidebar"] hr { border-color: #2A2F55; }

/* ---------- Hero ---------- */
.v-hero {
    background: #101233;
    background-image:
        radial-gradient(900px 300px at 88% -10%, rgba(244,161,24,.28), transparent 60%),
        radial-gradient(700px 320px at 10% 120%, rgba(15,158,142,.30), transparent 60%);
    padding: 40px 42px 34px;
    border-radius: 24px;
    color: #fff;
    margin-bottom: 26px;
}
.v-hero h1 { font-size: 46px; font-weight: 800; margin: 0; color: #fff; line-height: 1.05; }
.v-hero .hi { font-family:'Noto Sans Devanagari',sans-serif; color:#F4A118; font-size:17px; margin-bottom:10px; }
.v-hero p { color: #C7C9DF; font-size: 15.5px; max-width: 62ch; line-height: 1.7; margin-top: 14px; }
.v-pill-row { margin-top: 20px; display: flex; flex-wrap: wrap; gap: 8px; }
.v-pill { border:1px solid rgba(255,255,255,.22); border-radius:999px; padding:6px 13px; font-size:12.5px; color:#EDEDF5; }

/* ---------- Metric tiles ---------- */
.v-stat {
    background:#fff; border-radius:14px; padding:18px 18px 16px;
    border:1px solid #E6E4DC; border-left:4px solid #101233; height:100%;
}
.v-stat.acc-gold { border-left-color:#F4A118; }
.v-stat.acc-teal { border-left-color:#0F9E8E; }
.v-stat.acc-coral { border-left-color:#E4572E; }
.v-stat .k { font-size:12.5px; color:#6B6F8C; font-weight:600; }
.v-stat .v { font-family:'Sora',sans-serif; font-size:30px; font-weight:800; color:#101233; line-height:1.2; margin-top:4px; }
.v-stat .d { font-size:12.5px; color:#0F9E8E; font-weight:600; }

/* ---------- Service + provider cards ---------- */
.v-card {
    background:#fff; border:1px solid #E6E4DC; border-radius:14px;
    padding:18px; height:100%;
}
.v-card .ico { font-size:30px; }
.v-card h4 { margin:8px 0 2px; font-size:16px; color:#101233; }
.v-card p { font-size:12.5px; color:#6B6F8C; margin:0; line-height:1.5; }

.v-provider { background:#fff; border:1px solid #E6E4DC; border-radius:14px; padding:18px; }
.v-provider .nm { font-family:'Sora',sans-serif; font-weight:700; font-size:17px; color:#101233; }
.v-provider .sv { font-size:13px; color:#6B6F8C; margin-bottom:10px; }
.v-provider .row { font-size:13px; color:#33375C; margin:3px 0; }

/* ---------- Badges ---------- */
.b { border-radius:999px; padding:4px 11px; font-size:11.5px; font-weight:700; display:inline-block; }
.b-verified { background:#E1F5F1; color:#0B6F63; }
.b-pending  { background:#FDF1DC; color:#8A5A06; }
.b-live     { background:#FBE3DC; color:#9C3517; }

/* ---------- Trust meter ---------- */
.v-trust { background:#101233; border-radius:16px; padding:22px; color:#fff; }
.v-trust .score { font-family:'Sora',sans-serif; font-size:46px; font-weight:800; color:#F4A118; line-height:1; }
.v-trust .lbl { font-size:12.5px; color:#B9BCD6; }
.v-bar { height:8px; border-radius:999px; background:#2A2F55; margin-top:14px; overflow:hidden; }
.v-bar span { display:block; height:100%; background:linear-gradient(90deg,#F4A118,#0F9E8E); }

/* ---------- Chat ---------- */
.v-msg-user { background:#101233; color:#fff; padding:12px 16px; border-radius:16px 16px 4px 16px; margin:8px 0 8px 18%; font-size:14.5px; }
.v-msg-bot  { background:#fff; border:1px solid #E6E4DC; color:#23264d; padding:12px 16px; border-radius:16px 16px 16px 4px; margin:8px 18% 8px 0; font-size:14.5px; }

/* ---------- Emergency ---------- */
.v-emergency {
    background:#E4572E;
    background-image: radial-gradient(600px 200px at 90% 0%, rgba(244,161,24,.55), transparent 65%);
    color:#fff; padding:26px 28px; border-radius:18px;
}
.v-emergency h2 { color:#fff; margin:0 0 6px; font-size:26px; }
.v-emergency p { color:#FFE6DC; margin:0; font-size:14.5px; }

/* ---------- Section heads ---------- */
.v-sec { font-family:'Sora',sans-serif; font-size:22px; font-weight:700; color:#101233; margin:26px 0 4px; }
.v-sub { font-size:13.5px; color:#6B6F8C; margin-bottom:14px; }

/* ---------- Buttons ---------- */
.stButton > button {
    border-radius:10px; border:1px solid #D9D7CE; background:#fff; color:#101233;
    font-weight:600; font-size:13.5px;
}
.stButton > button:hover { border-color:#101233; color:#101233; background:#F2F1EC; }
.stButton > button[kind="primary"] { background:#101233; color:#fff; border-color:#101233; }
.stButton > button[kind="primary"]:hover { background:#23264d; color:#fff; }

/* ---------- Footer ---------- */
.v-foot { text-align:center; color:#6B6F8C; font-size:13px; padding:26px 0 10px; }
.v-foot b { color:#101233; }
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# API LAYER  (graceful demo fallback when the backend is down)
# ============================================================

SERVICE_ICONS = {
    "Electrician": "⚡",
    "Plumber": "🚿",
    "AC Repair": "❄️",
    "Carpenter": "🪚",
    "Painter": "🎨",
    "Appliance Repair": "🔌",
    "Cleaning": "🧹",
    "Mechanic": "🔧",
}

DEMO = {
    "services": [
        {"id": 1, "name": "Electrician", "description": "Wiring, switchboards, inverters"},
        {"id": 2, "name": "Plumber", "description": "Leakages, fittings, motors"},
        {"id": 3, "name": "AC Repair", "description": "Servicing, gas refill, installation"},
        {"id": 4, "name": "Carpenter", "description": "Furniture, doors, woodwork"},
        {"id": 5, "name": "Painter", "description": "Home and shop painting"},
        {"id": 6, "name": "Appliance Repair", "description": "TV, fridge, washing machine"},
        {"id": 7, "name": "Cleaning", "description": "Deep cleaning, tanks, sofas"},
        {"id": 8, "name": "Mechanic", "description": "Two and four wheeler repair"},
    ],
    "providers": [
        {"id": 1, "business_name": "Rajesh Electricals", "full_name": "Rajesh Kumar",
         "service": "Electrician", "rating": 4.9, "reviews": 132, "completed_jobs": 245,
         "experience_years": 11, "verification_status": "verified", "availability_status": "online",
         "distance_km": 1.2, "price": 299, "trust_score": 96, "area": "Civil Lines"},
        {"id": 2, "business_name": "Sharma Plumbing Works", "full_name": "Amit Sharma",
         "service": "Plumber", "rating": 4.8, "reviews": 98, "completed_jobs": 189,
         "experience_years": 8, "verification_status": "verified", "availability_status": "online",
         "distance_km": 2.4, "price": 249, "trust_score": 94, "area": "Sadar Bazar"},
        {"id": 3, "business_name": "CoolCare AC Services", "full_name": "Vikram Singh",
         "service": "AC Repair", "rating": 4.7, "reviews": 76, "completed_jobs": 156,
         "experience_years": 6, "verification_status": "verified", "availability_status": "busy",
         "distance_km": 3.1, "price": 499, "trust_score": 91, "area": "New Mandi"},
        {"id": 4, "business_name": "Verma Auto Point", "full_name": "Suresh Verma",
         "service": "Mechanic", "rating": 4.6, "reviews": 54, "completed_jobs": 112,
         "experience_years": 4, "verification_status": "pending", "availability_status": "online",
         "distance_km": 4.2, "price": 349, "trust_score": 82, "area": "Khatauli"},
    ],
    "bookings": [
        {"id": 1024, "service": "AC Repair", "provider": "Vikram Singh", "booking_date": "2026-09-18",
         "booking_time": "10:00", "status": "confirmed", "address": "Civil Lines, Muzaffarnagar",
         "is_emergency": False, "estimated_price": 499},
        {"id": 1025, "service": "Electrician", "provider": "Rajesh Kumar", "booking_date": "2026-09-20",
         "booking_time": "14:30", "status": "pending", "address": "New Mandi, Muzaffarnagar",
         "is_emergency": False, "estimated_price": 299},
        {"id": 1019, "service": "Plumber", "provider": "Amit Sharma", "booking_date": "2026-09-08",
         "booking_time": "09:00", "status": "completed", "address": "Sadar Bazar, Muzaffarnagar",
         "is_emergency": True, "estimated_price": 348},
    ],
    "notifications": [
        {"id": 1, "title": "Booking accepted", "message": "Vikram Singh accepted your AC Repair request for 18 Sep, 10:00 AM.",
         "notification_type": "booking", "is_read": False, "created_at": "2026-09-16T09:12:00"},
        {"id": 2, "title": "Visit tomorrow", "message": "Rajesh Kumar arrives tomorrow between 2:30 and 3:30 PM.",
         "notification_type": "reminder", "is_read": False, "created_at": "2026-09-16T08:02:00"},
        {"id": 3, "title": "Payment received", "message": "₹348 paid for booking #1019 via UPI.",
         "notification_type": "payment", "is_read": True, "created_at": "2026-09-08T17:40:00"},
    ],
    "demand": [
        {"area_name": "Muzaffarnagar City", "latitude": 29.4727, "longitude": 77.7081, "total_requests": 95, "completed_requests": 78},
        {"area_name": "Civil Lines", "latitude": 29.4760, "longitude": 77.7085, "total_requests": 85, "completed_requests": 61},
        {"area_name": "New Mandi", "latitude": 29.4620, "longitude": 77.7080, "total_requests": 72, "completed_requests": 59},
        {"area_name": "Sadar Bazar", "latitude": 29.4755, "longitude": 77.7030, "total_requests": 65, "completed_requests": 55},
        {"area_name": "Khatauli", "latitude": 29.2800, "longitude": 77.7300, "total_requests": 60, "completed_requests": 41},
        {"area_name": "Shahpur", "latitude": 29.3500, "longitude": 77.5500, "total_requests": 50, "completed_requests": 33},
        {"area_name": "Jansath Road", "latitude": 29.4500, "longitude": 77.7200, "total_requests": 45, "completed_requests": 36},
        {"area_name": "Budhana", "latitude": 29.2900, "longitude": 77.4700, "total_requests": 42, "completed_requests": 25},
        {"area_name": "Purqazi", "latitude": 29.5600, "longitude": 77.8200, "total_requests": 38, "completed_requests": 22},
        {"area_name": "Rohana", "latitude": 29.5200, "longitude": 77.6500, "total_requests": 35, "completed_requests": 24},
    ],
    "insights": [
        {"area_name": "Civil Lines", "service": "AC Repair", "demand_level": "very high",
         "available_providers": 8, "total_requests": 210, "unmet_requests": 41,
         "recommendation": "Onboard 4 more AC technicians; 19% of requests go unserved on weekends."},
        {"area_name": "New Mandi", "service": "Electrician", "demand_level": "high",
         "available_providers": 5, "total_requests": 164, "unmet_requests": 28,
         "recommendation": "Evening slots sell out first — add two providers for the 4–7 PM window."},
        {"area_name": "Khatauli", "service": "Mechanic", "demand_level": "medium",
         "available_providers": 3, "total_requests": 96, "unmet_requests": 22,
         "recommendation": "Doorstep two-wheeler service is requested but unavailable here."},
        {"area_name": "Sadar Bazar", "service": "Plumber", "demand_level": "high",
         "available_providers": 12, "total_requests": 151, "unmet_requests": 9,
         "recommendation": "Supply is healthy. Hold onboarding and focus on response times."},
    ],
}


def api(method: str, path: str, **kwargs):
    """Call the backend. Returns (ok, data). Never raises."""
    try:
        r = requests.request(method, f"{API_BASE}{path}", timeout=6, **kwargs)
        r.raise_for_status()
        return True, r.json()
    except Exception as exc:  # backend offline / route missing
        st.session_state.api_error = str(exc)
        return False, None


def get_services():
    ok, data = api("GET", "/services")
    if ok and data.get("services"):
        return data["services"]
    return DEMO["services"]


def get_providers(service_id=None):
    params = {"service_id": service_id} if service_id else None
    ok, data = api("GET", "/providers", params=params)
    if ok and data.get("providers"):
        return data["providers"]
    if service_id:
        names = {s["id"]: s["name"] for s in DEMO["services"]}
        want = names.get(service_id)
        matched = [p for p in DEMO["providers"] if p["service"] == want]
        return matched or DEMO["providers"]
    return DEMO["providers"]


def get_bookings(customer_id):
    ok, data = api("GET", "/bookings", params={"customer_id": customer_id})
    if ok and data.get("bookings"):
        return data["bookings"]
    return DEMO["bookings"] + st.session_state.local_bookings


def create_booking(payload):
    ok, data = api("POST", "/bookings", json=payload)
    if ok:
        return data.get("booking", payload)
    payload = dict(payload)
    payload["id"] = random.randint(2000, 9999)
    payload["status"] = "pending"
    st.session_state.local_bookings.append(payload)
    return payload


def get_notifications(user_id):
    ok, data = api("GET", f"/notifications/{user_id}")
    if ok and data.get("notifications"):
        return data["notifications"]
    return DEMO["notifications"]


def get_demand(service_id=None):
    params = {"service_id": service_id} if service_id else None
    ok, data = api("GET", "/demand", params=params)
    if ok and data.get("demand"):
        return data["demand"]
    rows = [dict(r) for r in DEMO["demand"]]
    if service_id:
        rng = random.Random(service_id)
        for r in rows:
            r["total_requests"] = max(8, int(r["total_requests"] * rng.uniform(0.55, 1.25)))
    return rows


def get_insights():
    ok, data = api("GET", "/business-insights")
    if ok and data.get("insights"):
        return data["insights"]
    return DEMO["insights"]


def get_admin_stats():
    ok, data = api("GET", "/admin/stats")
    if ok and data.get("stats"):
        return data["stats"]
    return {"customers": 12450, "providers": 1280, "bookings_today": 342,
            "revenue_month": 243800, "verified_providers": 1145, "open_complaints": 17}


# ============================================================
# SESSION STATE
# ============================================================

DEMO_CUSTOMER_ID = "11111111-1111-1111-1111-111111111111"

defaults = {
    "local_bookings": [],
    "chat": [{"role": "assistant",
              "text": "Namaste 👋 Tell me what's broken — in English, हिंदी or Hinglish — and I'll find a verified professional near you."}],
    "emergency": False,
    "selected_service": None,
    "language": "English",
    "user_id": DEMO_CUSTOMER_ID,
    "api_error": None,
}
for k, v in defaults.items():
    st.session_state.setdefault(k, v)

T = {
    "English": {"need": "What do you need fixed?", "book": "Book", "greet": "Welcome back"},
    "हिंदी": {"need": "आपको क्या ठीक करवाना है?", "book": "बुक करें", "greet": "आपका स्वागत है"},
}
LANG = st.session_state.language
tr = T.get(LANG, T["English"])

services = get_services()

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div style="padding:10px 0 18px;">
          <div style="font-size:30px;">🛡️</div>
          <div class="v-display" style="font-size:23px;font-weight:800;margin-top:4px;">VISHVAS 360</div>
          <div style="font-size:12px;color:#B9BCD6 !important;">Verified help, close to home</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")

    mode = st.radio(
        "Go to",
        ["Find a service", "Ask the assistant", "My bookings",
         "Provider workspace", "Admin control centre"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("**Quick actions**")

    if st.button("🚨 Emergency service", use_container_width=True):
        st.session_state.emergency = True
        st.rerun()

    unread = sum(1 for n in get_notifications(st.session_state.user_id) if not n.get("is_read"))
    if st.button(f"🔔 Notifications ({unread})", use_container_width=True):
        st.toast(f"{unread} unread updates waiting in My bookings.")

    st.session_state.language = st.selectbox("Language", ["English", "हिंदी"],
                                             index=["English", "हिंदी"].index(LANG))

    st.markdown("---")
    connected = st.session_state.api_error is None
    st.caption("● Live data" if connected else "● Sample data — backend offline")
    st.caption("VISHVAS 360 · v1.0")

# ============================================================
# HERO
# ============================================================

st.markdown(
    """
<div class="v-hero">
  <div class="hi">विश्वास ३६०</div>
  <h1>Trusted help for every<br>household repair.</h1>
  <p>Describe the problem by voice or text in your own language. VISHVAS 360 matches you
     with a background-verified professional nearby, holds the payment until the job is done,
     and keeps you posted at every step.</p>
  <div class="v-pill-row">
    <span class="v-pill">ID + photo verified</span>
    <span class="v-pill">Trust score on every profile</span>
    <span class="v-pill">Emergency response in ~8 min</span>
    <span class="v-pill">Secure payments</span>
    <span class="v-pill">English · हिंदी · Hinglish</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# EMERGENCY MODE
# ============================================================

if st.session_state.emergency:
    st.markdown(
        """
    <div class="v-emergency">
      <h2>🚨 Emergency service</h2>
      <p>We alert every online verified provider within 5 km at once. First to accept is dispatched.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Providers online nearby", "12")
    c2.metric("Typical arrival", "8 min")
    c3.metric("Emergency callout fee", "₹99")

    with st.form("emergency_form"):
        a, b = st.columns(2)
        etype = a.selectbox("What's happening?",
                            ["Power failure / sparking", "Water leakage or burst pipe",
                             "AC breakdown", "Vehicle breakdown", "Lock or door damage", "Something else"])
        phone = b.text_input("Phone number for the provider to call", placeholder="9XXXXXXXXX")
        addr = st.text_area("Where should they come?", placeholder="House / shop number, landmark, area")
        detail = st.text_input("One line about the problem", placeholder="Main switchboard is sparking")
        sent = st.form_submit_button("Send emergency request", type="primary", use_container_width=True)

    if sent:
        if not addr.strip() or not phone.strip():
            st.error("Add your address and phone number so the provider can reach you.")
        else:
            create_booking({
                "customer_id": st.session_state.user_id,
                "service_id": 1,
                "booking_date": str(date.today()),
                "booking_time": datetime.now().strftime("%H:%M"),
                "address": addr,
                "description": f"EMERGENCY — {etype}. {detail}",
                "is_emergency": True,
                "estimated_price": 99,
                "status": "pending",
            })
            st.success("Request broadcast. Keep your phone reachable — you'll get a call within minutes.")

    if st.button("Leave emergency mode"):
        st.session_state.emergency = False
        st.rerun()
    st.stop()

# ============================================================
# 1 · FIND A SERVICE
# ============================================================

if mode == "Find a service":

    stats = [
        ("Active bookings", "2", "1 provider on the way", ""),
        ("Jobs completed", "18", "3 this month", "acc-teal"),
        ("Saved professionals", "6", "People you re-hire", "acc-gold"),
        ("Wallet balance", "₹850", "Refunds land here", "acc-coral"),
    ]
    cols = st.columns(4)
    for col, (k, v, d, cls) in zip(cols, stats):
        col.markdown(
            f'<div class="v-stat {cls}"><div class="k">{k}</div>'
            f'<div class="v">{v}</div><div class="d">{d}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown(f'<div class="v-sec">{tr["need"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="v-sub">Pick a category, or let the assistant read your description and choose for you.</div>',
                unsafe_allow_html=True)

    grid = st.columns(4)
    for i, s in enumerate(services):
        with grid[i % 4]:
            st.markdown(
                f'<div class="v-card"><div class="ico">{SERVICE_ICONS.get(s["name"], "🛠️")}</div>'
                f'<h4>{s["name"]}</h4><p>{s.get("description") or ""}</p></div>',
                unsafe_allow_html=True,
            )
            if st.button(f'{tr["book"]} · {s["name"]}', key=f'svc{s["id"]}', use_container_width=True):
                st.session_state.selected_service = s
                st.rerun()

    # ---------- Booking flow ----------
    sel = st.session_state.selected_service
    if sel:
        st.markdown(f'<div class="v-sec">Book {sel["name"]}</div>', unsafe_allow_html=True)
        matched = get_providers(sel["id"])

        with st.form("booking_form"):
            left, right = st.columns(2)

            with left:
                options = ["Match me automatically (recommended)"] + [
                    f'{p["full_name"]} · ⭐ {p["rating"]} · trust {p.get("trust_score", "—")}' for p in matched
                ]
                choice = st.selectbox("Who should come?", options)
                address = st.text_area("Service address",
                                       placeholder="House / shop number, landmark, area, pincode")
                description = st.text_area("Describe the problem",
                                           placeholder="Outdoor unit makes noise and cooling stopped since yesterday")

            with right:
                bdate = st.date_input("Date", value=date.today(), min_value=date.today())
                slot = st.selectbox("Time slot",
                                    ["08:00", "10:00", "12:00", "14:00", "16:00", "18:00"])
                price = matched[0].get("price", 299) if matched else 299
                st.markdown(
                    f'<div class="v-stat acc-gold"><div class="k">Estimated visit charge</div>'
                    f'<div class="v">₹{price}</div>'
                    f'<div class="d">Final amount confirmed after inspection</div></div>',
                    unsafe_allow_html=True,
                )
                pay = st.radio("Payment", ["UPI", "Card", "Cash after service"], horizontal=False)

            ok_btn = st.form_submit_button("Confirm booking", type="primary", use_container_width=True)

        if ok_btn:
            if not address.strip():
                st.error("Add the service address so the provider can find you.")
            else:
                provider_id = None if choice.startswith("Match") else matched[options.index(choice) - 1]["id"]
                booking = create_booking({
                    "customer_id": st.session_state.user_id,
                    "provider_id": provider_id,
                    "service_id": sel["id"],
                    "booking_date": str(bdate),
                    "booking_time": slot,
                    "address": address,
                    "description": description,
                    "is_emergency": False,
                    "estimated_price": price,
                    "payment_method": pay,
                    "status": "pending",
                })
                st.success(f'Booked. Reference #{booking.get("id", "—")} — you\'ll get a confirmation as soon as a provider accepts.')
                st.balloons()
                st.session_state.selected_service = None

        if st.button("Cancel"):
            st.session_state.selected_service = None
            st.rerun()

    # ---------- Providers ----------
    st.markdown('<div class="v-sec">Verified professionals near you</div>', unsafe_allow_html=True)
    st.markdown('<div class="v-sub">Trust score combines ID verification, ratings, completed jobs, response time and complaint history.</div>',
                unsafe_allow_html=True)

    pcols = st.columns(4)
    for col, p in zip(pcols, get_providers()[:4]):
        with col:
            verified = p.get("verification_status") == "verified"
            badge = ('<span class="b b-verified">✓ Verified</span>' if verified
                     else '<span class="b b-pending">Verification in review</span>')
            live = ('<span class="b b-live">Available now</span>'
                    if p.get("availability_status") == "online" else "")
            st.markdown(
                f"""
                <div class="v-provider">
                  <div class="nm">{p.get("full_name", p.get("business_name"))}</div>
                  <div class="sv">{p.get("service","")} · {p.get("experience_years",0)} yrs experience</div>
                  <div class="row">⭐ {p.get("rating","—")} from {p.get("reviews",0)} reviews</div>
                  <div class="row">📍 {p.get("distance_km","—")} km · {p.get("area","")}</div>
                  <div class="row">🛡️ Trust score <b>{p.get("trust_score","—")}/100</b></div>
                  <div class="v-bar"><span style="width:{p.get('trust_score',0)}%"></span></div>
                  <div style="margin-top:12px;display:flex;gap:6px;flex-wrap:wrap;">{badge}{live}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ============================================================
# 2 · AI ASSISTANT
# ============================================================

elif mode == "Ask the assistant":

    st.markdown('<div class="v-sec">Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="v-sub">Describe the problem in plain words. The assistant picks the right category, checks who is free nearby, and drafts the booking for you to confirm.</div>',
                unsafe_allow_html=True)

    quick = ["AC is not cooling", "Bathroom tap is leaking", "Need an electrician today", "Bike won't start"]
    qcols = st.columns(4)
    for col, q in zip(qcols, quick):
        if col.button(q, use_container_width=True, key=f"q{q}"):
            st.session_state.chat.append({"role": "user", "text": q})
            st.session_state.chat.append({
                "role": "assistant",
                "text": f"Got it — that's a **{'AC Repair' if 'AC' in q else 'Plumber' if 'tap' in q else 'Electrician' if 'electric' in q else 'Mechanic'}** job. "
                        "Three verified professionals are online within 4 km. Shall I book the earliest slot today?"})
            st.rerun()

    for m in st.session_state.chat:
        cls = "v-msg-user" if m["role"] == "user" else "v-msg-bot"
        who = "You" if m["role"] == "user" else "VISHVAS"
        st.markdown(f'<div class="{cls}"><b>{who}</b><br>{m["text"]}</div>', unsafe_allow_html=True)

    text = st.chat_input("Type in English, हिंदी or Hinglish…")
    if text:
        st.session_state.chat.append({"role": "user", "text": text})
        ok, data = api("POST", "/assistant", json={"message": text, "user_id": st.session_state.user_id})
        reply = data.get("reply") if ok and data else (
            "Thanks — I've noted that. I'll shortlist verified providers near your address and "
            "show you the earliest available slot. Want me to go ahead?")
        st.session_state.chat.append({"role": "assistant", "text": reply})
        st.rerun()

    st.markdown('<div class="v-sec">Book by voice</div>', unsafe_allow_html=True)
    vl, vr = st.columns([2, 1])
    with vl:
        clip = st.audio_input("Record your request")
        if clip:
            st.success("Recording received. The assistant will transcribe it and confirm the details with you.")
    with vr:
        st.markdown(
            '<div class="v-card"><h4>Languages supported</h4>'
            '<p>English · हिंदी · Hinglish · ਪੰਜਾਬੀ<br>Replies come back in the language you used.</p></div>',
            unsafe_allow_html=True,
        )

# ============================================================
# 3 · MY BOOKINGS
# ============================================================

elif mode == "My bookings":

    st.markdown('<div class="v-sec">My bookings</div>', unsafe_allow_html=True)

    bookings = get_bookings(st.session_state.user_id)
    tabs = st.tabs(["Upcoming", "Completed", "Updates"])

    def render(bk):
        badge = {"confirmed": ("b-verified", "Confirmed"),
                 "pending": ("b-pending", "Waiting for provider"),
                 "completed": ("b-verified", "Completed"),
                 "cancelled": ("b-live", "Cancelled")}.get(bk.get("status", "pending"),
                                                           ("b-pending", bk.get("status", "")))
        with st.container(border=True):
            a, b, c = st.columns([3, 3, 2])
            with a:
                emg = " 🚨" if bk.get("is_emergency") else ""
                st.markdown(f'<div class="v-display" style="font-size:18px;font-weight:700;">{bk.get("service","Service")}{emg}</div>',
                            unsafe_allow_html=True)
                st.caption(f'Reference #{bk.get("id","—")} · {bk.get("address","")}')
            with b:
                st.write(f'👨‍🔧 {bk.get("provider") or "Matching a provider…"}')
                st.write(f'📅 {bk.get("booking_date","")} at {bk.get("booking_time","")}')
            with c:
                st.markdown(f'<span class="b {badge[0]}">{badge[1]}</span>', unsafe_allow_html=True)
                st.write(f'₹{bk.get("estimated_price","—")}')
            if bk.get("status") == "completed":
                with st.expander("Rate this job"):
                    r = st.slider("Rating", 1, 5, 5, key=f'r{bk["id"]}')
                    txt = st.text_input("What went well or wrong?", key=f't{bk["id"]}')
                    if st.button("Submit review", key=f's{bk["id"]}'):
                        api("POST", "/reviews", json={"booking_id": bk["id"], "rating": r, "review_text": txt,
                                                      "customer_id": st.session_state.user_id})
                        st.success("Review saved. It feeds directly into the provider's trust score.")
            else:
                x, y = st.columns(2)
                x.button("Track provider", key=f'tr{bk["id"]}', use_container_width=True)
                if y.button("Cancel booking", key=f'cn{bk["id"]}', use_container_width=True):
                    api("PATCH", f'/bookings/{bk["id"]}/status', json={"status": "cancelled"})
                    st.warning("Cancellation sent. Free of charge up to 2 hours before the slot.")

    with tabs[0]:
        upcoming = [b for b in bookings if b.get("status") in ("pending", "confirmed", "in_progress")]
        if not upcoming:
            st.info("Nothing scheduled. Pick a category under **Find a service** to book your first job.")
        for b in upcoming:
            render(b)

    with tabs[1]:
        done = [b for b in bookings if b.get("status") in ("completed", "cancelled")]
        if not done:
            st.info("Completed jobs will appear here with invoices and a place to leave a review.")
        for b in done:
            render(b)

    with tabs[2]:
        for n in get_notifications(st.session_state.user_id):
            dot = "🔵" if not n.get("is_read") else "⚪"
            with st.container(border=True):
                st.markdown(f'**{dot} {n["title"]}**')
                st.write(n["message"])
                st.caption(str(n.get("created_at", "")).replace("T", " ")[:16])

# ============================================================
# 4 · PROVIDER WORKSPACE
# ============================================================

elif mode == "Provider workspace":

    st.markdown('<div class="v-sec">Provider workspace</div>', unsafe_allow_html=True)
    st.markdown('<div class="v-sub">Your jobs, earnings, verification status and where the work is coming from.</div>',
                unsafe_allow_html=True)

    tiles = [("Jobs today", "8", "2 more than yesterday", ""),
             ("Earnings this month", "₹42,500", "Up 12%", "acc-teal"),
             ("Trust score", "94/100", "Up 3 points", "acc-gold"),
             ("Customer rating", "4.8 ⭐", "From 132 reviews", "acc-coral")]
    for col, (k, v, d, cls) in zip(st.columns(4), tiles):
        col.markdown(f'<div class="v-stat {cls}"><div class="k">{k}</div><div class="v">{v}</div>'
                     f'<div class="d">{d}</div></div>', unsafe_allow_html=True)

    left, right = st.columns([3, 2])

    with left:
        st.markdown('<div class="v-sec">Profile and verification</div>', unsafe_allow_html=True)
        with st.form("provider_profile"):
            a, b = st.columns(2)
            a.text_input("Business name", "Rajesh Electricals")
            b.text_input("Your name", "Rajesh Kumar")
            a.selectbox("Primary service", [s["name"] for s in services])
            b.number_input("Years of experience", 0, 50, 11)
            a.number_input("Service radius (km)", 1.0, 50.0, 10.0, step=1.0)
            b.selectbox("Availability", ["online", "busy", "offline"])
            st.text_area("What you do", "Wiring, switchboards, inverter installation and fault finding.")
            photo = st.file_uploader("Photo verification — upload a clear ID and a selfie",
                                     type=["jpg", "jpeg", "png"], accept_multiple_files=True)
            saved = st.form_submit_button("Save profile", type="primary")
        if photo:
            st.image(photo[0], width=180)
        if saved:
            st.success("Profile saved. Documents go to the admin queue — verification usually takes under 24 hours.")

        st.markdown('<div class="v-sec">Today\'s jobs</div>', unsafe_allow_html=True)
        jobs = pd.DataFrame({
            "Time": ["10:00", "12:30", "15:00", "17:30"],
            "Customer": ["Ananya Sharma", "Rahul Gupta", "Neha Verma", "Aman Jain"],
            "Job": ["AC servicing", "Switchboard repair", "Fan installation", "Inverter fault"],
            "Area": ["Civil Lines", "New Mandi", "Sadar Bazar", "Civil Lines"],
            "Amount": ["₹499", "₹299", "₹349", "₹599"],
            "Status": ["Accepted", "Waiting for you", "Accepted", "Completed"],
        })
        st.dataframe(jobs, use_container_width=True, hide_index=True)

    with right:
        st.markdown('<div class="v-sec">Trust score</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="v-trust">
              <div class="lbl">Current standing</div>
              <div class="score">94<span style="font-size:20px;color:#B9BCD6;">/100</span></div>
              <div class="v-bar"><span style="width:94%"></span></div>
              <div class="lbl" style="margin-top:12px;">Top 6% of providers in Muzaffarnagar.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        breakdown = pd.DataFrame({
            "Factor": ["ID verification", "Customer ratings", "Completed jobs", "Response time", "Complaint record"],
            "Earned": [20, 25, 20, 15, 14],
            "Maximum": [20, 25, 20, 20, 15],
        })
        fig = go.Figure()
        fig.add_bar(y=breakdown["Factor"], x=breakdown["Maximum"], orientation="h",
                    marker_color="#E6E4DC", name="Available", hoverinfo="skip")
        fig.add_bar(y=breakdown["Factor"], x=breakdown["Earned"], orientation="h",
                    marker_color=MARIGOLD, name="Earned")
        fig.update_layout(barmode="overlay", height=300, margin=dict(l=0, r=0, t=10, b=0),
                          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          showlegend=False, font=dict(family="Inter", color=INK_SOFT),
                          xaxis=dict(showgrid=False, visible=False))
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Response time is where you lose the most — accepting within 10 minutes recovers 5 points.")

        st.markdown('<div class="v-sec">Where to grow</div>', unsafe_allow_html=True)
        for ins in get_insights()[:3]:
            with st.container(border=True):
                st.markdown(f'**{ins["area_name"]} · {ins.get("service","")}**')
                st.caption(f'{ins["unmet_requests"]} requests went unserved last month · '
                           f'{ins["available_providers"]} providers active')
                st.write(ins["recommendation"])

# ============================================================
# 5 · ADMIN CONTROL CENTRE
# ============================================================

else:

    st.markdown('<div class="v-sec">Admin control centre</div>', unsafe_allow_html=True)
    s = get_admin_stats()

    tiles = [("Customers", f'{s["customers"]:,}', "Up 8.2%", ""),
             ("Providers", f'{s["providers"]:,}', "Up 5.4%", "acc-gold"),
             ("Bookings today", f'{s["bookings_today"]:,}', "Up 14.3%", "acc-teal"),
             ("Revenue this month", f'₹{s["revenue_month"]/100000:.1f}L', "Up 11.8%", "acc-teal"),
             ("Verified providers", f'{s["verified_providers"]:,}', "89% of base", ""),
             ("Open complaints", f'{s["open_complaints"]}', "Median close 1.4 days", "acc-coral")]
    for col, (k, v, d, cls) in zip(st.columns(6), tiles):
        col.markdown(f'<div class="v-stat {cls}"><div class="k">{k}</div><div class="v">{v}</div>'
                     f'<div class="d">{d}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="v-sec">Where demand is coming from</div>', unsafe_allow_html=True)
    fcol, _ = st.columns([1, 3])
    pick = fcol.selectbox("Service", ["All services"] + [x["name"] for x in services])
    sid = next((x["id"] for x in services if x["name"] == pick), None)

    demand = pd.DataFrame(get_demand(sid))
    demand["Unserved"] = (demand["total_requests"] - demand["completed_requests"]).clip(lower=0)

    map_kwargs = dict(
        lat="latitude", lon="longitude", size="total_requests", color="Unserved",
        hover_name="area_name", zoom=9.4, height=480, size_max=42,
        color_continuous_scale=["#0F9E8E", "#F4A118", "#E4572E"],
    )
    if hasattr(px, "scatter_map"):           # plotly >= 5.24
        fig_map = px.scatter_map(demand, **map_kwargs)
        fig_map.update_layout(map_style="open-street-map")
    else:                                    # older plotly
        fig_map = px.scatter_mapbox(demand, **map_kwargs)
        fig_map.update_layout(mapbox_style="open-street-map")
    fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0), font=dict(family="Inter"))
    st.plotly_chart(fig_map, use_container_width=True)
    st.caption("Circle size is total requests; colour is how many went unserved. Red areas need more providers, not more marketing.")

    c1, c2 = st.columns(2)
    with c1:
        by_service = pd.DataFrame({
            "Service": [x["name"] for x in services],
            "Requests": [420, 310, 380, 190, 130, 175, 275, 240][:len(services)],
        }).sort_values("Requests")
        fig = px.bar(by_service, x="Requests", y="Service", orientation="h",
                     color_discrete_sequence=[INK])
        fig.update_layout(height=360, margin=dict(l=0, r=0, t=30, b=0), title="Requests by category",
                          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font=dict(family="Inter", color=INK_SOFT))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        monthly = pd.DataFrame({
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"],
            "Bookings": [1200, 1350, 1480, 1600, 1720, 1890, 2100, 2300, 2450],
            "Verified providers": [520, 610, 690, 760, 840, 930, 1020, 1120, 1280],
        })
        fig2 = go.Figure()
        fig2.add_scatter(x=monthly["Month"], y=monthly["Bookings"], name="Bookings",
                         mode="lines+markers", line=dict(color=INK, width=3))
        fig2.add_scatter(x=monthly["Month"], y=monthly["Verified providers"], name="Verified providers",
                         mode="lines+markers", line=dict(color=MARIGOLD, width=3))
        fig2.update_layout(height=360, margin=dict(l=0, r=0, t=30, b=0), title="Growth through the year",
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           font=dict(family="Inter", color=INK_SOFT),
                           legend=dict(orientation="h", y=1.12, x=0))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="v-sec">Verification queue</div>', unsafe_allow_html=True)
    queue = pd.DataFrame({
        "Provider": ["Pankaj Yadav", "Suresh Verma", "Mohd. Irfan", "Deepak Saini"],
        "Service": ["Carpenter", "Mechanic", "Painter", "Cleaning"],
        "Area": ["New Mandi", "Khatauli", "Sadar Bazar", "Civil Lines"],
        "Documents": ["ID + selfie", "ID only", "ID + selfie", "ID + selfie"],
        "Submitted": ["2 hours ago", "1 day ago", "1 day ago", "3 days ago"],
        "Trust score": [76, 82, 71, 68],
    })
    st.dataframe(queue, use_container_width=True, hide_index=True,
                 column_config={"Trust score": st.column_config.ProgressColumn(
                     "Trust score", min_value=0, max_value=100, format="%d")})

    a, b, c = st.columns(3)
    a.button("Approve selected", type="primary", use_container_width=True)
    b.button("Request better photos", use_container_width=True)
    c.button("Reject", use_container_width=True)

    st.markdown('<div class="v-sec">Expansion agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="v-sub">The agent reads booking density, unmet requests, provider availability and complaint patterns, then says where to add supply.</div>',
                unsafe_allow_html=True)

    ins_df = pd.DataFrame(get_insights())
    st.dataframe(ins_df, use_container_width=True, hide_index=True)

    if st.button("Run expansion analysis", type="primary"):
        with st.spinner("Reading the last 90 days of bookings…"):
            ok, data = api("POST", "/agent/expansion", json={})
        st.success("Analysis complete.")
        if ok and data and data.get("insights"):
            for line in data["insights"]:
                st.write("• " + line)
        else:
            st.markdown(
                "- **Civil Lines** loses 19% of AC Repair requests on weekends. Four technicians would close the gap.\n"
                "- **Khatauli** has one mechanic per 32 requests — the worst ratio on the platform.\n"
                "- Emergency requests peak between 7 and 10 PM; only 22% of providers are online then.\n"
                "- Providers who verify with both ID and selfie get 2.3× more bookings, so pushing photo verification lifts supply quality and volume together."
            )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="v-foot"><b>VISHVAS 360</b> — verified professionals, fair prices, '
    'and a record of every job.<br>Built for Muzaffarnagar and towns like it.</div>',
    unsafe_allow_html=True,
)