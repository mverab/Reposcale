"""Batch report generation — the active product direction."""

import csv
import io
from datetime import datetime

from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

router = APIRouter()


def _filter_events(events: list, start: datetime, end: datetime) -> list:
    return [
        e for e in events
        if start <= datetime.fromisoformat(str(e["timestamp"])) <= end
    ]


@router.get("/csv")
def export_csv(
    start: datetime = Query(...),
    end: datetime = Query(...),
):
    from app.ingest import events_store

    filtered = _filter_events(events_store, start, end)

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["page", "referrer", "timestamp"])
    writer.writeheader()
    for event in filtered:
        writer.writerow(event)

    output.seek(0)
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=report.csv"},
    )


@router.get("/summary")
def summary_report(
    start: datetime = Query(...),
    end: datetime = Query(...),
):
    from app.ingest import events_store

    filtered = _filter_events(events_store, start, end)
    pages = {}
    for e in filtered:
        pages[e["page"]] = pages.get(e["page"], 0) + 1

    return {
        "period": {"start": str(start), "end": str(end)},
        "total_events": len(filtered),
        "top_pages": sorted(pages.items(), key=lambda x: -x[1])[:10],
    }
