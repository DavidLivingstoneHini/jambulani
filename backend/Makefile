.PHONY: help install db db-stop migrate seed run dev docker-up docker-down docker-logs reset

help:
	@echo ""
	@echo "  ── Docker (zero config) ──────────────────────────"
	@echo "  make docker-up       Start full stack (backend + db)"
	@echo "  make docker-down     Stop and remove containers"
	@echo "  make docker-logs     Tail backend logs"
	@echo ""
	@echo "  ── Local development ─────────────────────────────"
	@echo "  make install         Create venv and install dependencies"
	@echo "  make db              Start PostgreSQL only (Docker)"
	@echo "  make db-stop         Stop PostgreSQL container"
	@echo "  make migrate         Run Django migrations"
	@echo "  make seed            Seed demo data"
	@echo "  make run             Start Django dev server"
	@echo "  make dev             db + migrate + seed + run (all-in-one)"
	@echo ""

# ── Local ─────────────────────────────────────────────────────────

install:
	python -m venv venv
	venv\Scripts\pip install -r requirements.txt

db:
	docker compose -f docker-compose.db.yml up -d

db-stop:
	docker compose -f docker-compose.db.yml down

migrate:
	venv\Scripts\python manage.py migrate

seed:
	venv\Scripts\python manage.py seed_data

run:
	venv\Scripts\python manage.py runserver

# ── Docker ────────────────────────────────────────────────────────

docker-up:
	docker compose up --build

docker-down:
	docker compose down -v

docker-logs:
	docker compose logs -f backend

reset: docker-down docker-up
