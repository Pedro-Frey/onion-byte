.PHONY: dev test lint format migrate migrate-create seed docker-up docker-down docker-build install

dev:
	uvicorn api.main:app --reload

test:
	pytest

lint:
	ruff check .

format:
	ruff format .

migrate:
	alembic upgrade head

migrate-create:
	alembic revision --autogenerate -m "auto"

seed:
	python scripts/seed_db.py

docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-build:
	docker compose build

install:
	pip install -r requirements.txt
