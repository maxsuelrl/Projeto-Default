# AGENTS.md — Instruções para agentes de IA neste repositório

Este arquivo é o **contrato** que qualquer agente (Cursor, Claude, Codex,
Copilot, etc.) deve seguir ao trabalhar em **qualquer projeto** que use este
template.

## Regras gerais

1. **Spec primeiro, código depois**. Se não existir `docs/PRD.md` e
   `docs/SDD.md` atualizados para a tarefa, peça/gere antes de codar.
2. **Trabalhe sempre em cima de uma tarefa do `docs/backlog.md`**. Se a tarefa
   não estiver lá, adicione-a antes (com critério de aceite).
3. **Nunca finalize uma tarefa** sem cumprir os checklists em
   `docs/checklists/qa-checklist.md` e `docs/checklists/security-checklist.md`.
4. **Toda aplicação** entregue deve conter as telas `/manual` e `/admin/logs`
   descritas em `docs/screens/`.
5. **Conventional Commits** + **PR template** obrigatório.
6. **Não faça force-push, não amende commits assinados**, e não pule hooks
   (`--no-verify`).
7. Em caso de dúvida sobre arquitetura, abra um **ADR** em `docs/adr/` antes de
   implementar.

## Ordem de execução de uma tarefa

```
ler tarefa em backlog.md
   └─> ler PRD/SDD relacionados
        └─> implementar (skill 30-development)
             └─> testes (skill 31-testing) — falhou? volte
                  └─> security (skill 32-security) — finding High? volte
                       └─> abrir PR (DoD 100%)
```

## Definition of Done (resumo)

- [ ] Critério de aceite da tarefa atendido
- [ ] Testes unit + integração novos/atualizados, verde no CI
- [ ] Cobertura ≥ 80% no diff
- [ ] `lint`, `typecheck`, `format` verdes
- [ ] SAST sem severidade High/Critical
- [ ] Sem segredos no diff (`gitleaks`)
- [ ] Sem dependências vulneráveis novas
- [ ] Telemetria/log estruturado adicionado quando aplicável
- [ ] Doc de usuário atualizada (`/manual` se a tarefa expõe UI)
- [ ] CHANGELOG entry

## O que **não** fazer

- Não criar dependências sem registrar versão fixa.
- Não comentar código óbvio ("// incrementa contador").
- Não silenciar testes ou regras de lint para "passar o CI".
- Não logar PII, segredos, tokens ou dados sensíveis.
- Não introduzir endpoints ou jobs sem autenticação/autorização.
