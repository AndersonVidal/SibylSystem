# SibylSystem — Modelo de Dados

> **Documento da Fase 2 (Arquitetura) — Task 2.3.**
> Fontes: `09-domain-model.md` (definição oficial das entidades e regras de negócio),
> `08-high-level-architecture.md`, PDD e CLAUDE.md (fonte de verdade).
> Em caso de conflito, o CLAUDE.md prevalece.
>
> **Propósito:** transformar o Modelo de Domínio em um **modelo de dados persistente** —
> estruturas persistidas, relacionamentos de dados, restrições de integridade, dados derivados
> e estratégia de armazenamento.
>
> **Restrições desta task:** não escolhe tecnologias nem banco de dados; não cria migrations,
> SQL, ORM ou detalhes de framework; não define tipos técnicos; não altera o domínio aprovado;
> não cria funcionalidades. Modela apenas **o que precisa ser guardado e como se relaciona**, em
> nível conceitual.

---

## 1. Data Model Overview

- **Como o domínio será representado em dados:** cada **entidade de domínio** com dados próprios
  vira uma **estrutura persistente independente** — uma para **Usuário**, uma para **Evento**,
  uma para **Tarefa** e uma para **Meta**. Não há estruturas intermediárias nem de ligação,
  porque o domínio não possui relacionamentos explícitos entre conceitos (Task 2.2, §6).

- **O que será persistido:**
  - **Usuário** — o proprietário único e sua credencial de acesso.
  - **Evento, Tarefa, Meta** — os três conceitos do núcleo, com os **atributos de negócio**
    definidos na Task 2.2 **mais a referência explícita de propriedade (`ownerId`)** ao Usuário
    dono do registro (ver nota abaixo e §4).

> **Nota sobre `ownerId` — decisão de modelo de dados, não de escopo de produto.** Cada registro
> de Evento, Tarefa e Meta persiste explicitamente quem é seu proprietário, por meio de um campo
> `ownerId` que referencia o Usuário. Isso **não altera** o produto: a experiência continua sendo
> de **usuário único**, sem multiusuário, compartilhamento ou qualquer funcionalidade nova.
> `ownerId` é uma escolha de **como os dados são guardados** — torna a propriedade **explícita**
> em vez de implícita, garantindo isolamento de dados desde já e permitindo evolução futura sem
> migração estrutural complexa. É um campo do **modelo de dados**, não um atributo do Modelo de
> Domínio (Task 2.2) — por isso aparece aqui e não lá.

- **O que NÃO será persistido:**
  - **Painel / Dashboard** — não é entidade; é composição derivada em tempo de consulta (Task
    2.2). Não há nada próprio a guardar.
  - **Sessão** — preocupação técnica de autenticação, fora do domínio.
  - **Qualquer dado derivável** — classificações temporais de eventos, condição "atrasada" de
    tarefas, estado "ativa/concluída" de metas e os blocos do dashboard (detalhado em §5).

- **Estratégia de armazenamento (conceitual):** **quatro coleções de registros**, uma por
  entidade, **sem referências cruzadas entre os três conceitos** (Evento, Tarefa e Meta não se
  referenciam entre si). Cada registro de Evento, Tarefa e Meta carrega uma **referência
  explícita de propriedade (`ownerId`)** ao Usuário — a única referência persistida do modelo.
  Cada registro é autossuficiente quanto a fatos de negócio: contém só os fatos que precisam
  sobreviver entre usos; tudo o que pode ser recalculado é deixado de fora.

> **Justificativa central:** o princípio de simplicidade e a ausência de vínculos no domínio
> levam ao modelo de dados mais enxuto possível — guardar só os fatos, derivar todo o resto.

---

## 2. Data Structures

Campos descritos por **significado de negócio**, sem tipos técnicos. Toda origem remete à Task
2.2 (Modelo de Domínio).

### Usuário

| Campo | Obrigatoriedade | Justificativa | Origem no domínio |
|---|---|---|---|
| **Identificador do registro** | Obrigatório | Identidade própria do registro (ver §3). | Entidade Usuário |
| **Identidade do proprietário** | Obrigatório | Representa "quem é" o único usuário; base do login. | Atributo "identidade do proprietário" |
| **Credencial de acesso** | Obrigatório | Necessária para autenticar o acesso ao espaço pessoal. O **como** técnico (formato/proteção) é de camada externa, fora desta task. | Atributo "credencial de acesso" |

### Evento

| Campo | Obrigatoriedade | Justificativa | Origem no domínio |
|---|---|---|---|
| **Identificador do registro** | Obrigatório | Identidade própria (ver §3). | Entidade Evento |
| **ownerId** | Obrigatório | Identifica o proprietário do evento, mesmo em contexto de usuário único, evitando propriedade implícita e facilitando isolamento/evolução futura. Referência ao Usuário (§4). | Decisão de modelo de dados (não é atributo de domínio) |
| **Título** | Obrigatório | Identifica o que ocorre; sem ele um evento não se distingue de outro. | Atributo "Título" |
| **Data** | Obrigatório | Define o conceito (algo que ocorre numa data) e é base da classificação temporal **derivada**. | Atributo "Data" |
| **Horário** | Opcional | Sem horário, o evento pertence ao dia inteiro. | Atributo "Horário" |

### Tarefa

| Campo | Obrigatoriedade | Justificativa | Origem no domínio |
|---|---|---|---|
| **Identificador do registro** | Obrigatório | Identidade própria (ver §3). | Entidade Tarefa |
| **ownerId** | Obrigatório | Identifica o proprietário da tarefa, mantendo isolamento de dados e permitindo evolução futura sem migração estrutural complexa. Referência ao Usuário (§4). | Decisão de modelo de dados (não é atributo de domínio) |
| **Título** | Obrigatório | Identifica a ação a executar. | Atributo "Título" |
| **Status** | Obrigatório | Estado real e persistido (Pendente/Concluída); resulta de ação explícita do usuário, logo precisa sobreviver entre usos. Padrão: Pendente. | Atributo/Estado "Status" |
| **Prazo** | Opcional | Tarefa sem prazo nunca é atrasada; quando existe, é insumo da condição derivada "atrasada". | Atributo "Prazo" |

### Meta

| Campo | Obrigatoriedade | Justificativa | Origem no domínio |
|---|---|---|---|
| **Identificador do registro** | Obrigatório | Identidade própria (ver §3). | Entidade Meta |
| **ownerId** | Obrigatório | Identifica o proprietário da meta, mantendo a propriedade explícita dos objetivos. Referência ao Usuário (§4). | Decisão de modelo de dados (não é atributo de domínio) |
| **Título** | Obrigatório | Identifica o objetivo. | Atributo "Título" |
| **Progresso** | Obrigatório | Fato persistido (0–100%) atualizado pelo usuário; determina o estado **derivado** ativa/concluída. Padrão: 0%. | Atributo "Progresso" |
| **Data-alvo** | Opcional | Meta pode existir sem prazo específico. | Atributo "Data-alvo" |

> **Não persistido por decisão de domínio:** o **horizonte temporal** da Meta (curto/médio/longo
> prazo) — é natureza qualitativa, não campo (Task 2.2, §3). Não vira campo aqui.

---

## 3. Identity Strategy

- **Todas as entidades possuem identidade própria?** **Sim.** Usuário, Evento, Tarefa e Meta são
  conceitos independentes, cada um com identidade própria de registro. Cada registro é
  individualmente referenciável (ex.: para editar, excluir, concluir, atualizar progresso).

- **Existem entidades dependentes?** **Não** para identidade. Evento, Tarefa e Meta carregam uma
  **referência de propriedade** (`ownerId`) ao Usuário (§4), mas não são "filhas" do Usuário:
  cada uma é um conceito independente com identidade própria, que apenas registra quem é seu
  dono. Não há, no MVP, estruturas que existam só como parte de outra (ex.: subtarefas estão fora
  do escopo).

- **Existe identidade derivada?** **Não.** Nenhum registro é identificado por combinação de
  campos de negócio (título, data, etc.); cada um tem identidade própria, independente de seus
  atributos. Isso evita colisões (ex.: dois eventos com mesmo título e data são registros
  distintos) e permite editar qualquer campo sem perder a identidade.

> A **natureza** do identificador (como é gerado/representado) é decisão técnica de camada
> posterior — aqui afirma-se apenas que **cada registro é unicamente identificável**.

---

## 4. Relationships

Classificação de cada relação como **Persistida**, **Conceitual** ou **Inexistente**, alinhada
à Task 2.2 (§6).

| Relação | Classificação | Justificativa |
|---|---|---|
| **Usuário ↔ Evento** | **Persistida** | Cada evento referencia explicitamente seu proprietário via `ownerId`. Decisão de modelo de dados que torna a propriedade explícita, sem alterar a experiência de usuário único. |
| **Usuário ↔ Tarefa** | **Persistida** | Cada tarefa referencia explicitamente seu proprietário via `ownerId`, mantendo isolamento de dados. |
| **Usuário ↔ Meta** | **Persistida** | Cada meta referencia explicitamente seu proprietário via `ownerId`, mantendo a propriedade explícita dos objetivos. |
| **Evento ↔ Tarefa** | **Inexistente** | Domínio: independentes entre si; nenhum dado os liga. |
| **Evento ↔ Meta** | **Conceitual (não persistida)** | A Meta é o "porquê"; o Evento o "quando". Vínculo apenas conceitual no MVP — não implementado como dado. |
| **Tarefa ↔ Meta** | **Conceitual (não persistida)** | A Meta pode inspirar tarefas, mas não há vínculo explícito no MVP (listado como fora de escopo). |

**Conclusão de relacionamentos:** o **único relacionamento persistido** é o de **propriedade**
(Usuário ↔ Evento/Tarefa/Meta via `ownerId`). **Não há nenhum relacionamento persistido entre
Evento, Tarefa e Meta** — entre os três conceitos as relações permanecem conceituais
(Evento↔Meta, Tarefa↔Meta) ou inexistentes (Evento↔Tarefa). Persistir a propriedade é decisão de
modelo de dados; não introduz multiusuário nem vínculos entre conceitos.

---

## 5. Derived Data Analysis

Informações que **não devem ser armazenadas** porque são **funções de campos já persistidos** e
da data corrente ("hoje"). Persistir um valor derivado criaria risco de inconsistência (o valor
"envelhece" quando o dia muda ou o campo de origem é editado).

| Informação | Persistir? | Derivar? | Por quê |
|---|---|---|---|
| **Evento de hoje** | Não | Sim | Função de `Data = hoje`; muda sozinha com a passagem dos dias. |
| **Evento futuro** | Não | Sim | Função de `Data > hoje`. |
| **Evento passado** | Não | Sim | Função de `Data < hoje`. |
| **"Próximos eventos" (janela 7 dias)** | Não | Sim | Função de `Data` entre amanhã e hoje+7; janela é regra de composição (reversível, D1), não dado. |
| **Tarefa atrasada** | Não | Sim | Função de (Status Pendente **e** possui Prazo **e** `Prazo < hoje`). Depende de "hoje". |
| **Tarefa pendente para hoje** | Não | Sim | Função de (Pendente **e** `Prazo = hoje`). |
| **Meta ativa** | Não | Sim | Função de `Progresso < 100%`. |
| **Meta concluída** | Não | Sim | Função de `Progresso = 100%`. |
| **Blocos do Dashboard** | Não | Sim | Composição em tempo de consulta a partir das estruturas; o Painel não tem dados próprios. |

> **Persistido vs. derivado — fronteira:** persiste-se o **fato bruto** (Data, Status, Prazo,
> Progresso); deriva-se toda **interpretação temporal ou de estado de exibição**. O `Status` da
> Tarefa **é** persistido (resulta de ação do usuário, não é recalculável); "atrasada" **não é**,
> pois é interpretação de Status + Prazo + hoje.

---

## 6. Integrity Rules

Apenas regras **já aprovadas** (PDD Parte 5 e Task 2.2). Nenhuma criada aqui.

**Gerais**
- **Título obrigatório** em Evento, Tarefa e Meta.
- **Identidade do proprietário e credencial obrigatórias** no Usuário.
- **Usuário único:** existe no máximo um proprietário no sistema.

**Evento**
- **Data obrigatória.**
- **Horário opcional.**

**Tarefa**
- **Status obrigatório**, restrito ao conjunto permitido **{Pendente, Concluída}**; padrão
  **Pendente** ao criar.
- **Prazo opcional.**

**Meta**
- **Progresso obrigatório**, dentro da faixa válida **0% a 100%**; padrão **0%**.
- **Data-alvo opcional.**

> Estados permitidos: a Tarefa tem conjunto fechado de status; a Meta **não** tem estado
> armazenado — seu estado é derivado do Progresso (§5), então a única restrição é a faixa do
> Progresso.

---

## 7. Evolution Readiness

| Evolução prevista | Modelo suporta? | Partes impactadas |
|---|---|---|
| **Notas / Informações** | **Sim, aditivamente** | Surge uma **nova estrutura independente** (ex.: "Nota"), no mesmo padrão das atuais. Não toca Usuário, Evento, Tarefa nem Meta. |
| **Recorrência** | **Sim, com impacto localizado** | Afeta **apenas a estrutura Evento** — acrescentando dados de recorrência ou uma estrutura auxiliar que gera ocorrências. Tarefa e Meta intactas. |
| **Relacionamento Meta → Tarefa** | **Sim, aditivamente** | Introduz o **primeiro relacionamento persistido entre conceitos** (hoje só existe a referência de propriedade ao Usuário). Acrescenta vínculo sem exigir mudar os atributos atuais. |
| **Multiusuário futuro** | **Sim, com impacto reduzido** | A propriedade **já é persistida** via `ownerId`; a evolução se resume essencialmente a **remover a restrição "usuário único"** e passar a tratar múltiplos donos. Justamente o que o `ownerId` antecipa: evitar migração estrutural complexa. Os atributos de negócio não mudam. |

- **O modelo suporta a evolução?** **Sim.** A escolha de estruturas independentes e sem dados
  derivados faz com que as evoluções sejam **aditivas** (Notas, Meta→Tarefa) ou **localizadas**
  (Recorrência em Evento; propriedade em multiusuário), sem reescrever o existente.

---

## 8. Data Model Review

- **Existe dado redundante?** **Não.** Cada campo aparece em uma única estrutura; não há cópia
  do mesmo fato em lugares diferentes (não há relacionamentos que poderiam duplicar dados).

- **Existe dado derivado sendo armazenado?** **Não.** Todas as classificações temporais e de
  estado de exibição foram explicitamente deixadas como derivadas (§5). Persiste-se apenas
  Status (Tarefa) e Progresso (Meta), que são fatos, não derivações.

- **Existe relacionamento desnecessário?** **Não.** O único relacionamento persistido é o de
  propriedade (`ownerId`), que tem propósito claro (isolamento de dados e evolução). Não há
  vínculos persistidos entre conceitos.

- **Existe campo sem propósito claro?** **Não.** Cada campo de negócio tem origem rastreável em
  um atributo do Modelo de Domínio (§2); o `ownerId` tem origem e justificativa explícitas como
  decisão de modelo de dados.

---

## Conclusão

1. **Estruturas persistentes oficiais do MVP:** continuam sendo **Usuário**, **Evento**,
   **Tarefa** e **Meta**. *(Painel e Sessão não são persistidos.)* A inclusão de `ownerId` em
   Evento, Tarefa e Meta é decisão de **modelo de dados** e **não** cria novas estruturas nem
   altera o escopo.

2. **Dados derivados (não armazenados):** classificação temporal de Eventos (hoje / futuro /
   passado e janela "próximos 7 dias"), **Tarefa atrasada** e "pendente para hoje", **Meta
   ativa / concluída**, e todos os **blocos do Dashboard**. Persiste-se o fato bruto (Data,
   Status, Prazo, Progresso); deriva-se a interpretação.

3. **Relacionamentos persistidos:** Evento, Tarefa e Meta possuem **relacionamento persistido
   com o Usuário** através de `ownerId`. **Não há relacionamento persistido entre Evento, Tarefa
   e Meta** — entre os três conceitos as relações permanecem conceituais (Evento↔Meta,
   Tarefa↔Meta) ou inexistentes (Evento↔Tarefa).

4. **O modelo está pronto para Wireframes (Task 2.4) e Setup Técnico (Task 2.5)?** **Sim.** As
   estruturas, campos (com obrigatoriedade), identidade, regras de integridade e dados derivados
   estão definidos e consistentes com o domínio aprovado, fornecendo base suficiente tanto para
   desenhar telas quanto para preparar o setup.

### Recomendação

> **Prosseguir para a Task 2.4 (Wireframes).**
> O modelo de dados é enxuto e direto: quatro estruturas independentes, nenhum dado derivado
> armazenado, nenhum relacionamento persistido e nenhuma regra criada além das já aprovadas.
> Está alinhado aos princípios do produto e pronto para sustentar as próximas tasks sem revisão
> prévia.

---

*Documento produzido na Task 2.3 — Modelo de Dados (Fase 2).*
