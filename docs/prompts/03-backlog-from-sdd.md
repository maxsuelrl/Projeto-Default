# Prompt — SDD → Backlog

Quebre `docs/SDD.md` em tarefas atômicas em `docs/backlog.md`, seguindo
`docs/templates/backlog.md`.

Regras:
- 1 tarefa = 1 PR. Se passar de `L`, quebre.
- IDs imutáveis: `T-001`, `T-002`...
- Cada tarefa com critério de aceite em **Gherkin**.
- Inclua sempre as tarefas `T-MANUAL-001`, `T-LOGS-001`, `T-OBS-001`,
  `T-SEC-001`, `T-SEC-002`, `T-CI-001`.
- Marque dependências e prioridade.
- Ordene por valor + dependências (caminho crítico primeiro).
