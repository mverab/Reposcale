"""Event ingestion API."""

from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

events_store = []


class Event(BaseModel):
    page: str
    referrer: str | None = None
    timestamp: datetime | None = None


@router.post("/")
def ingest_event(event: Event):
    if event.timestamp is None:
        event.timestamp = datetime.utcnow()
    events_store.append(event.model_dump())
    return {"status": "received", "count": len(events_store)}


@router.get("/count")
def event_count():
    return {"count": len(events_store)}
