# Changelog

Formato: [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) +
[SemVer](https://semver.org/lang/pt-BR/).

## [Unreleased]
### Added
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

