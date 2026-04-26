# Prompt — Release notes

Gere `docs/RELEASE.md` (a partir do template) e atualize `CHANGELOG.md`.

Fontes:
- Commits desde a última tag (`git log <last>..HEAD --pretty=format:%s`).
- Tarefas concluídas no `backlog.md`.
- ADRs novos.

Saída:
- `RELEASE.md` com highlights, breaking changes, migrações e rollback.
- `CHANGELOG.md` em formato Keep a Changelog.
- Sumário curto (5 bullets) para o Slack/email.
