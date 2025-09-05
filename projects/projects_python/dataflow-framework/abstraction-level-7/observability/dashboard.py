from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import threading
from typing import Any


def create_app(shared_state: Any) -> FastAPI:
    """
    Create and configure a FastAPI application for the observability dashboard.

    Args:
        shared_state (Any): The object holding metrics, traces, and errors.

    Returns:
        FastAPI: Configured FastAPI application instance.
    """
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    def root() -> dict[str, str]:
        """
        Root endpoint to verify the dashboard service is running.
        """
        return {
            "message": "Observability dashboard is running. Use /stats, /trace, or /errors endpoints."
        }

    @app.get("/stats")
    def get_stats() -> Any:
        """
        Retrieve collected metrics from the shared state.
        """
        return shared_state.get_metrics()

    @app.get("/trace")
    def get_trace() -> Any:
        """
        Retrieve execution traces from the shared state.
        """
        return shared_state.get_traces()

    @app.get("/errors")
    def get_errors() -> Any:
        """
        Retrieve logged errors from the shared state.
        """
        return shared_state.get_errors()

    return app


def run_dashboard(shared_state: Any, host: str = "127.0.0.1", port: int = 8000) -> None:
    """
    Run the observability dashboard using Uvicorn.

    Args:
        shared_state (Any): The object holding metrics, traces, and errors.
        host (str): The host address for the server.
        port (int): The port to bind the server to.
    """
    app = create_app(shared_state)
    uvicorn.run(app, host=host, port=port, log_level="info")


def start_dashboard_thread(shared_state: Any) -> None:
    """
    Start the dashboard in a separate thread to run alongside the main process.

    Args:
        shared_state (Any): The object holding metrics, traces, and errors.
    """
    thread = threading.Thread(target=run_dashboard, args=(shared_state,), daemon=False)
    thread.start()
