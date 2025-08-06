import sys

sys.path.append("..")

from src.supabase_service.app import supabase
from datetime import datetime, timezone

def connect_user_profile(username: str, profile_id: str):
    # Date
    today = datetime.now(timezone.utc).isoformat()
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
    connect_user_profile("hafiz", "3118281")
