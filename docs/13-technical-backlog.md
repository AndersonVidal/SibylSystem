# SibylSystem — Backlog Técnico

> **Documento da Fase 2 (Arquitetura) — Task 2.6.**
> Fontes: PDD, CLAUDE.md (fonte de verdade) e `08`–`12` (arquitetura, domínio, dados, UX, setup).
> Em caso de conflito, o CLAUDE.md prevalece.
>
> **Propósito:** transformar a arquitetura da Fase 2 em um **backlog técnico implementável** —
> épicos, tasks pequenas, dependências, mapeamento de releases e análise de risco.
>
> **Restrições desta task:** não implementa, não escreve código, não cria migrations/telas; não
> altera decisões anteriores; não cria funcionalidades; não discute otimizações prematuras.
> Apenas **organiza o trabalho técnico**.
>
> O backlog é detalhado o suficiente para que cada task de implementação seja executada
> individualmente **sem redefinir** arquitetura, domínio, dados ou UX.

---

## 1. Technical Work Breakdown

Blocos de trabalho agrupados por área técnica, espelhando os módulos da Task 2.1 + fundação +
operação.

| Área | Origem | Conteúdo |
|---|---|---|
| **Fundação do Projeto** | Task 2.5 (§6) | Scaffolding Django, apps de domínio, SQLite, layout base, navegação, htmx, qualidade (Ruff/Black/pre-commit). |
| **Autenticação (Acesso)** | E1 / Task 2.1 | Usuário único, login, logout, proteção de acesso. |
| **Tarefas** | E3 / Task 2.2–2.3 | Estrutura de dados + criar, listar, concluir. |
| **Eventos** | E2 | Estrutura de dados + criar, listar. |
| **Metas** | E4 | Estrutura de dados + criar, listar, atualizar progresso. |
| **Dashboard (Painel)** | E5 | Os 5 blocos + ordenação + anti-sobreposição + ações diretas. |
| **Gestão Plena** | Should Have | Editar/Excluir dos três conceitos. |
| **Deploy & Operação** | Task 2.5 (§8–9) | Produção, hospedagem com volume persistente, backups, monitoramento mínimo. |

---

## 2. Dependency Analysis

**O que precisa existir antes:**
- A **Fundação** (scaffolding + layout) precede tudo.
- A **Autenticação** precede todos os conceitos (o `ownerId` vem do usuário autenticado — Task 2.3;
  e todas as telas internas são protegidas — Task 2.4).
- Cada **estrutura de dados** de um conceito precede as operações desse conceito.
- Cada **bloco do Dashboard** depende do conceito que ele consome (Painel apenas lê — Task 2.1).
- **Deploy** depende de existir um conjunto funcional executável.

**O que pode ser desenvolvido em paralelo (em princípio):**
- Após Fundação + Autenticação, os três conceitos (**Tarefas, Eventos, Metas**) são independentes
  entre si (independência de domínio — Task 2.2/2.3) e poderiam ser construídos em paralelo. Como
  o projeto tem **um desenvolvedor**, a execução é sequencial, seguindo a ordem do PDD.

**O que depende de quê (cadeia, sem ciclos):**
```
Fundação → Autenticação → [Tarefas | Eventos | Metas] → Blocos do Dashboard (por conceito)
                                                       → Gestão Plena (por conceito)
Conjunto funcional → Deploy & Operação
```

**Ordem lógica de construção:** segue a "Ordem de Construção" do PDD (Parte 7), detalhada na §5.

---

## 3. Technical Epics

| ID | Nome | Objetivo | Valor entregue | Dependências | Critério de conclusão |
|---|---|---|---|---|---|
| **TE-0** | Fundação do Projeto | Preparar o esqueleto técnico (Task 2.5) e as garantias de qualidade. | Base sobre a qual todo o resto é construído; app roda localmente. | — | Projeto Django sobe localmente, apps de domínio criados, layout base com navegação e htmx disponíveis, e qualidade (Ruff/Black/pre-commit) configurada. |
| **TE-1** | Autenticação | Proteger o espaço pessoal do usuário único. | Acesso seguro; pré-requisito de todos os conceitos. | TE-0 | Usuário consegue logar/deslogar; telas internas exigem sessão. |
| **TE-2** | Tarefas | Registrar e concluir tarefas. | O fluxo mais frequente; valor imediato (R1). | TE-1 | Criar, listar e concluir tarefas funcionando, com estados vazio/conteúdo. |
| **TE-3** | Eventos | Registrar ocorrências datadas. | Compromissos fora da memória (R2). | TE-1 | Criar e listar eventos funcionando, com estados vazio/conteúdo. |
| **TE-4** | Metas | Registrar objetivos e acompanhar progresso. | Objetivos visíveis e rastreáveis (R3). | TE-1 | Criar, listar e atualizar progresso de metas funcionando. |
| **TE-5** | Dashboard (Painel) | Consolidar os 5 blocos em uma visão. | A principal experiência do produto. | TE-2, TE-3, TE-4 (por bloco) | Os 5 blocos exibem seus itens conforme regras, com ordenação e anti-sobreposição. |
| **TE-6** | Gestão Plena | Editar/Excluir os três conceitos. | Dados confiáveis a longo prazo (R4); MVP encerrado. | TE-2, TE-3, TE-4 | Editar e excluir disponíveis para Evento, Tarefa e Meta. |
| **TE-7** | Deploy & Operação | Publicar e operar o MVP com segurança de dados. | Sistema utilizável de verdade pelo usuário. | Conjunto funcional do R1 | App em produção com volume persistente, backups e monitoramento mínimo. |

---

## 4. Technical Tasks

Tasks pequenas, executáveis individualmente. Toda task de criação preenche `ownerId` a partir do
usuário autenticado (Task 2.3) — registrado uma vez aqui para não repetir em cada linha.

### TE-0 — Fundação do Projeto

| ID | Nome | Objetivo | Dependências | Resultado esperado |
|---|---|---|---|---|
| T0.1 | Scaffolding + apps de domínio | Criar projeto Django com `config/` e apps `accounts/events/tasks/goals/dashboard`; SQLite configurado. | — | Servidor de desenvolvimento sobe; estrutura da Task 2.5 (§6) presente. |
| T0.2 | Layout base + navegação + htmx | Template base com navegação persistente (Dashboard/Eventos/Tarefas/Metas + Logout), CSS estrutural mínimo e htmx integrado. | T0.1 | Telas herdam o layout; navegação e htmx prontos para uso. |
| T0.3 | Qualidade do projeto | Configurar Ruff, Black e pre-commit (Critérios de Qualidade do CLAUDE.md). | T0.1 | Lint/format automáticos e hook de pre-commit ativos antes do código de conceito. |

### TE-1 — Autenticação

| ID | Nome | Objetivo | Dependências | Resultado esperado |
|---|---|---|---|---|
| T1.1 | Provisionar usuário único | Mecanismo para criar/garantir o único Usuário (Task 2.3, restrição "usuário único"). | T0.1 | Existe um usuário apto a autenticar. |
| T1.2 | Login | Tela de Login + autenticação de sessão (Task 2.4). | T0.2, T1.1 | Usuário autentica e é levado ao Dashboard. |
| T1.3 | Logout | Ação persistente de encerrar sessão. | T1.2 | Usuário desloga e retorna ao Login. |
| T1.4 | Proteção de acesso | Exigir sessão nas telas internas; raiz → Dashboard (autenticado) ou Login (não autenticado). | T1.2 | Telas internas inacessíveis sem sessão. |

### TE-2 — Tarefas

| ID | Nome | Objetivo | Dependências | Resultado esperado |
|---|---|---|---|---|
| T2.1 | Estrutura de dados Tarefa | Definir modelo (título, status, prazo, `ownerId`) + migration; status padrão Pendente. | T1.1 | Estrutura persistente de Tarefa conforme Task 2.3. |
| T2.2 | Criar Tarefa | Formulário na tela Tarefas (título obrigatório; prazo opcional). | T2.1, T1.4 | Tarefa criada como Pendente e listada. |
| T2.3 | Listar Tarefas | Tela Tarefas com estados vazio/conteúdo; indicação **derivada** de atrasada (Task 2.3). | T2.1, T1.4 | Lista de tarefas com status e prazo visíveis. |
| T2.4 | Concluir Tarefa | Ação de conclusão (transição Pendente→Concluída) via htmx. | T2.3 | Tarefa concluída sai dos blocos do Dashboard. |

### TE-3 — Eventos

| ID | Nome | Objetivo | Dependências | Resultado esperado |
|---|---|---|---|---|
| T3.1 | Estrutura de dados Evento | Definir modelo (título, data, horário opcional, `ownerId`) + migration. | T1.1 | Estrutura persistente de Evento conforme Task 2.3. |
| T3.2 | Criar Evento | Formulário na tela Eventos (título e data obrigatórios; horário opcional). | T3.1, T1.4 | Evento criado e listado. |
| T3.3 | Listar Eventos | Tela Eventos com estados vazio/conteúdo. | T3.1, T1.4 | Lista de eventos com data e horário (quando houver). |

### TE-4 — Metas

| ID | Nome | Objetivo | Dependências | Resultado esperado |
|---|---|---|---|---|
| T4.1 | Estrutura de dados Meta | Definir modelo (título, progresso, data-alvo opcional, `ownerId`) + migration; progresso padrão 0; validar faixa 0–100. | T1.1 | Estrutura persistente de Meta conforme Task 2.3. |
| T4.2 | Criar Meta | Formulário na tela Metas (título obrigatório; data-alvo opcional; progresso inicia em 0). | T4.1, T1.4 | Meta criada como ativa e listada. |
| T4.3 | Listar Metas | Tela Metas com estados vazio/conteúdo; indicação **derivada** ativa/concluída. | T4.1, T1.4 | Lista de metas com progresso e data-alvo (quando houver). |
| T4.4 | Atualizar Progresso | Ação de atualizar progresso (0–100%) via htmx. | T4.3 | Progresso atualizado; meta sai de "ativa" ao atingir 100%. |

### TE-5 — Dashboard (Painel)

| ID | Nome | Objetivo | Dependências | Resultado esperado |
|---|---|---|---|---|
| T5.1 | Página do Dashboard + bloco Tarefas Atrasadas | Criar a página e o bloco (Pendente + possui prazo + `prazo < hoje`); ações diretas reusam T2.4. | T2.4 | Dashboard exibe atrasadas com estado vazio tranquilizador. |
| T5.2 | Bloco Tarefas Pendentes | Pendentes sem atraso (sem prazo ou `prazo ≥ hoje`). | T5.1, T2.4 | Bloco de pendentes no Dashboard, sem sobrepor atrasadas. |
| T5.3 | Bloco Eventos de Hoje | `data = hoje`. | T5.1, T3.3 | Bloco de eventos de hoje no Dashboard. |
| T5.4 | Bloco Próximos Eventos | `data` entre amanhã e hoje+7 (D1). | T5.3 | Bloco "próximos 7 dias", sem sobrepor "hoje". |
| T5.5 | Bloco Metas Ativas | Progresso `< 100%`. | T5.1, T4.4 | Bloco de metas ativas no Dashboard. |
| T5.6 | Ordenação final + anti-sobreposição | Aplicar a ordem recomendada (Task 2.4 §4) e verificar que nenhum item aparece em dois blocos. | T5.2, T5.4, T5.5 | Dashboard completo, ordenado e sem duplicidade entre blocos. |

### TE-6 — Gestão Plena (Should Have)

| ID | Nome | Objetivo | Dependências | Resultado esperado |
|---|---|---|---|---|
| T6.1 | Editar/Excluir Evento | Edição (reusa o formulário) e exclusão na tela Eventos. | T3.3 | Evento editável e removível. |
| T6.2 | Editar/Excluir Tarefa | Edição e exclusão na tela Tarefas. | T2.3 | Tarefa editável e removível. |
| T6.3 | Editar/Excluir Meta | Edição e exclusão na tela Metas. | T4.3 | Meta editável e removível. |

### TE-7 — Deploy & Operação

| ID | Nome | Objetivo | Dependências | Resultado esperado |
|---|---|---|---|---|
| T7.1 | Preparar para produção | Configuração de produção, servir estáticos, variáveis de ambiente (Task 2.5). | Conjunto funcional R1 | App pronta para rodar fora do ambiente de desenvolvimento. |
| T7.2 | Hospedar + deploy inicial | Provisionar instância com **volume persistente** (SQLite) e publicar. | T7.1 | Aplicação acessível em produção. |
| T7.3 | Backups + monitoramento mínimo | Cópia agendada do arquivo SQLite + uptime/logs (mitiga T1 da Task 2.5). | T7.2 | Dados protegidos por backup; disponibilidade observável. |

---

## 5. Release Mapping

Alinhado à Estratégia de Releases do PDD (Parte 7). Cada release gera software utilizável.

### R1 — Fundação Funcional
**Tasks:** T0.1, T0.2, T0.3, T1.1, T1.2, T1.3, T1.4, T2.1, T2.2, T2.3, T2.4, T5.1, T5.2, T7.1, T7.2, T7.3.
**Entrega utilizável:** o usuário loga, registra/lista/conclui tarefas e vê o Dashboard com
"Atrasadas" e "Pendentes" — **em produção, com backups**. Pendências saem da memória.

### R2 — Visão do Dia e da Semana
**Tasks:** T3.1, T3.2, T3.3, T5.3, T5.4.
**Entrega utilizável:** eventos registrados e listados; Dashboard passa a exibir "Eventos de Hoje"
e "Próximos Eventos" — **4 de 5 blocos**.

### R3 — Visão Completa da Vida
**Tasks:** T4.1, T4.2, T4.3, T4.4, T5.5, T5.6.
**Entrega utilizável:** metas com progresso; Dashboard completo (5 blocos) ordenado e sem
sobreposição — **MVP Must Have finalizado**.

### R4 — Gestão Plena
**Tasks:** T6.1, T6.2, T6.3.
**Entrega utilizável:** edição e exclusão para os três conceitos — **MVP encerrado**.

---

## 6. Vertical Slice Analysis

- **Menor conjunto de tasks que gera uma aplicação utilizável:** T0.1, T0.2, T1.1–T1.4, T2.1–T2.3.
  Com isso o usuário já **loga e registra/lista tarefas** — uma fatia vertical de ponta a ponta
  (autenticação → conceito → tela). Acrescentar T2.4 e T5.1/T5.2 completa o valor do R1.

- **Primeiro momento em que o usuário consegue usar o sistema:** ao final dessa fatia (login +
  tarefas). O primeiro **release** utilizável em produção é o **R1** (após T7.1–T7.3).

- **Existe dependência excessiva?** **Não.** A única dependência forte é a Autenticação, que
  antecede os conceitos — inevitável e barata (Django nativo). Os conceitos são independentes
  entre si; o Dashboard depende apenas dos conceitos que consome, bloco a bloco. A cadeia é um
  grafo acíclico, permitindo entrega incremental cedo.

---

## 7. Risk Analysis

| # | Risco | Causa | Impacto | Mitigação |
|---|---|---|---|---|
| B1 | **Autenticação como gargalo** | Tudo depende dela | Atraso no início bloqueia todo o resto | É pequena (Django nativo) e é a primeira após a fundação; mantê-la enxuta (sem JWT/OAuth — Task 2.5). |
| B2 | **Acoplamento Dashboard ↔ conceitos** | Blocos consomem os conceitos | Mudança em um conceito repercute no bloco | Blocos incrementais por release; Painel apenas **lê** (Task 2.1, mitiga A1/A2). |
| B3 | **Fundação insuficiente** | Pular layout/navegação/htmx | Retrabalho ao adicionar telas | TE-0 cobre scaffolding, layout, navegação e htmx antes dos conceitos. |
| B4 | **Tasks grandes demais** | Misturar modelo + operações + UI numa task | Difícil executar/validar individualmente | Estrutura de dados separada das operações; uma operação por task. |
| B5 | **`ownerId` inconsistente** | Criar registro sem setar o proprietário | Dado órfão; quebra a propriedade explícita (Task 2.3) | Toda task de criação seta `ownerId` do usuário autenticado (nota da §4). |
| B6 | **Perda de dados antes do backup** | Usar em produção sem T7.3 | Perda de registros reais | T7.3 (backups) faz parte do **R1**, não é adiado. |
| B7 | **Implementação prematura** | Antecipar API, recorrência, vínculos, multiusuário | Complexidade fora de escopo | Backlog cobre só o MVP; evoluções ficam para depois (Tasks 2.2/2.3/2.5). |

> Não há **dependências circulares**: o grafo da §2 é acíclico (fundação → auth → conceitos →
> dashboard; deploy após conjunto funcional).

---

## 8. Backlog Review

- **Existe task redundante?** **Não.** Cada task cobre uma capacidade distinta; ações diretas do
  Dashboard **reusam** as operações dos conceitos (ex.: T5.1 reusa T2.4), sem duplicar lógica.

- **Existe task faltando?** **Não**, frente ao MVP. Todas as 21 features do backlog do PDD (Parte
  7) estão cobertas (tabela abaixo), além de fundação, deploy e operação.

- **Existe task excessivamente grande?** **Não.** A maior granularidade (estrutura de dados) foi
  isolada das operações; cada operação (criar/listar/concluir/progresso/editar/excluir) é uma
  task pequena. Edição+exclusão por conceito podem ser divididas em duas se necessário.

- **O backlog está alinhado ao MVP?** **Sim.** Mapeia 1:1 os épicos/features do PDD e respeita
  arquitetura, domínio, dados, UX e setup aprovados.

**Cobertura de features (PDD Parte 7 → tasks):**

| Feature | Task | Feature | Task |
|---|---|---|---|
| F1.1 Login | T1.2 | F4.1 Criar Meta | T4.2 |
| F1.2 Logout | T1.3 | F4.2 Listar Metas | T4.3 |
| F2.1 Criar Evento | T3.2 | F4.3 Atualizar Progresso | T4.4 |
| F2.2 Listar Eventos | T3.3 | F4.4 Editar Meta | T6.3 |
| F2.3 Editar Evento | T6.1 | F4.5 Excluir Meta | T6.3 |
| F2.4 Excluir Evento | T6.1 | F5.1 Eventos de Hoje | T5.3 |
| F3.1 Criar Tarefa | T2.2 | F5.2 Próximos Eventos | T5.4 |
| F3.2 Listar Tarefas | T2.3 | F5.3 Tarefas Pendentes | T5.2 |
| F3.3 Concluir Tarefa | T2.4 | F5.4 Tarefas Atrasadas | T5.1 |
| F3.4 Editar Tarefa | T6.2 | F5.5 Metas Ativas | T5.5 |
| F3.5 Excluir Tarefa | T6.2 | | |

> **Nota de consistência (PDD):** o backlog do PDD lista **21 features** (E1:2, E2:4, E3:5, E4:5,
> E5:5; 15 Must + 6 Should). Os totais-resumo do PDD que antes citavam "16 features · 14 Must"
> foram **corrigidos na Task 2.7** para refletir essa realidade. Este backlog cobre **todas as 21**
> features listadas.

---

## Conclusão

1. **Quantos épicos técnicos existem?** **8** (TE-0 a TE-7).

2. **Quantas tasks técnicas existem?** **30.**
   (TE-0: 3 · TE-1: 4 · TE-2: 4 · TE-3: 3 · TE-4: 4 · TE-5: 6 · TE-6: 3 · TE-7: 3.)

3. **Ordem oficial de implementação:**
   T0.1 → T0.2 → T0.3 → T1.1 → T1.2 → T1.3 → T1.4 → T2.1 → T2.2 → T2.3 → T2.4 → T5.1 → T5.2 →
   T7.1 → T7.2 → T7.3 **(R1)** → T3.1 → T3.2 → T3.3 → T5.3 → T5.4 **(R2)** → T4.1 → T4.2 → T4.3 →
   T4.4 → T5.5 → T5.6 **(R3)** → T6.1 → T6.2 → T6.3 **(R4)**.

4. **Primeiro release utilizável:** **R1 — Fundação Funcional** (login + tarefas + Dashboard de
   tarefas, em produção com backups). A primeira fatia vertical utilizável surge ainda antes,
   com login + criar/listar tarefas (§6).

5. **O backlog está pronto para iniciar a Fase 3 (Implementação)?** **Sim.** As tasks são
   pequenas, ordenadas, sem ciclos, cobrem 100% do MVP e carregam contexto suficiente para
   execução individual sem redefinir arquitetura, domínio, dados ou UX.

### Recomendação

> **Encerrar a Fase 2.**
> A arquitetura está completa e consistente do produto ao backlog: alto nível (2.1), domínio
> (2.2), dados (2.3), UX (2.4), setup (2.5) e backlog (2.6). O backlog é implementável de forma
> incremental, alinhado aos releases do PDD, e pode iniciar a Fase 3 sem revisão prévia.

---

*Documento produzido na Task 2.6 — Backlog Técnico (Fase 2).*
