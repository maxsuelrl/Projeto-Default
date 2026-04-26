# Tooling, plugins e MCPs por fase

> Sugestão de stack conectada ao Cursor + GitHub. Cada item está **opcional**;
> escolha por projeto e registre no SDD.

## Fase 1 — Planejamento
| Função | Ferramenta |
|---|---|
| IDE/agente | Cursor (este repo) com skills em `.cursor/rules/` |
| MCP de issues | GitHub MCP / Linear MCP (criar tarefas direto do backlog) |
| MCP de docs | Context7 (consultar docs de libs sem alucinar versão) |
| MCP de filesystem | nativo do Cursor |
| Diagramas | Mermaid (no markdown) + Excalidraw |
| RFC/ADR | template em `docs/templates/ADR-0000-template.md` |

## Fase 2 — Prototipação
| Função | Ferramenta |
|---|---|
| UI generativa | Google Stitch, v0.dev, Figma Make, Galileo AI |
| Design source | Figma (com Tokens Studio) |
| Sync tokens | Style Dictionary / Tokens Studio → CSS/Tailwind |
| Acessibilidade no design | Stark, Able, Contrast Checker |
| Handoff | Figma Dev Mode / Zeplin |

## Fase 3a — Desenvolvimento
| Função | Ferramenta |
|---|---|
| Lint/format | ESLint + Prettier (JS/TS), Ruff + Black (Py), golangci-lint |
| Type | TypeScript strict, mypy/pyright, sqlc, Prisma |
| Logger | Pino, Winston, structlog, Zap, Logback |
| Tracing | OpenTelemetry SDK + Collector |
| Métricas | Prometheus client, OTel metrics |
| Feature flags | Unleash, ConfigCat, LaunchDarkly |
| Cache | Redis / Valkey |
| Fila | RabbitMQ / Kafka / SQS / Redis Streams |

## Fase 3b — Testes (QA)
| Camada | Ferramenta |
|---|---|
| Unit | Vitest/Jest, Pytest, Go test, JUnit |
| Integração | Testcontainers, Supertest, httpx |
| Contrato | Pact, Schemathesis, Dredd, OpenAPI Validator |
| E2E web | Playwright |
| E2E mobile | Detox / Maestro |
| Visual | Chromatic / Percy / Playwright snapshots |
| a11y | axe-core, Lighthouse CI |
| Performance | k6, Artillery, Lighthouse CI |
| Cobertura | c8/Istanbul, coverage.py, gocov |

## Fase 3c — Segurança (DevSecOps)
| Tipo | Ferramenta |
|---|---|
| SAST | Semgrep (rules `p/owasp-top-ten` + linguagem), CodeQL |
| Secrets | Gitleaks, TruffleHog |
| SCA | npm audit, pip-audit, govulncheck, Trivy `fs` |
| Container | Trivy `image`, Grype, Dockle |
| IaC | Checkov, tfsec, KICS |
| DAST | OWASP ZAP (smoke em staging) |
| SBOM | Syft (CycloneDX/SPDX) |
| Cofre de segredos | Vault, AWS Secrets Manager, Azure Key Vault, GCP SM |

## Fase 4 — Finalização & Operação
| Função | Ferramenta |
|---|---|
| Logs (sink) | Grafana Loki, Elastic/OpenSearch, CloudWatch, Datadog, Azure Monitor |
| Métricas | Prometheus + Grafana, Datadog, New Relic |
| Tracing | Tempo/Jaeger, Datadog APM, Honeycomb |
| Erros | Sentry, Bugsnag |
| Status page | Statuspage, Better Uptime |
| Alertas | Alertmanager, PagerDuty, Opsgenie |
| Release notes | release-please, semantic-release |
| Manual no produto | MDX + Pagefind / Algolia DocSearch |

## MCPs recomendados no Cursor
- **GitHub** — para criar PRs, ler issues, runs do CI.
- **Linear/Jira** — sincronizar `backlog.md` com tickets.
- **Context7** — docs atualizadas de libs/SDKs.
- **Sentry** — puxar erros para reproduzir + criar tarefa.
- **Postgres/MySQL** — explorar schema / rodar queries (somente leitura no
  modo dev).
- **Playwright** — gerar/manter testes E2E.
- **Filesystem** — nativo, para o template manter consistência.
- **Browser/Computer-use** — para validação manual de UI quando necessário.

## Integração com este repo
- Skills em `.cursor/rules/` orientam o agente em cada fase.
- Workflows em `.github/workflows/` aplicam os gates QA/Sec automaticamente.
- Templates em `docs/templates/` viram os artefatos vivos do projeto.
