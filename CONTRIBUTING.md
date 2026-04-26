# Contribuindo

Antes de abrir um PR:

1. Leia `AGENTS.md` e `README.md`.
2. Verifique se a tarefa está em `docs/backlog.md` (se não, adicione).
3. Crie branch `feat/T-xxx-<slug>`.
4. Use **Conventional Commits**.
5. Marque os checklists do `.github/pull_request_template.md` (DoD, QA, Sec).
6. Garanta que `/manual` e `/admin/logs` continuam passando smoke E2E.

## Setup local

```bash
make setup      # ou ./scripts/bootstrap (a definir por projeto)
make lint
make test
```

## Skills do Cursor

- `.cursor/rules/00-core.mdc` — sempre ativa.
- `.cursor/rules/10-planning.mdc` — para PRD/SDD/backlog.
- `.cursor/rules/30-development.mdc` — durante implementação.
- `.cursor/rules/31-testing.mdc` — geração de testes.
- `.cursor/rules/32-security.mdc` — revisão de segurança antes do PR.
- `.cursor/rules/40-finalization.mdc` — release.

## Comunicação

Use o template adequado em `.github/ISSUE_TEMPLATE/`. Vulnerabilidades:
seguir `SECURITY.md`.
