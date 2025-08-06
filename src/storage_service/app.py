import sys

sys.path.append("..")

from src.supabase_service.app import supabase
import os

BUCKET_NAME = "sessions"


def check_session_is_available(username: str) -> bool:
    try:
        response = supabase.storage.from_(BUCKET_NAME).list()
        user_files = [
            f["name"] for f in response if f["name"].startswith(f"{username}_")
        ]
        return len(user_files) > 0
    except Exception as e:
        print(f"Erreur check_session_is_available: {e}")
        return False


def get_session(username: str, output_path: str) -> bool:
    try:
        response = supabase.storage.from_(BUCKET_NAME).list()
        user_files = [
            f["name"] for f in response if f["name"].startswith(f"{username}_")
        ]
        if not user_files:
            print("Aucun fichier trouvé pour ce username.")
            return False
        user_files.sort(
            key=lambda x: int(x.rsplit("_", 1)[-1].split(".")[0]), reverse=True
        )
        latest_file = user_files[0]
        data = supabase.storage.from_(BUCKET_NAME).download(latest_file)
        with open(output_path, "wb") as f:
            f.write(data)
        print(f"Session téléchargée : {latest_file}")
        return True
    except Exception as e:
        print(f"Erreur get_session: {e}")
        return False


def store_session(file_path: str):
    filename = os.path.basename(file_path)
    try:
        with open(file_path, "rb") as f:
            supabase.storage.from_(BUCKET_NAME).upload(filename, f, {"upsert": "true"})
        print(f"Session uploadée : {filename}")
    except Exception as e:
        print(f"Erreur store_session: {e}")
