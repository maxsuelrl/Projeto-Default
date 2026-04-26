#!/usr/bin/env node
// Bootstrap portável de um novo projeto a partir deste template.
// Funciona em Linux, macOS e Windows (PowerShell/cmd) sem rsync/sed/bash.
//
// Uso:
//   node scripts/new-project.mjs <nome-do-projeto> [destino]
//   ./scripts/new-project.mjs   <nome-do-projeto> [destino]   (Linux/macOS)
//
// Requisitos: Node >= 20 e git no PATH.

import { execSync } from "node:child_process";
import { cpSync, existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const ROOT = resolve(__dirname, "..");

const [, , nameArg, destArg] = process.argv;
if (!nameArg) {
  console.error("Uso: node scripts/new-project.mjs <nome-do-projeto> [destino]");
  process.exit(1);
}

const NAME = nameArg;
const DEST = resolve(destArg ?? join("..", NAME));

if (existsSync(DEST)) {
  console.error(`Destino '${DEST}' já existe. Aborte ou escolha outro.`);
  process.exit(1);
}

console.log(`→ Copiando template para ${DEST}...`);
mkdirSync(DEST, { recursive: true });

const SKIP = new Set([
  ".git",
  "node_modules",
  ".venv",
  "dist",
  "build",
  "__pycache__",
  ".pytest_cache",
  ".ruff_cache",
  ".mypy_cache",
  "coverage",
  "htmlcov",
]);
cpSync(ROOT, DEST, {
  recursive: true,
  filter: (src) => {
    const parts = src.replace(ROOT, "").split(/[\\/]/);
    return !parts.some((p) => SKIP.has(p));
  },
});

process.chdir(DEST);

console.log("→ Renomeando docs do template para artefatos vivos...");
mkdirSync("docs/adr", { recursive: true });
mkdirSync("docs/manual/pt-BR", { recursive: true });
mkdirSync("docs/postmortems", { recursive: true });

const docs = [
  "PRD.md",
  "SDD.md",
  "backlog.md",
  "RISKS.md",
  "RELEASE.md",
  "THREAT-MODEL.md",
  "SECURITY-REVIEW.md",
  "PRIVACY-LGPD.md",
  "RUNBOOK.md",
];
for (const f of docs) {
  const target = join("docs", f);
  if (!existsSync(target)) cpSync(join("docs/templates", f), target);
}
if (!existsSync("CHANGELOG.md")) {
  cpSync("docs/templates/CHANGELOG.md", "CHANGELOG.md");
}

console.log("→ Substituindo placeholder do nome...");
function replaceInFile(path, search, replace) {
  if (!existsSync(path)) return;
  const content = readFileSync(path, "utf8");
  const next = content.replaceAll(search, replace);
  if (next !== content) writeFileSync(path, next);
}
for (const f of docs) replaceInFile(join("docs", f), "<Nome do Projeto>", NAME);

const readmeContent = `# ${NAME}\n\n${readFileSync("README.md", "utf8")
  .split("\n")
  .slice(1)
  .join("\n")}`;
writeFileSync("README.md", readmeContent);

console.log("→ Inicializando git...");
rmSync(".git", { recursive: true, force: true });
execSync("git init -q", { stdio: "inherit" });
execSync("git add .", { stdio: "inherit" });
execSync('git commit -q -m "chore: bootstrap a partir de Projeto-Padrão"', {
  stdio: "inherit",
});

console.log(`→ Preparando stack obrigatória (FastAPI + PrimeVue + Postgres)...`);
for (const f of ["apps/backend/.env.example", "apps/frontend/.env.example"]) {
  const target = f.replace(".example", "");
  if (existsSync(f) && !existsSync(target)) cpSync(f, target);
}

console.log(`
✔ Pronto em ${DEST}

Stack já configurada:
  apps/backend   → FastAPI 0.115 + SQLAlchemy 2 + Alembic + Postgres + Argon2
  apps/frontend  → Vue 3 + PrimeVue 4 (Aura) + Vite + TypeScript + Pinia
  docker-compose.yml + docker-compose.prod.yml

Próximos passos:
  1. Edite docs/PRD.md (idéia → PRD; ver docs/prompts/01-prd-from-idea.md)
  2. Edite docs/SDD.md (PRD → SDD; ver docs/prompts/02-sdd-from-prd.md)
  3. Quebre o backlog em docs/backlog.md
  4. cd ${NAME} && make setup && make up    # sobe local em http://localhost:5173
  5. Primeiro usuário admin (no host):
       curl -X POST http://localhost:8000/auth/register \\
         -H "content-type: application/json" \\
         -d '{"email":"admin@example.com","password":"changeme123","role":"admin"}'
`);
