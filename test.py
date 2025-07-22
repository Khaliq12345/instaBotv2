import httpx


def get_followers(user_id: str):
    headers = {
        "accept": "application/json",
        "x-access-key": "key",
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
        print(len(followers))


if __name__ == "__main__":
    try:
        get_followers("347827209")
    except Exception as e:
        print(f"Error - {e}")
