# VISHVAS 360

AI-powered trusted local service marketplace for customers, providers and administrators.

## Run locally

```bash
cp .env.example .env
# set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY
pip install -r requirements.txt
uvicorn backend.main:app --reload
# in another terminal
streamlit run frontend/app.py
```

The API is backed by the supplied Supabase schema. Without `GROQ_API_KEY`, the assistant uses a deterministic multilingual-friendly fallback, so booking discovery remains available. Real payments require a server-side gateway integration; the Streamlit Razorpay widget is explicitly demo-only.

## Core API

- `GET /health`, `/services`, `/providers`
- `POST /bookings`, `PATCH /bookings/{id}/status`
- `POST /assistant`, `/payments`, `/reviews`, `/complaints`
- `GET /notifications/{user_id}`, `/admin/stats`

Booking and payment statuses intentionally match the schema (`approved`, `success`, etc.). State transitions and completed-booking review rules are validated server-side.
