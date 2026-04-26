# Backlog — <Nome do Projeto>

> Tarefas atômicas derivadas do SDD. **1 tarefa = 1 PR.** IDs são imutáveis.

## Convenções
- Status: `todo`, `wip`, `review`, `done`, `blocked`.
- Prioridade: `P0` (bloqueia release) > `P1` > `P2` > `P3`.
- Estimativa: `S` (≤ ½ dia), `M` (1-2 dias), `L` (3-5 dias). Acima disso,
  quebrar.

## Tarefas

- [ ] **T-001 — Bootstrap do projeto** [P0][S][todo]
  - Contexto: criar repo a partir do `Projeto-Padrão`.
  - AC:
    - Given o repo recém-clonado
    - When rodo `make setup`
    - Then lint, typecheck e testes rodam verdes.
  - Dependências: —
  - Riscos: ferramentas faltando no ambiente.

- [ ] **T-MANUAL-001 — Tela `/manual`** [P0][M][todo]
  - Spec: `docs/screens/manual-screen.spec.md`.
  - AC: rota acessível autenticada, busca, índice, conteúdo MDX, smoke E2E.

- [ ] **T-LOGS-001 — Tela `/admin/logs` (técnicos)** [P0][M][todo]
  - Spec: `docs/screens/logs-screen.spec.md`.
  - AC: filtros (período, nível, serviço, categoria, userId, traceId), busca,
    paginação por cursor, export CSV/JSON, RBAC admin/operador.

- [ ] **T-AUDIT-001 — Tela `/admin/audit-logs` (auditoria)** [P0][M][todo]
  - Spec: `docs/screens/audit-logs-screen.spec.md`.
  - AC: append-only, schema de auditoria com `actor/action/entity/before/after`,
    hash chain de integridade, retenção ≥ 5 anos, RBAC admin/auditor.

- [ ] **T-OBS-001 — Logger estruturado + correlação** [P0][S][todo]
  - AC: todo handler de borda emite log com schema definido no SDD.

- [ ] **T-SEC-001 — Headers de segurança + CSP** [P0][S][todo]
- [ ] **T-SEC-002 — Auth (login/logout/refresh) + rate limit** [P0][M][todo]
- [ ] **T-CI-001 — Pipeline ci.yml + security.yml** [P0][S][todo]
