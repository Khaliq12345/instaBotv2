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
import time
import os


def process(profile_link: str):
    # Login
    ig_client = instagram_login(IG_USERNAME, IG_PASSWORD)
    # Follow
    follow_user(ig_client, profile_link)
    # Like Latest Post
    like_latest_post(ig_client, profile_link)


# Login
def instagram_login(username: str, password: str) -> Client:
    timestamp = int(time.time())
    session_file = f"{username}_{timestamp}.json"
    client = Client()
    try:
        if check_session_is_available(username):
            get_session(username, session_file)
            try:
                client.load_settings(session_file)
                client.login(username, password)
                print("Connected With Session")
                return client
            except Exception as e:
                print(f"Expired Session: {e}")
        print("Normal Login")
        client.login(username, password)
        client.dump_settings(session_file)
        store_session(session_file)
        print("New Session Saved")
    finally:
        if os.path.exists(session_file):
            os.remove(session_file)
            print(f"File Deleted {session_file}")
    return client


# Follow
def follow_user(client: Client, profile_link: str):
    try:
        username = profile_link.rstrip("/").split("/")[-1]
        print(f"username -- {username}")
        user = client.search_users(username)[0]
        user_id = user.pk
        print(f"userid -- {user_id}")
        client.user_follow(user_id)
        print(f"Now Following {username}")
    except Exception as e:
        print(f"Erreur follow_user: {e}")


# Like Latest Post
def like_latest_post(client: Client, profile_link: str):
    try:
        username = profile_link.rstrip("/").split("/")[-1]
        user = client.search_users(username)[0]
        user_id = user.pk
        medias = client.user_medias_v1(user_id, amount=1)
        if not medias:
            print(f"No post {username}")
            return
        latest_media = medias[0]
        client.media_like(latest_media.id)
        print(f"Liked latest post of {username}")
    except Exception as e:
        print(f"Erreur like_latest_post: {e}")


def start_bot():
    username = IG_USERNAME
    # Call gvus
    profile = get_valid_users(username)
    print(f"-- Profile -- {profile}")
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
