# VISHVAS 360

VISHVAS 360 is an AI-powered trusted local-services marketplace with customer, provider and admin portals. It includes multilingual text/voice intent detection, emergency dispatch, provider trust scoring, payments, notifications, verification, demand analytics and expansion insights.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
source .venv/bin/activate
pip install -r requirements.txt
pip install -r frontend/requirements.txt
cp .env.example .env
# Add SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY to .env
# Run backend/schema.sql in Supabase SQL Editor
uvicorn backend.main:app --reload
# In another terminal:
cd frontend && streamlit run app.py
```

The API remains importable without credentials and exposes `/health`; database routes return a clear 503 until Supabase is configured. Never expose the service-role key to Streamlit or the browser.

## Production integration

- `backend/schema.sql` is the complete schema for the supplied database design and seeds the eight service categories.
- `backend/ml_models.py` provides a transparent multilingual TF-IDF + Logistic Regression intent model. Add labeled production conversations before retraining or replace it with a hosted model.
- Provider matching prioritizes approved providers by computed trust score; emergency requests are surfaced through the AI response and can be extended with location/radius filtering.
- `backend/sync_api.py` remains available for the Streamlit snapshot/voice workflow and imports the same FastAPI app.
- Configure `VISHWAS_API_URL` in the frontend to synchronize the local demo with the API.

## Security checklist

Use Supabase Auth and RLS for user-facing clients, keep service-role access server-side, add payment-provider webhook verification, private document storage, rate limiting, audit logs, and authenticated WebSockets/FCM before public launch.
