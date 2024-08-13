DOCKER_COMPOSE_FILE	= ./docker-compose.yml
DOCKER_COMPOSE_LOCAL_FILE	= ./docker-compose.local.yml

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

.PHONY: up-local down-local re-local logs-local
