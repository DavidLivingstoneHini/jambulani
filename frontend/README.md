# Jambulani — Customized Club Jerseys

A full-stack e-commerce application for customized football jerseys. Built with **Nuxt 3** (frontend) and **Django REST Framework** (backend), running with **PostgreSQL** via **Docker**.

---

## 📁 Project Structure

```
jambulani/
├── docker-compose.yml          # Combined Docker Compose (recommended)
├── jambulani-backend/          # Django REST Framework API
│   ├── config/                 # Django project settings & URL config
│   ├── store/                  # Main app (models, views, serializers, admin)
│   │   ├── models.py           # League, Collection, Category, Product, Cart, etc.
│   │   ├── serializers.py      # DRF serializers
│   │   ├── views.py            # ViewSets & API views
│   │   ├── admin.py            # Django Admin config
│   │   ├── urls.py             # API URL routing
│   │   └── filters.py         # Product filtering
│   ├── Dockerfile
│   ├── docker-compose.yml      # Backend-only Docker Compose
│   ├── requirements.txt
│   └── entrypoint.sh           # DB wait + migrate + seed
└── jambulani-frontend/         # Nuxt 3 application
    ├── assets/css/             # Global Tailwind CSS
    ├── components/
    │   ├── layout/             # AppHeader, AppFooter
    │   ├── cart/               # CartDrawer
    │   └── product/            # ProductCard
    ├── composables/            # useApi (fetch wrapper)
    ├── layouts/                # Default layout
    ├── pages/
    │   ├── index.vue           # Home page
    │   ├── products/
    │   │   ├── index.vue       # Product listing
    │   │   └── [slug].vue      # Product detail
    │   └── checkout.vue        # Checkout page
    ├── stores/                 # Pinia stores (cart)
    ├── types/                  # TypeScript interfaces
    ├── Dockerfile
    ├── docker-compose.yml
    └── nuxt.config.ts
```

---

## 🚀 Quick Start (Recommended — Full Stack via Docker)

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/) installed

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd jambulani
```

### 2. Start everything with one command
```bash
docker compose up --build
```

This will:
1. Start PostgreSQL
2. Run Django migrations
3. Seed demo data (products, leagues, collections, admin user)
4. Start the Django API on `http://localhost:8000`
5. Build and start the Nuxt frontend on `http://localhost:3000`

### 3. Access the application
| Service | URL |
|---------|-----|
| **Frontend** | http://localhost:3000 |
| **Django Admin** | http://localhost:8000/admin |
| **API Root** | http://localhost:8000/api/v1/ |

**Admin credentials:** `admin` / `admin123`

---

## 🔧 Development Setup (Without Docker)

### Backend

**Requirements:** Python 3.12+, PostgreSQL

```bash
cd jambulani-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env to match your local PostgreSQL credentials

# Set POSTGRES_HOST=localhost in .env

# Run migrations
python manage.py migrate

# Seed demo data
python manage.py seed_data

# Start development server
python manage.py runserver
```

### Frontend

**Requirements:** Node.js 20+

```bash
cd jambulani-frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# .env already points to http://localhost:8000

# Start development server
npm run dev
```

---

## 🗄️ API Endpoints

All endpoints are prefixed with `/api/v1/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/products/` | List products (filterable, searchable, paginated) |
| `GET` | `/products/{slug}/` | Product detail |
| `GET` | `/products/featured/` | Featured products |
| `GET` | `/leagues/` | All leagues |
| `GET` | `/leagues/{slug}/` | League detail |
| `GET` | `/collections/` | All collections |
| `GET` | `/categories/` | All categories |
| `GET` | `/patches/` | Available patches |
| `GET` | `/cart/` | Get current cart |
| `POST` | `/cart/` | Add item to cart |
| `PATCH` | `/cart/{id}/` | Update cart item quantity |
| `DELETE` | `/cart/{id}/` | Remove item from cart |
| `DELETE` | `/cart/clear/` | Clear entire cart |
| `POST` | `/newsletter/subscribe/` | Subscribe to newsletter |

### Product Filtering
```
GET /api/v1/products/?league=england-premier-league&min_price=20&max_price=50&search=manchester&ordering=price&page=2
```

---

## 🛠️ Django Admin

Access at `http://localhost:8000/admin` with `admin` / `admin123`.

Manage from admin:
- **Products** — Full catalog management with images, pricing, sizes, patches
- **Leagues** — Country/competition leagues
- **Collections** — Product collections (Kids, Goalkeeper, etc.)
- **Categories** — Product categories
- **Patches** — Available jersey patches with extra pricing
- **Size Charts** — Size guide images per product
- **Newsletter Subscribers** — Email list management
- **Cart Items** — Active sessions

---

## 🏗️ Tech Stack

### Backend
- **Django 5** + **Django REST Framework**
- **PostgreSQL** (via psycopg2)
- **django-filter** — Advanced filtering
- **django-cors-headers** — CORS support
- **Gunicorn** — Production WSGI server

### Frontend
- **Nuxt 3** (latest stable)
- **Vue 3** with Composition API
- **Pinia** — State management (cart)
- **Tailwind CSS** — Utility-first styling
- **TypeScript** — Full type safety
- **@vueuse/core** — Composable utilities

### Infrastructure
- **Docker** + **Docker Compose**
- **PostgreSQL 16**

---

## 🎨 Design Implementation

The UI faithfully implements the provided Figma designs:
- ✅ Announcement bar with language selector & WhatsApp chat button
- ✅ Full navigation with search, cart icon with badge, account menu
- ✅ Mobile-responsive hamburger menu
- ✅ Hero banner with CTA
- ✅ Trust badges (Shipping, Phone, WhatsApp, Quality)
- ✅ Featured products carousel/grid
- ✅ Country leagues grid with colored cards
- ✅ Other collections grid
- ✅ Personalization & Social Networks CTAs
- ✅ 4-column footer with newsletter subscription
- ✅ Product detail page with image gallery, size selection, customization fields
- ✅ Cart drawer with quantity controls
- ✅ Product listing page with filters and pagination

---

## 📝 Notes

- **Session-based cart**: No authentication required. Cart is stored server-side using Django sessions.
- **Demo products**: The `seed_data` management command pre-populates leagues, collections, patches, and 6 sample products. Upload product images via Django Admin.
- **Personalization**: Products support custom name and number printing (stored with cart items).
- **Patches**: Each product can have selectable patches at an additional price.
