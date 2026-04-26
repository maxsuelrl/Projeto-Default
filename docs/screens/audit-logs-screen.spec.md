# Spec — Tela `/admin/audit-logs` (Auditoria de Ações)

## Objetivo

Trilha de auditoria **somente** de **ações do usuário** sobre dados do
sistema. Diferente de `/admin/logs` (técnico, com ruído de operação), aqui
o conteúdo é **limpo, consultável e seguro**, com retenção e mascaramento
estritos para atender LGPD, SOC2 e investigações forenses.

> **Regra de ouro**: se o evento descreve "o que o sistema fez" → vai pra
> `/admin/logs`.
> Se descreve "o que o usuário fez" (ou um sistema agindo em nome dele) →
> vai pra `/admin/audit-logs`.

## Rota e permissões

- Rota: `/admin/audit-logs`.
- Permissões: papel `auditor` ou `admin` (mais restrito que `/admin/logs`,
  que aceita `operator`).
- Acesso ao audit-log **gera audit-log** (`audit.audit_view`). Auditor
  legítimo terá um trace de uso normal; comportamento anômalo dispara
  alerta.

## Schema de evento de auditoria

Sink **separado** do log técnico (banco append-only, recomendação:
PostgreSQL com tabela `audit_events` particionada por mês, ou serviço
dedicado tipo Datadog Audit Trail / AWS CloudTrail Lake). **Não usar o
mesmo sink do logs técnicos** — diferente retenção, diferente RBAC.

```json
{
  "ts": "2026-04-26T14:33:21.001Z",
  "actor": {
    "userId": "u_123",
    "email": "operador@empresa.com",
    "role": "operator",
    "tenantId": "t_42",
    "ip": "203.0.113.10",
    "userAgent": "Mozilla/5.0 ...",
    "sessionId": "s_abc"
  },
  "action": "user.update",
  "entity": {
    "type": "user",
    "id": "u_777",
    "tenantId": "t_42"
  },
  "before": { "role": "viewer", "active": true },
  "after":  { "role": "editor", "active": true },
  "outcome": "ok",
  "reason": "ticket OPS-1234 — promoção solicitada por gerente",
  "requestId": "req_abc",
  "traceId": "0af7651916cd43dd...",
  "integrity": {
    "prevHash": "sha256:...",
    "hash": "sha256:..."
  }
}
```

### Campos obrigatórios
- `actor`: quem fez (incluindo IP/UA para forense).
- `action`: verbo em `dot.case` (`auth.login`, `user.update`,
  `payment.refund`, `data.export`).
- `entity`: o que foi afetado (com `tenantId` em multitenant).
- `before` / `after`: diff explícito do estado afetado, **com PII
  mascarada** (CPF → `***.***.***-12`, e-mail → `o***@empresa.com`).
- `outcome`: `ok | denied | error`.
- `reason`: campo livre (usado em ações sensíveis: aprovações, exportações,
  exclusões em massa).
- `integrity.hash`: hash encadeado com o evento anterior (write-once).
  Permite detecção de adulteração offline.

## Categorias mínimas de ações auditadas

- **Identidade**: `auth.login` (sucesso/falha), `auth.logout`,
  `auth.password_reset`, `auth.mfa_enroll`, `auth.session_revoke`.
- **Autorização**: `role.assign`, `role.revoke`, `permission.grant`,
  `permission.deny`.
- **Dados sensíveis**: `data.read_pii`, `data.export`, `data.delete`,
  `data.bulk_update`.
- **Operações destrutivas**: `entity.delete`, `entity.archive`,
  `tenant.purge`.
- **Pagamentos** (se aplicável): `payment.create`, `payment.refund`,
  `payment.fail`.
- **Configuração**: `config.update`, `feature_flag.toggle`,
  `secret.rotate`.

## Layout

```
┌──────────────────────────────────────────────────────────────────────┐
│  Auditoria                              [Export ▾]  [Verificar hash] │
├──────────────────────────────────────────────────────────────────────┤
│ Período [Últimos 30d ▾]  Ator [____]  Tenant [____]  Action [____]  │
│ Entidade [____]  Outcome [todos ▾]  q [_____________]                 │
├──────────────────────────────────────────────────────────────────────┤
│ ts                  ator                action       entidade  result │
│ 2026-04-26 14:33    operador@empresa.com user.update u_777     ok    │
│   └─ ver diff before/after · razão · integridade                      │
│ ...                                                                   │
└──────────────────────────────────────────────────────────────────────┘
```

### Detalhe (drawer)
- `before` × `after` lado a lado com diff visual (PII já mascarada).
- Cadeia de integridade: botão "verificar" recalcula hash da janela
  selecionada e mostra ✅ / ❌.
- Link "ver evento técnico" leva a `/admin/logs?traceId=...` (mesma
  correlação, telas separadas).

## Funcionalidades obrigatórias

- Filtros: período, ator (`userId` ou e-mail), tenant, action, entity,
  outcome, busca textual em `reason`.
- Paginação **cursor + ordem decrescente determinística**
  (`ts DESC, id DESC`).
- Export CSV/JSON **assinado** (HMAC) — quem exportou, quando, filtros
  usados.
- **Sem edição. Sem exclusão.** Audit-log é append-only por contrato.
- Modo "investigação": congela um conjunto de eventos para evidência
  (snapshot imutável com URL pública para um auditor externo, com TTL).
- Verificação de cadeia de integridade (hash chain) na UI.
- A11y: navegação 100% por teclado, leitor de tela.

## Segurança e privacidade

- RBAC server-side. UI só esconde itens de outro tenant; backend **nunca**
  retorna eventos cross-tenant.
- Mascaramento de PII no momento da gravação (não da leitura).
- Retenção: mínimo **5 anos** para identidade e dados sensíveis (LGPD/
  SOC2); configurável por categoria. Apaga **somente** quando legalmente
  obrigado, com ato registrado em `audit.retention_purge`.
- Backup imutável (Object Lock S3 / Azure Blob immutable).
- Acesso ao audit-log é, ele próprio, evento auditado (`audit.audit_view`,
  `audit.audit_export`).
- Alertas: 5 falhas de login do mesmo ator < 5min, export > N eventos,
  acesso em horário atípico, etc.

## Critérios de aceite

- E2E: como `auditor`, abrir `/admin/audit-logs`, filtrar por ator e
  exportar JSON. Como `operator`, receber 403.
- E2E: tentar editar/deletar um evento via API → 405/403 e gera
  `audit.tamper_attempt`.
- Integridade: rodar verificação numa janela de 1000 eventos →
  hash bate (sem ❌).
- Sem PII bruta na resposta (`grep` por padrões CPF/cartão/e-mail
  completo deve falhar).
- Performance: P95 de query < 2s para 30d em ambiente padrão.

## Stack sugerida

- Banco: Postgres (tabela append-only com trigger anti-update/delete +
  hash chain) ou serviço dedicado (Datadog Audit Trail, AWS CloudTrail
  Lake, GCP Audit Logs, Snowflake imutável).
- Backend: writer dedicado, idempotente (chave `requestId+action+entity`).
- Frontend: tabela virtualizada + diff viewer (`react-diff-viewer-continued`).
