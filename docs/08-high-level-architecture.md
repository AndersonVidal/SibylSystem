# SibylSystem — Arquitetura de Alto Nível

> **Documento da Fase 2 (Arquitetura) — Task 2.1.**
> Fontes: PDD (definição oficial do produto) e CLAUDE.md (fonte de verdade).
> Em caso de conflito, o CLAUDE.md prevalece.
>
> **Propósito:** definir a arquitetura **conceitual** de alto nível — quais módulos,
> responsabilidades e fronteiras são necessários para implementar o produto da Fase 1.
>
> **Restrições desta task:** não escolhe tecnologias, frameworks, banco de dados; não discute
> APIs, controllers, migrations, infraestrutura, deployment ou autenticação técnica; não cria
> detalhes de implementação. O foco é **modelar responsabilidades do sistema**, não construí-lo.

---

## 1. Architectural Goals

Objetivos que a arquitetura deve atender, derivados exclusivamente do PDD.

| # | Objetivo | Justificativa (origem no PDD) |
|---|---|---|
| G1 | **Simplicidade estrutural** | Princípio 1 ("Simplicidade acima de sofisticação") e a definição do MVP como "menor versão capaz". A estrutura deve ter o mínimo de partes necessárias para entregar os três conceitos + dashboard. |
| G2 | **Clareza de responsabilidades** | Princípio 2 ("Clareza") e o princípio anti-sobreposição da Parte 6 ("dashboard agrega e resume; telas de conceito detalham e gerenciam um único conceito cada"). Cada parte do sistema deve ter um papel óbvio. |
| G3 | **Baixo custo de manutenção** | Princípio 4 ("Baixa manutenção") e o público-alvo de usuário único, que "não comporta sobrecarga operacional". Menos partes e fronteiras nítidas reduzem o esforço de manter. |
| G4 | **Evolução incremental** | Princípio 5 ("Evolução incremental") e a estratégia de 4 releases (R1→R4). A arquitetura deve permitir adicionar capacidades por etapas sem reescrever o existente. |
| G5 | **Centralização / consolidação** | Princípio 6 ("Centralização das informações") e o Papel do Dashboard (Parte 6): o produto existe para substituir ferramentas dispersas por um ponto central. A arquitetura precisa de um lugar que consolide. |
| G6 | **Separação por conceito de negócio** | Parte 4 (Domain Definition) define Evento, Tarefa e Meta com **limites conceituais explícitos e mutuamente exclusivos**. A arquitetura deve preservar essas fronteiras, não fundi-las. |
| G7 | **Adequação a usuário único** | Parte 2 (Público-Alvo) e a lista de "Fora do Escopo" (multiusuário, compartilhamento). A arquitetura não deve carregar complexidade de colaboração/multiusuário. |
| G8 | **Redução de carga cognitiva (também para quem mantém)** | Princípio 7. Uma arquitetura legível e previsível reduz o esforço mental tanto de uso quanto de manutenção. |

---

## 2. System Responsibilities

Responsabilidades que o sistema precisa cumprir, agrupadas por afinidade. Derivadas das
Capacidades do MVP (Parte 3) e dos Épicos (Parte 7).

| Grupo | Responsabilidades |
|---|---|
| **R-Acesso** | Autenticar o usuário único (login); encerrar a sessão (logout); proteger o espaço pessoal contra acesso não autorizado. |
| **R-Eventos** | Registrar, listar, editar e excluir ocorrências datadas; classificar um evento no tempo (passado / hoje / futuro / próximos 7 dias). |
| **R-Tarefas** | Registrar, listar, editar e excluir ações; concluir uma tarefa; determinar o estado de uma tarefa (Pendente / Concluída / Atrasada) a partir de prazo e status. |
| **R-Metas** | Registrar, listar, editar e excluir objetivos; atualizar o progresso (0–100%); determinar se uma meta está Ativa (<100%) ou Concluída (=100%). |
| **R-Consolidação** | Reunir, a partir dos três conceitos, os 5 blocos do dashboard; aplicar as regras de inclusão/exclusão de cada bloco; garantir o princípio anti-sobreposição (nenhum item em dois blocos). |

> Observação: cada grupo de responsabilidade mapeia diretamente para um épico do PDD
> (E1→R-Acesso, E2→R-Eventos, E3→R-Tarefas, E4→R-Metas, E5→R-Consolidação). Não há
> responsabilidade no PDD que fique sem grupo, nem grupo sem origem no PDD.

---

## 3. High-Level Modules

Cinco módulos, cada um representando uma **área de negócio / capacidade**, não tecnologia.

### Módulo de Acesso

- **Responsabilidade:** garantir que o espaço pessoal só seja usado pelo proprietário; abrir e
  encerrar a sessão de uso.
- **Pertence ao módulo:** o conceito de "sessão ativa"; login; logout; a noção de que existe
  um único usuário.
- **NÃO pertence ao módulo:** qualquer dado de Evento, Tarefa ou Meta; qualquer regra de
  negócio dos conceitos; a composição do dashboard. (Como a autenticação é feita tecnicamente
  está fora do escopo desta task.)

### Módulo de Eventos

- **Responsabilidade:** manter as ocorrências datadas da vida do usuário e seu posicionamento
  no tempo.
- **Pertence ao módulo:** o conceito Evento (data, horário opcional); as operações criar /
  listar / editar / excluir; a classificação temporal (hoje / futuro / passado / dentro da
  janela de próximos eventos).
- **NÃO pertence ao módulo:** conclusão (isso é Tarefa); progresso (isso é Meta); a montagem
  visual do dashboard; conhecer Tarefas ou Metas.

### Módulo de Tarefas

- **Responsabilidade:** manter as ações que o usuário precisa executar e seu ciclo de
  conclusão.
- **Pertence ao módulo:** o conceito Tarefa (prazo opcional, status); as operações criar /
  listar / editar / excluir / concluir; a regra de estado **Pendente / Concluída / Atrasada**
  (atrasada = pendente, com prazo, prazo < hoje).
- **NÃO pertence ao módulo:** datas de ocorrência (isso é Evento); progresso percentual (isso
  é Meta); a montagem do dashboard; conhecer Eventos ou Metas.

### Módulo de Metas

- **Responsabilidade:** manter os objetivos do usuário e a evolução em direção a eles.
- **Pertence ao módulo:** o conceito Meta (progresso 0–100%, data-alvo opcional, horizonte
  qualitativo); as operações criar / listar / editar / excluir / atualizar progresso; a regra
  de estado **Ativa (<100%) / Concluída (=100%)**.
- **NÃO pertence ao módulo:** ações com conclusão binária (isso é Tarefa); ocorrências datadas
  (isso é Evento); a montagem do dashboard; conhecer Tarefas ou Eventos.

### Módulo de Painel (Dashboard)

- **Responsabilidade:** consolidar, em uma única visão, "o que importa agora", reunindo os 5
  blocos a partir dos três conceitos.
- **Pertence ao módulo:** a definição dos 5 blocos (Eventos de Hoje, Próximos Eventos, Tarefas
  Pendentes, Tarefas Atrasadas, Metas Ativas); as regras de **inclusão/exclusão e composição**
  de cada bloco; o princípio anti-sobreposição (um item nunca em dois blocos).
- **NÃO pertence ao módulo:** criar, editar ou excluir conceitos; **possuir** as regras de
  negócio dos conceitos (a definição do que é "atrasada" ou "ativa" mora nos módulos de
  conceito; o Painel apenas as consulta e as compõe em blocos).

---

## 4. Module Relationships

Relações **conceituais** (não diagramas técnicos).

- **Dependências:**
  - O **Módulo de Acesso** é um **pré-requisito transversal**: todo uso do sistema pressupõe
    uma sessão ativa. Os demais módulos dependem da existência de acesso, mas o Acesso não
    depende de nenhum deles (não conhece Evento, Tarefa nem Meta).
  - O **Módulo de Painel depende dos três módulos de conceito** (Eventos, Tarefas, Metas):
    ele **consome/consulta** o que eles mantêm para compor os blocos. A dependência é em um
    único sentido.

- **Independências:**
  - **Eventos, Tarefas e Metas são independentes entre si.** Nenhum conhece ou depende do
    outro — coerente com a Parte 4 do PDD ("Tarefa ↔ Evento: independentes"; "Meta → Tarefas e
    Eventos: relação apenas conceitual, sem vínculo implementado no MVP").
  - Os módulos de conceito **não dependem do Painel** — existem e funcionam sem ele.

- **Módulo central:**
  - Para a **entrega de valor / experiência**, o **Painel é o centro**: o PDD afirma que o
    dashboard é "a experiência principal do produto" e o "motor de valor".
  - Para a **fundação / produção de dados**, os **três módulos de conceito** são a base que
    alimenta o Painel. O Acesso é o **portão** que protege tudo.
  - Síntese do sentido das relações: **Acesso protege → Conceitos produzem → Painel
    consolida.**

---

## 5. Dependency Analysis

- **Existe módulo acoplado demais?**
  O candidato natural é o **Painel**, que depende dos três conceitos. O acoplamento, porém, é
  **inerente ao seu propósito** (consolidar) e **unidirecional** (só o Painel conhece os
  conceitos; eles não o conhecem). Mitigação conceitual: manter o Painel como **consumidor de
  leitura** — ele compõe blocos, mas **não** detém as regras de negócio dos conceitos. Assim o
  acoplamento fica limitado a "ler e apresentar", não a "decidir regras".

- **Existe módulo desnecessário?**
  Não. Cada um dos cinco mapeia para um épico do PDD e para uma capacidade do MVP. Remover
  qualquer um deixa uma capacidade obrigatória sem dono.

- **Existe módulo com responsabilidade excessiva?**
  O risco está no Painel concentrar regras demais. Para evitá-lo, a fronteira é explícita: as
  regras de **estado de cada conceito** (atrasada, ativa, classificação temporal) pertencem ao
  módulo do conceito; o Painel detém apenas as regras de **seleção e composição de blocos**.

- **Simplificações avaliadas:**
  - *Fundir Eventos + Tarefas + Metas em um único "módulo de itens"?* **Rejeitado.** O PDD os
    define com limites conceituais mutuamente exclusivos e regras de estado distintas; fundi-los
    violaria o objetivo G6 e reintroduziria a confusão que o Guia de Classificação combate.
  - *Eliminar o Painel e deixar cada tela com seu resumo?* **Rejeitado.** Isso recriaria
    "listas dispersas", exatamente o problema que a visão combate (Parte 6, Papel do Dashboard).
  - **Conclusão:** o conjunto de cinco módulos já está no menor tamanho coerente com o produto.

---

## 6. Evolution Analysis

Análise à luz da filosofia de evolução incremental (sem criar funcionalidades novas).

- **Módulos estáveis (baixa probabilidade de mudança):**
  - **Acesso** — usuário único é uma decisão de produto estável; multiusuário está
    explicitamente fora de escopo.
  - **Núcleo conceitual de Eventos, Tarefas e Metas** — os três conceitos têm definição e
    limites maduros e fechados na Fase 1.

- **Módulos com maior probabilidade de evoluir:**
  - **Painel** — concentra decisões marcadas como **reversíveis**: D1 (janela de "Próximos
    Eventos" = 7 dias) e, indiretamente, D2 (forma do progresso de Meta). Mudanças de
    apresentação tendem a recair aqui.
  - **Eventos** — a recorrência é citada como funcionalidade futura (Parte 4); quando vier,
    afeta principalmente este módulo.
  - **Metas** — um eventual vínculo explícito Meta→Tarefa/Evento (hoje só conceitual) seria
    uma evolução que tocaria este módulo e suas relações.

- **Onde funcionalidades futuras provavelmente se encaixariam:**
  - **Notas / Informações** (lacuna identificada na Task 1.3 e deixada fora do MVP) encaixaria
    naturalmente como um **novo módulo de conceito irmão** de Eventos/Tarefas/Metas, seguindo o
    mesmo padrão. Se precisasse aparecer no dashboard, entraria como **um novo bloco consumido
    pelo Painel** — sem alterar os módulos existentes. Isso valida que o padrão "conceito como
    módulo + Painel consome" suporta crescimento incremental (G4).

---

## 7. Architectural Risks

| # | Risco | Causa | Impacto | Mitigação conceitual |
|---|---|---|---|---|
| A1 | **Centralização excessiva no Painel** | O Painel toca os três conceitos; tende a virar um "módulo que sabe tudo". | Mudanças em qualquer conceito podem repercutir no Painel; perda de clareza. | Restringir o Painel a **consumir e compor**; manter as regras de negócio nos módulos de conceito. Dependência sempre unidirecional. |
| A2 | **Responsabilidade de regras temporais sem dono claro** | "Atrasada", "ativa", "evento de hoje" envolvem comparação com a data corrente e poderiam ser reivindicadas tanto pelo conceito quanto pelo Painel. | Regra duplicada ou divergente entre tela de conceito e dashboard. | Definir como **dono o módulo do conceito** (ele decide o estado do item); o Painel apenas seleciona itens já classificados para cada bloco. |
| A3 | **Acoplamento crescente Painel ↔ conceitos** | Cada novo conceito ou bloco exige tocar o Painel. | Custo de evolução concentrado num ponto. | Padrão estável "conceito produz / Painel consome"; novos conceitos entram como módulos irmãos e, opcionalmente, como novo bloco — sem reescrever os demais. |
| A4 | **Erosão das fronteiras entre conceitos** | Semelhança superficial entre Evento/Tarefa/Meta pode tentar fusões ou campos compartilhados. | Volta da confusão conceitual; violação de G6. | Reafirmar os limites da Parte 4 do PDD como fronteira de módulo; cada conceito permanece com seu próprio módulo e regras. |
| A5 | **Complexidade prematura por crescimento futuro** | Antecipar recorrência, vínculos Meta→Tarefa, Notas, etc. | Arquitetura inflada antes da validação do MVP. | Manter o escopo nos cinco módulos atuais; tratar evoluções apenas quando validadas (Princípio 5; Filosofia de Desenvolvimento do CLAUDE.md). |

---

## 8. Architecture Review

- **Está alinhada aos princípios do produto?** **Sim.** Cinco módulos, fronteiras unidirecionais
  e padrão único de relacionamento atendem a Simplicidade (G1), Clareza (G2), Baixa manutenção
  (G3) e Evolução incremental (G4). A existência de um módulo dedicado à consolidação honra a
  Centralização (G5) e o papel do dashboard.

- **Existe módulo redundante?** **Não.** Cada módulo corresponde a um épico e a uma capacidade
  obrigatória do MVP; nenhum se sobrepõe a outro (princípio anti-sobreposição respeitado).

- **Existe responsabilidade sem dono?** **Não**, após as decisões de fronteira deste documento:
  - Estado de cada item (atrasada/ativa/classificação temporal) → módulo do conceito (mitiga A2).
  - Seleção/composição de blocos e anti-sobreposição → Painel.
  - Sessão e proteção de acesso → Acesso.

- **É simples o suficiente para um sistema de usuário único?** **Sim.** A topologia é rasa
  (espelha a navegação "tudo a um passo do dashboard"), sem camadas de colaboração,
  compartilhamento ou multiusuário — coerentes com o público-alvo e a lista de fora do escopo.

---

## Conclusão

1. **Módulos oficiais da arquitetura de alto nível:**
   - Módulo de **Acesso**
   - Módulo de **Eventos**
   - Módulo de **Tarefas**
   - Módulo de **Metas**
   - Módulo de **Painel (Dashboard)**

2. **Módulo mais importante:** o **Painel (Dashboard)**. O PDD o define como "a experiência
   principal do produto" e o "motor de valor" — é onde a clareza (o propósito do produto) é
   colhida. Ressalva: ele é o centro de **valor**, mas depende dos três módulos de conceito, que
   são a **fundação** que o alimenta, e do Acesso, que é o **portão** de tudo.

3. **Fluxo conceitual principal do produto:**
   **Acessar** (sessão protegida) → **alimentar** (registrar Eventos, Tarefas e Metas nos seus
   módulos, com baixa fricção) → **consolidar** (o Painel reúne tudo nos 5 blocos) → **consultar
   e decidir** (a visão única responde "o que importa agora") → **agir** (concluir tarefa,
   atualizar progresso), o que se reflete de volta no Painel. O caminho quente do dia a dia é
   *consultar o Painel* (Fluxo F7), com alimentação leve e contínua.

4. **A arquitetura está pronta para servir de base ao Modelo de Domínio (Task 2.2)?** **Sim.**
   Os limites de cada conceito estão mapeados a módulos com responsabilidades claras e donos
   definidos para cada regra; isso fornece a moldura dentro da qual o Modelo de Domínio detalhará
   atributos e relações.

### Recomendação

> **Prosseguir para a Task 2.2 (Modelo de Domínio).**
> A arquitetura de alto nível está alinhada aos princípios do produto, é simples o suficiente
> para um sistema de usuário único e não possui responsabilidades sem dono. As evoluções
> previstas (D1, D2, recorrência, Notas) têm lugar claro no padrão proposto e não exigem revisão
> da arquitetura antes de continuar.

---

*Documento produzido na Task 2.1 — Arquitetura de Alto Nível (Fase 2).*
