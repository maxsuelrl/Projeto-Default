# Checklist de Segurança (AppSec)

> Baseado em OWASP ASVS L2 + Top 10 + LGPD. Aplicado por tarefa.

## AuthN / AuthZ
- [ ] Autenticação obrigatória em rotas privadas; default = negar.
- [ ] Autorização por papel/atributo (RBAC/ABAC) + teste de IDOR.
- [ ] Senhas com Argon2id (ou bcrypt ≥ 12) + política mínima.
- [ ] MFA disponível para admins.
- [ ] Sessões: rotação no login, expiração, revogação.

## Entrada / saída
- [ ] Validação com schema (zod/pydantic/JSR-303).
- [ ] Encoding/escape de saída.
- [ ] Proteção contra SQLi/NoSQLi (queries parametrizadas/ORM).
- [ ] Proteção contra XSS (sanitizar HTML rico, CSP estrita).
- [ ] CSRF token em forms cookie-based.

## Headers e transporte
- [ ] HTTPS obrigatório, HSTS preload.
- [ ] CSP estrita, sem `unsafe-inline`/`unsafe-eval` quando possível.
- [ ] X-Content-Type-Options: nosniff.
- [ ] Referrer-Policy: no-referrer (ou strict-origin-when-cross-origin).
- [ ] Permissions-Policy mínima.
- [ ] Cookies: `Secure; HttpOnly; SameSite=Lax|Strict`.
- [ ] CORS restrito.

## Segredos
- [ ] Nenhum segredo no repo (Gitleaks verde).
- [ ] `.env.example` com chaves, valores reais em cofre (Vault/SM/KV).
- [ ] Rotação documentada.

## Logs e privacidade
- [ ] Sem PII/segredos em logs (mascaramento).
- [ ] Eventos de segurança auditáveis (login, mudança de papel, export).
- [ ] LGPD: base legal mapeada, retenção configurada, direito de exclusão.

## Dependências e supply chain
- [ ] Versões fixas (lockfile commitado).
- [ ] SCA verde (`npm audit --omit=dev`/`pip-audit`/`govulncheck`).
- [ ] Trivy `fs` + `image` (se Docker) sem High/Critical.
- [ ] Provenance/SBOM gerado (CycloneDX) — opcional, recomendado.

## IaC e infraestrutura
- [ ] Checkov/tfsec verdes.
- [ ] Princípio do menor privilégio em IAM.
- [ ] Rede privada por padrão; egress controlado.
- [ ] Backups + restore testado.

## Resiliência
- [ ] Rate limiting em auth e endpoints sensíveis.
- [ ] Lockout/throttling progressivo.
- [ ] Idempotência em escrita externa (chave em header).

## Observabilidade de segurança
- [ ] `/admin/logs?category=security` retorna eventos esperados.
- [ ] Alertas (PagerDuty/Opsgenie) configurados para falhas críticas.
