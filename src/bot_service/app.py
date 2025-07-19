from src.get_valid_users.app import get_valid_users
from src.connect_user_profile.app import connect_user_profile

def process(profile_link: str):
    pass

def start_bot():
    username = 'Mark'
    # Call gvus
    profile = get_valid_users(username)
    if not profile:
        return
    profile_link = profile["profile_link"]
    # Login, Follow and Like latest post
    process(profile_link)
    # Call cups
    connect_user_profile(username, profile['profile_id'])

if __name__ == "__main__":
    start_bot()
