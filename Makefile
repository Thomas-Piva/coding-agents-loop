.PHONY: up down tmux logs clean build ps login-gemini login-claude login-codex

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

# OAuth login helpers — usa -no-browser per WSL2 (stampa URL da aprire manualmente)
login-gemini:
	docker exec -it cliproxy ./CLIProxyAPI -login -no-browser

login-claude:
	docker exec -it cliproxy ./CLIProxyAPI -claude-login -no-browser

# Codex usa browser OAuth (callback su porta 54545)
login-codex:
	docker exec -it cliproxy ./CLIProxyAPI -codex-login -no-browser
