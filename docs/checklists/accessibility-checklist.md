# Checklist de Acessibilidade — WCAG 2.2 AA

- [ ] Estrutura semântica (landmarks, headings em ordem).
- [ ] Texto alternativo em imagens significativas; `alt=""` em decorativas.
- [ ] Contraste ≥ 4.5:1 (texto) e 3:1 (UI).
- [ ] Foco visível e ordem lógica de tabulação.
- [ ] Componentes interativos com role/aria adequados.
- [ ] Mensagens de erro associadas via `aria-describedby`.
- [ ] Sem armadilhas de teclado.
- [ ] Targets ≥ 24×24 CSS px (idealmente 44×44).
- [ ] Movimento/animações respeitam `prefers-reduced-motion`.
- [ ] Áudio/vídeo com legendas e transcrição.
- [ ] Testado com NVDA/VoiceOver (smoke).
- [ ] axe sem violações High/Critical no CI.
