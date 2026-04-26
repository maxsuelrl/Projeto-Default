# Projeto-Padrão — Template de Desenvolvimento 100% IA

Estrutura padrão para iniciar **qualquer** projeto de software seguindo o fluxo
**SDD (Spec-Driven Development) → Prototipação → Ciclo Dev/Test/Sec → Finalização**.

> Objetivo: garantir que toda nova ideia siga o mesmo trilho, com QA e
> Segurança embutidos no ciclo, e que **toda** entrega contenha as telas
> obrigatórias de **Manual do Usuário** e **Logs do Sistema**.

---

## 1. Fluxo end-to-end

```
┌──────────────┐    ┌──────────────┐    ┌──────────────────────────────┐    ┌──────────────────┐
│ 1. PLANEJAR  │ →  │ 2. PROTOTIPAR│ →  │ 3. CICLO ITERATIVO           │ →  │ 4. FINALIZAR     │
│  (PRD + SDD) │    │  (Stitch +   │    │  Dev → Test → Sec → Review   │    │  (Manual + Logs  │
│              │    │  Figma/v0)   │    │  ↻ por tarefa do backlog.md  │    │  + Release)      │
└──────────────┘    └──────────────┘    └──────────────────────────────┘    └──────────────────┘
       │                   │                          │                              │
       ▼                   ▼                          ▼                              ▼
  docs/PRD.md         docs/UX/                  src/ + tests/                  /manual e /logs
  docs/SDD.md         (telas, flows)            CI: lint+test+SAST             docs/RELEASE.md
  docs/backlog.md                               +deps +secrets                 CHANGELOG.md
```

Cada fase tem **skill (Cursor rule)**, **template de doc** e **checklist**
correspondentes neste repositório.

---

## 2. Estrutura do repositório

```
.
├── AGENTS.md                       # Instruções para qualquer agente de IA
├── README.md                       # Este arquivo
├── SECURITY.md                     # Política de divulgação responsável
├── CONTRIBUTING.md                 # Como contribuir / fluxo de PR
├── CODEOWNERS
├── .editorconfig
├── .gitignore
│
├── .cursor/
│   └── rules/                      # Skills do Cursor por fase
│       ├── 00-core.mdc             # Regras gerais (sempre on)
│       ├── 10-planning.mdc         # Fase 1: PRD/SDD
│       ├── 20-prototyping.mdc      # Fase 2: Stitch/UI
│       ├── 30-development.mdc      # Fase 3a: Codificação
│       ├── 31-testing.mdc          # Fase 3b: QA / testes
│       ├── 32-security.mdc         # Fase 3c: AppSec
│       ├── 40-finalization.mdc     # Fase 4: Manuais, logs, release
│       └── 90-screens-mandatory.mdc# Telas obrigatórias (manual + logs)
│
├── docs/
│   ├── templates/                  # Copie e renomeie ao iniciar projeto
│   │   ├── PRD.md
│   │   ├── SDD.md
│   │   ├── backlog.md
│   │   ├── ADR-0000-template.md
│   │   ├── DoR.md                  # Definition of Ready
│   │   ├── DoD.md                  # Definition of Done
│   │   ├── RISKS.md
│   │   ├── RELEASE.md
│   │   └── CHANGELOG.md
│   ├── checklists/
│   │   ├── qa-checklist.md
│   │   ├── security-checklist.md
│   │   ├── accessibility-checklist.md
│   │   ├── performance-checklist.md
│   │   └── release-checklist.md
│   ├── screens/
│   │   ├── manual-screen.spec.md   # Spec da tela /manual
│   │   └── logs-screen.spec.md     # Spec da tela /admin/logs
│   ├── tooling.md                  # MCPs, plugins, integrações
│   └── prompts/                    # Prompts reutilizáveis por fase
│       ├── 01-prd-from-idea.md
│       ├── 02-sdd-from-prd.md
│       ├── 03-backlog-from-sdd.md
│       ├── 04-task-implementation.md
│       ├── 05-test-generation.md
│       ├── 06-security-review.md
│       └── 07-release-notes.md
│
├── .github/
│   ├── pull_request_template.md
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── security_report.md
│   ├── dependabot.yml
│   └── workflows/
│       ├── ci.yml                  # lint + test + coverage
│       ├── security.yml            # SAST + secrets + deps
│       └── release.yml             # changelog + tag
│
└── scripts/
    └── new-project.sh              # Bootstrap de um novo projeto
```

---

## 3. As 4 fases em detalhe

### Fase 1 — Planejar (SDD)
1. Idéia bruta → `docs/templates/PRD.md` (Product Requirements Document).
2. PRD → `docs/templates/SDD.md` (Spec-Driven Design: contratos, modelos,
   decisões arquiteturais, NFRs).
3. SDD → `docs/templates/backlog.md` em **tarefas atômicas** (cada uma
   testável individualmente, com critério de aceite).

Skill: `.cursor/rules/10-planning.mdc`
Prompts: `docs/prompts/01-*`, `02-*`, `03-*`.

### Fase 2 — Prototipar
- UI no **Google Stitch** + iteração em **v0 / Figma Make**.
- Exporte os fluxos para `docs/UX/` (será criada por projeto).
- Defina design tokens (cor, tipografia, espaçamento) já no SDD.

Skill: `.cursor/rules/20-prototyping.mdc`.

### Fase 3 — Ciclo iterativo (Dev → Test → Sec)
Para **cada tarefa** do `backlog.md`, em ordem:

1. **Dev**: implementar com a skill `30-development.mdc` (TDD opcional).
2. **Test**: skill `31-testing.mdc` gera/atualiza testes unit + integração + E2E
   conforme `qa-checklist.md`. CI roda em PR.
3. **Sec**: skill `32-security.mdc` aplica `security-checklist.md` + roda SAST,
   scan de dependências e segredos.
4. **Review**: PR só funde se DoD bater 100%.

> **Gate obrigatório**: nenhuma tarefa é fechada com testes vermelhos, finding
> de SAST de severidade **High/Critical** ou cobertura < 80% do código novo.

### Fase 4 — Finalizar
- Tela `/manual` populada (ver `docs/screens/manual-screen.spec.md`).
- Tela `/admin/logs` ativa em todos os sistemas (ver
  `docs/screens/logs-screen.spec.md`).
- `RELEASE.md` + `CHANGELOG.md` atualizados.
- `release-checklist.md` 100%.

Skill: `.cursor/rules/40-finalization.mdc`.

---

## 4. Telas obrigatórias em **todo** sistema

| Tela            | Rota sugerida   | Quem vê        | Spec                                   |
|-----------------|-----------------|----------------|----------------------------------------|
| Manual do usuário| `/manual`      | Qualquer user  | `docs/screens/manual-screen.spec.md`   |
| Logs do sistema  | `/admin/logs`  | Admin/Operador | `docs/screens/logs-screen.spec.md`     |

Estão descritas como contrato (campos, filtros, permissões, telemetria,
acessibilidade) para serem implementadas em qualquer stack.

---

## 5. Tooling / MCPs recomendados

Ver `docs/tooling.md` para a stack completa (Cursor MCPs, GitHub, Linear,
Stitch, Figma, Sentry, Datadog/Grafana, Semgrep, Trivy, Gitleaks, Playwright,
etc.) e em que fase usar cada um.

---

## 6. Como iniciar um novo projeto

```bash
./scripts/new-project.sh meu-novo-projeto
```

O script copia este esqueleto para `../meu-novo-projeto`, inicializa git,
cria os docs a partir dos templates e abre o backlog em branco pronto para
ser preenchido a partir do PRD.

### 6.1 Setup do GitHub (uma vez por repo)

#### Obrigatório
1. **Permitir Actions criarem PRs** (para o `release-please` funcionar):
   `Settings → Actions → General → Workflow permissions` →
   marque **"Allow GitHub Actions to create and approve pull requests"**.

   *Alternativa*: criar PAT fine-grained (`contents:write`, `pull-requests:write`)
   e salvar como secret `RELEASE_PLEASE_TOKEN`. O workflow usa
   `RELEASE_PLEASE_TOKEN || GITHUB_TOKEN`.

#### Sobre Code Scanning (custo)
**Code scanning** (a aba "Security → Code scanning alerts" e o upload de SARIF
de Semgrep/Trivy/CodeQL) é:

- **Grátis em repositórios públicos** ✅
- **Pago em repositórios privados** (parte do **GitHub Advanced Security – GHAS**)

Você **não precisa** de GHAS para os gates de segurança funcionarem. Mesmo
sem ele:
- Semgrep, Gitleaks, Trivy e ZAP **continuam rodando** no CI.
- O job **continua falhando** o PR em findings High/Critical.
- Os relatórios SARIF são salvos como **artifact** do run (download por
  release/PR), em vez de aparecerem na aba Security.

Para desligar o upload de SARIF (caso o repo seja privado e sem GHAS),
em `Settings → Secrets and variables → Actions → Variables` defina:

| Variável | Valor | Efeito |
|---|---|---|
| `ENABLE_CODE_SCANNING_UPLOAD` | `false` | SARIF do Semgrep/Trivy vira artifact em vez de upload |
| `ENABLE_CODEQL` | `false` | Pula o job CodeQL inteiro |

Se o repo for público (ou tiver GHAS), pode ignorar — o default já é o
caminho ideal e tudo aparece em "Security".

Tabela rápida do que custa o quê:

| Recurso | Repo público | Repo privado |
|---|---|---|
| Code scanning (SARIF, CodeQL) | grátis | GHAS (pago) |
| Secret scanning + push protection | grátis | GHAS (pago) |
| Dependabot alerts/updates | grátis | grátis |
| Actions (rodar Semgrep/Trivy/Gitleaks/ZAP) | grátis | grátis (cota do plano) |

#### Recomendado
2. **Habilitar Dependabot alerts**: `Settings → Code security → Dependabot` →
   ativar **Dependabot alerts** e **Dependabot security updates** (grátis em
   qualquer repo).
3. **Branch protection** em `main`: exigir CI verde, PR review e
   Conventional Commits.

---

## 7. Convenções rápidas

- **Branch**: `feat/<tarefa-id>-<slug>`, `fix/...`, `chore/...`.
- **Commits**: Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `sec:`).
- **PR**: deve referenciar a tarefa do `backlog.md` e marcar todos os itens do
  `pull_request_template.md`.
- **ADR**: toda decisão arquitetural não-óbvia vira um ADR em `docs/adr/`.
