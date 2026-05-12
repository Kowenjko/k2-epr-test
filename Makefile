SHELL := /bin/bash

API = docker compose exec api
CLIENT = docker compose exec client


#-----------------------------------------------------------
# Docker
#-----------------------------------------------------------

dev:
	docker compose up --build

down:
	docker compose down

up:
	docker compose up -d

res-dev: down dev

build:
	docker compose build

restart: down up
	
logs:
	docker compose logs -f

ps:
	docker compose ps

#-----------------------------------------------------------
# Database
#-----------------------------------------------------------

revision:
	@if [ -z "$(msg)" ]; then \
		echo "⚠️ Usage: make revision msg=\"description\""; \
		exit 1; \
	fi
	$(API) uv run alembic revision --autogenerate -m "$(msg)"

migrate:
	$(API) uv run alembic upgrade head

downgrade:
	$(API) uv run alembic downgrade -1

seed:
	$(API) uv run seed.py

seed-reset:
	$(API) uv run seed.py --reset

# --------------------------
# Test
# --------------------------
test:
	$(API) uv run pytest -v

# --------------------------
# Installation
# --------------------------
env-api:
	@test -f api/.env || cp api/.env.example api/.env

env-client:
	@test -f client/.env || cp client/.env.example client/.env

c.install:
	docker compose run --rm --no-deps client yarn install

install: env-api env-client build c.install up migrate seed-reset 

