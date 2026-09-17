# Backend and database connection

The Streamlit app can now synchronise its marketplace snapshot through FastAPI. Set:

```bash
# frontend/.env or shell environment
VISHWAS_API_URL=http://127.0.0.1:8000
```

Start the database-backed API from the repository root:

```bash
cp .env.example .env
# add SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY
# run backend/schema.sql in the Supabase SQL editor
uvicorn backend.sync_api:app --reload
```

Then start Streamlit in a second terminal:

```bash
cd frontend
streamlit run app.py
```

Every booking, payment, verification, moderation, notification, and reminder mutation is first written to the existing local JSON store and then sent to `PUT /sync/state`. On startup, the app loads the saved snapshot from `GET /sync/state`. If the API is unavailable, the demo continues in offline mode and shows no credentials in the browser.

For production, replace the snapshot endpoint with authenticated user-scoped relational writes and enable Supabase Row Level Security. Do not expose `SUPABASE_SERVICE_ROLE_KEY` to Streamlit or client-side code.
