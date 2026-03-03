# Jambulani — Customized Football Jerseys

Full-stack e-commerce app: **Nuxt 4** frontend + **Django REST Framework** backend.  
Custom jersey ordering with name, number, patch personalisation.

---

## Tech Stack

| Layer     | Technology |
|-----------|-----------|
| Frontend  | Nuxt 4 (Vue 3 + TypeScript), Tailwind CSS, Pinia |
| Backend   | Django 4.2, Django REST Framework, PostgreSQL |
| Auth      | JWT (djangorestframework-simplejwt) |
| Dev infra | Docker Compose |

---

## Prerequisites

Install these before starting:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (includes Docker Compose)
- [Node.js 20+](https://nodejs.org/) and npm
- [Python 3.11+](https://www.python.org/) (only needed for local backend dev; Docker handles prod)

---

## Quickstart (Recommended — Docker for DB, local for app servers)

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/jambulani.git
cd jambulani
```

### 2. Start PostgreSQL via Docker
```bash
cd backend
docker compose -f docker-compose.db.yml up -d
```

This starts a Postgres container on port **5432** with:
- Database: `jambulani`
- User: `jambulani`
- Password: `jambulani`

### 3. Set up the backend
```bash
cd backend

# Copy environment file
cp .env.example .env

# Create a Python virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Seed the database with sample products, leagues, collections, patches
python manage.py seed_data

# Create an admin superuser (follow the prompts)
python manage.py createsuperuser

# Start the backend server
python manage.py runserver
```

Backend runs at: **http://localhost:8000**  
Django admin: **http://localhost:8000/admin**

### 4. Set up the frontend

Open a **new terminal tab**:
```bash
cd frontend

# Copy environment file
cp .env.example .env

# Install dependencies
npm install

# Start the development server
npm run dev
```

Frontend runs at: **http://localhost:3000**

---

## Full Docker Setup (optional — runs everything in containers)

If you prefer to run everything in Docker:
```bash
# From the repo root
docker compose up --build
```

Services:
- **db** — PostgreSQL on port 5432
- **backend** — Django on port 8000
- **frontend** — Nuxt on port 3000

Then seed data in the running backend container:
```bash
docker compose exec backend python manage.py seed_data
docker compose exec backend python manage.py createsuperuser
```

---

## Environment Variables

### Backend (`backend/.env`)
```env
SECRET_KEY=your-secret-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=jambulani
DB_USER=jambulani
DB_PASSWORD=jambulani
DB_HOST=localhost        # use "db" if running inside Docker Compose
DB_PORT=5432

CORS_ALLOWED_ORIGINS=http://localhost:3000
MEDIA_URL=/media/
```

### Frontend (`frontend/.env`)
```env
NUXT_PUBLIC_API_BASE=http://localhost:8000/api/v1
NUXT_PUBLIC_MEDIA_BASE=http://localhost:8000
```

---

## Static Images (Leagues, Collections, Hero)

The homepage uses static images you place in:
```
frontend/public/assets/images/
├── hero-banner.jpg               ← Hero section background
├── personalization-bg.jpg        ← Personalization card background
├── social-bg.jpg                 ← Social Networks card background
│
├── leagues/
│   ├── champions-league.jpg
│   ├── europa-league.jpg
│   ├── copa-america.jpg
│   ├── asian-cup.jpg
│   └── african-nations-cup.jpg
│
└── collections/
    ├── kids.jpg
    ├── large-sizes.jpg
    ├── goalkeeper.jpg
    ├── authentic-pro-player.jpg
    ├── shorts.jpg
    └── socks.jpg
```

Until images are added, coloured fallback backgrounds display automatically.

---

## Product Images (Dynamic / Seeded)

Product images are managed through Django Admin:

1. Go to **http://localhost:8000/admin**
2. Log in with your superuser credentials
3. Navigate to **Store → Products**
4. Select a product → scroll to **Product Images** → upload images

Images are served from `/media/` by the Django dev server.

The `seed_data` command creates 16 products (8 featured) with placeholder data — you can add real images through admin.

---

## API Endpoints

All endpoints are prefixed with `/api/v1/`.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/products/` | List all products (supports `?search=`, `?league=`, `?collection=`) |
| `GET` | `/products/featured/` | Featured products for homepage |
| `GET` | `/products/{slug}/` | Single product detail |
| `GET` | `/leagues/` | All leagues |
| `GET` | `/collections/` | All collections |
| `GET` | `/cart/` | Get current cart |
| `POST` | `/cart/items/` | Add item to cart |
| `PATCH` | `/cart/items/{id}/` | Update cart item quantity |
| `DELETE` | `/cart/items/{id}/` | Remove cart item |
| `POST` | `/auth/register/` | Register new user |
| `POST` | `/auth/login/` | Login (returns JWT tokens) |
| `POST` | `/auth/logout/` | Logout |
| `GET/PUT` | `/auth/profile/` | Get/update user profile |

---

## Django Admin

The admin panel at **http://localhost:8000/admin** lets you manage:

- **Products** — name, price, description, images, sizes, discount, featured flag
- **Leagues** — name, slug, sort order
- **Collections** — name, slug, sort order
- **Patches** — name, extra price
- **Size Charts** — name, image, description
- **Orders** — view and manage customer orders
- **Users** — manage customer accounts

---

## Project Structure
```
jambulani/
├── backend/
│   ├── accounts/          # User auth (register, login, JWT, profile)
│   ├── store/             # Products, cart, orders, leagues, collections
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── management/commands/seed_data.py
│   ├── config/            # Django settings, root URL conf
│   ├── manage.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── docker-compose.db.yml   ← DB only (for local dev)
│
└── frontend/
    ├── app/
    │   ├── assets/css/    # Tailwind + global styles
    │   ├── components/
    │   │   ├── layout/    # AppHeader.vue, AppFooter.vue
    │   │   ├── cart/      # CartDrawer.vue
    │   │   └── product/   # ProductCard.vue
    │   ├── composables/   # useApi.ts, useClientStore.ts
    │   ├── layouts/       # default.vue (header + footer + rewards tab)
    │   ├── pages/         # index.vue, products/[slug].vue, login, register...
    │   ├── plugins/       # auth.client.ts
    │   ├── stores/        # auth.ts, cart.ts (Pinia)
    │   └── types/         # TypeScript interfaces
    ├── public/
    │   └── assets/images/ # Static images (see above)
    ├── nuxt.config.ts
    ├── tailwind.config.ts
    └── package.json
```

---

## Troubleshooting

**`django.db.OperationalError: could not connect to server`**  
→ Make sure the DB container is running: `docker compose -f docker-compose.db.yml up -d`

**`Module not found` errors in frontend**  
→ Run `npm install` inside the `frontend/` directory

**Images not loading**  
→ Check that `NUXT_PUBLIC_MEDIA_BASE=http://localhost:8000` is set in `frontend/.env`  
→ For static images (leagues/collections), verify filenames match exactly (lowercase, hyphens)

**Admin login doesn't work**  
→ Make sure you ran `python manage.py createsuperuser`

**Cart / auth not working after refresh**  
→ Ensure both frontend and backend are running simultaneously

---

## Running Tests
```bash
# Backend tests
cd backend
python manage.py test

# Frontend type check
cd frontend
npm run typecheck
```

---