from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

def create_dashboard_router(state_engine):
    router = APIRouter()

    @router.get("/")
    async def root():
        return {"message": "Dashboard is running. Visit /stats, /trace, or /errors endpoints."}

    @router.get("/stats")
    async def get_stats():
        with state_engine.metrics_lock:
            return JSONResponse(content=state_engine.metrics)

    @router.get("/trace")
    async def get_trace():
        with state_engine.traces_lock:
            recent_trace = list(state_engine.traces)[-100:]
            traces_formatted = [{"line": t[0], "path": t[1]} for t in recent_trace]
            return {"traces": traces_formatted}

    @router.get("/errors")
    async def get_errors():
        with state_engine.errors_lock:
            recent_errors = list(state_engine.errors)[-100:]
            errors_formatted = [{"processor": e[0], "error": e[1]} for e in recent_errors]
            return {"errors": errors_formatted}

    return router


def create_dashboard_app(state_engine):
    app = FastAPI(title="Dataflow Observability Dashboard")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    dashboard_router = create_dashboard_router(state_engine)
    app.include_router(dashboard_router, prefix="/api")

    return app
