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
- Listar `/manual` e `/admin/logs` como telas obrigatórias.

Em pontos sem informação suficiente: levantar **open questions** ao final.
