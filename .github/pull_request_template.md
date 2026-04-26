# PR — <título curto>

Refs: T-XXX (link para o `backlog.md`).

## O que muda
- ...

## Por quê
- ...

## Como testar
1. ...
2. ...

## Checklists
### DoD
- [ ] Critério de aceite (Gherkin) atendido
- [ ] Lint, format, typecheck verdes
- [ ] Testes verdes (unit + integ + E2E quando aplicável)
- [ ] Cobertura do diff ≥ 80%
- [ ] `CHANGELOG.md` (Unreleased) atualizado

### QA — `docs/checklists/qa-checklist.md`
- [ ] Estados de UI (default/loading/empty/error)
- [ ] a11y (axe sem High/Critical, teclado, contraste)
- [ ] Performance dentro do budget
- [ ] Telas obrigatórias `/manual` e `/admin/logs` ainda passam smoke

### Segurança — `docs/checklists/security-checklist.md`
- [ ] AuthN/AuthZ revisados
- [ ] Validação de entrada + encoding de saída
- [ ] Sem segredos no diff (Gitleaks)
- [ ] SAST sem High/Critical
- [ ] SCA sem dependência vulnerável nova
- [ ] Logs sem PII / segredos
- [ ] Headers/CSP/cookies revisados (se aplicável)

### Documentação
- [ ] `/manual` atualizado se a tarefa expõe UI
- [ ] ADR criado se houve decisão arquitetural
- [ ] Spec de telas obrigatórias atualizada se mudou contrato

## Riscos e rollback
- ...
