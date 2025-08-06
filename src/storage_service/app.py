import sys

sys.path.append("..")

from src.core.config import SUPABASE_URL, SUPABASE_KEY
import os
from supabase import create_client, Client


def get_supabase_session() -> Client:
    return create_client(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_KEY)


supabase = get_supabase_session()
BUCKET_NAME = "sessions"


def check_session_is_available(username: str) -> bool:
    filename = f"{username}.json"
    try:
        response = supabase.storage.from_(BUCKET_NAME).list()
        return any(file["name"] == filename for file in response)
    except Exception as e:
        print(f"Erreur check_session_is_available: {e}")
        return False


def get_session(username: str, output_path: str) -> bool:
    filename = f"{username}.json"
    try:
        data = supabase.storage.from_(BUCKET_NAME).download(filename)
        with open(output_path, "wb") as f:
            f.write(data)
        return True
    except Exception as e:
        print(f"Erreur get_session: {e}")
        return False


def store_session(file_path: str):
    filename = os.path.basename(file_path)
    try:
        with open(file_path, "rb") as f:
            supabase.storage.from_(BUCKET_NAME).upload(
                filename, f, {"upsert": "true"}
            )
        print(f"Session uploadée : {filename}")
    except Exception as e:
        print(f"Erreur store_session: {e}")
