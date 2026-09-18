-- Run this in the Supabase SQL editor once.
-- The application does not execute schema changes automatically.

insert into public.service_categories (name, description) values
('Electrician','Wiring, switches, fans and electrical repairs'),
('Plumber','Pipes, taps, leaks and drainage'),
('AC Repair','Cooling, servicing and gas refill'),
('Carpenter','Furniture, doors and woodwork'),
('Painter','Walls, paint and whitewashing'),
('Appliance Repair','Fridge, washing machine, oven and TV'),
('Cleaning','Home, office and deep cleaning'),
('Mechanic','Car, bike, scooter and vehicle repair')
on conflict (name) do nothing;

create index if not exists idx_provider_services_service on public.provider_services(service_id, provider_id);
create index if not exists idx_bookings_customer_created on public.bookings(customer_id, created_at desc);
create index if not exists idx_bookings_provider_status on public.bookings(provider_id, status, created_at desc);
create index if not exists idx_notifications_user_unread on public.notifications(user_id, is_read, created_at desc);
