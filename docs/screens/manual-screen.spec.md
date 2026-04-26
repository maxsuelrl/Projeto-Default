# Spec — Tela `/manual` (Manual do Usuário)

## Objetivo
Documentação **embutida** no produto, sempre disponível para o usuário final,
versionada junto do código, sem dependência de site externo.

## Rota e permissões
- Rota: `/manual` (autenticada). Versão pública opcional em `/help`.
- Permissões: qualquer usuário autenticado pode ler.
- A11y: WCAG 2.2 AA.

## Layout
```
┌──────────────────────────────────────────────────────────────────┐
│  [Logo] Manual                                  [🔍 buscar...]   │
├──────────────┬───────────────────────────────────────────────────┤
│ Sumário      │ # Título da seção                                 │
│ - Primeiros  │                                                   │
│   passos     │ Conteúdo MDX/markdown...                          │
│ - Funcional. │                                                   │
│ - FAQ        │ ## Subseção                                       │
│ - Atalhos    │                                                   │
│ - Glossário  │ Vídeos, imagens, callouts (info/warn/danger).     │
│ - Suporte    │                                                   │
└──────────────┴───────────────────────────────────────────────────┘
                                           [< anterior]  [próximo >]
```

## Conteúdo (estrutura mínima)
1. **Primeiros passos** — onboarding em 3-5 passos.
2. **Funcionalidades** — uma seção por feature P0/P1.
3. **Atalhos de teclado**.
4. **FAQ**.
5. **Solução de problemas** (com link "Reportar bug").
6. **Glossário**.
7. **Política de privacidade & LGPD** (link).
8. **Contato/Suporte**.

## Fonte do conteúdo
- Arquivos em `docs/manual/**.mdx` (ou `.md`), versionados.
- Front-matter:
  ```yaml
  ---
  title: ...
  section: primeiros-passos
  order: 10
  updatedAt: 2026-01-01
  audience: [end-user, admin]
  ---
  ```

## Funcionalidades obrigatórias
- **Busca client-side** (Pagefind/Fuse.js), com destaque de match.
- **Sumário lateral** auto-gerado a partir dos H2/H3.
- **Navegação anterior/próximo** entre seções.
- **Deep links** com âncoras (`/manual/funcionalidades#exportar`).
- **Print friendly** (CSS `@media print`).
- **Multi-idioma** (i18n via pasta por locale: `docs/manual/pt-BR/`,
  `docs/manual/en/`).
- **Indicador "última atualização"** por seção.
- **Botão "feedback"** (👍/👎 + comentário) que envia evento `manual.feedback`
  para a fila de telemetria.

## Telemetria
Eventos esperados (aparecem em `/admin/logs?service=manual`):
- `manual.view` `{section}`
- `manual.search` `{query, results}`
- `manual.feedback` `{section, score, comment?}`

## Critérios de aceite
- E2E: abrir `/manual`, buscar termo presente, clicar resultado, validar
  âncora.
- E2E: navegar com teclado do início ao fim sem armadilhas.
- a11y: axe sem violações High/Critical.
- Conteúdo: existem ao menos as 8 seções listadas.

## Stack sugerida
- React/Next.js: `@next/mdx` + `pagefind`.
- Vue/Nuxt: `@nuxt/content`.
- Backend-rendered: pasta de markdown + `markdown-it` + busca via Lunr.
- Mobile: Markdown renderer (react-native-markdown-display) + Algolia DocSearch.
