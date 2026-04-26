# Changelog

Formato: [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) +
[SemVer](https://semver.org/lang/pt-BR/).

## 1.0.0 (2026-04-26)


### Features

* **ci:** tornar upload de SARIF opcional para repos sem GHAS ([c9f9980](https://github.com/maxsuelrl/Projeto-Default/commit/c9f9980787b1b55f315f69a12ea0f0cc6a43a3ef))
* estrutura padrão Projeto-Padrão (SDD + ciclo Dev/Test/Sec + telas obrigatórias) ([#1](https://github.com/maxsuelrl/Projeto-Default/issues/1)) ([9ac8ceb](https://github.com/maxsuelrl/Projeto-Default/commit/9ac8cebb724017ddb2252fc21251f1b50fe600a7))
* hardening pré-produção (CVE-2026-33634, audit-logs, threat model, runbook) ([975bc6f](https://github.com/maxsuelrl/Projeto-Default/commit/975bc6f87c5d34fefbba135091b468f5764dfdf5))
* hardening pré-produção (CVE-2026-33634, audit-logs, threat model, runbook) ([7c1fc0f](https://github.com/maxsuelrl/Projeto-Default/commit/7c1fc0f84f2a07cb4ecb40ebfe9963d2faadab75))
* stack obrigatória PrimeVue + FastAPI + Postgres + Docker (ADR-0001) ([4542c7f](https://github.com/maxsuelrl/Projeto-Default/commit/4542c7fb00c7f2f4bee12229f945311b21f065f2))
* stack obrigatória PrimeVue + FastAPI + Postgres + Docker (ADR-0001) ([d279747](https://github.com/maxsuelrl/Projeto-Default/commit/d279747d9975302ba334a8a0ace40f9b09bc89d1))


### Bug Fixes

* **ci:** faz CI/Security passarem na main após stack obrigatória ([7814247](https://github.com/maxsuelrl/Projeto-Default/commit/7814247c3609daf39dce74c38b09873cd35d81c8))
* **ci:** faz CI/Security passarem na main após stack obrigatória ([a1dc1be](https://github.com/maxsuelrl/Projeto-Default/commit/a1dc1be858ed57299e13c5d9c9a6a2e4b436916f))
* **ci:** release-please em modo manifest + SARIF opcional para repos sem GHAS ([772e099](https://github.com/maxsuelrl/Projeto-Default/commit/772e099eeb7c23be5260022a6ef4d2061c37504f))
* **ci:** release-please em modo manifest + token fallback + setup docs ([6a3f116](https://github.com/maxsuelrl/Projeto-Default/commit/6a3f1166b28e74d4b8d156abd2794d5d1a0a9e9e))
* **ci:** SHAs válidos das Actions + hashFiles em job condition ([b42b86c](https://github.com/maxsuelrl/Projeto-Default/commit/b42b86c96fbbb9d454fc2a05c1bbaeed27f5f15b))
* **ci:** SHAs válidos das Actions + hashFiles em job condition ([226c2a2](https://github.com/maxsuelrl/Projeto-Default/commit/226c2a272c47e03e92f64c04a2ce3d2a8f5b4cd3))

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
