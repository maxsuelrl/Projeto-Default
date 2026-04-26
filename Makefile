.PHONY: help setup up down logs lint test sec build new-project \
        backend-shell frontend-shell db-shell migrate \
        backend-test frontend-test backend-lint frontend-lint

help:
	@echo "Stack: PrimeVue + FastAPI + Postgres (Docker)."
	@echo ""
	@echo "Targets:"
	@echo "  setup            - copia .env.example -> .env nas duas apps"
	@echo "  up               - sobe stack de desenvolvimento (compose up)"
	@echo "  down             - para stack"
	@echo "  logs             - logs do compose (todos os serviços)"
	@echo "  build            - build das imagens"
	@echo "  migrate          - alembic upgrade head no backend"
	@echo "  lint / test      - lint+test em backend e frontend"
	@echo "  sec              - gitleaks + semgrep locais"
	@echo "  backend-shell    - shell no container backend"
	@echo "  frontend-shell   - shell no container frontend"
	@echo "  db-shell         - psql no container db"
	@echo "  new-project NAME=<nome>  - bootstrap de novo projeto a partir do template"

setup:
	@test -f apps/backend/.env || cp apps/backend/.env.example apps/backend/.env
	@test -f apps/frontend/.env || cp apps/frontend/.env.example apps/frontend/.env
	@echo "✔ .env criados (revise antes de subir)"

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f --tail=200

build:
	docker compose build

migrate:
	docker compose exec backend alembic upgrade head

backend-shell:
	docker compose exec backend bash

frontend-shell:
	docker compose exec frontend sh

db-shell:
	docker compose exec db psql -U $${POSTGRES_USER:-app} -d $${POSTGRES_DB:-app}

backend-lint:
	docker compose run --rm backend ruff check .

frontend-lint:
	docker compose run --rm frontend npm run lint

backend-test:
	docker compose run --rm backend pytest

frontend-test:
	docker compose run --rm frontend npm test

lint: backend-lint frontend-lint
test: backend-test frontend-test

sec:
	@command -v gitleaks >/dev/null && gitleaks detect --no-banner -v || echo "(instale gitleaks)"
	@command -v semgrep  >/dev/null && semgrep scan --config p/owasp-top-ten --error || echo "(instale semgrep)"

new-project:
	@test -n "$(NAME)" || (echo "Use: make new-project NAME=<nome>"; exit 1)
	@if command -v node >/dev/null; then \
		node ./scripts/new-project.mjs "$(NAME)" $(if $(DEST),"$(DEST)"); \
	else \
		./scripts/new-project.sh "$(NAME)" $(if $(DEST),"$(DEST)"); \
	fi
