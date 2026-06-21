# Estrutura de Telas — SibylSystem

> Artefato da **Task 1.5 (Fase 1 — Definição do Produto)**.
> Fontes: [`CLAUDE.md`](../CLAUDE.md) (fonte de verdade), [`01-product-vision.md`](./01-product-vision.md), [`02-mvp-scope.md`](./02-mvp-scope.md), [`03-core-concepts.md`](./03-core-concepts.md), [`04-user-flows.md`](./04-user-flows.md).
> Em caso de conflito, o CLAUDE.md prevalece.
> Escopo desta task: quais telas existem, seu propósito, relação e navegação.
> **Não** trata de arquitetura, tecnologia, banco, implementação, wireframes, mockups, cores,
> tipografia ou componentes visuais. **Não** altera escopo nem cria funcionalidades.
> Usa exclusivamente conceitos e fluxos já aprovados.

---

## 1. Screen Inventory

| Tela | Objetivo | Fluxos suportados | Frequência | Classificação |
|---|---|---|---|---|
| **Login** | Autenticar o usuário único e dar acesso ao espaço pessoal | F1 (Login), Logout | Ocasional | **Administração** |
| **Dashboard** | Visão consolidada do que importa agora (5 blocos) | F7 (Consultar); ponto de partida para F4 e para abrir as listas | Muito frequente | **Essencial** |
| **Eventos** (lista) | Ver e gerenciar eventos | F2 (Registrar), editar/excluir, listar | Frequente/Ocasional | **Essencial** |
| **Tarefas** (lista) | Ver e gerenciar tarefas | F3 (Registrar), F4 (Concluir), editar/excluir, listar | Frequente | **Essencial** |
| **Metas** (lista) | Ver e gerenciar metas | F5 (Registrar), F6 (Atualizar progresso), editar/excluir, listar | Ocasional | **Essencial** |

**Observações sobre granularidade de telas:**

- As ações de **criar/editar** de cada conceito (preencher os dados) podem ocorrer em uma área
  de formulário **dentro** da respectiva tela de conceito. Tratamos isso como responsabilidade
  da tela do conceito, não como tela autônoma — coerente com o princípio de "poucas telas bem
  definidas" (ver §5). Não é decisão visual, e sim de organização de responsabilidades.
- Não há tela de "configurações" no MVP: usuário único, sem funcionalidades que exijam
  configuração (notificações, integrações etc. estão fora do escopo). Logout é uma ação,
  acessível de forma persistente, não uma tela.

**Estrutura mínima resultante:** **5 telas** — Login, Dashboard, Eventos, Tarefas, Metas.

---

## 2. Navigation Structure

- **Tela inicial após login:** **Dashboard**. É o ponto de entrada natural (Task 1.4: o
  dashboard é o motor de valor e a porta de entrada do dia).
- **Telas acessadas diretamente** (navegação principal, sempre disponível): Dashboard, Eventos,
  Tarefas, Metas. Navegação **rasa** — todas a um passo de distância.
- **Telas/ações acessadas a partir de outras telas:**
  - Do **Dashboard**, o usuário pode ir a um item (ex.: concluir uma tarefa pendente — F4) ou
    abrir a lista correspondente para ver mais.
  - Criar/editar de um conceito é acessado **de dentro** da tela daquele conceito.
  - **Login** antecede tudo; **Logout** retorna ao Login.
- **Telas centrais para a experiência:** **Dashboard** (consulta/visão) e, secundariamente, as
  três telas de conceito (alimentação/manutenção).

**Mapa conceitual de navegação (não é wireframe):**

```
Login
  └─► Dashboard (inicial)
        ├─► Eventos  (criar/editar/excluir/listar)
        ├─► Tarefas  (criar/editar/excluir/concluir/listar)
        ├─► Metas    (criar/editar/excluir/atualizar progresso/listar)
        └─► (ações diretas sobre itens exibidos, ex.: concluir tarefa)
Logout ◄── (acessível de forma persistente) ──► volta ao Login
```

---

## 3. Screen Responsibilities

### Login

- **Espera encontrar:** um meio de entrar no sistema.
- **Deve aparecer:** entrada de credenciais e ação de autenticar.
- **NÃO deve aparecer:** nenhum dado pessoal, conceito ou navegação do sistema (antes de
  autenticar).

### Dashboard

- **Espera encontrar:** um resumo do que importa agora.
- **Deve aparecer:** os cinco blocos definidos — eventos de hoje, próximos eventos, tarefas
  pendentes, tarefas atrasadas, metas ativas — e acesso rápido às telas de conceito.
- **NÃO deve aparecer:** formulários completos de cadastro, listagens exaustivas de tudo,
  histórico/relatórios, ou qualquer informação fora dos cinco blocos. O dashboard **resume**,
  não substitui as telas de conceito.

### Eventos

- **Espera encontrar:** seus eventos e como gerenciá-los.
- **Deve aparecer:** lista de eventos e as ações criar/editar/excluir.
- **NÃO deve aparecer:** tarefas, metas, ou os blocos do dashboard. Mantém-se restrita ao
  conceito Evento.

### Tarefas

- **Espera encontrar:** suas tarefas e como gerenciá-las/concluí-las.
- **Deve aparecer:** lista de tarefas e as ações criar/editar/excluir/concluir.
- **NÃO deve aparecer:** eventos, metas, ou o resumo do dashboard. Restrita ao conceito Tarefa.

### Metas

- **Espera encontrar:** suas metas e seu progresso.
- **Deve aparecer:** lista de metas e as ações criar/editar/excluir/atualizar progresso.
- **NÃO deve aparecer:** eventos, tarefas, ou o resumo do dashboard. Restrita ao conceito Meta.

> Princípio anti-sobreposição: o **Dashboard agrega e resume**; as **telas de conceito detalham
> e gerenciam** um único conceito cada. Nenhuma tela de conceito tenta ser um mini-dashboard, e
> o dashboard não tenta ser uma tela de gestão completa.

---

## 4. Dashboard Analysis

- **Papel dentro do produto:** é a materialização do valor central da visão — "clareza com
  baixo esforço" numa única visão. Responde "o que fazer / o que está pendente ou atrasado /
  quais metas estão ativas".
- **Tela comum ou experiência principal?** **A experiência principal.** A Task 1.4 classificou
  "Consultar Dashboard" como **muito frequente** e como o motor de valor; é a tela inicial e o
  ponto de retorno do usuário.
- **Quanto do valor depende dele?** A **maior parte do valor de consulta**. As telas de conceito
  sustentam a alimentação, mas o ganho percebido (clareza, priorização, redução de carga mental)
  concentra-se no dashboard. Sem ele, o produto vira um conjunto de listas dispersas — justamente
  o problema que a visão combate.
- **Mais tempo no dashboard ou nas telas de cadastro?** **No dashboard** (consulta), por design.
  A filosofia da Task 1.4 — *alimentar pouco e fácil, consultar muito e com clareza* — implica
  que as telas de cadastro existam para serem rápidas e pouco demoradas, enquanto o dashboard é
  onde o usuário permanece obtendo valor.

---

## 5. Navigation Philosophy

- **Navegação rasa, não profunda.** *Justificativa:* a visão prioriza rapidez de uso e baixa
  carga cognitiva; tudo que importa está a um passo do dashboard. Navegação profunda aumentaria
  fricção e esforço de organização — o oposto do propósito.
- **Poucas telas bem definidas, não muitas telas pequenas.** *Justificativa:* princípios de
  simplicidade e clareza; cinco telas com responsabilidades nítidas (§3) evitam dispersão e
  sobreposição. Cada conceito tem uma casa; o dashboard agrega.
- **Resolver rápido, navegar pouco.** *Justificativa:* os fluxos mais frequentes (consultar,
  concluir, registrar tarefa — Task 1.4) devem ser concluídos com poucos passos. O usuário não
  deve precisar "passear" pelo sistema para obter valor; o dashboard entrega a maior parte de
  imediato.
- **Centralidade do dashboard.** *Justificativa:* alinha estrutura de telas ao motor de valor
  identificado nas Tasks 1.1 e 1.4.

---

## 6. Frequency-Based Design Analysis

| Categoria | Telas | Implicação estrutural |
|---|---|---|
| **Exigem mínimo atrito** | **Dashboard** (muito frequente) e **Tarefas** (frequente — registrar/concluir) | Devem ser diretas, com as ações mais usadas (consultar, concluir, registrar tarefa) ao alcance imediato. São o caminho quente do dia a dia. |
| **Toleram mais etapas** | **Metas** (ocasional — registrar/atualizar progresso) e **Eventos** (frequente/ocasional) | Podem comportar um pouco mais de passos no cadastro/atualização sem prejudicar a experiência, por serem menos repetidas. |
| **Raramente utilizadas** | **Login** (ocasional) | Pode ser a mais simples possível; não precisa otimizar para repetição, e sim para clareza de acesso. |

**Impactos sobre a estrutura:** concentrar a redução de fricção onde a frequência é maior
(Dashboard e Tarefas) e aceitar fluxos um pouco mais longos onde a frequência é baixa (Metas,
Eventos, Login). Isso direciona o esforço de simplicidade ao que o usuário mais repete — sem
qualquer decisão visual.

---

## 7. Risks and Ambiguities

| Risco | Impacto | Mitigação conceitual |
|---|---|---|
| **Dashboard sobrecarregado** | Perda da clareza que é o propósito; ruído | Restringir aos cinco blocos definidos; nada de histórico/relatórios/listas exaustivas (§3). |
| **Telas redundantes** | Confusão sobre onde fazer cada coisa; manutenção maior | Manter um conceito por tela e o dashboard como único agregador; criar/editar dentro da tela do conceito, não em telas avulsas. |
| **Responsabilidades confusas** (tela de conceito virando mini-dashboard ou vice-versa) | Sobreposição; o usuário não sabe onde encontrar o quê | Fronteiras de responsabilidade da §3; dashboard resume, conceito gerencia. |
| **Excesso de navegação** | Fricção; contraria rapidez de uso | Navegação rasa (§5); tudo a um passo do dashboard. |
| **Proliferação de telas futuras** | Erosão da simplicidade ao longo do tempo | Toda nova tela deve justificar-se por um problema da Task 1.1 e respeitar "poucas telas bem definidas". |

> Pontos em aberto que dependem das **Regras Funcionais** (próxima etapa): como exatamente cada
> bloco do dashboard filtra seus itens (ex.: o que conta como "próximo"/"atrasado"). Isso afeta
> o *conteúdo* das telas, não a *estrutura* aqui definida — não bloqueia.

---

## Conclusão

1. **Qual é a estrutura mínima de telas do MVP?**
   **Cinco telas:** Login, Dashboard, Eventos, Tarefas, Metas. Criar/editar ocorrem dentro da
   tela de cada conceito; Logout é ação persistente, não tela.

2. **Existe alguma tela desnecessária?**
   Não. Cada tela suporta fluxos aprovados e tem responsabilidade única. Não há tela de
   configurações (sem necessidade no MVP).

3. **Existe alguma tela essencial ausente?**
   Não. As cinco telas cobrem autenticação, os três conceitos e a visão consolidada. Nenhuma
   funcionalidade aprovada fica sem lar.

4. **O Dashboard deve ser considerado a experiência principal do produto?**
   **Sim.** É a tela inicial, a mais frequente e onde se concentra o valor de consulta —
   coerente com as Tasks 1.1 e 1.4.

**Recomendação: Prosseguir para a Task 1.6.** A estrutura de telas é mínima, sem redundância e
sem lacunas; os pontos em aberto são de regras funcionais (conteúdo dos blocos), a tratar
adiante.

---

## Observações Futuras

- **OF (1.5-a).** Se "informações relevantes"/notas (OF da Task 1.3) entrarem em fase futura,
  exigirão repensar a estrutura de telas — fora do MVP.
- **OF (1.5-b).** Eventual tela de configurações só se justificará quando surgirem itens
  configuráveis (ex.: notificações/integrações) — todos fora do escopo atual.
- **OF (1.5-c).** Visões de histórico/evolução de metas poderiam tornar-se uma tela própria no
  futuro, sem sobrecarregar o dashboard.
