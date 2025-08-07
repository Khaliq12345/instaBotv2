from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from multiprocessing import Process
from src.bot_service.app import start_bot as run_bot
from src.supabase_service.app import start_processus, update_status_by_process_id, get_status_by_process_id

app = FastAPI(title="InstaBot v2")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
running_processes = {}

@app.post("/start-bot/{username}")
def start_bot(username: str):
    process = Process(target=run_bot, args=[username])
    process.start()
    running_processes[str(process.pid)] = process
    start_processus(username, str(process.pid), "running")
    return {"message": f"Bot started for {username}", "process_id": process.pid}

@app.post("/stop-bot/{process_id}")
def stop_bot(process_id: str):
    process = running_processes.get(process_id)
    if not process:
        raise HTTPException(status_code=404, detail="Process not found")
    process.terminate()
    process.join()
    update_status_by_process_id(process_id, "stopped")
    del running_processes[process_id]
    return {"message": f"Bot with process ID {process_id} stopped"}

@app.get("/check-status/{process_id}")
def check_status(process_id: str):
    status = get_status_by_process_id(process_id)
    if status:
        return {"process_id": process_id, "status": status}
    raise HTTPException(status_code=404, detail="Process not found")
