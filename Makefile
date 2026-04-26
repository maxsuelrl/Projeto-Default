.PHONY: help setup lint test sec release new-project

help:
	@echo "Targets:"
	@echo "  setup        - instala dependências do projeto (sobrescreva por stack)"
	@echo "  lint         - lint + format check"
	@echo "  test         - roda suíte de testes (unit + integ)"
	@echo "  sec          - roda Semgrep + Gitleaks + SCA local"
	@echo "  release      - gera RELEASE.md + CHANGELOG.md"
	@echo "  new-project NAME=<nome> [DEST=<dir>]"

setup:
	@echo "Defina o setup específico da stack (npm ci / pip install / go mod download)."

lint:
	@echo "Defina lint da stack (eslint / ruff / golangci-lint)."

test:
	@echo "Defina test da stack (vitest / pytest / go test)."

sec:
	@command -v gitleaks >/dev/null && gitleaks detect --no-banner -v || echo "(instale gitleaks)"
	@command -v semgrep >/dev/null && semgrep --config p/owasp-top-ten --error || echo "(instale semgrep)"

release:
	@echo "Atualize docs/RELEASE.md e CHANGELOG.md (use docs/prompts/07-release-notes.md)."

new-project:
	@test -n "$(NAME)" || (echo "Use: make new-project NAME=<nome>"; exit 1)
	@if command -v node >/dev/null; then \
		node ./scripts/new-project.mjs "$(NAME)" $(if $(DEST),"$(DEST)"); \
	else \
		./scripts/new-project.sh "$(NAME)" $(if $(DEST),"$(DEST)"); \
	fi
