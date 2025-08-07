import sys

sys.path.append("..")

from src.core.config import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client, Client


def get_supabase_session() -> Client:
    return create_client(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_KEY)


def start_processus(username: str, process_id: str, status: str = "running"):
    supabase = get_supabase_session()
    return (
        supabase.table("processus")
        .upsert(
            {"username": username, "process_id": process_id, "status": status},
            on_conflict="username",
        )
        .execute()
    )


def update_status_by_username(username: str, status: str):
    supabase = get_supabase_session()
    return (
        supabase.table("processus")
        .update({"status": status})
        .eq("username", username)
        .execute()
    )

def update_status_by_process_id(process_id: str, status: str):
    supabase = get_supabase_session()
    return (
        supabase.table("processus")
        .update({"status": status})
        .eq("process_id", process_id)
        .execute()
    )


def get_status_by_process_id(process_id: str):
    supabase = get_supabase_session()
    response = (
        supabase.table("processus")
        .select("status")
        .eq("process_id", process_id)
        .limit(1)
        .execute()
    )
    if response.data:
        return response.data[0]["status"]
    return None

