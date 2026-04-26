# Security Review — <release vX.Y.Z ou tarefa T-XXX>

> Revisão de segurança formal. Aplicada em **toda release** e em **toda
> tarefa que toque** auth, pagamento, dados pessoais, integração externa,
> permissões ou upload.
> Para um pulse-check rápido por tarefa, use `docs/checklists/security-checklist.md`.

## 1. Contexto

- Tarefa(s) / release: ...
- Diff: <link para PR ou tag>
- Componentes afetados: ...
- Linkar `docs/THREAT-MODEL.md` seções aplicáveis: ...

## 2. Mudanças com impacto de segurança

| Área | Mudança | Risco potencial | Onde foi mitigado |
|------|---------|-----------------|-------------------|
| AuthN | ... | ... | ... |
| AuthZ | ... | ... | ... |
| Validação | ... | ... | ... |
| Crypto | ... | ... | ... |
| Logs/Audit | ... | ... | ... |

## 3. Resultados de scans

| Scanner | Versão | Findings High/Critical | Link |
|---------|--------|------------------------|------|
| Semgrep | ... | 0 | run #... |
| Gitleaks | ... | 0 | run #... |
| Trivy fs | v0.35.0 (SHA pinado) | 0 | run #... |
| CodeQL | ... | 0 | run #... |
| SCA (`npm audit`/`pip-audit`/`govulncheck`) | ... | 0 | local |
| ZAP baseline (staging) | ... | 0 alta | run #... |

> Findings ignorados precisam de justificativa neste documento (com prazo
> de revisão).

## 4. Verificação de checklist

- [ ] `docs/checklists/security-checklist.md` 100%
- [ ] Headers + CSP revisados (`securityheaders.com` ou equivalente)
- [ ] Logs sem PII (sample de 10 eventos revisado)
- [ ] Audit-log emitindo eventos esperados
- [ ] Threat Model atualizado se o fluxo crítico mudou
- [ ] Rotina de rotação de segredos validada (último uso < 90 dias)

## 5. Testes de segurança específicos

(Marcar os aplicáveis ao diff.)

- [ ] IDOR multi-tenant
- [ ] Brute-force / lockout
- [ ] CSRF
- [ ] SSRF
- [ ] Upload mal-formado
- [ ] Injection (SQL/NoSQL/Command)
- [ ] XSS reflected/stored/DOM
- [ ] Open redirect
- [ ] Privilege escalation horizontal/vertical

## 6. Riscos residuais

- Aceitos: ... (referenciar `THREAT-MODEL §7`)
- Acompanhados: ...

## 7. Decisão

- [ ] **Aprovado** para deploy
- [ ] **Aprovado com condições** (listar)
- [ ] **Reprovado** (motivo)

## 8. Aprovadores

- Reviewer de segurança: ___ — data: ___
- Eng lead: ___ — data: ___
- DPO (se houver dado pessoal): ___ — data: ___
