# Spec — Tela `/admin/logs` (Logs **Técnicos** do Sistema)

> **Esta tela é só para logs técnicos** (o que o sistema fez). Auditoria de
> ações do usuário fica em outra tela com regras mais estritas — ver
> [`audit-logs-screen.spec.md`](./audit-logs-screen.spec.md).
>
> | Tela | Conteúdo | Acesso | Retenção |
> |---|---|---|---|
> | `/admin/logs` | Erros, latência, requests, jobs, integrações | `admin`, `operator` | 30-90 dias |
> | `/admin/audit-logs` | Ações do usuário (login, edição, export) | `admin`, `auditor` | ≥ 5 anos, append-only |
>
> Os dois são correlacionáveis via `traceId`/`requestId`.

## Objetivo
Visualização operacional dos logs estruturados de **todos** os serviços do
projeto, com filtros, busca e export. Não substitui o stack de
observabilidade externo; é a "porta da frente" dentro do produto para
operadores e admins. **Não use esta tela como trilha legal/forense** —
para isso existe `/admin/audit-logs`.

## Rota e permissões
- Rota: `/admin/logs`.
- Permissões: somente papéis `admin` e `operator`. Outros recebem 403.
- Auditoria: cada acesso gera `audit.log_view {by, filters}`.

## Schema de log técnico (fonte da verdade)
Todo serviço **deve** emitir JSON com este shape mínimo:

```json
{
  "ts": "2026-04-26T13:45:00.123Z",
  "level": "info",                     // debug|info|warn|error|fatal
  "service": "api",                    // nome do microserviço
  "env": "prod",                       // dev|staging|prod
  "category": "app",                   // app|security|integration|job
  "event": "http.request",             // dot.case
  "message": "GET /users/123 200",
  "traceId": "0af7651916cd43dd...",
  "spanId": "00f067aa0ba902b7",
  "userId": "u_123",                   // opcional
  "tenantId": "t_42",                  // opcional, se multitenant
  "requestId": "req_abc",
  "route": "/users/:id",
  "method": "GET",
  "status": 200,
  "latencyMs": 142,
  "outcome": "ok",                     // ok|error
  "errorCode": null,
  "errorStackHash": null,              // hash da stack (sem stack bruta)
  "context": { /* livre, sem PII */ }
}
```

**Eventos de auditoria** (login, alteração de papel, export de dados,
exclusão) **não** entram aqui — vão pra `/admin/audit-logs` com schema
próprio (ver `audit-logs-screen.spec.md`).

> Mascarar PII e segredos antes de logar. Tokens nunca, mesmo truncados.

## Camadas
1. **Coleta**: stdout JSON → agente (Fluent Bit / OTel Collector / Vector).
2. **Sink**: Loki, Elastic/OpenSearch, CloudWatch, Datadog ou Azure Monitor.
3. **API interna** `GET /internal/logs`:
   - Query params: `from`, `to`, `level`, `service`, `category`, `event`,
     `userId`, `traceId`, `q` (full text), `cursor`, `limit` (default 100,
     max 500).
   - Resposta: `{ items: Log[], nextCursor?: string }`.
4. **UI** consome a API.

## Layout
```
┌────────────────────────────────────────────────────────────────────────┐
│  Logs                                          [Export ▾]  [Atualizar] │
├────────────────────────────────────────────────────────────────────────┤
│ Período [Últimas 24h ▾]  Nível [todos ▾]  Serviço [todos ▾]            │
│ Categoria [todos ▾]  userId [____]  traceId [____]  q [_____________]  │
│ [Salvar filtro]  [Compartilhar link]                                    │
├────────────────────────────────────────────────────────────────────────┤
│ ts ▾                level  service  event           outcome  latency   │
│ 2026-04-26 13:45    INFO   api      user.login      ok       142ms    │
│   └─ traceId · userId · expandir JSON                                   │
│ ...                                                                    │
│                              [carregar mais]                            │
└────────────────────────────────────────────────────────────────────────┘
```

### Detalhe do log (drawer)
- JSON completo formatado.
- Botão "ver trace" (deep link para Tempo/Jaeger/Datadog APM com `traceId`).
- Botão "ver eventos do mesmo `requestId`".
- Botão "copiar como cURL" quando o evento é HTTP.

## Funcionalidades obrigatórias
- Filtros: período (presets + custom), nível, serviço, categoria, `userId`,
  `traceId`, busca textual.
- Paginação por **cursor**, ordem decrescente.
- Auto-refresh opcional (5s/15s/30s).
- Salvar filtro como bookmark + compartilhar via URL com query string.
- Export CSV/JSON do conjunto filtrado (limite configurável).
- Filtro "category=security" pré-pronto (eventos técnicos de segurança:
  rate-limit, csrf-fail, mfa-challenge). Para **ações** do usuário use
  `/admin/audit-logs`.
- Realce visual por nível (warn=âmbar, error=vermelho, fatal=vermelho fundo).
- Tema dark; densidade compacta/confortável.
- Acessibilidade: tabela navegável por teclado, leitor de tela.

## Segurança
- RBAC server-side (não confiar no client).
- Rate limit no `/internal/logs` (ex.: 60 req/min/usuário).
- Sem dados de outros tenants quando multitenant.
- Mascarar campos sensíveis remanescentes (`***`).
- Auditoria de acesso (`audit.log_view`).

## Telemetria da própria tela
- `logs.search` `{filters}`
- `logs.export` `{format, count}`
- `logs.detail_open` `{event, traceId}`

## Critérios de aceite
- E2E: como `admin`, abrir `/admin/logs`, aplicar filtros, exportar CSV;
  como `user`, receber 403.
- Performance: P95 da query < 1.5s para 24h em ambiente padrão.
- a11y: axe sem violações High/Critical, navegação 100% por teclado.
- Conformidade: nenhuma resposta contém PII não mascarada.

## Stack sugerida
- Frontend: tabela virtualizada (TanStack Table + react-window) ou
  AG Grid (community).
- Backend: BFF com adapter por sink (Loki/Elastic/CloudWatch/Datadog).
- Observabilidade: OpenTelemetry SDK em todos os serviços.
