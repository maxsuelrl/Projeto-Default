# Prompt — PRD → SDD

Você é um Tech Lead. Use `docs/PRD.md` para preencher
`docs/templates/SDD.md` em `docs/SDD.md`.

Obrigatório:
- Diagrama Mermaid de arquitetura.
- OpenAPI mínimo (paths principais).
- DDL ou schema Prisma das entidades.
- NFRs com números (P95, RPS, RPO/RTO).
- ADRs para: linguagem, banco, auth, infra, observabilidade.
- Plano de testes com cobertura mínima 80% no diff.
- Plano de release (canário + rollback).
- Listar telas obrigatórias: `/manual`, `/admin/logs` (técnicos) e
  `/admin/audit-logs` (auditoria de ações).
- Inicializar `docs/THREAT-MODEL.md` se houver: auth, pagamento, multitenant,
  upload, dados pessoais, integrações externas.
- Inicializar `docs/PRIVACY-LGPD.md` se houver dado pessoal.
- Inicializar `docs/RUNBOOK.md` com as seções principais (mesmo vazias).

Em pontos sem informação suficiente: levantar **open questions** ao final.
