from supabase import create_client, Client
from config import Config

def get_supabase():
    url = Config.SUPABASE_URL
    key = Config.SUPABASE_API_KEY
    supabase: Client = create_client(url, key)
    return supabase
