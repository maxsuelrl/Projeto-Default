# Prompt — Revisão de segurança

Aplique o `docs/checklists/security-checklist.md` ao diff atual.

Roteiro:
1. Liste rotas/handlers/jobs novos ou alterados.
2. Para cada um: AuthN, AuthZ, validação, encoding, logging, rate limit,
   tratamento de erro.
3. Rode (ou indique como rodar) Semgrep, Gitleaks, SCA, Trivy.
4. Reporte findings High/Critical com:
   - Caminho do arquivo + linha
   - Categoria (CWE/OWASP)
   - Sugestão de correção
5. Verifique se logs cobrem `category=security` e estão sem PII.
6. Aprove só com todos os itens marcados.
