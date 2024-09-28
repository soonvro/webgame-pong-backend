DOCKER_COMPOSE_FILE	= ./docker-compose.yml
DOCKER_COMPOSE_LOCAL_FILE	= ./docker-compose.local.yml
APP_DIR	= ./Space-Pin-Pong

SERVICE_APP = app
SERVICE_DB = db
SERVICE_REDIS = redis

all:
	@echo "Usage: make [up-local|down-local|re-local|logs-local]"

up-local:
	docker compose -f $(DOCKER_COMPOSE_FILE) -f $(DOCKER_COMPOSE_LOCAL_FILE) up -d

down-local:
	docker compose -f $(DOCKER_COMPOSE_FILE) -f $(DOCKER_COMPOSE_LOCAL_FILE) down

re-local: down-local
	docker compose -f $(DOCKER_COMPOSE_FILE) -f $(DOCKER_COMPOSE_LOCAL_FILE) up -d --build

logs-local:
	docker compose -f $(DOCKER_COMPOSE_FILE) -f $(DOCKER_COMPOSE_LOCAL_FILE)  logs -f

command-app-local:
	docker compose -f $(DOCKER_COMPOSE_FILE) -f $(DOCKER_COMPOSE_LOCAL_FILE) exec $(SERVICE_APP) python manage.py $(CMD)

mk-requeirements:
	pip list --format=freeze > $(APP_DIR)/requirements.txt

.PHONY: up-local down-local re-local logs-local mk-requeirements
