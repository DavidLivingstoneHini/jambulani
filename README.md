# Jambulani — Customized Football Jerseys

Full-stack e-commerce application for customized football jerseys.
Built with **Nuxt 4** (Vue 3 + TypeScript) on the frontend and **Django REST Framework** on the backend.

---

## Tech Stack

| Layer    | Technology                                      |
|----------|-------------------------------------------------|
| Frontend | Nuxt 4, Vue 3, TypeScript, Tailwind CSS, Pinia  |
| Backend  | Django 5.1.4, Django REST Framework, PostgreSQL   |
| Auth     | Custom JWT with HttpOnly cookies + token rotation |
| Infra    | Docker + Docker Compose                         |

---

## Prerequisites

You only need two things installed:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) — runs the entire backend automatically
- [Node.js 20+](https://nodejs.org/) — runs the frontend dev server

> No Python installation required — Python 3.11 runs inside Docker.

> **Why Python 3.11?** Some dependencies (notably Pillow) do not yet provide pre-built wheels for Python 3.13/3.14, which means they require compiling from source and additional system dependencies. Python 3.11 was chosen for full ecosystem compatibility and stability across all platforms.


---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/DavidLivingstoneHini/jambulani.git
cd jambulani
```

---

### 2. Start the backend with Docker

The backend container handles everything automatically on first boot:
migrations, static files, and demo data (including the admin account), make sure you have your docker running.

```bash
cd backend
cp .env.example .env
docker compose up --build
```

That's it. Wait for this line in the logs:

```
PostgreSQL ready.
Redis ready.
seeding complete.
```

The backend is now running at **http://localhost:8000**

> **Note:** The first build takes ~60 seconds to pull images and install dependencies.
> Subsequent starts are instant.

---

### 3. Start the frontend

Open a **new terminal tab** and run:

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

The frontend is now running at **http://localhost:3000**

---

## Login Credentials

### Django Admin

URL: **http://localhost:8000/admin**

| Field    | Value                  |
|----------|------------------------|
| Email    | `admin@jambulani.com`  |
| Password | `admin123`             |

### Customer Account (for testing the storefront)

Register a new account at **http://localhost:3000/register**, or use the API directly:

```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "reviewer@test.com",
    "first_name": "Test",
    "last_name": "Reviewer",
    "password": "StrongPass123!",
    "password_confirm": "StrongPass123!"
  }'
```

---

## What Gets Created Automatically

When Docker starts for the first time, `seed_data` populates the database with:

- **16 products** (8 featured on homepage) with full details
- **5 leagues** — Champions League, Europa League, Copa America, Asian Cup, African Nations Cup
- **6 collections** — Kids, Large Sizes, Goalkeeper, Authentic/Pro Player, Shorts, Socks
- **3 patches** — Champions League badge, Europa League badge, No Patch
- **1 size chart**
- **Admin superuser** — `admin@jambulani.com` / `admin123`

---

## Adding Images

Add images for the seeded Products through the Django Admin Panel:
**Admin → Store → Products → [select product] → Product Images → Upload**

---

## Stopping and Restarting

```bash
# Stop everything
docker compose down

# Restart (data is preserved in Docker volumes)
docker compose up

# Full reset — wipes the database and starts fresh
docker compose down -v
docker compose up --build
```

---

## API Reference

All endpoints are prefixed `/api/v1/`.

| Method            | Endpoint                        | Description                        |
|-------------------|---------------------------------|------------------------------------|
| `GET`             | `/products/`                    | List products (`?search=`, `?league=`, `?collection=`) |
| `GET`             | `/products/featured/`           | Featured products for homepage     |
| `GET`             | `/products/{slug}/`             | Product detail                     |
| `GET`             | `/leagues/`                     | All active leagues                 |
| `GET`             | `/collections/`                 | All active collections             |
| `GET`             | `/cart/`                        | View current cart                  |
| `POST`            | `/cart/items/`                  | Add item to cart                   |
| `PATCH`           | `/cart/items/{id}/`             | Update cart item quantity          |
| `DELETE`          | `/cart/items/{id}/`             | Remove cart item                   |
| `DELETE`          | `/cart/clear/`                  | Empty the cart                     |
| `POST`            | `/auth/register/`               | Create account                     |
| `POST`            | `/auth/login/`                  | Login (sets HttpOnly cookies)      |
| `POST`            | `/auth/logout/`                 | Logout (clears cookies)            |
| `POST`            | `/auth/refresh/`                | Rotate refresh token               |
| `GET` / `PATCH`   | `/auth/me/`                     | Get / update profile               |
| `POST`            | `/auth/change-password/`        | Change password                    |
| `POST`            | `/newsletter/subscribe/`        | Newsletter signup                  |
| `GET`             | `/health/`                      | Comprehensive health check         |
| `GET`             | `/metrics/`                     | Prometheus metrics (debug only     |

---

## Backend Commands
```bash
# View logs for all services
docker compose logs -f

# View specific service logs
docker compose logs -f backend
docker compose logs -f celery_worker
docker compose logs -f redis

# Run Django management commands
docker compose exec backend python manage.py shell
docker compose exec backend python manage.py dbshell

# Monitor Redis
docker compose exec redis redis-cli monitor
docker compose exec redis redis-cli info stats

# Check Celery tasks
docker compose exec celery_worker celery -A config inspect active
docker compose exec celery_worker celery -A config inspect scheduled

# Run manual Celery task
docker compose exec backend python manage.py shell
>>> from store.tasks import send_newsletter_confirmation
>>> send_newsletter_confirmation.delay('test@example.com')
```
---

## Health Check & Monitoring

```bash
# Comprehensive health check
curl http://localhost:8000/health/

# Check cache headers
curl -I http://localhost:8000/api/v1/products/featured/

# View rate limit headers
curl -I http://localhost:8000/api/v1/products/

# Prometheus metrics (debug mode only)
curl http://localhost:8000/metrics/
```


## Troubleshooting

**Docker won't start — port 8000 already in use**
```bash
# Find and kill whatever is using port 8000
# macOS / Linux:
lsof -ti:8000 | xargs kill -9
# Windows (PowerShell):
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Redis connection refused**
```bash
# Check if Redis is running
docker compose ps redis

# View Redis logs
docker compose logs redis

# Restart Redis
docker compose restart redis
```

**Celery tasks not executing**
```bash
# Check Celery worker status
docker compose ps celery_worker

# View Celery logs
docker compose logs celery_worker

# Restart Celery
docker compose restart celery_worker
```

**Cache not working (always MISS)**
```bash
# Check Redis memory usage
docker compose exec redis redis-cli info memory

# Clear Redis cache
docker compose exec redis redis-cli FLUSHALL

# Verify cache is working
docker compose exec redis redis-cli monitor
```

**Admin page looks unstyled (plain HTML)**
```bash
# Re-collect static files inside the running container
docker compose exec backend python manage.py collectstatic --noinput
docker compose restart backend
```

**Frontend can't reach the backend (network error)**
Make sure `frontend/.env` contains:
```
NUXT_PUBLIC_API_BASE=http://localhost:8000/api/v1
NUXT_PUBLIC_MEDIA_BASE=http://localhost:8000
```

**Database is empty / seed data missing**
```bash
# Re-run seed manually inside the running container
docker compose exec backend python manage.py seed_data
```

**Want a completely fresh start**
```bash
docker compose down -v   # -v removes volumes (wipes database)
docker compose up --build
```
