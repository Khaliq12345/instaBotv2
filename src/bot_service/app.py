import sys


sys.path.append("..")

from src.core.config import IG_USERNAME, IG_PASSWORD
from src.storage_service.app import (
    check_session_is_available,
    store_session,
    get_session,
)
from src.get_valid_users.app import get_valid_users
from src.connect_user_profile.app import connect_user_profile
from instagrapi import Client


def process(profile_link: str):
    # Login
    ig_client = instagram_login(IG_USERNAME, IG_PASSWORD)
    # Follow
    follow_user(ig_client, profile_link)


#
def instagram_login(username: str, password: str) -> Client:
    session_file = f"{username}.json"
    client = Client()
    #
    if check_session_is_available(username):
        get_session(username, session_file)
        try:
            client.load_settings(session_file)
            client.login(username, password)
            print("Connected With Session")
            return client
        except Exception as e:
            print(f"Expired Session: {e}")
    #
    print("Normal Login")
    client.login(username, password)
    #
    client.dump_settings(session_file)
    store_session(session_file)
    print("New Session Saved")
    return client


# Follow
def follow_user(client: Client, profile_link: str):
    print(f"Profile Link : {profile_link}")
    username = profile_link.rstrip("/").split("/")[-1]
    try:
        user_id = client.user_id_from_username(username)
        client.user_follow(user_id)
        print(f"Now Following {username}")
    except Exception as e:
        print(f"Erreur follow_user: {e}")


def start_bot():
    username = "Mark"
    # Call gvus
    profile = get_valid_users(username)
    print(f"-- Profile ;; {profile}")
    if not profile:
        return
    profile_link = profile["profile_link"]
    # Login, Follow and Like latest post
    print(f"Processing -- {profile_link}")
    process(profile_link)
    # Call cups
    # connect_user_profile(username, profile["profile_id"])


if __name__ == "__main__":
    start_bot()
