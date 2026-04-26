# ADR-0001 — Stack obrigatória do template

- **Status**: aceito
- **Data**: 2026-04-26
- **Decisores**: time core do `Projeto-Padrão`
- **Contexto**: o template anterior era stack-agnostic. Cada projeto novo
  redecidia frontend/backend/banco e isso virava débito (decisões repetidas,
  inconsistências, falta de reuso de componentes/skills/CI). Como o objetivo
  é desenvolvimento 100% IA padronizado, fixar a stack acelera o onboarding
  e reduz a superfície de erro.

## Decisão

Todos os projetos derivados deste template **devem** usar:

| Camada | Tecnologia |
|---|---|
| Frontend | Vue 3 + **PrimeVue 4** (preset Aura) + Vite + TypeScript + Pinia |
| Backend | **FastAPI** + Pydantic v2 + SQLAlchemy 2 + Alembic + Argon2id + structlog |
| Banco | **Postgres 16** com extensão `pgcrypto` |
| Orquestração | **Docker Compose** (dev) e build multi-stage (prod) |

Mudanças desta stack exigem ADR específico no projeto derivado, com
justificativa técnica e impacto estimado. Não é proibido — é só explícito.

## Alternativas consideradas

- **React + Material UI / shadcn**: maior comunidade JS, mas exigiria
  manter dois templates ou abandonar Vue. Vue+PrimeVue dá tabela, datepicker,
  validação acessível out-of-the-box sem decidir 5 libs adicionais.
- **Django**: ORM e admin maduros, mas FastAPI é mais aderente a APIs
  tipadas (Pydantic v2) e tem melhor suporte assíncrono para integrações.
- **MongoDB**: menos overhead inicial, mas perde transação ACID e a cadeia
  de hash do audit-log fica mais frágil. Postgres + JSONB cobre os casos
  schemaless quando necessário.
- **Kubernetes em vez de Compose**: Compose é suficiente para dev e
  deploys pequenos; o template não impede migração para k8s depois.

## Consequências

- **Positivas**:
  - Skills do Cursor (`30-development`, `32-security`) ficam concretas
    (sabem onde aplicar — `apps/backend`, `apps/frontend`).
  - CI deixa de "detectar stack" e roda jobs específicos.
  - Telas obrigatórias `/manual`, `/admin/logs`, `/admin/audit-logs` já
    nascem implementadas.
  - Bootstrap `make setup && make up` deixa o projeto rodando localmente.
- **Negativas / dívida**:
  - Time precisa subir nessas tecnologias antes (curva de aprendizado).
  - Projetos com necessidade muito específica (ex.: app desktop, mobile
    nativo) não se encaixam — devem usar **outro** template.
- **Impacto em segurança / compliance**:
  - Argon2id, headers/CSP do FastAPI, trigger append-only do audit-log e
    Trivy scan das imagens viram **default**, não opcionais.
