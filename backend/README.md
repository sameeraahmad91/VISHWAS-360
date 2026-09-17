# FastAPI backend

The backend uses Supabase tables for production persistence. Required environment variables are documented in the root `.env.example`.

Expected tables include `profiles`, `service_categories`, `service_providers`, `provider_services`, `bookings`, `reviews`, `payments`, `complaints`, `notifications`, `demand_data`, and `business_insights`.

Start from the repository root:

```bash
uvicorn backend.main:app --reload
```

The offline Streamlit demo does not import this module, which lets a new contributor run the product without credentials. Keep the Supabase service-role key server-side only; never expose it in Streamlit or browser code.
