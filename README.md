# Jambulani — Customized Football Jerseys

Full-stack e-commerce application for customized club jerseys.

**Stack:** Nuxt 4 · Vue 3 · Django REST Framework · PostgreSQL · JWT Auth · Docker

---

## Project Structure
```
jambulani/
├── backend/    ← Django REST Framework API
├── frontend/   ← Nuxt 4 frontend
└── README.md   ← You are here
```

---

## Prerequisites — Install These Once

| Tool | Version | Install |
|------|---------|---------|
| Docker Desktop | Latest | [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop) |
| Node.js | 20+ | [nodejs.org](https://nodejs.org) (LTS) |
| Python | 3.11–3.13 | [python.org](https://www.python.org/downloads) |
| uv | Latest | See below |

**Install uv (Python package manager):**

Windows (PowerShell):
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

macOS / Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Restart your terminal after installing. Verify: `uv --version`

> **Why uv?** Plain `pip install` fails on certain Python versions because it tries to compile
> packages like Pillow and psycopg2 from source, which requires a C compiler. uv always
> downloads pre-built binaries — no compiler, no errors, works on any OS.

---

## Option A — Full Docker (Recommended)

Everything runs in containers. Zero configuration required.

### 1. Backend
```bash
cd jambulani/backend
cp .env.example .env
docker compose up --build
```

First run takes 3–5 minutes. Wait until you see:
```
backend  | Starting gunicorn...
```

| Service | URL |
|---------|-----|
| API | http://localhost:8000/api/v1/ |
| Admin panel | http://localhost:8000/admin |

Admin login: `admin@jambulani.com` / `admin123`

### 2. Frontend

Open a new terminal:
```bash
cd jambulani/frontend
cp .env.example .env
npm install
npm run dev
```

Open: http://localhost:3000

### Stop everything
```bash
# In the backend terminal:
Ctrl+C
docker compose down
```

---

## Option B — Local Development

The database runs in Docker. Django and Nuxt run directly on your machine.
Better for development — you get full error output and hot reload.

### Backend
```bash
cd jambulani/backend

# Copy environment file — no edits needed, credentials match the db container
cp .env.example .env

# Start PostgreSQL only (Docker)
docker compose -f docker-compose.db.yml up -d

# Install Python dependencies
uv sync

# Activate the virtual environment
# Windows:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

# Run migrations and seed demo data
python manage.py migrate
python manage.py seed_data

# Start the backend
python manage.py runserver
```

Verify: http://localhost:8000/api/v1/products/ should return product JSON.
Admin: http://localhost:8000/admin → `admin@jambulani.com` / `admin123`

### Frontend

Open a new terminal:
```bash
cd jambulani/frontend
cp .env.example .env
npm install
npm run dev
```

Open: http://localhost:3000

### Stop everything
```bash
# Backend terminal: Ctrl+C
# Frontend terminal: Ctrl+C

# Stop the database container:
cd jambulani/backend
docker compose -f docker-compose.db.yml down
```

---

## Testing the Application

Test in this order after getting everything running:

**1. Products load**
Open http://localhost:3000 — the home page should show featured products and league cards.
This confirms the frontend is successfully talking to the backend.

**2. Browse and filter**
Go to http://localhost:3000/products — try searching, filtering by league, and changing price range.

**3. Product detail**
Click any product — check the image gallery, size selector, name/number customization fields.

**4. Cart**
Select a size and click Add to Cart. The cart drawer should slide in from the right.
Try changing quantity and removing the item.

**5. Register**
Go to http://localhost:3000/register and create an account.
You should be redirected home with your name visible in the header.

**6. Login / Logout**
Click your name → Sign Out. Then go to http://localhost:3000/login and sign back in.

**7. Account page**
Go to http://localhost:3000/account — update your name and shipping address.
Try the Change Password tab.

**8. Protected route**
Sign out, then go directly to http://localhost:3000/account.
You should be automatically redirected to /login.

**9. Admin panel**
Open http://localhost:8000/admin, log in with `admin@jambulani.com` / `admin123`.
Go to Products → Add Product, fill in the details, save.
Refresh http://localhost:3000/products — your product should appear.

**10. API directly**
These should all return JSON in your browser or Postman:
```
GET http://localhost:8000/api/v1/products/
GET http://localhost:8000/api/v1/leagues/
GET http://localhost:8000/api/v1/products/featured/
```

---

## Troubleshooting

**PowerShell blocks `.venv\Scripts\Activate.ps1`:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then retry the activation command.

**`uv sync` says "No interpreter found for Python 3.11":**
```powershell
# Confirm Python 3.11 is installed
py -3.11 --version

# Point uv to it explicitly
uv sync --python "py -3.11"
```

**`python manage.py migrate` fails with "connection refused":**
The database container is not running. Fix:
```bash
docker compose -f docker-compose.db.yml up -d
# Wait 5 seconds, then retry
python manage.py migrate
```

**Port 8000 already in use:**
```powershell
# Windows
netstat -ano | findstr :8000
taskkill /PID  /F

# macOS/Linux
lsof -ti:8000 | xargs kill
```

**Port 5432 already in use:**
You have PostgreSQL installed natively on your machine. The Docker database container
can't start because something is already using that port.
Either stop your local PostgreSQL service, or change `POSTGRES_PORT=5433` in `.env`
and in `docker-compose.db.yml`.

**Frontend shows blank page or API errors:**
Check that `frontend/.env` exists and contains:
```
NUXT_PUBLIC_API_BASE=http://localhost:8000/api/v1
NUXT_PUBLIC_MEDIA_BASE=http://localhost:8000
```

**Everything was working, broke after restarting the computer:**
Docker Desktop needs to be open and running before starting containers.
Open it from the Start menu, wait for the whale icon in the taskbar, then rerun your commands.

**Wipe everything and start fresh:**
```bash
cd jambulani/backend
docker compose down -v
docker compose up --build
```
`-v` removes the database volume so migrations and seed data run 