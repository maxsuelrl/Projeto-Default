# Prompt — Implementar uma tarefa do backlog

Implemente a tarefa `T-XXX` de `docs/backlog.md`.

Procedimento:
1. Leia a tarefa e a parte do SDD correspondente.
2. Crie branch `feat/T-XXX-<slug>`.
3. Aplique a skill `.cursor/rules/30-development.mdc`.
4. Adicione testes (skill `31-testing.mdc`).
5. Rode SAST/SCA/Gitleaks (skill `32-security.mdc`).
6. Atualize `CHANGELOG.md` (Unreleased) e `/manual` se afetar UI.
7. Abra PR usando `.github/pull_request_template.md`.

Restrições:
- Não pular DoD (`docs/templates/DoD.md`).
- Não comentar código óbvio.
- Logs estruturados nas bordas conforme schema do
  `docs/screens/logs-screen.spec.md`.
