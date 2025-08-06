import sys

sys.path.append("..")

from src.core.config import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client, Client


def get_supabase_session() -> Client:
    return create_client(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_KEY)


supabase = get_supabase_session()
