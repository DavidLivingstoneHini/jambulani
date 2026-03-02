# Jambulani — Backend API

Django REST Framework · PostgreSQL · JWT Authentication

---

## How to Run

There are two ways. Pick one.

---

### Option 1 — Docker (Recommended)

**One command. Zero setup. Works on Windows, macOS, Linux.**

> Requires: [Docker Desktop](https://www.docker.com/products/docker-desktop/) (free)

```bash
git clone <repo-url>
cd jambulani/backend
docker compose up --build
```

That's it. Docker handles Python, PostgreSQL, migrations, and seed data automatically.

| Service  | URL                           |
|----------|-------------------------------|
| API      | http://localhost:8000/api/v1/ |
| Admin    | http://localhost:8000/admin   |

**Admin login:** `admin@jambulani.com` / `admin123`

To stop: `docker compose down`

---

### Option 2 — Local Development

Runs Django directly on your machine. Still uses PostgreSQL, but only the database runs in Docker.

**Requirements:**
- Docker Desktop (for the database container)
- Python 3.11, 3.12, or 3.13
- `uv` — a modern Python package manager (replaces pip entirely)

#### Step 1 — Install uv

`uv` fetches pre-built binary packages. It never compiles from source, so there are no C compiler errors, no Visual C++ requirements, no zlib errors — on any OS, any Python version.

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Close and reopen your terminal. Verify: `uv --version`

#### Step 2 — Clone and set up

```bash
git clone <repo-url>
cd jambulani/backend

# Copy environment config
cp .env.example .env

# Install all Python dependencies
uv sync
```

`uv sync` reads `pyproject.toml` and `uv.lock`, downloads pre-built wheels, and creates a `.venv` automatically. No activation needed — `uv run` handles it.

#### Step 3 — Start PostgreSQL (Docker, database only)

```bash
docker compose -f docker-compose.db.yml up -d
```

This starts only PostgreSQL on port 5432. Your Django process runs locally.

#### Step 4 — Migrate, seed, run

```bash
uv run python manage.py migrate
uv run python manage.py seed_data
uv run python manage.py runserver
```

Or with the Makefile shortcut:
```bash
make dev   # does db + migrate + seed + runserver in one command
```

API running at: http://localhost:8000/api/v1/
Admin: http://localhost:8000/admin → `admin@jambulani.com` / `admin123`

---

## Why uv instead of pip?

This is the core fix for the wheel compilation errors reviewers hit with plain pip:

| Problem with `pip install` | How `uv` solves it |
|---|---|
| `psycopg2-binary` fails on Python 3.14 — no pre-built wheel | `uv` resolves a compatible version automatically |
| Pillow fails — "zlib not found", requires C compiler | `uv` always downloads a pre-built binary wheel |
| "Microsoft Visual C++ 14.0 required" on Windows | `uv` never compiles from source |
| Different behavior per machine (Python version, pip version) | `uv.lock` guarantees bit-for-bit identical installs everywhere |
| Slow (Pillow is 46MB to compile) | `uv` is 10–100× faster than pip |

The wheel errors you saw happen because `psycopg2-binary==2.9.9` and `Pillow==10.4.0` do not have pre-built binaries for Python 3.14. `uv` resolves `>=` ranges to a version that has a binary wheel for whatever Python you're running.

---

## Project Structure

```
backend/
├── pyproject.toml          ← All dependencies declared here
├── uv.lock                 ← Exact locked versions (committed to git)
├── .python-version         ← Tells uv which Python version to use (3.11)
├── .env.example            ← Copy to .env for local dev
├── docker-compose.yml      ← Full stack (backend + db)
├── docker-compose.db.yml   ← DB only (for local dev)
├── Makefile                ← Developer shortcuts
├── Dockerfile
├── entrypoint.sh
├── manage.py
├── config/
│   ├── settings.py         ← Single settings file, reads from .env
│   └── urls.py
├── accounts/               ← Auth app
│   ├── models.py           ← Custom User + RefreshToken
│   ├── authentication.py   ← JWT DRF authenticator
│   ├── tokens.py           ← JWT issue/decode
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
└── store/                  ← Product catalog app
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── admin.py
    ├── filters.py
    └── management/commands/seed_data.py
```

---

## API Reference

### Auth — `/api/v1/auth/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register/` | Create account |
| POST | `/auth/login/` | Login → sets HttpOnly JWT cookies |
| POST | `/auth/logout/` | Logout + revoke refresh token |
| POST | `/auth/token/refresh/` | Silent token refresh (uses cookie) |
| GET | `/auth/session/` | Check current session |
| GET/PATCH | `/auth/me/` | Get / update profile |
| POST | `/auth/password/change/` | Change password, revoke all sessions |

### Store — `/api/v1/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products/` | List products (filterable, paginated) |
| GET | `/products/{slug}/` | Product detail |
| GET | `/products/featured/` | Featured products |
| GET | `/leagues/` | All leagues |
| GET | `/collections/` | All collections |
| GET | `/patches/` | All patches |
| GET/POST | `/cart/` | Session cart |
| PATCH/DELETE | `/cart/{id}/` | Update/remove item |
| DELETE | `/cart/clear/` | Clear cart |
| POST | `/newsletter/subscribe/` | Newsletter signup |

**Filtering:**
```
GET /api/v1/products/?league=premier-league&min_price=20&max_price=80&search=arsenal&ordering=-price&page=2
```

---

## Authentication Architecture

Two-token system, zero secrets in localStorage:

| Token | Type | TTL | Storage |
|-------|------|-----|---------|
| Access token | Signed JWT (HS256) | 15 minutes | JS memory only |
| Refresh token | Opaque SHA-256 hash | 30 days | HttpOnly cookie |

**Security features:**
- Refresh token rotation on every `/token/refresh/` call
- Token reuse detection — replay of a rotated token revokes the entire family
- Password change revokes all active refresh token families
- Auth endpoints rate-limited to 10 req/min (brute-force protection)
- `Secure`, `HttpOnly`, `SameSite=Lax` cookie flags
- Constant-time login (prevents user enumeration)

---

## Troubleshooting

**Port 5432 already in use:**
Something else is using PostgreSQL. Either stop it, or change the port in `docker-compose.db.yml` and `.env`.

**Port 8000 already in use:**
```bash
# macOS/Linux:
lsof -ti:8000 | xargs kill
# Windows PowerShell:
netstat -ano | findstr :8000
# then: taskkill /PID <pid> /F
```

**uv not found after install:**
Restart your terminal. uv adds itself to PATH but the current session won't see it until you restart.

**Docker containers fail to start:**
```bash
docker compose down -v
docker compose up --build
```
