# VISHVAS 360 synthetic dataset

These JSON files support the offline Streamlit demo. All names, coordinates, prices, bookings, and metrics are synthetic examples created for development and demonstration only.

## Files

| File | Purpose |
| --- | --- |
| `providers.json` | Provider profiles, service skills, availability, verification flags, and metrics. |
| `bookings.json` | Historical and active service requests used by matching, analytics, and earnings views. |
| `notifications.json` | Local notification inbox. |
| `reminders.json` | Local reminder schedule. |
| `service_requests.json` | Normalized training/analytics examples with multilingual request text, intent, urgency, and labels. |
| `reviews.json` | Synthetic review events used to demonstrate reputation analytics. |
| `demand.json` | City/locality/service demand and supply observations for heatmaps and expansion insights. |

## Normalized request fields

`request_id`, `text`, `language`, `city`, `zone`, `service`, `problem_type`, `priority`, `channel`, `lat`, `lon`, and `provider_skill`.

The request examples intentionally include English, Hindi, Hinglish, Marathi, Gujarati, and Tamil phrasing. They are not a substitute for a production-labelled corpus; validate consent, language coverage, and model quality before using them for training.
