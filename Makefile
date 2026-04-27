.PHONY: help dev up logs down

help:
	@echo "Available targets:"
	@echo "  make dev   Build/start the Docker stack and follow backend/frontend logs"
	@echo "  make up    Build/start the Docker stack in the background"
	@echo "  make logs  Follow backend and frontend logs"
	@echo "  make down  Stop and remove the Docker stack"

dev: up logs

up:
	docker compose up -d --build

logs:
	docker compose logs -f backend frontend

down:
	docker compose down
