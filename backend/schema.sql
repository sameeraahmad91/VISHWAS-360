-- VISHVAS 360: minimal Supabase schema for the API and Streamlit sync layer
-- Run this in the Supabase SQL editor. Keep the service-role key server-side.

create table if not exists public.app_state (
  state_key text primary key,
  payload jsonb not null,
  updated_at timestamptz not null default now()
);

create index if not exists app_state_updated_at_idx on public.app_state (updated_at desc);

-- The API's relational routes expect these tables. Create the full domain schema
-- in your Supabase project before enabling the corresponding production routes.
-- app_state is intentionally independent so the offline demo can be promoted
-- without changing its seeded JSON shape first.
