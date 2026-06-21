# Conceitos Fundamentais — SibylSystem

> Artefato da **Task 1.3 (Fase 1 — Definição do Produto)**.
> Fontes: [`CLAUDE.md`](../CLAUDE.md) (fonte de verdade), [`01-product-vision.md`](./01-product-vision.md), [`02-mvp-scope.md`](./02-mvp-scope.md).
> Em caso de conflito, o CLAUDE.md prevalece.
> Escopo desta task: definir os conceitos e suas fronteiras conceituais.
> **Não** trata de arquitetura, tecnologia, banco, telas, fluxos, modelo de dados ou regras
> funcionais específicas. **Não** cria conceitos novos sem justificativa robusta.

---

## 1. Concept Definitions

### Evento

- **O que é:** algo que **ocorre** em uma data específica (podendo ter horário). É ancorado no
  tempo e existe independentemente de uma ação do usuário — acontece *quando* chega a data.
- **O que não é:** não é algo a ser "feito" pelo usuário no sentido de uma pendência com
  conclusão; não é um objetivo de longo prazo. Um evento não é "concluído" — ele simplesmente
  ocorre, passa e fica no passado.
- **Propósito no sistema:** registrar compromissos e ocorrências datadas para que o usuário
  saiba o que acontece **hoje** e **a seguir**, alimentando os blocos "Eventos de hoje" e
  "Próximos eventos" do dashboard. Resolve o problema de compromissos guardados na memória ou
  dispersos.

### Tarefa

- **O que é:** uma **ação que precisa ser executada** pelo usuário. Pode ter prazo ou não, e
  possui um estado (pendente/concluída). Seu eixo central é a **execução** e a **conclusão**.
- **O que não é:** não é uma ocorrência datada que independe do usuário (isso é Evento); não é
  um objetivo amplo com horizonte e progresso (isso é Meta). Uma tarefa não "acontece sozinha":
  exige ação.
- **Propósito no sistema:** registrar pendências para que nada essencial seja esquecido e para
  que o usuário acompanhe o que falta fazer. Alimenta os blocos "Tarefas pendentes" e "Tarefas
  atrasadas" do dashboard.

### Meta

- **O que é:** um **objetivo a ser alcançado**, com horizonte temporal (curto/médio/longo prazo)
  e uma noção de **progresso**. É um estado futuro desejado, geralmente alcançado por meio de
  múltiplas ações ao longo do tempo.
- **O que não é:** não é uma ação única e pontual (isso é Tarefa); não é uma ocorrência datada
  (isso é Evento). Uma meta normalmente não se cumpre com um único ato, e sim com avanço
  acumulado.
- **Propósito no sistema:** dar visibilidade aos objetivos de vida e à evolução em direção a
  eles, conectando o esforço cotidiano ao que o usuário pretende alcançar. Alimenta o bloco
  "Metas ativas" do dashboard.

---

## 2. Concept Boundaries

### Evento vs Tarefa

- **Eixo distintivo:** *ocorrência datada* (Evento) versus *ação a executar* (Tarefa).
- Um Evento **acontece** em um momento; uma Tarefa **precisa ser feita**.
- Um Evento não tem o estado "concluído"; uma Tarefa tem.
- **Zona cinzenta:** compromissos que exigem ação para acontecer (ex.: "ir à academia").
  Critério de desempate: se o valor está em *saber que ocorre naquele momento*, é Evento; se o
  valor está em *lembrar de executar e marcar como feito*, é Tarefa.

### Tarefa vs Meta

- **Eixo distintivo:** *ação pontual com conclusão* (Tarefa) versus *objetivo amplo com
  horizonte e progresso* (Meta).
- Uma Tarefa termina quando é concluída; uma Meta avança por progresso até ser alcançada.
- **Zona cinzenta:** ações grandes que parecem objetivo (ex.: "organizar o apartamento todo").
  Critério de desempate: se é resolvível em um esforço único e tem conclusão binária, é Tarefa;
  se demanda várias ações ao longo do tempo e faz sentido medir progresso, é Meta.

### Evento vs Meta

- **Eixo distintivo:** *momento que ocorre* (Evento) versus *estado futuro desejado* (Meta).
- Um Evento é pontual e datado; uma Meta é um horizonte com avanço acumulado.
- **Zona cinzenta:** marcos com data (ex.: "prova do concurso em 10/2026"). Critério de
  desempate: a *prova* (ocorrência datada) é Evento; *ser aprovado no concurso* (objetivo com
  progresso) é Meta. O evento pode ser um marco a serviço da meta, mas são conceitos distintos.

---

## 3. Relationship Between Concepts

Relações **conceituais** (não técnicas, sem dependências de implementação):

- **Meta → Tarefas e Eventos:** o CLAUDE.md afirma que uma Meta "pode originar tarefas e
  eventos". Conceitualmente, a Meta é o "porquê" de longo prazo; Tarefas e Eventos são parte do
  "como" e do "quando" no cotidiano. Uma meta de "ser aprovado em concurso" pode inspirar a
  tarefa "estudar edital" e o evento "prova em 10/2026".
- **Tarefa ↔ Evento:** independentes entre si, mas complementares no tempo do usuário. Uma
  tarefa pode estar associada a uma data (prazo) e um evento pode demandar preparação (tarefas),
  porém cada um mantém sua natureza própria.
- **Horizonte temporal compartilhado:** os três convivem na linha do tempo da vida do usuário —
  Evento marca o *quando ocorre*, Tarefa marca o *quando precisa estar feito* (se houver prazo),
  Meta marca o *até quando se quer alcançar*.

> Importante: no MVP, vínculo explícito entre Meta e suas Tarefas/Eventos está **fora do escopo**
> (ver Task 1.2). A relação aqui é conceitual e orienta o entendimento, não um requisito.

---

## 4. Classification Guide (árvore de decisão)

Para algo que o usuário deseja registrar:

```
O que você quer registrar?
│
├─ É um objetivo amplo, que você quer ALCANÇAR ao longo do tempo,
│  e faz sentido acompanhar PROGRESSO?
│        │
│        └─ SIM ─────────────────────────────────► é uma META
│
├─ (não) É uma OCORRÊNCIA com data definida, que vai ACONTECER
│  naquele momento (com ou sem horário) e não precisa ser "concluída"?
│        │
│        └─ SIM ─────────────────────────────────► é um EVENTO
│
└─ (não) É uma AÇÃO que VOCÊ precisa EXECUTAR e poder marcar
   como concluída (com ou sem prazo)?
         │
         └─ SIM ────────────────────────────────► é uma TAREFA
```

**Perguntas-guia de desempate:**

- "Isso **acontece** num momento ou **precisa ser feito** por mim?" → ocorrência = Evento; ação = Tarefa.
- "Resolvo com **um esforço** e marco como feito, ou avanço **aos poucos** até alcançar?" → conclusão única = Tarefa; progresso = Meta.
- "Tem **data em que ocorre**, ou **horizonte até quando quero chegar lá**?" → data de ocorrência = Evento; horizonte de objetivo = Meta.

---

## 5. Real World Classification

| Exemplo | Classificação | Explicação |
|---|---|---|
| Comprar guarda-roupa | **Tarefa** | Ação pontual a executar, com conclusão binária. Consta como exemplo de tarefa no CLAUDE.md. |
| Consulta médica | **Evento** | Ocorrência datada (com horário) que acontece naquele momento; não se "conclui", ocorre. |
| Natação terça-feira às 18h | **Evento** | Ocorrência com data e horário. *(Zona cinzenta: a recorrência semanal é funcionalidade futura — no MVP registra-se como evento pontual.)* |
| Pagar conta de energia | **Tarefa** | Ação a executar, com conclusão. *(Zona cinzenta: é recorrente mensal; recorrência está fora do MVP — registra-se como tarefa, eventualmente com prazo.)* |
| Comprar apartamento | **Meta** | Objetivo amplo, horizonte longo, alcançado por múltiplas ações; faz sentido medir progresso. Exemplo de meta no CLAUDE.md. |
| Concluir pós-graduação | **Meta** | Objetivo de longo prazo com progresso ao longo do tempo. Exemplo de meta no CLAUDE.md. |
| Melhorar tempo nos 50m livre | **Meta** | Objetivo com horizonte e progresso mensurável. Exemplo de meta no CLAUDE.md. |
| Preparação para concurso público | **Meta** | Objetivo amplo com horizonte e progresso (alinhado a "ser aprovado em concurso"). Origina tarefas (estudar) e eventos (prova). |
| Construção do projeto RAIRE | **Meta** | Objetivo de longo prazo, multi-ação, com progresso. Exemplo de meta no CLAUDE.md ("Construir o RAIRE"). |
| Fazer limpeza do apartamento | **Tarefa** | Ação a executar com conclusão. *(Zona cinzenta: se for entendido como esforço amplo e contínuo, aproxima-se de Meta; como ato único, é Tarefa.)* |

---

## 6. Domain Completeness Analysis

**Conclusão:** para o **domínio definido pela visão e pelo escopo do MVP**, os três conceitos
— Evento, Tarefa e Meta — são **suficientes**.

**Justificativa:**

- A visão organiza a vida em torno de: o que **acontece** (Evento), o que **precisa ser feito**
  (Tarefa) e o que se **pretende alcançar** (Meta). Esses três eixos cobrem "o que preciso
  fazer / o que estou fazendo / o que pretendo alcançar / como evoluo" — exatamente o que o
  dashboard do MVP entrega.
- Todos os exemplos do CLAUDE.md e os exemplos da seção 5 foram classificados sem necessidade de
  um quarto conceito.

**Possível lacuna observada (sem criar conceito novo agora):**

- A seção "Visão" do CLAUDE.md menciona centralizar também **"informações relevantes"** —
  conteúdo puramente informativo, sem data de ocorrência, sem ação a executar e sem ser um
  objetivo. Exemplos concretos que **não** se encaixam bem nos três conceitos: "tamanho de
  roupa de um familiar", "senha/credencial de referência", "lista de filmes para assistir",
  "anotações de uma reunião".
- **Demonstração da insuficiência:** forçar essas informações em Tarefa cria pendências que
  nunca se concluem; forçá-las em Evento exige uma data que não existe; em Meta, não há objetivo
  nem progresso. Logo, há uma classe de informação não coberta.
- **Por que NÃO criar o conceito agora:** "informações relevantes" **não consta do Escopo do
  MVP** (Task 1.2) — o MVP cobre apenas Eventos, Tarefas, Metas e Dashboard. Criar um quarto
  conceito ("Nota"/"Informação") agora violaria os princípios de simplicidade e de não antecipar
  funcionalidades. A insuficiência só se materializa **fora** do escopo atual.
- **Alternativas (registradas como observação futura, não decididas aqui):** (a) manter os três
  conceitos e tratar "informações relevantes" como evolução pós-MVP; (b) avaliar, em fase
  futura, um conceito de "Nota/Informação" caso o uso real comprove a necessidade. Recomenda-se
  (a) para o MVP.

---

## 7. Risks and Ambiguities

| Ambiguidade conceitual | Impacto |
|---|---|
| **Tarefa recorrente vs Evento recorrente** (ex.: "pagar luz", "natação semanal") | UX e futuras regras: sem recorrência no MVP, o usuário pode hesitar entre recriar manualmente como Tarefa ou Evento. Afeta evolução (recorrência futura). |
| **Ação ampla vs Meta** (ex.: "organizar o apartamento", "fazer limpeza") | UX: usuário pode classificar inconsistentemente. Afeta regras de progresso e a clareza do dashboard. |
| **Marco datado de uma Meta** (ex.: "prova do concurso") | UX e regras: o evento-marco e a meta coexistem; sem vínculo no MVP, a relação fica implícita. Afeta evolução (vínculo Meta→Evento). |
| **"Informações relevantes" sem lar conceitual** | Produto/evolução: classe de conteúdo citada na visão mas fora do MVP; risco de o usuário sentir falta de onde guardar notas. |
| **Tarefa com prazo vs Evento datado** | Regras: "tarefa atrasada" depende de prazo; a fronteira com Evento datado precisará de regra clara (Task de Regras Funcionais). |

Esses pontos pertencem majoritariamente às **Regras Funcionais** (próxima etapa da Fase 1) e à
**evolução pós-MVP**; não são lacunas que impeçam avançar.

---

## Conclusão

1. **Os conceitos atuais são suficientes?**
   Sim, para o domínio do MVP. Evento, Tarefa e Meta cobrem "o que acontece / o que fazer / o
   que alcançar", que é o valor definido na visão.

2. **Existe alguma lacuna conceitual?**
   Uma lacuna **potencial e fora do escopo atual**: "informações relevantes" (notas) citadas na
   visão não têm conceito próprio. Demonstrada com exemplos, mas **não** essencial ao MVP —
   registrada como observação futura, sem criar conceito agora.

3. **Existe algum conceito redundante?**
   Não. Evento, Tarefa e Meta têm eixos distintos (ocorrência / ação / objetivo) e não se
   sobrepõem; as zonas cinzentas têm critérios de desempate.

4. **Existe algum conceito faltando?**
   Nenhum **essencial** ao MVP. O único candidato ("Nota/Informação") fica fora do escopo e só
   deve ser avaliado em fase futura se o uso real comprovar a necessidade.

**Recomendação: Prosseguir para a Task 1.4.** As ambiguidades remanescentes são de regras
funcionais e de evolução, a serem tratadas no momento apropriado da Fase 1.

---

## Observações Futuras

- **OF (1.3-a).** Avaliar, pós-MVP, um conceito de **Nota/Informação** para "informações
  relevantes" citadas na visão — somente com justificativa de uso real.
- **OF (1.3-b).** Recorrência (de Eventos e/ou Tarefas) impacta a classificação; tratar no
  roadmap de evoluções futuras.
- **OF (1.3-c).** Vínculo conceitual Meta → Tarefas/Eventos (marcos) pode tornar-se vínculo
  explícito em fase futura, fora do MVP.
