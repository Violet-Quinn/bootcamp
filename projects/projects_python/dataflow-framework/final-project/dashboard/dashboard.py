from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

CACHE_CONTROL_HEADERS = {
    "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
    "Pragma": "no-cache",
    "Expires": "0",
}

def create_dashboard_router(state_engine):
    router = APIRouter()

    @router.get("/")
    async def root():
        return {"message": "Dashboard is running. Visit /stats, /trace, or /errors endpoints."}

    @router.get("/stats")
    async def get_stats():
        with state_engine.metrics_lock:
            content = dict(state_engine.metrics)
        return JSONResponse(content=content, headers=CACHE_CONTROL_HEADERS)

    @router.get("/trace")
    async def get_trace():
        with state_engine.traces_lock:
            recent_trace = list(state_engine.traces)[-100:]
            traces_formatted = [{"line": t[0], "path": t[1]} for t in recent_trace]
        return JSONResponse(content={"traces": traces_formatted}, headers=CACHE_CONTROL_HEADERS)

    @router.get("/errors")
    async def get_errors():
        with state_engine.errors_lock:
            recent_errors = list(state_engine.errors)[-100:]
            errors_formatted = [{"processor": e[0], "error": e[1]} for e in recent_errors]
        return JSONResponse(content={"errors": errors_formatted}, headers=CACHE_CONTROL_HEADERS)

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
