#!/usr/bin/env bash
# Bootstrap de um novo projeto a partir deste template.
# Uso:  ./scripts/new-project.sh <nome-do-projeto> [destino]

set -euo pipefail

NAME="${1:-}"
DEST="${2:-../$NAME}"

if [[ -z "$NAME" ]]; then
  echo "Uso: $0 <nome-do-projeto> [destino]" >&2
  exit 1
fi

if [[ -e "$DEST" ]]; then
  echo "Destino '$DEST' já existe. Aborte ou escolha outro." >&2
  exit 1
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "→ Copiando template para $DEST..."
mkdir -p "$DEST"
rsync -a \
  --exclude ".git" \
  --exclude "node_modules" \
  --exclude ".venv" \
  --exclude "dist" \
  --exclude "build" \
  --exclude "__pycache__" \
  --exclude ".pytest_cache" \
  --exclude ".ruff_cache" \
  --exclude ".mypy_cache" \
  --exclude "coverage" \
  --exclude "htmlcov" \
  "$ROOT"/ "$DEST"/

cd "$DEST"

echo "→ Renomeando docs do template para artefatos vivos..."
mkdir -p docs/adr docs/manual/pt-BR docs/postmortems
for src in PRD.md SDD.md backlog.md RISKS.md RELEASE.md \
           THREAT-MODEL.md SECURITY-REVIEW.md PRIVACY-LGPD.md RUNBOOK.md; do
  [[ -f "docs/$src" ]] || cp "docs/templates/$src" "docs/$src"
done
[[ -f CHANGELOG.md ]] || cp docs/templates/CHANGELOG.md CHANGELOG.md

echo "→ Substituindo placeholder do nome..."
# sed compatível com macOS e Linux
sedi() { if sed --version >/dev/null 2>&1; then sed -i "$@"; else sed -i "" "$@"; fi; }
sedi "s/<Nome do Projeto>/$NAME/g" docs/PRD.md docs/SDD.md docs/backlog.md docs/RISKS.md docs/RELEASE.md 2>/dev/null || true
echo "# $NAME" > README.md.new
tail -n +2 README.md >> README.md.new || true
mv README.md.new README.md

echo "→ Inicializando git..."
rm -rf .git
git init -q
git add .
git commit -q -m "chore: bootstrap a partir de Projeto-Padrão"

for f in apps/backend/.env.example apps/frontend/.env.example; do
  target="${f%.example}"
  [[ -f "$target" ]] || cp "$f" "$target"
done

echo
echo "✔ Pronto em $DEST"
echo
echo "Stack: apps/backend (FastAPI) + apps/frontend (PrimeVue) + Postgres + Docker"
echo
echo "Próximos passos:"
echo "  1. Edite docs/PRD.md (idéia → PRD)"
echo "  2. Edite docs/SDD.md (PRD → SDD)"
echo "  3. Quebre o backlog em docs/backlog.md"
echo "  4. make setup && make up   # sobe a stack em localhost:5173"
