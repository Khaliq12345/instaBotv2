import sys

sys.path.append("..")

import httpx
from src.core.config import HIKERAPI_TOKEN, SUPABASE_KEY, SUPABASE_URL
from supabase import create_client, Client


def get_supabase_session() -> Client:
    return create_client(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_KEY)


def save_followers(followers: list[dict]) -> None:
    try:
        client = get_supabase_session()
        for follower in followers:
            try:
                client.table("scraped_account").insert(follower).execute()
            except Exception as e:
                print(f"Error - User already exists - {e}")
    except Exception as e:
        print(f"Error saving user to DB - {e}")


def parse_followers(followers: list[dict]) -> list[dict]:
    outputs = []
    for follower in followers:
        outputs.append(
            {
                "profile_id": follower.get("id"),
                "profile_link": f"https://www.instagram.com/{follower.get('username')}",
            }
        )
    return outputs


def get_followers(user_id: str):
    headers = {
        "accept": "application/json",
        "x-access-key": HIKERAPI_TOKEN,
    }

    params = {
        "user_id": user_id,
    }

    response = httpx.get(
        "https://api.hikerapi.com/gql/user/followers/chunk",
        params=params,
        headers=headers,
    )
    response.raise_for_status()
    json_data = response.json()
    if isinstance(json_data, list):
        followers = json_data[0]
        parsed_followers = parse_followers(followers)
        if parsed_followers:
            save_followers(parsed_followers)


if __name__ == "__main__":
    try:
        get_followers("347827209")
    except Exception as e:
        print(f"Error - {e}")
