DOCKER_COMPOSE_FILE=./docker-compose.dev.yml
PYTHON=python3.12

.PHONY: help build run run-full stop

help:
	@echo "Available commands:"
	@echo "  make help           - Show this help message"
	@echo "  make build          - Build the Docker images"
	@echo "  make run            - Run the necessary services using Docker Compose"
	@echo "  make run-full            - Run all the services using Docker Compose"
	@echo "  make stop           - Stop the running containers"


# Build the Docker images
build:
	docker compose -f $(DOCKER_COMPOSE_FILE) --profile full  build --no-cache

# Run the necessary services using Docker Compose
run:
	docker compose -f $(DOCKER_COMPOSE_FILE) up

# Run all the services using Docker Compose
run-full:
	docker compose -f $(DOCKER_COMPOSE_FILE) --profile full up

# Stop the running containers
stop:
	docker compose -f $(DOCKER_COMPOSE_FILE) down
