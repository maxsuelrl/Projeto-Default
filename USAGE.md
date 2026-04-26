# USAGE — Manual prático do `Projeto-Padrão`

> Como aplicar este repositório no seu dia a dia, do **"tive uma idéia"** ao
> **"está em produção"**, em 100% IA.

Este manual é o **complemento prático** do `README.md`. Ele responde:

1. [Como configurar uma vez](#1-setup-único-uma-vez-na-vida)
2. [Como começar um projeto novo](#2-começando-um-projeto-novo-fase-1-e-2)
3. [Rotina de desenvolvimento por tarefa](#3-rotina-diária-fase-3-ciclo-iterativo)
4. [O que rodar antes de abrir o PR](#4-checklist-rápido-antes-do-pr)
5. [Como fechar uma versão / release](#5-fechando-uma-versão-fase-4)
6. [Como recuperar o fluxo quando algo dá errado](#6-troubleshooting-do-dia-a-dia)
7. [Cola de comandos](#7-cola-de-comandos)

---

## 1. Setup único (uma vez na vida)

> Você só faz isso **uma vez por máquina** e **uma vez por repositório novo**.

### 1.1 Na sua máquina (instalar ferramentas)

Mínimo necessário (o resto cada projeto define no SDD):

```bash
# Cursor (IDE com agente)
# https://cursor.com  — instale e faça login

# Git + GitHub CLI
brew install git gh        # macOS
sudo apt install git gh    # Linux Debian/Ubuntu

# Scanners locais (opcionais mas recomendados)
brew install semgrep gitleaks trivy
# ou: pipx install semgrep ; go install github.com/zricethezav/gitleaks/v8@latest

# Login no GitHub CLI
gh auth login
```

### 1.2 No GitHub (uma vez por repositório novo)

Em `Settings → Actions → General → Workflow permissions`:
- Marque **"Allow GitHub Actions to create and approve pull requests"** ✅
  *(necessário para o `release-please`)*

Em `Settings → Code security → Dependabot`:
- Ligue **Dependabot alerts** + **Dependabot security updates** ✅

Se o repo for **privado sem GHAS**, em `Settings → Secrets and variables → Actions → Variables` adicione:
- `ENABLE_CODE_SCANNING_UPLOAD = false`
- `ENABLE_CODEQL = false`

(Se for público, ignore — o default já funciona e é gratuito.)

### 1.3 No Cursor (uma vez)

As skills em `.cursor/rules/` são detectadas automaticamente. Confirme que
sua extensão Cursor leu `00-core.mdc` (a barra de chat menciona a regra
ativa). Recomendados para potencializar:

| MCP | Uso | Como instalar |
|---|---|---|
| GitHub | criar/ler issues e PRs do chat | `Settings → MCP → Add → GitHub` |
| Linear | sincronizar `backlog.md` com tickets | idem |
| Context7 | docs atualizadas de libs | idem (este repo já usa) |
| Playwright | gerar/manter testes E2E | idem |

---

## 2. Começando um projeto novo (Fase 1 e 2)

### 2.1 Bootstrap

```bash
# Estando na pasta-mãe deste template
./scripts/new-project.sh meu-app
cd ../meu-app
gh repo create meu-app --private --source=. --remote=origin --push
```

O script já:
- Copia o esqueleto para `../meu-app`.
- Renomeia `docs/templates/PRD.md` → `docs/PRD.md` (idem SDD, backlog, etc.).
- Inicializa git com primeiro commit.

Se preferir usar este repo como **template do GitHub** em vez do script:
`Use this template → Create a new repository`.

### 2.2 Idéia → PRD (Spec-Driven Development)

No Cursor, abra um chat **dentro do projeto novo** e cole o conteúdo de
`docs/prompts/01-prd-from-idea.md`, substituindo a idéia. Exemplo real:

> Você é um Product Manager sênior. Recebi a idéia abaixo e preciso de um PRD
> seguindo estritamente o template `docs/templates/PRD.md`.
>
> **Idéia**: "Quero um app web para meu studio de pilates gerenciar alunos,
> agendamentos recorrentes e pagamentos mensais via Pix. Recepcionista
> agenda, professor confirma presença, dono vê faturamento."
>
> Saída: `docs/PRD.md` completo.

Revise o PRD que ele gerou. **Edite manualmente** o que estiver fora de
contexto. Não confie cegamente — o agente é seu copiloto, não seu PO.

### 2.3 PRD → SDD (decisões técnicas)

Mesma idéia, prompt `docs/prompts/02-sdd-from-prd.md`:

> Use `docs/PRD.md` para preencher `docs/templates/SDD.md` em `docs/SDD.md`.
> Inclua diagrama Mermaid, OpenAPI mínimo, DDL, NFRs com números, ADRs e
> plano de testes/release. Levante open questions ao final.

Aqui o agente vai te perguntar coisas tipo:
- *"Linguagem? Banco? Auth via e-mail/Google? Multi-tenant?"*

Responda. As decisões viram **ADRs** em `docs/adr/ADR-0001-*.md`. Você
nunca mais vai esquecer por que escolheu Postgres em vez de Mongo.

### 2.4 SDD → backlog atômico

Prompt `docs/prompts/03-backlog-from-sdd.md`. Resultado: `docs/backlog.md`
com tarefas tipo:

```
- [ ] T-008 — Login com e-mail e senha [P0][M][todo]
  - Contexto: SDD §3.2, ADR-0003
  - Critério de aceite (Gherkin):
    - Given um usuário cadastrado
    - When envio POST /auth/login com credenciais válidas
    - Then recebo 200 + cookie HttpOnly Secure SameSite=Lax
    - And um log info com event=user.login outcome=ok é emitido
  - Dependências: T-002 (schema users), T-007 (rate limit middleware)
  - Riscos: brute force — mitigado em T-009 (lockout exponencial)
```

> **Regra de ouro**: 1 tarefa = 1 PR. Se uma tarefa está estimada em `L`
> (3-5 dias), quebre em duas. Nunca tente fazer "uma feature inteira" num
> PR só.

### 2.5 Prototipação (Fase 2)

1. Use **Google Stitch / v0 / Figma Make** para gerar telas a partir do PRD.
2. Salve os fluxos em `docs/UX/flows.md` (Mermaid).
3. Defina design tokens em `docs/UX/tokens.md` (cor, tipografia, spacing).
4. **Sempre** adicione no inventário as duas telas obrigatórias:
   `/manual` e `/admin/logs`.

### 2.6 Quando o planejamento está "pronto"?

Quando você consegue marcar todos os itens da `docs/templates/DoR.md`
**em pelo menos as 3-5 tarefas P0**. Não espere o backlog ficar perfeito;
ele evolui junto com o projeto.

---

## 3. Rotina diária (Fase 3 — Ciclo iterativo)

### 3.1 O loop por tarefa

```
┌──────────────────────────────────────────────────────────┐
│  ESCOLHER tarefa (T-xxx) em docs/backlog.md              │
│         ↓                                                │
│  CRIAR branch  feat/T-xxx-<slug>                         │
│         ↓                                                │
│  IMPLEMENTAR (skill 30-development)                      │
│         ↓                                                │
│  TESTAR (skill 31-testing)  ── falhou? ──► VOLTA ↑       │
│         ↓                                                │
│  REVISAR Sec (skill 32-security) ── High? ──► VOLTA ↑    │
│         ↓                                                │
│  COMMIT + PUSH + PR (template marcado)                   │
│         ↓                                                │
│  CI verde + review humano  ──►  MERGE                    │
└──────────────────────────────────────────────────────────┘
```

### 3.2 Passo a passo, com comandos reais

**Passo 1 — Pegar tarefa**
```bash
# Veja o backlog
sed -n '/^- \[ \]/p' docs/backlog.md | head -20
# Pegue a próxima P0 sem dependência aberta. Ex.: T-008
```

**Passo 2 — Branch**
```bash
git checkout main && git pull
git checkout -b feat/T-008-login-email-senha
```

**Passo 3 — Implementar (Cursor chat)**

Cole `docs/prompts/04-task-implementation.md` e diga:
> Implemente a tarefa **T-008** seguindo `.cursor/rules/30-development.mdc`.

A skill `00-core` vai te lembrar de:
- Ler o trecho do SDD relacionado.
- Manter logs estruturados nas bordas.
- Atualizar `CHANGELOG.md` (Unreleased).
- Atualizar `/manual` se a tarefa expõe UI.

**Passo 4 — Testes**

```text
> Aplique a skill 31-testing.mdc na tarefa T-008. Cubra: feliz, credencial
> errada, lockout, payload inválido, a11y do form de login, contrato OpenAPI
> da rota /auth/login. Cobertura ≥ 80% do diff.
```

Rode local:
```bash
make test     # ou npm test, pytest, go test ./... — depende da stack
```

**Passo 5 — Segurança**

```text
> Aplique 32-security.mdc no diff atual. Liste rotas/handlers novos e
> verifique AuthN/AuthZ, validação, rate limit, logs sem PII. Rode (ou
> indique como rodar) Semgrep, Gitleaks e SCA.
```

Rode local:
```bash
make sec
# que executa:
#   gitleaks detect --no-banner -v
#   semgrep --config p/owasp-top-ten --error
```

**Passo 6 — Commit + push + PR**

```bash
git add -A
git commit -m "feat(auth): login com e-mail e senha (T-008)

- POST /auth/login com cookie HttpOnly Secure SameSite=Lax
- Rate limit 10/min/IP, lockout exponencial após 5 falhas
- Logs estruturados: event=user.login outcome=ok|error
- Atualiza /manual seção 'Acessando a conta'
- Cobertura do diff: 87%"
git push -u origin feat/T-008-login-email-senha
gh pr create --fill --base main --draft
```

O template `.github/pull_request_template.md` aparece automaticamente.
**Marque os checklists** (DoD, QA, Sec). Se está em draft, o agente pode
pedir review quando terminar.

### 3.3 Quanto tempo cada passo dura?

> Não é uma questão de tempo, é uma questão de **gates**. Não passe pro
> próximo passo enquanto:
>
> - Lint/typecheck/format → **vermelho** = volta
> - Testes → **vermelho** = volta
> - Cobertura do diff < 80% → volta
> - SAST/SCA com **High/Critical** = volta
> - Logs com PII = volta

### 3.4 Tarefas obrigatórias todo projeto (não esqueça)

Independente do produto, o backlog **sempre** tem essas:

| ID | Descrição | Prioridade |
|---|---|---|
| `T-OBS-001` | Logger estruturado + correlação (traceId) | P0 |
| `T-CI-001` | Pipeline `ci.yml` + `security.yml` rodando | P0 |
| `T-SEC-001` | Headers de segurança + CSP | P0 |
| `T-SEC-002` | Auth (login/logout/refresh) + rate limit | P0 |
| `T-MANUAL-001` | Tela `/manual` (spec em `docs/screens/`) | P0 |
| `T-LOGS-001` | Tela `/admin/logs` (spec em `docs/screens/`) | P0 |

Se elas não estão em `docs/backlog.md`, copie do template antes de começar.

---

## 4. Checklist rápido antes do PR

> Se um item está em **vermelho**, **não abra o PR**. Resolva primeiro.

```text
[ ] Critério de aceite Gherkin atendido (testei manualmente)
[ ] make lint  → verde
[ ] make test  → verde
[ ] Cobertura do diff ≥ 80%
[ ] make sec   → 0 finding High/Critical
[ ] Sem PII em logs (revisei o que vai pra `/admin/logs`)
[ ] CHANGELOG.md (Unreleased) atualizado
[ ] /manual atualizado (se a tarefa expõe UI)
[ ] /admin/logs continua passando smoke (se houver UI)
[ ] PR template marcado
```

Os checklists completos estão em `docs/checklists/` — sirva-se à vontade.

---

## 5. Fechando uma versão (Fase 4)

Quando todas as tarefas P0/P1 do milestone estão `done`:

### 5.1 Antes de tagear
```text
> Use docs/prompts/07-release-notes.md para gerar docs/RELEASE.md e
> atualizar CHANGELOG.md.
```

Revise os 5 bullets de "highlights". Confirme:
- Breaking changes documentados.
- Plano de rollback testado em staging.
- `release-checklist.md` 100%.

### 5.2 Tagear
Como o repo usa **release-please**, você **não tagea manualmente**:

1. Faça merge na `main`.
2. O workflow `release.yml` abre automaticamente uma PR `chore: release vX.Y.Z`.
3. Você revisa, mergea, e ele cria a tag + release no GitHub.

Se quiser forçar um release agora: `Actions → Release → Run workflow`.

### 5.3 Pós-release (24h)

A tela `/admin/logs` **vira o seu painel**:
- Filtre `level=error` período "últimas 24h" — sem aumento esperado.
- Filtre `category=security` — sem eventos novos suspeitos.
- Métricas P95, taxa 5xx, alertas Sentry.

Se algo passou despercebido: rollback (instruções no `RELEASE.md`).

---

## 6. Troubleshooting do dia a dia

### "O agente não está seguindo as skills"
- Confirme que está no projeto certo (`.cursor/rules/` existe).
- Recarregue a janela do Cursor.
- Cite a skill explicitamente: *"Aplique `.cursor/rules/30-development.mdc`"*.

### "CI falhou em release-please"
> *"GitHub Actions is not permitted to create or approve pull requests"*

Veja `README.md` §6.1 — falta ligar a flag em Settings ou criar
`RELEASE_PLEASE_TOKEN`.

### "CI falhou em upload de SARIF (Code scanning not enabled)"
Repo privado sem GHAS. Defina as variáveis:
- `ENABLE_CODE_SCANNING_UPLOAD = false`
- `ENABLE_CODEQL = false`

### "Backlog inchou demais e perdi o controle"
1. Releia `docs/PRD.md` § Escopo. Tudo que não atende objetivo do milestone
   atual vira `docs/backlog.md` seção `## Próximas iterações`.
2. Quebre tarefas `L` em pares de `M` ou trios de `S`.
3. Use `gh issue` + MCP do Linear para visualizar Kanban — markdown não é
   bom pra mais de ~50 itens ativos.

### "Esqueci de fazer ADR antes de codar e mudei o banco"
Crie o ADR retroativo agora. Melhor tarde do que nunca. Marque
`Status: aceito (registrado retroativamente em <data>)`.

### "Tarefa cresceu no meio do caminho"
Pare. Faça commit do que tem como WIP. Quebre o restante em `T-xxx-2`,
`T-xxx-3` no backlog. Fechar PR de 800 linhas é receita pra bug.

### "Conflito entre testes e prazo"
Não existe. Se "não dá tempo de testar", a tarefa estava mal estimada.
Reduza escopo, não qualidade. Releia o DoD.

---

## 7. Cola de comandos

```bash
# Bootstrap
./scripts/new-project.sh nome-app

# Dia a dia
git checkout -b feat/T-xxx-slug
make lint
make test
make sec
git commit -m "feat(area): descrição (T-xxx)"
gh pr create --fill --base main --draft

# Release
gh workflow run release.yml      # forçar abertura da PR de release
gh release list

# Investigação rápida
gh run list --limit 5            # últimos runs
gh run view --log-failed         # log do que falhou
gh pr checks <pr-number>         # status dos checks
```

### Mapa mental do repo (cole na cabeça)

```
.cursor/rules/   = skills do agente por fase (00 core, 10 plan, 20 proto,
                   30 dev, 31 test, 32 sec, 40 release, 90 telas)
docs/templates/  = formulários em branco — copie para docs/<nome>.md
docs/checklists/ = listas que você marca antes do PR
docs/screens/    = contrato das telas obrigatórias /manual e /admin/logs
docs/prompts/    = prompts prontos pra colar no chat do Cursor
docs/tooling.md  = quais MCPs/ferramentas usar em cada fase
.github/         = CI/Sec/Release + templates de PR/issue
scripts/         = automações (bootstrap)
```

---

## TL;DR — sua semana usando este template

| Quando | Faça |
|---|---|
| Idéia nova | Bootstrap → PRD (prompt 01) → SDD (02) → backlog (03) |
| Toda manhã | Pegar próxima tarefa P0/P1 do `backlog.md` |
| Para cada tarefa | Branch → prompt 04 (dev) → 05 (test) → 06 (sec) → PR |
| Antes do PR | Checklist §4 deste doc |
| Fim do milestone | Prompt 07 → merge na `main` → release automático |
| Toda segunda | Olhar `/admin/logs?category=security` da semana |

Está tudo aqui no repo. Use, evolua, e abra PR melhorando este `USAGE.md`
sempre que descobrir um atalho novo.
