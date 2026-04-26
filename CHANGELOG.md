# Changelog

Formato: [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) +
[SemVer](https://semver.org/lang/pt-BR/).

## [Unreleased]

### Added (stack obrigatória — ADR-0001)
- `apps/backend/` — **FastAPI** + Pydantic v2 + SQLAlchemy 2 + Alembic +
  Argon2id + structlog. Rotas: `/auth/{register,login}`,
  `/manual/sections`, `/admin/logs`, `/admin/audit-logs`,
  `/admin/audit-logs/verify`, `/health`, `/ready`. Middleware com headers
  de segurança, CSP estrita, rate limiting (SlowAPI) e correlação por
  `X-Request-Id`.
- `apps/frontend/` — **Vue 3 + PrimeVue 4** (preset Aura) + Vite + TS +
  Pinia. Views: `Login`, `Home`, `Manual`, `AdminLogs`, `AdminAuditLogs`,
  `Forbidden`, `NotFound`. Router com guards de RBAC; cliente HTTP fetch
  com `ApiError`; store de auth com expiração de JWT.
- Migrations Alembic (`0001_init`) — Postgres 16 + `pgcrypto`. Trigger
  bloqueia `UPDATE/DELETE` em `audit_events` (append-only por contrato).
- `app.audit.emit_audit()` com cadeia de hash sha256 (`prev_hash → hash`)
  e mascaramento de PII (CPF, e-mail, password, token).
- `docker-compose.yml` (dev) + `docker-compose.prod.yml` (prod) com
  healthchecks, rede privada e Postgres não exposto em prod.
- Dockerfiles multi-stage (dev + prod) para backend (uvicorn) e frontend
  (Nginx servindo build estático com headers de segurança espelhados).
- Testes essenciais: cadeia de auditoria (Pytest) + store de auth (Vitest).
- ADR-0001 documentando a decisão da stack e alternativas consideradas.

### Changed
- `Makefile` reescrito para a stack: `make setup`, `up`, `down`, `logs`,
  `migrate`, `backend-shell`, `frontend-shell`, `db-shell`, `lint`,
  `test`, `sec`, `new-project`.
- `ci.yml` com jobs `backend` (Postgres em service), `frontend` (Node 22) e
  `docker-build` que valida `--target prod` das duas imagens.
- `security.yml` ganhou `trivy-image` (matriz backend/frontend) que builda
  e escaneia as imagens.
- Skills `00-core`, `30-development` e SDD template descrevem a stack
  como obrigatória, com referência a ADR-0001.
- `new-project.{mjs,sh}` inicializam `.env` das duas apps e mostram
  `make setup && make up` nos próximos passos.

### Added (anteriores)
- Estrutura inicial do template **Projeto-Padrão** (skills do Cursor por fase,
  templates de docs, checklists QA/Sec, specs das telas obrigatórias `/manual`
  e `/admin/logs`, workflows CI/Sec/Release, script de bootstrap).
- Tela obrigatória **`/admin/audit-logs`** (auditoria de ações, append-only,
  hash chain) — `docs/screens/audit-logs-screen.spec.md`.
- Templates **`THREAT-MODEL.md`** (STRIDE/ASVS), **`SECURITY-REVIEW.md`**
  (revisão formal por release/tarefa sensível) e **`PRIVACY-LGPD.md`**
  (DPIA simplificado).
- Template **`RUNBOOK.md`** (deploy, rollback, restore, incidentes,
  rotação de segredos).
- Versão portátil do bootstrap: **`scripts/new-project.mjs`** (Node 20+,
  funciona em Linux/macOS/Windows sem rsync/sed/bash).
- CodeQL agora detecta a stack (jobs separados para JS/TS, Python e Go) em
  vez de rodar uma matrix fixa.

### Changed
- Skills do Cursor refinadas:
  - `00-core` mais curta, exigindo PARAR a implementação se faltar PRD/SDD/
    backlog (em vez de "gerar para conseguir codar").
  - `90-screens-mandatory` enxuta e referenciando as 3 telas.
  - `30-development` e `32-security` com `description:` que sinaliza acionamento
    manual em vez de `alwaysApply`.
- Tela `/admin/logs` agora declara explicitamente que é só para **logs
  técnicos**, com schema enriquecido (`route`, `method`, `status`,
  `errorStackHash`). Auditoria foi separada para `/admin/audit-logs`.
- Backlog template incluí `T-AUDIT-001`.

### Fixed
- `release-please` em modo manifest com fallback de token
  (`RELEASE_PLEASE_TOKEN || GITHUB_TOKEN`).
- Upload de SARIF condicional via `vars.ENABLE_CODE_SCANNING_UPLOAD` para
  repos sem GHAS.

### Security
- **trivy-action** atualizado para **v0.35.0 pinado por SHA**
  (`57a97c7e7821a5776cebc9bb87c984fa69cba8f1`) — única versão confirmadamente
  segura após a CVE-2026-33634 (supply chain attack que force-pushou 76 de 77
  tags do `aquasecurity/trivy-action` em 2026-03-19).
- Todas as Actions de terceiros agora pinadas por SHA imutável (checkout,
  setup-node, setup-python, setup-go, upload-artifact, gitleaks-action,
  codeql-action, zaproxy/action-baseline, googleapis/release-please-action).

