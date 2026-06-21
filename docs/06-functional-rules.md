# Regras Funcionais — SibylSystem

> Artefato da **Task 1.6 (Fase 1 — Definição do Produto)**.
> Fontes: [`CLAUDE.md`](../CLAUDE.md) (fonte de verdade) e Tasks 1.1–1.5.
> Em caso de conflito, o CLAUDE.md prevalece.
> Escopo desta task: como Evento, Tarefa e Meta se comportam dentro do sistema.
> **Não** trata de arquitetura, tecnologia, banco, implementação, tabelas/entidades.
> **Não** cria funcionalidades, não altera escopo nem redefine conceitos.
> Toda regra é justificada pela visão, pelos conceitos e pela simplicidade.
>
> **Convenção:** "hoje" é a data corrente do usuário. As regras usam comparação por **data**
> (dia), não por instante, salvo quando o horário existir e for relevante.

---

## 1. Evento — Regras Funcionais

**Definições temporais (por data):**

- **Evento futuro:** `data do evento > hoje`.
- **Evento atual (de hoje):** `data do evento = hoje`.
- **Evento passado:** `data do evento < hoje`.

**Como aparecem no Dashboard:**

- Eventos de hoje → bloco "Eventos de Hoje".
- Eventos futuros dentro da janela → bloco "Próximos Eventos".
- Eventos passados → **não** aparecem no dashboard (o dashboard é sobre "agora e a seguir"; o
  passado não apoia a decisão do dia). Permanecem acessíveis na tela de Eventos.

**O que significa "Próximos Eventos":**

- Eventos com `data` entre **amanhã** e **hoje + 7 dias** (inclusive).

**Respostas explícitas:**

- **Qual a janela temporal?** **7 dias** (próxima semana). *Justificativa:* é a menor janela
  que entrega antecipação útil para uma rotina pessoal (ritmo semanal), sem transformar o bloco
  numa agenda longa que competiria com a clareza do dashboard. É uma **decisão de produto
  reversível** — pode ser ajustada após uso real (ver Observações Futuras).
- **Existe limite de quantidade?** **Não há limite artificial** no MVP; a própria janela de 7
  dias limita naturalmente o volume. *Justificativa:* simplicidade — evita introduzir regra de
  paginação/corte sem necessidade comprovada.
- **Eventos sem horário — tratamento conceitual:** o horário é **opcional** (CLAUDE.md: "Pode
  possuir horário"). Um evento sem horário pertence ao **dia inteiro**: é tratado como ocorrência
  daquele dia, sem posição específica na linha do tempo do dia. Conceitualmente equivale a "algo
  que acontece neste dia". *Justificativa:* preserva simplicidade e cobre exemplos reais
  (consultas com horário; compromissos só com data).

---

## 2. Tarefa — Regras Funcionais

### Status possíveis

- **Status existentes:** **Pendente** e **Concluída** (dois estados).
- **O MVP precisa de mais de dois status?** **Não.** *Justificativa:* o escopo (Task 1.2) prevê
  apenas "concluir" como transição de estado, e os conceitos (Task 1.3) definem a Tarefa pelo
  eixo execução/conclusão. Estados extras (ex.: "em andamento", "cancelada") seriam
  funcionalidade nova e adicionariam carga cognitiva — contrariando simplicidade. Dois estados
  bastam para alimentar "pendentes" e "atrasadas".

### Prazo

- **O prazo é obrigatório?** **Não.** O prazo é **opcional** (CLAUDE.md: "Pode possuir prazo /
  Pode não possuir prazo").
- **O que significa uma tarefa sem prazo?** É uma pendência **sem data limite** — precisa ser
  feita, mas não tem cobrança temporal. *Consequência:* uma tarefa sem prazo **nunca é
  considerada atrasada**.

### Atraso

- **Quando uma tarefa é atrasada?** Quando está **Pendente** **e** possui prazo **e**
  `prazo < hoje` (o prazo já passou). Uma tarefa com `prazo = hoje` **não** está atrasada — ela
  é pendente para hoje.
- **Como aparece no Dashboard?** No bloco **"Tarefas Atrasadas"**. Para evitar duplicidade,
  uma tarefa atrasada aparece **apenas** nesse bloco, e **não** em "Tarefas Pendentes" (ver §4).

### Conclusão

- **O que caracteriza uma tarefa concluída?** A tarefa cujo status foi alterado para
  **Concluída** pela ação explícita do usuário (Fluxo 4). Uma tarefa concluída sai de
  "pendentes" e de "atrasadas". *Justificativa:* conclusão é um ato deliberado do usuário —
  coerente com o eixo de execução do conceito Tarefa.

---

## 3. Meta — Regras Funcionais

### Progresso

- **Representação conceitual:** **percentual de 0% a 100%**.
- **Percentual, marcos ou outro?** **Percentual.** *Justificativa:* é a forma **universal e
  mais simples** de representar avanço para qualquer meta (comprar apartamento, melhorar tempo,
  concluir pós), atende ao Fluxo 6 ("atualizar progresso") com uma única ação e não exige
  estrutura adicional. **Marcos** seriam um modelo mais rico, porém mais complexo e não
  essencial ao MVP — ficam como observação futura.

### Horizonte Temporal

- **Meta possui prazo / data-alvo?** A **data-alvo é opcional**. O CLAUDE.md afirma que a Meta
  "possui horizonte temporal"; esse horizonte é entendido de forma **qualitativa** (curto, médio
  ou longo prazo, conforme a Missão do Produto) e está sempre presente como **natureza** da
  meta. Uma **data-alvo específica** é um detalhe opcional.
- **Meta pode existir sem prazo?** **Sim** — sem data-alvo específica. *Justificativa:* metas
  reais como "comprar apartamento" frequentemente não têm data exata; exigir data-alvo criaria
  fricção e dados artificiais, contrariando simplicidade. O horizonte qualitativo (longo prazo,
  etc.) permanece como leitura conceitual, sem ser um campo obrigatório no MVP.

### Estado da Meta

- **Meta ativa:** meta com **progresso < 100%** (e não excluída). *Justificativa:* enquanto não
  alcançada, está em andamento e deve permanecer visível em "metas ativas".
- **Meta concluída:** meta com **progresso = 100%** (objetivo alcançado). Sai de "metas ativas".
  *Justificativa:* 100% representa o objetivo atingido — estado terminal natural, sem necessidade
  de um campo de status separado (o progresso já carrega essa informação → mais simples).

---

## 4. Dashboard Rules

> Princípio comum: cada bloco mostra **somente** o que apoia a decisão "agora e a seguir";
> nenhum item aparece em dois blocos (evita ruído e preserva clareza — Task 1.5 §3).

### Eventos de Hoje

- **Inclusão:** eventos com `data = hoje`.
- **Exclusão:** eventos passados e futuros.
- **Objetivo:** dar clareza imediata do que ocorre no dia.

### Próximos Eventos

- **Inclusão:** eventos com `data` entre **amanhã** e **hoje + 7 dias** (inclusive).
- **Exclusão:** eventos de hoje (já em "Eventos de Hoje"), eventos passados e eventos além de 7
  dias.
- **Objetivo:** antecipar a semana, reduzindo risco de esquecimento.

### Tarefas Pendentes

- **Inclusão:** tarefas **Pendentes** que **não** estão atrasadas — ou seja, sem prazo, ou com
  `prazo >= hoje`.
- **Exclusão:** tarefas concluídas e tarefas atrasadas (estas vão para o bloco próprio).
- **Objetivo:** mostrar o que falta fazer e ainda está dentro do prazo (ou sem prazo).

### Tarefas Atrasadas

- **Inclusão:** tarefas **Pendentes** com prazo e `prazo < hoje`.
- **Exclusão:** tarefas concluídas; tarefas sem prazo; tarefas com `prazo >= hoje`.
- **Objetivo:** destacar o que venceu, apoiando a priorização do urgente.

### Metas Ativas

- **Inclusão:** metas com **progresso < 100%**.
- **Exclusão:** metas concluídas (100%).
- **Objetivo:** manter os objetivos em andamento visíveis no dia a dia.

---

## 5. Simplicity Analysis

| Regra | Aumenta ou reduz simplicidade? | Observação |
|---|---|---|
| Evento futuro/atual/passado por data | **Reduz complexidade** (comparação direta de datas) | OK |
| Janela "Próximos" = 7 dias fixos | **Mantém simples** (constante única, sem configuração) | OK; revisável |
| Sem limite de quantidade | **Reduz complexidade** (sem paginação no MVP) | OK |
| Evento sem horário = dia inteiro | **Mantém simples** | OK |
| Tarefa com 2 status | **Reduz carga cognitiva** (mínimo necessário) | OK |
| Prazo opcional | **Mantém simples** (alinha ao conceito) | OK |
| Atraso = pendente + prazo vencido | **Simples** (uma condição clara) | OK |
| Atrasada não duplica em pendentes | **Aumenta clareza** (sem duplicidade) | OK |
| Progresso percentual | **Mais simples que marcos** | OK; marcos = futuro |
| Data-alvo opcional; horizonte qualitativo | **Evita dados artificiais** | OK |
| Meta ativa = progresso < 100% | **Dispensa campo de status** (progresso já indica) | OK |

**Conclusão da análise:** nenhuma regra introduz complexidade desnecessária. Não há regra a
simplificar — todas usam comparações diretas e mínimas, coerentes com o princípio "na dúvida,
a solução simples".

---

## 6. Edge Cases

| Caso | Comportamento esperado |
|---|---|
| **Evento sem horário** | Pertence ao dia inteiro; entra em "Eventos de Hoje" se `data = hoje`; sem posição de horário específica. |
| **Tarefa sem prazo** | Válida; permanece em "Tarefas Pendentes" até ser concluída; **nunca** entra em "Atrasadas". |
| **Meta sem data-alvo** | Válida; permanece ativa enquanto progresso < 100%; horizonte é apenas qualitativo. |
| **Meta com progresso 100%** | Torna-se **Concluída**; sai de "Metas Ativas". |
| **Evento no mesmo dia (hoje)** | Entra em "Eventos de Hoje"; **não** entra em "Próximos Eventos". |
| **Tarefa concluída após o prazo** | Ao concluir, deixa de ser pendente/atrasada e sai do dashboard. O MVP **não** registra "concluída com atraso" — conclusão é conclusão (simplicidade). *(Distinção fica como observação futura.)* |
| **Tarefa com `prazo = hoje`** | É **pendente** (não atrasada); entra em "Tarefas Pendentes". |
| **Evento passado** | Não aparece no dashboard; permanece acessível na tela de Eventos. |

---

## 7. Consistency Review

- **Conflitos entre conceitos:** nenhum. Evento (ocorrência datada), Tarefa (ação com
  conclusão) e Meta (objetivo com progresso) mantêm eixos distintos; as regras não os
  sobrepõem.
- **Ambiguidades restantes:** as que vinham das Tasks 1.1–1.5 foram resolvidas aqui — status de
  tarefa, regra de atraso, janela de "próximos", critério de "meta ativa" e forma de medir
  progresso. Restam apenas **decisões de produto reversíveis** (janela de 7 dias; percentual vs
  marcos), explicitamente registradas, não ambiguidades.
- **Regras redundantes:** evitadas por design — a separação Pendentes/Atrasadas impede que uma
  tarefa apareça em dois blocos.
- **Regras excessivamente complexas:** nenhuma (ver §5).

**Ajustes propostos:** nenhum necessário. As regras estão consistentes entre si e com os
artefatos anteriores.

---

## Conclusão

1. **Todas as ambiguidades anteriores foram resolvidas?**
   Sim. As ambiguidades funcionais sinalizadas nas Tasks 1.1–1.5 (status, atraso, "próximos",
   "meta ativa", progresso) estão definidas e justificadas.

2. **Existe alguma regra funcional ainda indefinida?**
   Não para o MVP. Permanecem apenas **decisões de produto reversíveis** (janela de 7 dias;
   percentual como forma de progresso), conscientes e documentadas, sujeitas a ajuste após uso.

3. **Existe alguma regra que deveria ser removida por excesso de complexidade?**
   Não. A análise de simplicidade (§5) não encontrou regra a remover ou simplificar.

4. **O domínio funcional do MVP pode ser considerado estabilizado?**
   **Sim.** Conceitos (Task 1.3) e regras (esta task) estão completos e consistentes para o
   escopo do MVP.

**Recomendação: Prosseguir para a Task 1.7.** O domínio funcional está estabilizado; os pontos
em aberto são escolhas de produto reversíveis, não bloqueios.

---

## Observações Futuras

- **OF (1.6-a).** Janela de "Próximos Eventos" (7 dias) pode tornar-se ajustável após uso real.
- **OF (1.6-b).** Progresso de Meta por **marcos** (alternativa ao percentual) pode ser avaliado
  pós-MVP.
- **OF (1.6-c).** Distinguir "tarefa concluída com atraso" (histórico de pontualidade) é
  evolução futura, fora do MVP.
- **OF (1.6-d).** Horizonte qualitativo de Meta (curto/médio/longo) poderia virar um atributo
  explícito no futuro, se o uso justificar.
