# Definition of Done (DoD)

Uma tarefa só pode ser fechada quando:

## Código
- [ ] Critério de aceite (Gherkin) atendido.
- [ ] Lint, format, typecheck verdes.
- [ ] Sem TODO/FIXME novos sem ticket associado.
- [ ] Sem `console.log`/prints temporários.

## Testes
- [ ] Unit + integração + (E2E se UI) atualizados.
- [ ] Cobertura do diff ≥ 80%.
- [ ] Nenhum teste `skip`/`only`.

## Segurança
- [ ] SAST sem severidade High/Critical.
- [ ] SCA sem dependência vulnerável nova.
- [ ] Sem segredos no diff (Gitleaks).
- [ ] Headers/CSP/permissões revisados quando aplicável.

## Observabilidade
- [ ] Logs estruturados nas bordas (handler/job/cron).
- [ ] Métricas/traces necessários adicionados.

## Docs
- [ ] `CHANGELOG.md` (Unreleased) atualizado.
- [ ] Manual do usuário (`/manual`) atualizado se a tarefa expõe UI.
- [ ] ADR criado se houve decisão arquitetural.

## Telas obrigatórias
- [ ] Em projetos com UI, `/manual` e `/admin/logs` continuam funcionando.
