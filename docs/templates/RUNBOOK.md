# Runbook — <Nome do Projeto>

> Documento operacional. Renomeie para `docs/RUNBOOK.md`. Aqui mora **tudo
> que você vai esquecer** depois de 2 meses sem mexer no projeto. Atualize
> imediatamente após qualquer mudança operacional.

## Índice
1. [Contatos e responsabilidades](#1-contatos-e-responsabilidades)
2. [Ambientes](#2-ambientes)
3. [Subir ambiente local](#3-subir-ambiente-local)
4. [Subir staging](#4-subir-staging)
5. [Deploy em produção](#5-deploy-em-produção)
6. [Rollback](#6-rollback)
7. [Restaurar backup](#7-restaurar-backup)
8. [Investigar erro 500](#8-investigar-erro-500)
9. [Investigar login falhando](#9-investigar-login-falhando)
10. [Consultar logs](#10-consultar-logs)
11. [Rotacionar segredos](#11-rotacionar-segredos)
12. [Incidente de segurança](#12-incidente-de-segurança)
13. [Manutenção programada](#13-manutenção-programada)

---

## 1. Contatos e responsabilidades

| Papel | Quem | Canal |
|-------|------|-------|
| Tech lead | ... | ... |
| On-call | ... | PagerDuty / Opsgenie |
| Segurança | ... | security@... |
| DPO | ... | dpo@... |
| Provider (cloud) — suporte | ... | console + ticket |

## 2. Ambientes

| Ambiente | URL | Branch | Database | Logs sink | Observação |
|----------|-----|--------|----------|-----------|------------|
| dev local | localhost | feature/* | docker | stdout | sem dados reais |
| staging | https://staging... | main (após merge) | rds-staging | Loki/Grafana | dados anonimizados |
| prod | https://app... | tag vX.Y.Z | rds-prod | Datadog | dados reais |

## 3. Subir ambiente local

```bash
git clone <repo>
cd <repo>
cp .env.example .env   # preencher segredos via cofre
make setup
make dev               # ou docker compose up
```

Acesse `http://localhost:3000`. Verifique `/manual` e `/admin/logs` no login
seed (`admin@local / dev123`).

Problemas comuns:
- Porta ocupada → `lsof -i :3000`.
- Migração faltando → `make db-migrate`.
- Cache → `make clean && make setup`.

## 4. Subir staging

Push para `main` → workflow `deploy-staging.yml` faz build, teste,
migração e deploy automático. Deploy manual: `gh workflow run deploy-staging.yml`.

Validar pós-deploy:
- [ ] Smoke E2E (`gh run list --workflow=e2e-staging.yml`).
- [ ] `/admin/logs?level=error&period=15m` → vazio.
- [ ] Métricas P95 estáveis em Grafana.

## 5. Deploy em produção

Pré-condições:
- [ ] Tag `vX.Y.Z` criada via release-please.
- [ ] `docs/RELEASE.md` revisado.
- [ ] `docs/checklists/release-checklist.md` 100%.
- [ ] Janela de manutenção comunicada (se aplicável).

```bash
gh workflow run deploy-prod.yml --ref vX.Y.Z
```

Estratégia: canário 1% → 10% → 50% → 100% (cada degrau aguarda 10 min ou
override manual).

Em cada degrau, verificar:
- 5xx < 0.5pp acima do baseline
- P95 < SLO
- alertas Sentry / Datadog
- `/admin/logs?level=error` sem novidades

## 6. Rollback

> Tempo alvo: < 5 minutos.

```bash
# 1. Reverte deploy para tag anterior
gh workflow run deploy-prod.yml --ref v<anterior>

# 2. Se houve migração, reverter ANTES (verificar plano em RELEASE.md)
make db-migrate-down VERSION=<anterior>

# 3. Limpar cache
make cache-flush
```

Pós-rollback:
- [ ] Postmortem em `docs/postmortems/YYYY-MM-DD-...md`.
- [ ] Issue para corrigir o que falhou.

## 7. Restaurar backup

### Banco
```bash
# Listar pontos de restauração
make db-snapshots

# Restaurar para um banco temporário
make db-restore SNAPSHOT=<id> TARGET=tmp_db

# Validar
psql tmp_db -c "SELECT count(*) FROM users;"

# Promover (com janela de manutenção)
make db-promote TARGET=tmp_db
```

### Object storage
- S3/Azure Blob com versionamento + Object Lock.
- Restauração: `aws s3api copy-object --version-id <id> ...`.

## 8. Investigar erro 500

1. Abra `/admin/logs?level=error&period=1h`.
2. Identifique `event` e `service` predominantes.
3. Use `traceId` no APM (Datadog/Tempo) para ver o span exato.
4. Se for integração externa: `category=integration` filtra.
5. Se for um usuário específico: filtre `userId`.
6. Tem padrão? Crie issue com `traceId`s exemplares.

Mitigação rápida:
- Feature flag `kill-switch` na rota.
- Rollback (§6).

## 9. Investigar login falhando

1. `/admin/audit-logs?action=auth.login&outcome=error&period=1h`.
2. Filtre por `actor.email` se for caso pontual.
3. Cruze com `/admin/logs?event=auth.*&period=1h` para ver erro técnico.
4. Possíveis causas: lockout exponencial, MFA expirado, integração de SSO
   com falha, rate-limit excessivo.

## 10. Consultar logs

| Cenário | Onde |
|---------|------|
| Erro de aplicação | `/admin/logs` (técnico) |
| Quem fez o quê | `/admin/audit-logs` (auditoria) |
| Throughput / latência | Grafana / Datadog |
| Stack trace completa | Sentry |
| Trace distribuído | Tempo / Jaeger / Datadog APM (`traceId`) |
| Logs do build | GitHub Actions → run específico |

## 11. Rotacionar segredos

Rotação obrigatória:
- A cada **90 dias** (calendarizar).
- **Imediatamente** após desligamento de pessoa com acesso.
- **Imediatamente** após qualquer suspeita de vazamento.

```bash
# 1. Criar novo segredo no cofre
vault kv put secret/<svc>/jwt_signing v=$(openssl rand -base64 32)

# 2. Restart rolling para os serviços lerem o novo
make restart-rolling SVC=<svc>

# 3. Confirmar token antigo invalidado
curl -H "Authorization: Bearer <token-antigo>" $URL  # deve retornar 401

# 4. Atualizar audit-log
# automaticamente: evento secret.rotate
```

Para credenciais de banco: usar IAM auth quando possível (sem segredo
estático).

## 12. Incidente de segurança

> Procedimento mínimo. Ajustar conforme severidade.

### Detecção
- Alerta automático (Datadog/PagerDuty).
- Reporte por canal `SECURITY.md`.

### Triagem (primeiros 30 min)
1. Confirmar: é um incidente real ou falso positivo?
2. Classificar severidade (Crítico/Alto/Médio/Baixo).
3. Abrir war-room (canal dedicado).
4. **Não** apagar evidência. Preservar logs.

### Contenção
1. Isolar componente afetado (feature flag, IP block, revogar token).
2. Rotacionar segredos comprometidos (§11).
3. Forçar logout global se sessão pode estar comprometida.

### Erradicação
1. Aplicar patch.
2. Revisar acesso de usuários potencialmente impactados.

### Recuperação
1. Restaurar serviço gradualmente, monitorando.
2. Validar com `/admin/audit-logs` que não há atividade suspeita.

### Pós-incidente
- [ ] Postmortem em `docs/postmortems/`.
- [ ] Notificação à ANPD em até 2 dias úteis se houver dado pessoal
      afetado (ver `docs/PRIVACY-LGPD.md` §8).
- [ ] Comunicação aos titulares afetados.
- [ ] Plano de ação com prazos.
- [ ] Atualizar `docs/THREAT-MODEL.md`.

## 13. Manutenção programada

```bash
# Ativa modo manutenção (banner + 503 nas rotas mutáveis)
make maintenance-on

# ... mudança ...

make maintenance-off
```

Comunicação prévia: 48h antes via e-mail + status page.
