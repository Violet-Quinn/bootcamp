from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import threading
from typing import Any

def create_app(shared_state: Any) -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.post("/upload")
    async def upload_file(file: UploadFile = File(...)):
        file_location = f"watch_dir/unprocessed/{file.filename}"
        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)
        return {"info": f"File '{file.filename}' saved at {file_location}"}

    @app.get("/")
    def root() -> dict[str, str]:
        return {
            "message": "Observability dashboard is running. Use /stats, /trace, /errors, /files/status, /files/history endpoints."
        }

    @app.get("/stats")
    def get_stats() -> Any:
        return shared_state.get_metrics()

    @app.get("/trace")
    def get_trace() -> Any:
        return shared_state.get_traces()

    @app.get("/errors")
    def get_errors() -> Any:
        return shared_state.get_errors()


    @app.get("/files/status")
    def get_files_status() -> dict:
        counts = shared_state.get_folder_counts()
        current = shared_state.get_current_file()
        return {
            "folder_counts": counts,
            "current_file": current,
        }

    @app.get("/files/history")
    def get_files_history() -> list:
        return shared_state.get_processed_file_history()

    return app

def run_dashboard(shared_state: Any, host: str = "127.0.0.1", port: int = 8000) -> None:
    app = create_app(shared_state)
    uvicorn.run(app, host=host, port=port, log_level="info")

def start_dashboard_thread(shared_state: Any) -> None:
    thread = threading.Thread(target=run_dashboard, args=(shared_state,), daemon=False)
    thread.start()
