import sys

sys.path.append("..")

from src.core.config import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client, Client
from datetime import datetime, timedelta, timezone


def get_supabase_session() -> Client:
    return create_client(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_KEY)


def get_valid_users(username: str):
    # Date Limit
    today = datetime.now(timezone.utc)
    seven_days_ago = today - timedelta(days=7)
    # Supabase
    supabase = get_supabase_session()
    page_size = 100
    offset = 0
    matched_row = None
    while True:
        condition = f"last_interaction_date.is.null,last_interaction_date.gt.{seven_days_ago.isoformat()}"
        scraped_account_response = (
            supabase.table("scraped_account")
            .select("*")
            .or_(condition)
            .limit(page_size)
            .offset(offset)
            .execute()
        )
        data = scraped_account_response.data
        if not data:
            break
        for matched_row in data:
            profil_link_response = (
                supabase.table("user_profile_links")
                .select("*")
                .eq("profile_id", matched_row["profile_id"])
                .eq("username", username)
                .execute()
            )
            if not profil_link_response.data:
                return matched_row
        offset += page_size
    return None


if __name__ == "__main__":
    print(get_valid_users("hafiz"))
