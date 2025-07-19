from supabase import create_client, Client
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL") or ""
SUPABASE_KEY = os.getenv("SUPABASE_KEY") or ""


def get_supabase_session() -> Client:
    return create_client(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_KEY)


def connect_user_profile(username: str, profile_id: str):
    # Date
    today = datetime.now(timezone.utc).isoformat()
    # Supabase
    supabase = get_supabase_session()
    # Insert
    supabase.table("user_profile_links").insert(
        {
            "profile_id": profile_id,
            "username": username,
        }
    ).execute()
    # Update
    supabase.table("scraped_account").update(
        {
            "last_interaction_date": today,
        }
    ).eq("profile_id", profile_id).execute()


if __name__ == "__main__":
    connect_user_profile("hafiz", "hafiz64")
