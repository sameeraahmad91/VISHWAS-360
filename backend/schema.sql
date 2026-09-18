-- VISHVAS 360 production Supabase schema
-- Run after enabling the Supabase Auth extension. Keep the service-role key server-side.
create extension if not exists pgcrypto;

create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  full_name text not null,
  phone text,
  role text not null default 'customer' check (role in ('customer','provider','admin')),
  language text default 'English',
  created_at timestamptz default now()
);
create table if not exists public.service_categories (
  id bigint generated always as identity primary key,
  name text not null unique,
  description text,
  created_at timestamptz default now()
);
create table if not exists public.service_providers (
  id bigint generated always as identity primary key,
  profile_id uuid not null references public.profiles(id) on delete cascade,
  business_name text,
  experience_years integer default 0 check (experience_years >= 0),
  description text,
  address text,
  latitude double precision,
  longitude double precision,
  service_radius_km double precision default 10 check (service_radius_km > 0),
  verification_status text default 'pending' check (verification_status in ('pending','approved','rejected')),
  availability_status text default 'offline' check (availability_status in ('available','busy','offline')),
  profile_photo_url text,
  created_at timestamptz default now()
);
create table if not exists public.provider_services (
  id bigint generated always as identity primary key,
  provider_id bigint not null references public.service_providers(id) on delete cascade,
  service_id bigint not null references public.service_categories(id) on delete cascade,
  price numeric check (price is null or price >= 0),
  created_at timestamptz default now(),
  unique(provider_id, service_id)
);
create table if not exists public.bookings (
  id bigint generated always as identity primary key,
  customer_id uuid not null references public.profiles(id),
  provider_id bigint references public.service_providers(id),
  service_id bigint not null references public.service_categories(id),
  booking_date date not null,
  booking_time time not null,
  address text not null,
  latitude double precision,
  longitude double precision,
  description text,
  status text not null default 'pending' check (status in ('pending','accepted','rejected','on_the_way','in_progress','completed','cancelled')),
  is_emergency boolean default false,
  estimated_price numeric check (estimated_price is null or estimated_price >= 0),
  created_at timestamptz default now()
);
create table if not exists public.payments (
  id bigint generated always as identity primary key,
  booking_id bigint not null references public.bookings(id),
  customer_id uuid not null references public.profiles(id),
  amount numeric not null check (amount >= 0),
  payment_method text check (payment_method in ('upi','card','netbanking','wallet','cash')),
  payment_status text not null default 'pending' check (payment_status in ('pending','success','failed','refunded')),
  transaction_id text,
  paid_at timestamptz,
  created_at timestamptz default now()
);
create table if not exists public.reviews (
  id bigint generated always as identity primary key,
  booking_id bigint not null unique references public.bookings(id),
  customer_id uuid not null references public.profiles(id),
  provider_id bigint not null references public.service_providers(id),
  rating integer not null check (rating between 1 and 5),
  review_text text,
  created_at timestamptz default now()
);
create table if not exists public.complaints (
  id bigint generated always as identity primary key,
  booking_id bigint references public.bookings(id),
  customer_id uuid references public.profiles(id),
  provider_id bigint references public.service_providers(id),
  subject text not null,
  description text not null,
  status text not null default 'open' check (status in ('open','investigating','resolved','closed')),
  created_at timestamptz default now(),
  resolved_at timestamptz
);
create table if not exists public.notifications (
  id bigint generated always as identity primary key,
  user_id uuid not null references public.profiles(id) on delete cascade,
  title text not null,
  message text not null,
  notification_type text,
  is_read boolean default false,
  created_at timestamptz default now()
);
create table if not exists public.provider_locations (
  id bigint generated always as identity primary key,
  provider_id bigint not null unique references public.service_providers(id) on delete cascade,
  latitude double precision not null,
  longitude double precision not null,
  updated_at timestamptz default now()
);
create table if not exists public.verification (
  id bigint generated always as identity primary key,
  provider_id bigint not null references public.service_providers(id) on delete cascade,
  identity_document_url text,
  address_proof_url text,
  profile_photo_url text,
  verification_status text not null default 'pending' check (verification_status in ('pending','approved','rejected')),
  verified_by uuid references public.profiles(id),
  verified_at timestamptz,
  rejection_reason text,
  created_at timestamptz default now()
);
create table if not exists public.demand_data (
  id bigint generated always as identity primary key,
  service_id bigint not null references public.service_categories(id),
  area_name text not null,
  latitude double precision,
  longitude double precision,
  total_requests integer default 0,
  completed_requests integer default 0,
  cancelled_requests integer default 0,
  date date default current_date,
  created_at timestamptz default now()
);
create table if not exists public.business_insights (
  id bigint generated always as identity primary key,
  service_id bigint references public.service_categories(id),
  area_name text not null,
  demand_level text check (demand_level in ('low','medium','high')),
  available_providers integer default 0,
  total_requests integer default 0,
  unmet_requests integer default 0,
  recommendation text,
  created_at timestamptz default now()
);
create table if not exists public.app_state (
  state_key text primary key,
  payload jsonb not null,
  updated_at timestamptz not null default now()
);

create index if not exists bookings_customer_idx on public.bookings(customer_id, created_at desc);
create index if not exists bookings_provider_idx on public.bookings(provider_id, booking_date desc);
create index if not exists demand_area_idx on public.demand_data(area_name, date desc);
create index if not exists notifications_user_idx on public.notifications(user_id, created_at desc);

insert into public.service_categories(name, description) values
 ('Electrician','Electrical repairs, wiring and installations'),('Plumber','Pipes, taps, leaks and water systems'),('AC Repair','Air-conditioner service and gas refill'),('Carpenter','Furniture, doors and woodwork'),('Painter','Interior and exterior painting'),('Appliance Repair','Fridge, TV, washing machine and appliance repairs'),('Cleaning','Home, office, sofa and deep cleaning'),('Mechanic','Car, bike, puncture and roadside assistance')
on conflict (name) do update set description = excluded.description;
