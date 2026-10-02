
.PHONY: install dev test lint format clean docker-up docker-down

# Development
install:
	cd backend && poetry install
	cd frontend && npm install

dev:
	docker compose up --build

# Testing
test:
	cd backend && pytest tests/ -v --cov=app

# Code quality
lint:
	cd backend && ruff check .
	cd backend && mypy app/

format:
	cd backend && black . && ruff check . --fix
	cd frontend && npx prettier --write src/

# Docker
docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f backend

# Database
db-init:
	cd backend && alembic upgrade head

db-reset:
	cd backend && alembic downgrade base && alembic upgrade head

# Cleanup
clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov

help:
	@echo "Available commands:"
	@grep -E "^\S+:" Makefile | head -20
