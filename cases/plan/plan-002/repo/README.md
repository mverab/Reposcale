# OrderHub

Monolithic order management system with notifications and reporting.

## Modules
- `app/api/` — REST endpoints
- `app/models/` — Data models
- `app/services/` — Business logic (notifications, reports)

## Known issues
- Report generation is slow under load
- Notifications should be async but aren't
