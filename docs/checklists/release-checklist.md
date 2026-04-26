# Checklist de Release

## Pré-release
- [ ] CI verde em `main`.
- [ ] Cobertura geral ≥ 80%.
- [ ] SAST/SCA sem High/Critical.
- [ ] `CHANGELOG.md` consolidado.
- [ ] `RELEASE.md` preenchido (highlights, breaking, rollback).
- [ ] `docs/manual/` atualizado e refletido em `/manual`.
- [ ] Tela `/admin/logs` funcional em staging contra dados reais.
- [ ] Migrações testadas (forward + rollback) em staging.
- [ ] Feature flags configuradas no painel.
- [ ] Dashboards e alertas atualizados (Grafana/Datadog).

## Release
- [ ] Tag SemVer criada.
- [ ] Deploy canário (1% → 10% → 50% → 100%).
- [ ] Métricas observadas em cada degrau.

## Pós-release (24h)
- [ ] Sem aumento de erro 5xx > 0.5pp.
- [ ] Latência P95 estável.
- [ ] Sem alertas de segurança novos.
- [ ] Notas de release publicadas (interno + externo).
