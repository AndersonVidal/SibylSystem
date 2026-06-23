# SibylSystem — Estrutura de UX e Wireframes Conceituais

> **Documento da Fase 2 (Arquitetura) — Task 2.4.**
> Fontes: PDD (definição oficial do produto), CLAUDE.md (fonte de verdade),
> `08-high-level-architecture.md`, `09-domain-model.md`, `10-data-model.md`.
> Em caso de conflito, o CLAUDE.md prevalece.
>
> **Propósito:** definir a estrutura de UX do MVP e produzir wireframes conceituais de todas as
> telas, focando em **organização da informação, navegação, hierarquia, ações e experiência**.
>
> **Restrições desta task:** não discute tecnologia, framework, backend ou banco; não cria design
> visual final, cores, tipografia, identidade visual ou componentes de biblioteca. Os wireframes
> são **conceituais** (estrutura, não estética).

---

## 1. UX Principles

Princípios de UX derivados diretamente dos princípios do produto (PDD, Parte 2) e da Filosofia
de Uso (PDD, Parte 6).

| Princípio de UX | Origem no PDD | O que significa na prática |
|---|---|---|
| **Consultar muito, alimentar pouco** | Filosofia de Uso: "alimentar pouco e fácil, consultar muito e com clareza". | A leitura (dashboard) é o caminho otimizado; o cadastro é o mais curto possível. |
| **Clareza antes de densidade** | Princípio 2 (Clareza); "o que não esclarece é ruído". | Cada tela mostra só o necessário; nada compete por atenção sem propósito. |
| **Baixa fricção no caminho quente** | Análise de frequência: F7, F4 e F3 são os mais frequentes. | Consultar dashboard, concluir e registrar tarefa exigem o mínimo de passos. |
| **Navegação rasa** | Parte 6: "tudo a um passo do dashboard". | Toda tela está a um clique do dashboard; sem hierarquias profundas. |
| **Anti-sobreposição** | Parte 5: "nenhum item aparece em dois blocos". | A informação não se repete entre blocos/telas; cada coisa tem um lugar. |
| **Redução de carga cognitiva** | Princípio 7. | O sistema "lembra pelo usuário"; a tela responde "o que importa agora" sem ele procurar. |

**Como o usuário deve se sentir:** no controle e aliviado — abre o sistema e vê imediatamente o
que precisa, sem caçar informação nem decidir por onde começar. A sensação-alvo é de **clareza
com baixo esforço** (Proposta de Valor, Parte 2).

**O que priorizar:** a consulta consolidada (dashboard); o caminho mais curto para concluir e
registrar tarefas; legibilidade imediata dos estados (atrasada, hoje, ativa).

**O que evitar:** formulários longos; telas que misturam conceitos; navegação profunda;
repetição de um mesmo item em vários lugares; qualquer elemento que aumente o esforço de
organização em vez de reduzi-lo (Filosofia de Uso).

---

## 2. Navigation Model

**Telas existentes (5):** Login, Dashboard, Eventos, Tarefas, Metas. (Criar/editar ocorrem
**dentro** da tela de cada conceito; não são telas autônomas — PDD, Parte 6.)

**Como chega / como retorna:**

- **Login** — ponto de entrada quando não há sessão ativa. Sai dele autenticando-se → Dashboard.
- **Dashboard** — tela inicial após login; centro da navegação. Alcançável de qualquer tela por
  um elemento de navegação persistente.
- **Eventos / Tarefas / Metas** — alcançáveis em **um passo** a partir da navegação persistente
  (presente em todas as telas internas). Retorno: para o Dashboard pelo mesmo elemento de
  navegação.
- **Logout** — ação persistente (não é tela); disponível em todas as telas internas; leva de
  volta ao Login.
- **Ações diretas no Dashboard** — sobre itens listados (ex.: concluir uma tarefa) sem sair da
  tela.

**Mapa de navegação textual:**

```
[Login]
   │ autentica
   ▼
[Dashboard] ◄──────────── (navegação persistente, presente em todas as telas internas)
   ├──► [Eventos]   ── criar / listar / editar / excluir ── volta ► [Dashboard]
   ├──► [Tarefas]   ── criar / listar / concluir / editar / excluir ── volta ► [Dashboard]
   ├──► [Metas]     ── criar / listar / atualizar progresso / editar / excluir ── volta ► [Dashboard]
   └──► (ações diretas sobre itens do próprio Dashboard, ex.: concluir tarefa)

[Logout] ◄── ação persistente em qualquer tela interna ──► retorna a [Login]
```

**Caminhos principais:**
- **Caminho de consulta (mais frequente):** Login → Dashboard → (lê os 5 blocos) → eventual ação
  direta. É o coração do uso diário.
- **Caminho de alimentação:** Dashboard → tela do conceito → criar item → volta ao Dashboard.
- **Caminho de manutenção:** Dashboard → tela do conceito → editar/excluir/concluir/atualizar.

> `ownerId` (Task 2.3) é **transparente** para a navegação e para o usuário: como o sistema é de
> usuário único, não há seleção de proprietário nem qualquer UI relacionada.

---

## 3. Screen Specifications

### Login

- **Objetivo:** autenticar o usuário único e abrir a sessão.
- **Informações exibidas:** identificação do sistema; campos de credencial; ação de autenticar.
- **Ações disponíveis:** autenticar (entrar).
- **Estado vazio:** é o estado natural — campos em branco aguardando preenchimento.
- **Estado com conteúdo:** credenciais preenchidas; após sucesso, redireciona ao Dashboard;
  em falha, mensagem clara sem expor detalhes técnicos.
- **Não deve exibir:** dados pessoais nem navegação do sistema (PDD, Parte 6).

### Dashboard

- **Objetivo:** apresentar, em uma visão, "o que importa agora" através dos 5 blocos.
- **Informações exibidas:** Eventos de Hoje, Próximos Eventos, Tarefas Pendentes, Tarefas
  Atrasadas, Metas Ativas — cada bloco com seus itens conforme regras da Parte 5.
- **Ações disponíveis:** navegar para as telas de conceito; ações diretas sobre itens (ex.:
  concluir tarefa); acessar Logout.
- **Estado vazio (global ou por bloco):** quando um bloco não tem itens, exibe uma mensagem de
  vazio tranquilizadora (ex.: "Nenhuma tarefa atrasada") — vazio é uma boa notícia, não um erro.
- **Estado com conteúdo:** blocos preenchidos na hierarquia definida na §4.
- **Não deve exibir:** formulários completos, listagens exaustivas ou histórico (PDD, Parte 6).

### Eventos

- **Objetivo:** ver e gerenciar eventos.
- **Informações exibidas:** lista de eventos com título, data e horário (quando houver).
- **Ações disponíveis:** criar, editar, excluir, listar.
- **Estado vazio:** convite a criar o primeiro evento.
- **Estado com conteúdo:** lista de eventos; cada item com ações de editar/excluir.
- **Não deve exibir:** tarefas, metas ou blocos do dashboard (separação por conceito).

### Tarefas

- **Objetivo:** ver, gerenciar e concluir tarefas.
- **Informações exibidas:** lista de tarefas com título, status (Pendente/Concluída), prazo
  (quando houver) e indicação visual de **atrasada** (derivada, não armazenada — Task 2.3).
- **Ações disponíveis:** criar, editar, excluir, concluir, listar.
- **Estado vazio:** convite a criar a primeira tarefa.
- **Estado com conteúdo:** lista de tarefas; ação de concluir destacada (caminho quente F4).
- **Não deve exibir:** eventos, metas ou blocos do dashboard.

### Metas

- **Objetivo:** ver, gerenciar metas e atualizar progresso.
- **Informações exibidas:** lista de metas com título, progresso (0–100%), data-alvo (quando
  houver) e indicação de estado **ativa/concluída** (derivado do progresso — Task 2.3).
- **Ações disponíveis:** criar, editar, excluir, atualizar progresso, listar.
- **Estado vazio:** convite a criar a primeira meta.
- **Estado com conteúdo:** lista de metas; controle de atualização de progresso por item.
- **Não deve exibir:** eventos, tarefas ou blocos do dashboard.

---

## 4. Dashboard Deep Analysis

O Dashboard é a principal experiência (PDD, Parte 6). Os 5 blocos não têm a mesma urgência nem a
mesma frequência de relevância, então a hierarquia deve refletir **"o que importa agora"**.

**Critérios de hierarquia:** urgência (risco de algo ser perdido) + imediatismo temporal (hoje
antes da semana, semana antes do longo prazo) + frequência de consulta.

**Ordenação recomendada (de cima para baixo):**

| Ordem | Bloco | Justificativa |
|---|---|---|
| 1 | **Tarefas Atrasadas** | Maior urgência: já passou do prazo; é o que mais corre risco e mais exige ação. Quando vazio, é uma boa notícia visível. |
| 2 | **Eventos de Hoje** | Ancora o dia: o que acontece hoje orienta a jornada imediata. |
| 3 | **Tarefas Pendentes** | O que falta fazer e ainda está no prazo — o trabalho "ativo" do dia. |
| 4 | **Próximos Eventos** | Antecipa a semana (janela de 7 dias); importante, porém não imediato. |
| 5 | **Metas Ativas** | Longo prazo; menor urgência e menor frequência (criação "Rara", progresso "Ocasional"). Fica como visão de fundo, sempre presente. |

**Qual bloco deve receber mais atenção (ênfase visual):** **Tarefas Atrasadas** — sinaliza risco
e demanda ação; deve se destacar quando houver itens (e sumir discretamente quando vazio).

**Qual bloco é mais importante (ao propósito diário):** o conjunto **"hoje + agora"** — Eventos
de Hoje e Tarefas (Atrasadas + Pendentes). É a resposta direta à pergunta central do produto
("o que preciso fazer, o que está pendente/atrasado"). Metas Ativas é o bloco menos urgente, mas
indispensável para conectar o cotidiano aos objetivos.

> **Natureza da decisão:** esta ordenação é uma **recomendação de UX reversível** (como a janela
> de 7 dias, D1). Não altera as regras dos blocos (Parte 5), apenas sua disposição visual.

---

## 5. Conceptual Wireframes

Estrutura conceitual em ASCII (sem estética). A barra de navegação persistente aparece em todas
as telas internas.

### Login

```
+--------------------------------------------------+
|                  SibylSystem                     |
+--------------------------------------------------+
|                                                  |
|              [ Identificação      ]              |
|              [ Credencial         ]              |
|                                                  |
|                  [  Entrar  ]                    |
|                                                  |
|        (mensagem de erro, se houver)             |
+--------------------------------------------------+
```

### Dashboard

```
+--------------------------------------------------+
| SibylSystem   Dashboard Eventos Tarefas Metas  [Logout] |
+--------------------------------------------------+
| TAREFAS ATRASADAS                                |
|  - <título>  prazo:<data>        [Concluir]      |
|  - <título>  prazo:<data>        [Concluir]      |
+--------------------------------------------------+
| EVENTOS DE HOJE                                  |
|  - <título>  <horário?>                          |
+--------------------------------------------------+
| TAREFAS PENDENTES                                |
|  - <título>  prazo:<data?>       [Concluir]      |
+--------------------------------------------------+
| PRÓXIMOS EVENTOS (próximos 7 dias)               |
|  - <título>  <data> <horário?>                   |
+--------------------------------------------------+
| METAS ATIVAS                                     |
|  - <título>  progresso:<0-100%>                  |
+--------------------------------------------------+
```

Estado vazio (por bloco):

```
+--------------------------------------------------+
| TAREFAS ATRASADAS                                |
|  (nenhuma tarefa atrasada)                       |
+--------------------------------------------------+
```

### Eventos

```
+--------------------------------------------------+
| SibylSystem   Dashboard Eventos Tarefas Metas  [Logout] |
+--------------------------------------------------+
| EVENTOS                          [ + Novo Evento ] |
+--------------------------------------------------+
|  - <título>   <data> <horário?>   [Editar][Excluir] |
|  - <título>   <data> <horário?>   [Editar][Excluir] |
+--------------------------------------------------+

Estado vazio:
+--------------------------------------------------+
| EVENTOS                          [ + Novo Evento ] |
|  Nenhum evento ainda. Crie o primeiro.           |
+--------------------------------------------------+

Criar/Editar (dentro da tela):
+--------------------------------------------------+
|  Título:  [______________________]              |
|  Data:    [__________]  Horário (opc): [_____]   |
|                 [ Salvar ]  [ Cancelar ]         |
+--------------------------------------------------+
```

### Tarefas

```
+--------------------------------------------------+
| SibylSystem   Dashboard Eventos Tarefas Metas  [Logout] |
+--------------------------------------------------+
| TAREFAS                          [ + Nova Tarefa ] |
+--------------------------------------------------+
|  - [ ] <título>  prazo:<data?>  (ATRASADA?)  [Concluir][Editar][Excluir] |
|  - [x] <título>  (concluída)                 [Editar][Excluir]           |
+--------------------------------------------------+

Estado vazio:
+--------------------------------------------------+
| TAREFAS                          [ + Nova Tarefa ] |
|  Nenhuma tarefa ainda. Crie a primeira.          |
+--------------------------------------------------+

Criar/Editar (dentro da tela):
+--------------------------------------------------+
|  Título:  [______________________]              |
|  Prazo (opcional): [__________]                 |
|                 [ Salvar ]  [ Cancelar ]         |
+--------------------------------------------------+
```

### Metas

```
+--------------------------------------------------+
| SibylSystem   Dashboard Eventos Tarefas Metas  [Logout] |
+--------------------------------------------------+
| METAS                             [ + Nova Meta ] |
+--------------------------------------------------+
|  - <título>   progresso:[#####-----] 50%  data-alvo:<data?>          |
|       [ Atualizar progresso ]  [Editar][Excluir]                     |
|  - <título>   progresso:[##########] 100% (concluída)               |
|       [Editar][Excluir]                                              |
+--------------------------------------------------+

Estado vazio:
+--------------------------------------------------+
| METAS                             [ + Nova Meta ] |
|  Nenhuma meta ainda. Crie a primeira.            |
+--------------------------------------------------+

Criar/Editar (dentro da tela):
+--------------------------------------------------+
|  Título:  [______________________]              |
|  Data-alvo (opcional): [__________]             |
|  Progresso: [ 0-100 % ]                          |
|                 [ Salvar ]  [ Cancelar ]         |
+--------------------------------------------------+
```

---

## 6. User Journey Validation

Contagem de passos a partir de uma sessão ativa (já no Dashboard). "Passo" = uma interação
significativa do usuário.

| Fluxo | Passos | Atrito? | Observação / melhoria estrutural |
|---|---|---|---|
| **Registrar Evento** | 4: Eventos → Novo Evento → preencher (título, data) → Salvar | Mínimo aceitável | Formulário curto; foco automático no título reduz fricção (melhoria de UX, não de escopo). |
| **Registrar Tarefa** (F3, quente) | 4: Tarefas → Nova Tarefa → preencher (título) → Salvar | Baixo | Só o título é obrigatório; prazo opcional. Caminho já enxuto. |
| **Concluir Tarefa** (F4, quente) | 1: ação direta "Concluir" no Dashboard | Nenhum | Disponível também na tela Tarefas. É o fluxo mais otimizado, como exige a alta frequência. |
| **Registrar Meta** (rara) | 4: Metas → Nova Meta → preencher (título) → Salvar | Baixo | Progresso assume 0% por padrão; data-alvo opcional. |
| **Atualizar Progresso** | 3: Metas → "Atualizar progresso" no item → confirmar | Baixo | Mora na tela Metas; poderia haver ação direta no Dashboard (melhoria reversível, fora do escopo atual). |
| **Consultar Dashboard** (F7, mais frequente) | 0 extra: é a tela inicial pós-login | Nenhum | O caminho de maior valor tem custo zero. |

**Conclusões:** os fluxos mais frequentes (F7, F4, F3) têm o menor custo, coerente com a análise
de fricção do PDD. Não há atrito desnecessário. As melhorias identificadas (foco automático no
título; eventual ação direta de progresso no Dashboard) são **opcionais e reversíveis**, não
alteram escopo e podem ser avaliadas após uso real.

---

## 7. Mobile vs Desktop Analysis

- **Desktop:** funciona bem. A navegação persistente em barra superior e os blocos/listas em
  coluna aproveitam o espaço; nenhum bloco depende de layout multicoluna obrigatório.
- **Mobile:** funciona conceitualmente. A estrutura é **linear e empilhável**: os 5 blocos do
  Dashboard e as listas das telas de conceito se organizam verticalmente; a navegação rasa
  (poucos destinos) cabe em um menu compacto.
- **Dependência de tela grande:** **não há.** Nenhuma tela exige largura para fazer sentido —
  não há tabelas densas, múltiplas colunas comparativas nem visualizações que dependam de área.
  A hierarquia do Dashboard (§4) preserva a ordem de importância tanto empilhada quanto em
  coluna.

> Conclusão: a estrutura é **agnóstica de tamanho de tela** por desenho (listas e blocos
> empilháveis), o que mantém aberta a evolução para mobile sem reestruturação — sem que isso
> signifique desenvolver mobile agora (fora do escopo).

---

## 8. UX Review

- **Existe tela sobrecarregada?** **Não.** Cada tela de conceito trata de um único conceito; o
  Dashboard resume sem expor formulários ou histórico (princípio anti-sobreposição, Parte 6).
- **Existe navegação excessiva?** **Não.** A navegação é rasa: tudo a um passo do Dashboard, com
  retorno sempre disponível.
- **Existe redundância?** **Não.** A regra anti-sobreposição garante que um item não apareça em
  dois blocos; o Dashboard agrega e as telas detalham, sem duplicar responsabilidades.
- **O Dashboard continua sendo o centro da experiência?** **Sim.** É a tela inicial, o destino de
  retorno, a de maior frequência (F7) e onde as ações quentes (concluir) acontecem diretamente.

---

## Conclusão

1. **A estrutura de UX está alinhada ao produto?** **Sim.** Reflete os princípios do PDD
   (consultar muito/alimentar pouco, clareza, baixa fricção, navegação rasa, anti-sobreposição) e
   respeita a estrutura de 5 telas e o papel central do Dashboard.

2. **O Dashboard continua sendo a principal experiência?** **Sim.** Tela inicial, centro da
   navegação, maior frequência de uso e lar das ações diretas do dia a dia.

3. **Existe mudança necessária antes da implementação?** **Não há mudança bloqueante.** As
   melhorias identificadas (ordenação dos blocos por urgência, foco automático no título, eventual
   ação direta de progresso no Dashboard) são **recomendações de UX reversíveis** que não alteram
   escopo, domínio nem dados.

4. **A UX está pronta para servir de base ao Setup Técnico (Task 2.5)?** **Sim.** Telas, navegação,
   informações, ações e estados (vazio/preenchido) estão definidos e consistentes com a
   arquitetura, o domínio e o modelo de dados aprovados.

### Recomendação

> **Prosseguir para a Task 2.5 (Setup Técnico).**
> A estrutura de UX é simples, centrada no Dashboard, sem telas sobrecarregadas, navegação
> excessiva ou redundância, e alinhada aos princípios do produto. As recomendações em aberto são
> reversíveis e não exigem revisão antes de continuar.

---

*Documento produzido na Task 2.4 — Estrutura de UX e Wireframes Conceituais (Fase 2).*
