DC := docker compose
SERVICE ?= web     # default target for service-specific commands (web|db)

.DEFAULT_GOAL := help

.PHONY: help \
        up stop \
        up-web up-db stop-web stop-db \
        rm \
        clean-project clean-all \
        logs logs-f \
        ps rebuild migrate createsuperuser

help: ## Show available commands
	@echo "Available commands:"
	@echo "  make start           - start app + db (detached)"
	@echo "  make stop            - stop app + db"
	@echo "  make start-web       - start API only (db will start as dependency)"
	@echo "  make start-db        - start database only"
	@echo "  make stop-web        - stop API only"
	@echo "  make stop-db         - stop database only"
	@echo "  make rm              - remove containers for this compose project (stops if needed)"
	@echo "  make clean-project   - remove containers, networks, volumes, and local images of this project"
	@echo "  make clean-all       - AGGRESSIVE: prune ALL unused images, volumes, networks, cache (system-wide)"
	@echo "  make logs            - show logs for a service (SERVICE=web|db; default=web)"
	@echo "  make logs-f          - follow logs in real time for a service (SERVICE=web|db)"
	@echo "  --- important ---"
	@echo "  make status              - show containers status"
	@echo "  make rebuild         - rebuild and start the whole stack"
	@echo "  make migrate         - run Django migrations inside web"
	@echo "  make createsuperuser - create Django superuser inside web"

# --- Core workflow ---
start: ## Start app + db (detached)
	$(DC) up -d

stop: ## Stop app + db
	$(DC) stop

# --- Service-specific start/stop ---
start-web: ## Start API only (db will start as dependency)
	$(DC) up -d web

start-db: ## Start database only
	$(DC) up -d db

stop-web: ## Stop API only
	$(DC) stop web

stop-db: ## Stop database only
	$(DC) stop db

# --- Containers removal (no images by default) ---
rm: ## Remove containers for this compose project (stops them if needed)
	$(DC) rm -sf

# --- Cleaners ---
clean-project: ## Remove containers, networks, volumes, and local images for this project
	$(DC) down -v --remove-orphans --rmi local

clean-all: ## AGGRESSIVE: system-wide prune of ALL unused images, volumes, networks, and build cache
	@echo "WARNING: This will remove ALL unused images, networks, volumes, and build cache on your machine."
	@echo "Proceeding in 3 seconds... (Ctrl+C to abort)"; sleep 3
	docker system prune -a --volumes -f

# --- Logs ---
logs: ## Show logs for a service (SERVICE=web|db)
	$(DC) logs $(SERVICE)

logs-f: ## Follow logs for a service in real time (SERVICE=web|db)
	$(DC) logs -f $(SERVICE)

# --- Important extras ---
status: ## Show containers status
	$(DC) ps

rebuild: ## Rebuild and start the whole stack (app + db)
	$(DC) up -d --build

migrate: ## Run Django migrations in the web container
	$(DC) exec web python manage.py migrate

createsuperuser: ## Create a Django superuser in the web container
	$(DC) exec web python manage.py createsuperuser
