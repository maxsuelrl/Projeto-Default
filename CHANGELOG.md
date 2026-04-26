# Changelog

Formato: [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) +
[SemVer](https://semver.org/lang/pt-BR/).

## 1.0.0 (2026-04-26)


### Features

* **ci:** tornar upload de SARIF opcional para repos sem GHAS ([c9f9980](https://github.com/maxsuelrl/Projeto-Default/commit/c9f9980787b1b55f315f69a12ea0f0cc6a43a3ef))
* estrutura padrão Projeto-Padrão (SDD + ciclo Dev/Test/Sec + telas obrigatórias) ([#1](https://github.com/maxsuelrl/Projeto-Default/issues/1)) ([9ac8ceb](https://github.com/maxsuelrl/Projeto-Default/commit/9ac8cebb724017ddb2252fc21251f1b50fe600a7))
* hardening pré-produção (CVE-2026-33634, audit-logs, threat model, runbook) ([975bc6f](https://github.com/maxsuelrl/Projeto-Default/commit/975bc6f87c5d34fefbba135091b468f5764dfdf5))
* hardening pré-produção (CVE-2026-33634, audit-logs, threat model, runbook) ([7c1fc0f](https://github.com/maxsuelrl/Projeto-Default/commit/7c1fc0f84f2a07cb4ecb40ebfe9963d2faadab75))


### Bug Fixes

* **ci:** release-please em modo manifest + SARIF opcional para repos sem GHAS ([772e099](https://github.com/maxsuelrl/Projeto-Default/commit/772e099eeb7c23be5260022a6ef4d2061c37504f))
* **ci:** release-please em modo manifest + token fallback + setup docs ([6a3f116](https://github.com/maxsuelrl/Projeto-Default/commit/6a3f1166b28e74d4b8d156abd2794d5d1a0a9e9e))
* **ci:** SHAs válidos das Actions + hashFiles em job condition ([b42b86c](https://github.com/maxsuelrl/Projeto-Default/commit/b42b86c96fbbb9d454fc2a05c1bbaeed27f5f15b))
* **ci:** SHAs válidos das Actions + hashFiles em job condition ([226c2a2](https://github.com/maxsuelrl/Projeto-Default/commit/226c2a272c47e03e92f64c04a2ce3d2a8f5b4cd3))

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
