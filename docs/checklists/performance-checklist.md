# Checklist de Performance

## Frontend (web)
- [ ] LCP < 2.5s (P75 mobile 4G).
- [ ] INP < 200ms.
- [ ] CLS < 0.1.
- [ ] JS crítico < 170 KB gz.
- [ ] Imagens otimizadas (AVIF/WebP, `loading="lazy"`).
- [ ] Code-splitting por rota.
- [ ] CDN + cache headers.
- [ ] Lighthouse CI (mobile) ≥ 90.

## Backend
- [ ] P95 < SLO (definido no SDD).
- [ ] Sem N+1 (verificado por log/SQL trace).
- [ ] Índices revisados nas queries novas.
- [ ] Cache (HTTP/Redis) onde faz sentido.
- [ ] Paginação por cursor em listas grandes.
- [ ] Backpressure em filas/streams.

## Infra
- [ ] HPA configurado (k8s) ou auto-scale equivalente.
- [ ] Limites de CPU/memória definidos.
- [ ] Teste de carga (k6/Artillery) cobre rotas P0.
