# Heatmap and expansion AI

The provider portal now computes demand from the current booking stream every time it renders. A newly created booking is persisted through `PUT /sync/state`, so the next refresh reflects the new locality/service demand and supply gap.

- **Heatmap intelligence:** demand, supply, gap, revenue, heat percentage, and geospatial coordinates are recomputed from live booking/provider state.
- **Expansion intelligence:** `expansion_recommendations()` ranks the provider's service by unmet demand, supply gap, revenue, and potential uplift, then produces locality-level recommendations.
- Use the provider portal's refresh/rerun action after a booking arrives to see the updated result. For a hosted deployment, replace the snapshot state with relational Supabase queries or a websocket event stream.

The API AI gateway provides:

- `POST /ai/understand` for chatbot and voice transcript intent classification.
- `POST /voice/transcribe` for optional faster-whisper transcription.
