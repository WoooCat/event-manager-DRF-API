# Event Manager API (Django + DRF)

A Dockerized REST API to manage events and user registrations.

## 1) What is this (features)
- CRUD for events: `title`, `description`, `date`, `location`, `organizer`
- User signup & **JWT auth** (access/refresh, **rotation + blacklist**, session-bound access)
- Register to an event (idempotent) + view attendees
- “My registrations” endpoints
- **Search** across multiple fields (DB-level ILIKE)
- Swagger UI: `http://localhost:8000/api/schema/swagger/`
- Email notification after successful registration (console in dev)

## 2) Tech stack
Django 5 · DRF · SimpleJWT · drf-spectacular · PostgreSQL · Docker/Compose

## 3) Make (quick commands)
```bash
make start         # build & start DB + API
make stop          # stop stack
make migrate       # apply migrations
make logs-f    # tail logs (S=web|db)
make status        # container status
make help          # list all targets
```

## 4) Run with Docker (via Make)
```bash
make start
make migrate
# optional admin:
docker compose exec web python manage.py createsuperuser
open http://localhost:8000/api/schema/swagger/
```

## 5) Create user → get tokens → refresh
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"Passw0rd!","email":"demo@example.com"}'

# Obtain access & refresh
curl -X POST http://localhost:8000/api/auth/jwt/create/ -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"Passw0rd!"}'

# Refresh (rotation + blacklist, session-bound) → returns NEW access & refresh
curl -X POST http://localhost:8000/api/auth/jwt/refresh/ -H "Content-Type: application/json" \
  -d '{"refresh":"<REFRESH>"}'
```

## 6) Events CRUD
```bash
# List (search/filter/order/paginate)
curl -H "Authorization: Bearer <ACCESS>" \
  "http://localhost:8000/api/events/?search=kyiv&ordering=-date"

# Create
curl -X POST http://localhost:8000/api/events/ -H "Authorization: Bearer <ACCESS>" \
  -H "Content-Type: application/json" \
  -d '{"title":"PyCon","description":"talks","date":"2025-08-20T09:30:40Z","location":"Kyiv"}'

# Retrieve
curl -H "Authorization: Bearer <ACCESS>" http://localhost:8000/api/events/1/

# Update
curl -X PATCH http://localhost:8000/api/events/1/ -H "Authorization: Bearer <ACCESS>" \
  -H "Content-Type: application/json" -d '{"location":"Lviv"}'

# Delete
curl -X DELETE -H "Authorization: Bearer <ACCESS>" http://localhost:8000/api/events/1/
```

## 7) Register for an event
```bash
# No request body; just the event id in the path
curl -X POST -H "Authorization: Bearer <ACCESS>" http://localhost:8000/api/events/5/register/
```

## 8) View my registrations
```bash
# All my registrations
curl -H "Authorization: Bearer <ACCESS>" http://localhost:8000/api/registrations/

# One registration (must belong to current user)
curl -H "Authorization: Bearer <ACCESS>" http://localhost:8000/api/registrations/4/

# Organizer-centric: attendees for a single event
curl -H "Authorization: Bearer <ACCESS>" http://localhost:8000/api/events/5/attendees/
```

## 9) Search
- Single query param: search
- Case-insensitive ILIKE across: title, description, location, organizer__username
- Multiple words are ANDed; each word can match any of those fields.

## 10) Email on registration
- On successful POST /api/events/{id}/register/, an email is sent after transaction commit.
- In dev the backend is console → see messages in web logs:
```bash
make logs S=web
```