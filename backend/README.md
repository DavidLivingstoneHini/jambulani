# Jambulani — Customized Football Jerseys

Full-stack e-commerce application for customized football jerseys.
Built with **Nuxt 4** (Vue 3 + TypeScript) on the frontend and **Django REST Framework** on the backend.

---

## Tech Stack

| Layer    | Technology                                      |
|----------|-------------------------------------------------|
| Frontend | Nuxt 4, Vue 3, TypeScript, Tailwind CSS, Pinia  |
| Backend  | Django 4.2, Django REST Framework, PostgreSQL   |
| Auth     | Custom JWT with HttpOnly cookies + token rotation |
| Infra    | Docker + Docker Compose                         |

> **Why Python 3.11?** Some dependencies (notably Pillow) do not yet provide pre-built wheels for Python 3.13/3.14, which means they require compiling from source and additional system dependencies. Python 3.11 was chosen for full ecosystem compatibility and stability across all platforms.

---

## Prerequisites

You only need two things installed:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) — runs the entire backend automatically
- [Node.js 20+](https://nodejs.org/) — runs the frontend dev server

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
migrations, static files, and demo data (including the admin account).

```bash
cd backend
cp .env.example .env
docker compose up --build
```

That's it. Wait for this line in the logs:

```
PostgreSQL ready.
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

The homepage sections use static images you place in the frontend folder.
The app works without them (coloured fallback backgrounds show instead),
but adding them makes it look exactly like the design.

```
frontend/public/assets/images/
├── hero-banner.jpg                   ← Hero section (1440 × 400px)
├── personalization-bg.jpg            ← Personalization card (700 × 300px)
├── social-bg.jpg                     ← Social Networks card (700 × 300px)
│
├── leagues/
│   ├── champions-league.jpg          (400 × 400px)
│   ├── europa-league.jpg
│   ├── copa-america.jpg
│   ├── asian-cup.jpg
│   └── african-nations-cup.jpg
│
└── collections/
    ├── kids.jpg                      (640 × 360px)
    ├── large-sizes.jpg
    ├── goalkeeper.jpg
    ├── authentic-pro-player.jpg
    ├── shorts.jpg
    └── socks.jpg
```

Product images are managed through the Django Admin:
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

## Running the Tests

### Backend

```bash
cd backend
cp .env.example .env

# Start just the database
docker compose -f docker-compose.db.yml up -d

# Set up a local Python environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run all 50 tests
python manage.py test store.tests accounts.tests --verbosity=2
```

### Frontend

```bash
cd frontend
npm install
npm test                   # run once
npm run test:watch         # watch mode during development
npm run test:coverage      # with coverage report
```

---

## Project Structure

```
jambulani/
├── backend/
│   ├── accounts/               # Auth: register, login, JWT, profile
│   │   ├── models.py           # Custom User + RefreshToken models
│   │   ├── views.py            # Register, Login, Logout, Refresh, Me
│   │   ├── serializers.py
│   │   ├── authentication.py   # JWT cookie authentication backend
│   │   ├── tokens.py           # JWT issue/verify helpers
│   │   ├── admin.py
│   │   └── tests/
│   │       └── test_auth.py    # 23 auth tests
│   ├── store/
│   │   ├── models.py           # Product, League, Collection, Cart, etc.
│   │   ├── views.py            # Product, Cart, Newsletter ViewSets
│   │   ├── serializers.py
│   │   ├── filters.py
│   │   ├── admin.py            # Rich admin with image previews + badges
│   │   ├── urls.py
│   │   └── tests/
│   │       ├── test_models.py  # Model unit tests
│   │       └── test_api.py     # API integration tests
│   ├── store/management/commands/
│   │   └── seed_data.py        # Demo data + admin user
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── Dockerfile
│   ├── docker-compose.yml      # Backend + PostgreSQL (use this)
│   ├── docker-compose.db.yml   # PostgreSQL only (for local dev)
│   ├── entrypoint.sh           # Auto: migrate + collectstatic + seed
│   ├── requirements.txt
│   └── .env.example
│
└── frontend/
    ├── app/
    │   ├── assets/css/         # Tailwind + global styles
    │   ├── components/
    │   │   ├── layout/         # AppHeader.vue, AppFooter.vue
    │   │   ├── cart/           # CartDrawer.vue
    │   │   └── product/        # ProductCard.vue
    │   ├── composables/        # useApi.ts, useClientStore.ts
    │   ├── layouts/            # default.vue (header + footer + rewards tab)
    │   ├── pages/              # index.vue, products/[slug].vue, account/
    │   ├── stores/             # auth.ts, cart.ts (Pinia)
    │   └── types/              # TypeScript interfaces
    ├── public/assets/images/   # Static images (leagues, collections, hero)
    ├── tests/
    │   ├── setup.ts
    │   ├── stores/             # cart.test.ts, auth.test.ts
    │   └── components/         # ProductCard.test.ts
    ├── nuxt.config.ts
    ├── vitest.config.ts
    ├── tailwind.config.ts
    └── package.json
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

---

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
