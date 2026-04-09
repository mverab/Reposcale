"""LiveMetrics — main application."""

from fastapi import FastAPI

from app.ingest import router as ingest_router
from app.reports import router as reports_router

app = FastAPI(title="LiveMetrics", version="0.3.0")

app.include_router(ingest_router, prefix="/api/events", tags=["events"])
app.include_router(reports_router, prefix="/api/reports", tags=["reports"])


@app.get("/health")
def health():
    return {"status": "ok"}
