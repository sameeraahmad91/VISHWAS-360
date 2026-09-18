-- Operational indexes for the supplied schema.
-- Run in Supabase SQL editor after the base tables are created.
create index if not exists idx_provider_services_service on public.provider_services(service_id, provider_id);
create index if not exists idx_providers_status_location on public.service_providers(verification_status, availability_status);
create index if not exists idx_bookings_customer_created on public.bookings(customer_id, created_at desc);
create index if not exists idx_bookings_provider_status on public.bookings(provider_id, status, created_at desc);
create index if not exists idx_notifications_user_unread on public.notifications(user_id, is_read, created_at desc);
create index if not exists idx_demand_service_area on public.demand_data(service_id, area_name, date desc);

-- The API expects these canonical values. This prevents accidental divergence
-- between the UI and database status vocabulary.
