# Prompt — Geração de testes

Para a tarefa `T-XXX`:

1. Identifique funções/componentes/rotas tocados.
2. Gere testes nas camadas exigidas pelo `qa-checklist.md`.
3. Garanta cobertura ≥ 80% do diff.
4. Inclua casos: feliz, erro, borda, vazio, loading (UI), sem permissão,
   payload inválido.
5. Para UI: inclua a11y (axe) e teclado.
6. Para API: inclua contrato (OpenAPI/Pact).
7. Sem mocks no núcleo; use fakes determinísticos.

Não silencie testes flaky — reporte como item separado no `RISKS.md`.
