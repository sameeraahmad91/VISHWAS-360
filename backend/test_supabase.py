from supabase_client import supabase

response = (
    supabase
    .table("service_categories")
    .select("*")
    .execute()
)

print(response.data)