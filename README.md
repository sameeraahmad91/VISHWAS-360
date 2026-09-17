# VISHVAS 360

AI-powered trusted local service marketplace for Indian cities. The project includes a Streamlit product demo with customer, service-provider, and admin portals, plus a FastAPI/Supabase backend contract for production integration.

## What is included

- Multilingual customer booking (English, Hindi, Marathi, Gujarati, Tamil)
- Natural-language intent detection for eight service categories
- Emergency dispatch mode with priority pricing
- Trust and reputation scoring across ratings, completion, punctuality, complaints, verification, job volume, and tenure
- Provider matching using trust, distance, price, emergency readiness, and language fit
- Voice-booking workflow with an editable transcript step for Whisper/STT integration
- Provider verification workflow for KYC, selfie/photo, police verification, and work proof
- Demand heatmaps and expansion recommendations by city, locality, service, demand, and supply
- Simulated payments, notifications, reminders, bookings, reviews, and admin moderation
- Seeded, domain-specific JSON data that can be replaced by Supabase/PostgreSQL data

## Run the working demo

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
pip install -r frontend/requirements.txt
cd frontend
streamlit run app.py
```

The admin demo PIN is `1234`. The Streamlit app runs fully with local JSON persistence and does not require Supabase credentials.

## Run the API (optional production integration)

Copy `.env.example` to `.env`, add Supabase credentials, then run:

```bash
uvicorn backend.main:app --reload
```

The API exposes services, providers, bookings, payments, reviews, complaints, demand, business insights, notifications, and assistant endpoints. The current Streamlit demo intentionally uses the local JSON store so it remains runnable offline; the API is the integration boundary for a hosted deployment.

## Dataset

The generated dataset lives in `frontend/data/` and contains realistic but synthetic records. See `frontend/data/DATA_DICTIONARY.md` for fields and privacy notes. Never use real Aadhaar, PAN, phone numbers, selfies, or payment credentials in this repository.

## Production hardening checklist

- Replace demo PIN and local JSON persistence with Supabase Auth, Row Level Security, and PostgreSQL/PostGIS.
- Connect `core.ai_reply` to Gemini/OpenAI and use embeddings for semantic provider search.
- Connect voice transcription to Whisper and translation to IndicTrans2 or a managed translation API.
- Replace `process_payment` with Razorpay/Cashfree server-side order creation and webhook verification.
- Store uploads in private object storage and run consented liveness/identity verification.
- Add authenticated WebSockets/FCM notifications, rate limiting, audit logs, and automated tests.
