# VISHVAS 360 — AI-Powered Trusted Local Service Marketplace

## Files
| File | Purpose |
|---|---|
| `app.py` | Home page with three portal boxes (Service Provider / Customer / Admin) |
| `customer.py` | AI chatbot booking, voice booking, multilingual UI, emergency mode, payments, reminders |
| `service_provider.py` | Job requests, trust score, photo/KYC verification, demand heatmap, expansion advice, earnings |
| `admin.py` | KPIs, provider moderation, bookings, demand intelligence, verification queue, revenue, broadcasts |
| `core.py` | Shared data store, i18n, AI matching engine, trust scoring, payments, notifications, theme |

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```
Admin demo PIN: **1234**

## Notes
- Data is seeded and stored as JSON in `./data/` so state survives restarts. Delete the folder to reset.
- Swap `core.ai_reply()` for an LLM call and the voice transcript box for Whisper/Google STT to go live.
- Replace `core.process_payment()` with Razorpay/Stripe SDK calls for real transactions.
