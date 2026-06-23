# SibylSystem — Modelo de Domínio

> **Documento da Fase 2 (Arquitetura) — Task 2.2.**
> Fontes: PDD (definição oficial do produto), CLAUDE.md (fonte de verdade) e
> `08-high-level-architecture.md` (definição oficial dos módulos).
> Em caso de conflito, o CLAUDE.md prevalece.
>
> **Propósito:** modelar o **domínio de negócio** do SibylSystem — entidades conceituais,
> atributos de negócio, estados, regras de domínio e fronteiras entre conceitos.
>
> **Restrições desta task:** não escolhe tecnologias; não define tabelas, banco de dados, ORM
> ou migrations; não discute APIs nem persistência; não cria detalhes técnicos; não altera o
> escopo nem cria funcionalidades. Descreve apenas **significado de negócio**.

---

## 1. Domain Overview

- **Núcleo do domínio:** a organização da vida pessoal do usuário em torno de **três conceitos
  mutuamente exclusivos** — **Evento**, **Tarefa** e **Meta** — e a **consolidação** deles em
  uma visão única (o Painel). O domínio existe para responder, a qualquer momento, "o que
  preciso fazer, o que está pendente/atrasado e quais objetivos estão ativos".

- **Conceitos centrais:**
  - **Evento** — algo que **ocorre** numa data (âncora no tempo, não se "conclui").
  - **Tarefa** — uma **ação** que o usuário precisa **executar** e marcar como feita.
  - **Meta** — um **objetivo** a alcançar, acompanhado por **progresso**.

- **Como se relacionam conceitualmente:** os três são **independentes em dados**, porém
  complementares na vida do usuário. A Meta é o "porquê" de longo prazo; Tarefas e Eventos são
  o "como" e o "quando" do cotidiano (relação **apenas conceitual**, sem vínculo de dados no
  MVP — Parte 4 do PDD). Sobre esses conceitos atua uma capacidade de **consolidação** (o
  Painel), que **lê** os três e os apresenta em blocos — sem ser, ele próprio, um conceito de
  dados.

---

## 2. Domain Entities

Apenas entidades necessárias para representar o domínio do MVP — nenhuma criada por
conveniência técnica.

| Entidade | Propósito | Responsabilidade | Módulo |
|---|---|---|---|
| **Evento** | Representar uma ocorrência datada da vida do usuário. | Conhecer **quando** ocorre e classificar-se no tempo (passado / hoje / futuro). | Eventos |
| **Tarefa** | Representar uma ação a executar. | Conhecer seu **status** e seu **prazo**, e determinar se está pendente, concluída ou atrasada. | Tarefas |
| **Meta** | Representar um objetivo a alcançar. | Conhecer seu **progresso** e determinar se está ativa ou concluída. | Metas |
| **Usuário** | Representar o **proprietário único** do sistema. | Sustentar a noção de "a quem o espaço pessoal pertence" e a identidade para acesso. | Acesso |

**Entidades deliberadamente NÃO criadas:**

- **Painel / Dashboard** — **não é entidade**. É uma **capacidade de consolidação** que compõe
  blocos a partir das três entidades de conceito; não possui dados próprios. Suas regras moram
  no **módulo de Painel** (ver §5), não numa entidade.
- **Sessão** — **não é entidade de domínio**. A noção de "sessão ativa" é uma preocupação
  técnica de autenticação (fora do escopo desta task), não um conceito de negócio.

> A entidade **Usuário** é mínima e periférica ao núcleo: num sistema de **usuário único** ela
> existe apenas para sustentar a proteção do espaço pessoal. O núcleo de valor são Evento,
> Tarefa e Meta.

---

## 3. Entity Attributes

Apenas significado de negócio — sem tipos técnicos.

### Evento

| Atributo | Obrigatoriedade | Justificativa |
|---|---|---|
| **Título** | Obrigatório | Identificação do que ocorre (ex.: "Natação", "Consulta médica"). Sem ele não se distingue um evento de outro. Derivado dos exemplos do PDD. |
| **Data** | Obrigatório | Define o conceito: um evento é "algo que ocorre **em uma data específica**" (Parte 4). É a âncora temporal e a base da classificação no tempo. |
| **Horário** | Opcional | PDD: "o horário é opcional; sem horário, o evento pertence ao dia inteiro" (Parte 4 e 5). |

### Tarefa

| Atributo | Obrigatoriedade | Justificativa |
|---|---|---|
| **Título** | Obrigatório | Identificação da ação (ex.: "Pagar conta"). Sem ele a tarefa não tem significado. Derivado dos exemplos do PDD. |
| **Status** | Obrigatório | Toda tarefa tem um estado (Pendente por padrão; Concluída por ação). É o eixo central do conceito — "execução e conclusão" (Parte 4). |
| **Prazo** | Opcional | PDD: "o prazo é opcional. Tarefa sem prazo nunca é considerada atrasada" (Parte 4 e 5). |

### Meta

| Atributo | Obrigatoriedade | Justificativa |
|---|---|---|
| **Título** | Obrigatório | Identificação do objetivo (ex.: "Concluir pós-graduação"). Derivado dos exemplos do PDD. |
| **Progresso** | Obrigatório | Percentual de 0% a 100%; é a noção que define a Meta e dispensa um campo de estado separado (Parte 4 e 5). Inicia em 0%. |
| **Data-alvo** | Opcional | PDD: "a data-alvo é opcional; a meta pode existir sem prazo específico" (Parte 4 e 5). |

> **Horizonte temporal (curto/médio/longo prazo):** segundo o PDD é uma **natureza qualitativa
> sempre presente, porém não é campo obrigatório** (Parte 5). Portanto **não é modelado como
> atributo** no MVP — é uma característica conceitual da Meta, não um dado armazenado.

### Usuário

| Atributo | Obrigatoriedade | Justificativa |
|---|---|---|
| **Identidade do proprietário** | Obrigatório | Representa "quem é" o único usuário do sistema, base para o login. |
| **Credencial de acesso** | Obrigatório | Necessária para autenticar o acesso ao espaço pessoal (Parte 3). O **como** técnico está fora do escopo desta task. |

> Mantido deliberadamente mínimo: não há perfil, preferências, configurações ou múltiplos
> usuários no MVP.

---

## 4. Entity States

### Evento — **sem estados de ciclo de vida**

Justificativa: o PDD afirma que "um evento não é concluído: simplesmente ocorre, passa e fica
no passado" (Parte 4). A classificação **passado / hoje / futuro** **não é um estado
armazenado**: é **derivada** da comparação entre a `Data` e a data corrente ("hoje"). Logo, o
Evento não transita entre estados — sua posição no tempo muda sozinha com a passagem dos dias.

### Tarefa — **Pendente → Concluída**

| Estado | Significado |
|---|---|
| **Pendente** | Estado inicial ao criar; ação ainda não executada. |
| **Concluída** | Ação realizada; definida por **ação explícita do usuário**. |

- **Transição aprovada:** Pendente → Concluída, disparada pela ação "concluir" do usuário.
- **"Atrasada" não é um terceiro estado:** é uma **condição derivada** = (Pendente **e** possui
  prazo **e** `prazo < hoje`). PDD: "não existem estados intermediários no MVP" (Parte 4).
- O retorno de Concluída para Pendente **não está definido no escopo aprovado**; não é criado
  aqui.

### Meta — **Ativa → Concluída** (determinada pelo progresso)

| Estado | Significado |
|---|---|
| **Ativa** | `Progresso < 100%`. |
| **Concluída** | `Progresso = 100%`; sai de "Metas Ativas". |

- **Como muda de estado:** o estado é **inteiramente função do atributo `Progresso`**. Atualizar
  o progresso é o único mecanismo; ao cruzar 100% torna-se Concluída e, por simetria do
  critério, voltar abaixo de 100% a reativa. PDD: "o progresso elimina a necessidade de um campo
  de estado separado" (Parte 4).

### Usuário — **sem estados de negócio relevantes**

Justificativa: em um sistema de usuário único, o proprietário simplesmente existe. "Sessão
ativa/inativa" é preocupação **técnica de autenticação**, não estado de domínio.

---

## 5. Domain Rules

Consolidação **somente** de regras já aprovadas (PDD Parte 5 e Task 2.1). A atribuição de dono
segue a fronteira definida na Task 2.1: **o módulo do conceito é dono do estado/classificação
do item; o Painel é dono da seleção e composição dos blocos.**

### Regras de Eventos

- A `Data` classifica o evento no tempo: `data = hoje` → de hoje; `data > hoje` → futuro;
  `data < hoje` → passado.
- Sem horário, o evento pertence ao **dia inteiro** (sem posição específica na linha do dia).

### Regras de Tarefas

- Status padrão ao criar: **Pendente**.
- Prazo é opcional; **tarefa sem prazo nunca é atrasada**.
- **Atrasada** = Pendente **e** possui prazo **e** `prazo < hoje`.
- **Pendente para hoje** (`prazo = hoje`) → é pendente, **não** atrasada.
- **Concluir** é ação explícita do usuário; tarefa concluída sai de todos os blocos do
  dashboard.

### Regras de Metas

- **Progresso** é percentual de **0% a 100%**, atualizado pelo usuário.
- **Data-alvo** é opcional.
- **Horizonte temporal** está sempre presente como natureza qualitativa; não é campo
  obrigatório.
- **Ativa** = `progresso < 100%`; **Concluída** = `progresso = 100%`.

### Regras do Painel

- Compõe **5 blocos**: Eventos de Hoje, Próximos Eventos, Tarefas Pendentes, Tarefas Atrasadas,
  Metas Ativas.
- **Eventos de Hoje:** `data = hoje`.
- **Próximos Eventos:** `data` entre **amanhã** e **hoje + 7 dias** (inclusive). Janela de 7
  dias — decisão reversível (D1).
- **Tarefas Pendentes:** pendentes **sem atraso** (sem prazo, ou `prazo ≥ hoje`).
- **Tarefas Atrasadas:** pendentes com prazo e `prazo < hoje`; aparecem **somente** neste bloco.
- **Metas Ativas:** progresso `< 100%`.
- **Eventos passados** não aparecem no dashboard (permanecem na tela de Eventos).
- **Anti-sobreposição:** nenhum item aparece em dois blocos.

> Observação de fronteira: a **derivação** de "atrasada" (Tarefa) e de "ativa" (Meta) e a
> **classificação temporal** (Evento) pertencem aos módulos de conceito; o Painel apenas
> **seleciona** itens já classificados e os organiza em blocos (mitiga o risco A2 da Task 2.1).

---

## 6. Relationships Analysis

| Par | Tipo de relacionamento | Justificativa |
|---|---|---|
| **Evento ↔ Tarefa** | **Nenhum** | PDD (Parte 4): "independentes entre si, complementares na linha do tempo". Não há dado que ligue um ao outro. |
| **Tarefa ↔ Meta** | **Apenas conceitual** | A Meta pode inspirar tarefas, mas "no MVP não há vínculo explícito implementado" (Parte 4). |
| **Evento ↔ Meta** | **Apenas conceitual** | Mesma base: "Meta → Tarefas e Eventos (conceitual)"; sem vínculo de dados no MVP. |
| **Conceitos ↔ Painel** | **Consumo unidirecional (não é relação entre entidades)** | O Painel **lê** Evento, Tarefa e Meta para compor blocos. O Painel não é entidade e não é conhecido pelos conceitos (Task 2.1: dependência em sentido único). |
| **Usuário ↔ Conceitos** | **Propriedade implícita (sem vínculo explícito)** | Conceitualmente tudo pertence ao único proprietário, mas, sendo **usuário único**, modelar um vínculo explícito seria estrutura prematura de multiusuário (fora do escopo). A propriedade é global/implícita. |

**Conclusão de relacionamentos:** **não existe nenhum relacionamento explícito de dados entre
os conceitos no MVP.** Criar qualquer vínculo agora violaria o escopo (vínculo Meta→Tarefa/Evento
está listado como fora do MVP) e o princípio da simplicidade.

> **Observação cruzada — `ownerId` (decisão da Task 2.3, registrada na Task 2.7).** No **modelo de
> dados**, a propriedade do Usuário sobre Evento, Tarefa e Meta é **persistida explicitamente** via
> um campo `ownerId` (ver `10-data-model.md`, §4). Isso **não contradiz** este modelo de domínio:
> - `ownerId` é uma **decisão de persistência**, não de domínio;
> - **não altera o domínio** — os conceitos, atributos de negócio, estados e regras permanecem os
>   desta Task 2.2 (`ownerId` não é atributo de domínio);
> - **não transforma o MVP em multiusuário** — a experiência continua de usuário único;
> - existe **apenas para preservar a evolução futura** (evitar migração estrutural complexa) e
>   garantir isolamento de dados desde já.
> Em resumo: no **domínio**, a propriedade é conceitual; na **camada de dados**, é materializada
> como `ownerId`. As duas leituras são coerentes entre si.

---

## 7. Domain Boundaries

### Pertence ao domínio

- As entidades **Evento, Tarefa, Meta** e (perifericamente) **Usuário**.
- Seus **atributos de negócio**, **estados** e **transições**.
- As **regras de negócio**: classificação temporal de eventos, status/atraso de tarefas, faixa
  e estado de progresso de metas.
- As **regras de composição do Painel** (definição e critérios de inclusão/exclusão dos blocos,
  anti-sobreposição) — pertencem ao **módulo de Painel** como capacidade de domínio, ainda que
  o Painel não seja uma entidade.
- A noção de **proprietário único** do espaço pessoal.

### Não pertence ao domínio

- Persistência, banco de dados, tabelas, ORM, migrations.
- Telas, navegação, formatação e apresentação visual dos blocos.
- Mecanismo técnico de **autenticação** e de **sessão**.
- Obtenção da **data corrente ("hoje")** — o domínio **usa** "hoje" como insumo de suas regras,
  mas **como** o relógio/calendário é obtido é responsabilidade de camada externa.
- Integrações, notificações, sincronizações (fora do escopo do MVP).

### Responsabilidade do domínio vs. de futuras camadas

- **Domínio:** decidir estados (pendente/concluída, ativa/concluída), validar a faixa de
  progresso (0–100%), classificar eventos no tempo, definir quais itens compõem cada bloco e
  garantir a anti-sobreposição.
- **Futuras camadas (fora desta task):** armazenar e recuperar dados, expor operações,
  autenticar tecnicamente, renderizar telas, fornecer a data corrente.

---

## 8. Domain Evolution Analysis

Análise das evoluções **já registradas** (sem adicioná-las).

| Evolução | Onde se encaixaria | Altera o domínio atual? | Exige revisar entidades atuais? |
|---|---|---|---|
| **Notas / Informações** | Nova entidade (ex.: "Nota") em um **novo módulo irmão** de Eventos/Tarefas/Metas; opcionalmente um novo bloco consumido pelo Painel. | **Aditivo** — acrescenta um conceito sem mexer nos existentes. | **Não.** Evento, Tarefa e Meta permanecem inalterados. |
| **Recorrência** | No **domínio de Evento** — introduziria a noção de recorrência (atributo ou uma entidade auxiliar que gera ocorrências). Hoje "cada ocorrência é um evento distinto" (Parte 4). | **Sim, localizado em Evento** — Tarefa e Meta não são afetadas. | **Sim, apenas Evento.** Revisão localizada; não toca as demais entidades. |
| **Vínculo Meta → Tarefa/Evento** | Na **camada de relacionamentos** — transformaria a relação hoje conceitual em vínculo explícito de dados. | **Sim** — introduz um relacionamento hoje inexistente por decisão de escopo. | **Parcialmente:** acrescenta uma associação; os **atributos** centrais das entidades tendem a permanecer. |

**Leitura geral:** o modelo atual **suporta** essas evoluções sem ser invalidado por elas. A
mais "barata" é Notas (puramente aditiva); recorrência é uma revisão **localizada** em Evento; o
vínculo Meta→Tarefa/Evento é a única que introduz **relacionamento** novo — coerente com tê-lo
deixado fora do MVP por simplicidade.

---

## 9. Domain Review

- **Existe entidade redundante?** **Não.** Evento, Tarefa e Meta são mutuamente exclusivas
  (limites da Parte 4); Usuário é mínima mas necessária para a proteção do espaço pessoal;
  Painel e Sessão foram corretamente **excluídos** como entidades.

- **Existe entidade faltando?** **Não**, para o MVP. Todo o escopo (3 conceitos + autenticação +
  dashboard) está coberto. Conceitos futuros (Nota) só entram quando validados.

- **Existe responsabilidade sem dono?** **Não.** Estado/classificação de cada item → módulo do
  conceito; composição dos blocos → módulo de Painel; proteção do espaço → módulo de Acesso.

- **Existe regra sem dono?** **Não.** Todas as regras da §5 estão atribuídas a Eventos, Tarefas,
  Metas ou Painel. Nota: as regras do Painel têm dono (o **módulo** de Painel) mesmo sem haver
  uma entidade Painel — regras de composição são uma capacidade de domínio, não precisam residir
  em uma entidade.

---

## Conclusão

1. **Entidades oficiais do domínio:**
   - **Evento**, **Tarefa**, **Meta** (núcleo do domínio).
   - **Usuário** (suporte, módulo de Acesso).
   - *(Painel e Sessão não são entidades.)*

2. **Entidade mais importante:** Não há uma entidade principal isolada no domínio. Evento,
   Tarefa e Meta compõem juntos o núcleo do SibylSystem, cada um representando um eixo distinto
   da organização pessoal: o que acontece, o que precisa ser feito e o que se deseja alcançar.
   Tarefa pode ser a entidade operacionalmente mais frequente, mas isso não a torna superior a
   Evento ou Meta no modelo de domínio. O Painel é a principal experiência de valor do produto,
   mas não é uma entidade de domínio.

3. **Existe relacionamento explícito entre os conceitos?** **Não.** No MVP há apenas relações
   **conceituais** (Meta ↔ Tarefa/Evento) e **consumo unidirecional** pelo Painel. Nenhum vínculo
   explícito de dados entre as entidades — por decisão de escopo.

4. **O modelo está pronto para o Modelo de Dados (Task 2.3)?** **Sim.** Entidades, atributos
   (com obrigatoriedade), estados, transições, regras com dono e ausência de relacionamentos
   explícitos estão definidos e consistentes com o PDD e com a Task 2.1.

### Recomendação

> **Prosseguir para a Task 2.3 (Modelo de Dados).**
> O modelo de domínio é simples, sem entidades redundantes ou faltantes, sem responsabilidades
> ou regras órfãs, e alinhado aos princípios do produto. As evoluções previstas têm encaixe
> claro e não exigem revisão do modelo antes de continuar.

---

*Documento produzido na Task 2.2 — Modelo de Domínio (Fase 2).*
