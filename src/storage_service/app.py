import sys

sys.path.append("..")

from src.supabase_service.app import get_supabase_session

BUCKET_NAME = "sessions"

def check_session_is_available(username: str) -> bool:
    supabase = get_supabase_session()
    filename = f"{username}.json"
    try:
        response = supabase.storage.from_(BUCKET_NAME).list()
        return any(file["name"] == filename for file in response)
    except Exception as e:
        print(f"Erreur check_session_is_available: {e}")
        return False


def get_session(username: str, output_path: str) -> bool:
    supabase = get_supabase_session()
    filename = f"{username}.json"
    try:
        data = supabase.storage.from_(BUCKET_NAME).download(filename)
        with open(output_path, "wb") as f:
            f.write(data)
        return True
    except Exception as e:
        print(f"Erreur get_session: {e}")
        return False


def store_session(filename: str, file_path: str):
    supabase = get_supabase_session()
    try:
        with open(file_path, "rb") as f:
            supabase.storage.from_(BUCKET_NAME).upload(filename, f, {"upsert": "true"})
        print(f"Session uploadée : {filename}")
    except Exception as e:
        print(f"Erreur store_session: {e}")
