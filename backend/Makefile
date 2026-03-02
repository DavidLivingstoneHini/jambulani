# ──────────────────────────────────────────────────────────────────
# Jambulani Backend — Developer commands
#
# Prerequisites:
#   Docker path:  Docker Desktop installed
#   Local path:   uv installed (https://docs.astral.sh/uv/getting-started/installation/)
# ──────────────────────────────────────────────────────────────────

.PHONY: help install db db-stop migrate seed run dev docker-up docker-down docker-logs reset

# Default
help:
	@echo ""
	@echo "  ── Docker (zero config) ─────────────────────────"
	@echo "  make docker-up       Start full stack (backend + db)"
	@echo "  make docker-down     Stop and remove containers"
	@echo "  make docker-logs     Tail backend logs"
	@echo ""
	@echo "  ── Local development (uv + Docker Postgres) ─────"
	@echo "  make install         Install Python deps via uv"
	@echo "  make db              Start PostgreSQL only (Docker)"
	@echo "  make db-stop         Stop PostgreSQL container"
	@echo "  make migrate         Run Django migrations"
	@echo "  make seed            Seed demo data"
	@echo "  make run             Start Django dev server"
	@echo "  make dev             db + migrate + seed + run (all-in-one)"
	@echo ""
	@echo "  make reset           Wipe DB volumes and re-seed"
	@echo ""

# ── Local: uv + Docker Postgres ──────────────────────────────────

install:
	@command -v uv >/dev/null 2>&1 || { echo "\n  uv not found. Install it:\n\n  Windows: powershell -ExecutionPolicy ByPass -c \"irm https://astral.sh/uv/install.ps1 | iex\"\n  macOS/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh\n\n  Then restart your terminal.\n"; exit 1; }
	uv sync
	@echo "\n  ✓ Dependencies installed. Run: make dev\n"

db:
	docker compose -f docker-compose.db.yml up -d
	@echo "  ✓ PostgreSQL running on localhost:5432"

db-stop:
	docker compose -f docker-compose.db.yml down

migrate:
	uv run python manage.py migrate

seed:
	uv run python manage.py seed_data

run:
	uv run python manage.py runserver

dev: db
	@sleep 2
	$(MAKE) migrate
	$(MAKE) seed
	$(MAKE) run

# ── Docker full stack ─────────────────────────────────────────────

docker-up:
	docker compose up --build

docker-down:
	docker compose down -v

docker-logs:
	docker compose logs -f backend

# ── Utilities ─────────────────────────────────────────────────────

reset: docker-down docker-up
