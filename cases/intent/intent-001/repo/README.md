# LiveMetrics

Real-time web analytics dashboard for small teams.

## Overview

LiveMetrics streams visitor data to a live dashboard using WebSocket connections. See your traffic, top pages, and referrers update in real time.

## Architecture

- **Backend**: FastAPI with WebSocket support
- **Data pipeline**: Event ingestion → aggregation → real-time push
- **Frontend**: React dashboard (planned)

## Quick start

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Roadmap

- [x] Event ingestion API
- [ ] Real-time WebSocket streaming
- [ ] Live dashboard UI
- [ ] Alerting rules
