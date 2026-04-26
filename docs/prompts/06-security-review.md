# Prompt — Revisão de segurança

Aplique:
- `docs/checklists/security-checklist.md` (pulse-check rápido), e
- `docs/templates/SECURITY-REVIEW.md` (formal, em **toda release** e em
  toda tarefa que toque auth/pagamento/dados pessoais/upload/permissões/
  integração externa).

Cruzar com `docs/THREAT-MODEL.md` (se existir) para garantir que cada
fluxo crítico afetado tem mitigação implementada.

Roteiro:
1. Liste rotas/handlers/jobs novos ou alterados.
2. Para cada um: AuthN, AuthZ, validação, encoding, logging, rate limit,
   tratamento de erro.
3. Rode (ou indique como rodar) Semgrep, Gitleaks, SCA, Trivy.
4. Reporte findings High/Critical com:
   - Caminho do arquivo + linha
   - Categoria (CWE/OWASP)
   - Sugestão de correção
5. Verifique:
   - logs técnicos sem PII (`/admin/logs`).
   - eventos esperados emitidos para auditoria (`/admin/audit-logs`).
6. Atualize `docs/THREAT-MODEL.md` se a mudança altera fluxo crítico.
7. Aprove só preenchendo `SECURITY-REVIEW.md` §7 com decisão.
