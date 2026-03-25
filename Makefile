.PHONY: up down tmux logs clean build ps

# Start all services in background
up:
	docker-compose up -d

# Stop and remove containers
down:
	docker-compose down

# Build agent Docker image
build:
	docker-compose build agents

# Attach tmux monitoring session (no task)
tmux:
	./tmux-start.sh

# Run a task via tmux (usage: make run TASK="Build a Flask API")
run:
	./tmux-start.sh "$(TASK)"

# Tail logs for all services
logs:
	docker-compose logs -f

# Show running container status
ps:
	docker-compose ps

# Remove workspace contents (keeps .gitkeep)
clean:
	find workspace/ -mindepth 1 ! -name '.gitkeep' -delete
	@echo "Workspace cleaned."

# OAuth login helpers
login-gemini:
	docker-compose run --rm cliproxy auth login gemini

login-claude:
	docker-compose run --rm cliproxy auth login claude

login-codex:
	docker-compose run --rm cliproxy auth login codex
