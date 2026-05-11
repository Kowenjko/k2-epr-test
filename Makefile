SHELL := /bin/bash

DEV_COMPOSE = docker compose
API = $(DEV_COMPOSE) exec api
CLIENT = $(DEV_COMPOSE) exec client


# --------------------------
# CLIENT COMMAND
# --------------------------
c.install:
	@if [ -z "$(name)" ]; then \
		echo "⚠️ Usage: make revision name=\"description\""; \
		exit 1; \
	fi
	$(CLIENT) yarn add $(name) 

# --------------------------
# DEV COMMANDS
# --------------------------

dev:
	$(DEV_COMPOSE) up --build

down:
	$(DEV_COMPOSE) down

up:
	$(DEV_COMPOSE) up -d

res-dev: down dev

restart: down up
	
logs:
	$(DEV_COMPOSE) logs -f

ps:
	$(DEV_COMPOSE) ps

install:
	dev migrate c.install

# --------------------------
# DATABASE MIGRATIONS (ALEMBIC)
# --------------------------

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


