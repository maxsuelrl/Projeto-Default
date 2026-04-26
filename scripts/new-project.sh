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
# rsync excluindo metadados do template
rsync -a \
  --exclude ".git" \
  --exclude "node_modules" \
  --exclude ".venv" \
  --exclude "dist" \
  --exclude "build" \
  "$ROOT"/ "$DEST"/

cd "$DEST"

echo "→ Renomeando docs do template para artefatos vivos..."
mkdir -p docs/adr docs/manual/pt-BR
[[ -f docs/PRD.md ]] || cp docs/templates/PRD.md docs/PRD.md
[[ -f docs/SDD.md ]] || cp docs/templates/SDD.md docs/SDD.md
[[ -f docs/backlog.md ]] || cp docs/templates/backlog.md docs/backlog.md
[[ -f docs/RISKS.md ]] || cp docs/templates/RISKS.md docs/RISKS.md
[[ -f docs/RELEASE.md ]] || cp docs/templates/RELEASE.md docs/RELEASE.md
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

echo
echo "✔ Pronto em $DEST"
echo
echo "Próximos passos:"
echo "  1. Edite docs/PRD.md (idéia → PRD)"
echo "  2. Edite docs/SDD.md (PRD → SDD)"
echo "  3. Quebre o backlog em docs/backlog.md"
echo "  4. Crie o repo remoto e faça o primeiro push"
