# Checklist de QA

> Aplicado por tarefa antes de fundir o PR.

## Funcional
- [ ] Critério de aceite Gherkin coberto por testes.
- [ ] Caminhos felizes + erros + bordas.
- [ ] i18n: textos extraídos, sem strings hard-coded de UI.
- [ ] Estados de UI: default, loading, empty, error.

## Pirâmide de testes
- [ ] Unit ≥ 80% do diff.
- [ ] Integração nas rotas/módulos tocados.
- [ ] Contrato (OpenAPI/Pact) atualizado quando aplicável.
- [ ] E2E para fluxos P0/P1.
- [ ] Visual regression em telas P0 (opcional, recomendado).

## Acessibilidade (WCAG 2.2 AA)
- [ ] axe sem violações High/Critical.
- [ ] Navegação completa por teclado.
- [ ] Contraste ≥ 4.5:1 (texto), 3:1 (UI).
- [ ] Foco visível.
- [ ] Labels e ARIA corretos.

## Performance
- [ ] Budgets do SDD respeitados (LCP/INP/TTI ou P95 backend).
- [ ] N+1, queries pesadas, payloads inflados — verificados.

## Compatibilidade
- [ ] Browsers/devices alvo do PRD.
- [ ] Dark mode + responsivo (mobile/tablet/desktop).

## Logs/Telemetria
- [ ] Eventos relevantes logados (entrada/saída/erros).
- [ ] Métricas RED quando aplicável.

## Telas obrigatórias
- [ ] `/manual` continua passando smoke E2E.
- [ ] `/admin/logs` continua passando smoke E2E.
