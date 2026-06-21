# Fluxos do Usuário — SibylSystem

> Artefato da **Task 1.4 (Fase 1 — Definição do Produto)**.
> Fontes: [`CLAUDE.md`](../CLAUDE.md) (fonte de verdade), [`01-product-vision.md`](./01-product-vision.md), [`02-mvp-scope.md`](./02-mvp-scope.md), [`03-core-concepts.md`](./03-core-concepts.md).
> Em caso de conflito, o CLAUDE.md prevalece.
> Escopo desta task: como o usuário interage com o sistema no dia a dia.
> **Não** trata de arquitetura, tecnologia, banco, telas, componentes visuais, modelo de dados.
> **Não** cria funcionalidades, não altera escopo, não redefine conceitos.
> Os fluxos usam **exclusivamente** funcionalidades já aprovadas na Task 1.2.

---

## 1. User Journey

### Como o usuário começa a utilizar o sistema

O usuário **autentica-se** (login) em seu espaço pessoal único. No início, faz uma **carga
inicial** do que já tem na cabeça ou disperso: registra eventos próximos (compromissos),
tarefas pendentes e suas metas atuais. Esse é o momento de maior volume de cadastro — equivale
a "tirar da memória" e colocar no sistema.

### Como ele mantém o sistema atualizado

No cotidiano, o usuário **adiciona itens à medida que surgem** (um novo compromisso, uma nova
pendência), **conclui tarefas** quando as realiza e **atualiza o progresso das metas**
periodicamente. A manutenção é incremental e de baixo volume — pequenos toques, não grandes
sessões de cadastro.

### Como ele obtém valor no dia a dia

O usuário **consulta o dashboard** como ponto de partida do dia (e quantas vezes precisar) para
ver: o que ocorre hoje, o que vem a seguir, o que está pendente, o que está atrasado e quais
metas estão ativas. O valor central — clareza com baixo esforço — vem principalmente da
**consulta**, sustentada por uma **alimentação leve e contínua**.

> Padrão ao longo do tempo: **alta alimentação no início → manutenção leve contínua → consulta
> frequente.** A sustentabilidade depende de o esforço de alimentação permanecer baixo (ver §6 e §7).

---

## 2. Core User Flows

### Fluxo 1 — Login

- **Objetivo:** acessar o espaço pessoal de forma autenticada.
- **Gatilho:** o usuário quer usar o sistema.
- **Passos principais:** informar credenciais → autenticar → acessar o sistema (dashboard como
  ponto de entrada natural).
- **Resultado esperado:** sessão ativa, usuário dentro do seu espaço pessoal.

### Fluxo 2 — Registrar Evento

- **Objetivo:** registrar uma ocorrência datada.
- **Gatilho:** surge um compromisso/ocorrência com data (e talvez horário).
- **Passos principais:** acionar "criar evento" → informar os dados do evento (incl. data e,
  se houver, horário) → salvar.
- **Resultado esperado:** evento registrado e disponível para listagem e para o dashboard
  (hoje/próximos).

### Fluxo 3 — Registrar Tarefa

- **Objetivo:** registrar uma ação a executar.
- **Gatilho:** surge uma pendência.
- **Passos principais:** acionar "criar tarefa" → informar os dados da tarefa (com ou sem
  prazo) → salvar.
- **Resultado esperado:** tarefa registrada como pendente, disponível para listagem e dashboard
  (pendentes/atrasadas).

### Fluxo 4 — Concluir Tarefa

- **Objetivo:** marcar uma pendência como realizada.
- **Gatilho:** o usuário executou a ação.
- **Passos principais:** localizar a tarefa (na listagem/dashboard) → acionar "concluir".
- **Resultado esperado:** tarefa passa a concluída; sai de "pendentes/atrasadas".

### Fluxo 5 — Registrar Meta

- **Objetivo:** registrar um objetivo a alcançar.
- **Gatilho:** o usuário define um objetivo de curto/médio/longo prazo.
- **Passos principais:** acionar "criar meta" → informar os dados da meta (incl. horizonte
  temporal) → salvar.
- **Resultado esperado:** meta registrada como ativa, disponível para listagem e dashboard
  (metas ativas).

### Fluxo 6 — Atualizar Progresso da Meta

- **Objetivo:** refletir o avanço em direção ao objetivo.
- **Gatilho:** houve progresso percebido na meta.
- **Passos principais:** localizar a meta → acionar "atualizar progresso" → registrar o novo
  progresso → salvar.
- **Resultado esperado:** progresso atualizado; evolução visível ao longo do tempo.

### Fluxo 7 — Consultar Dashboard

- **Objetivo:** obter, numa única visão, clareza sobre o que importa agora.
- **Gatilho:** o usuário quer saber o que fazer / o estado da sua vida no momento.
- **Passos principais:** acessar o dashboard → ler os cinco blocos (eventos de hoje, próximos
  eventos, tarefas pendentes, tarefas atrasadas, metas ativas).
- **Resultado esperado:** usuário com visão consolidada, apto a priorizar e decidir.

---

## 3. Daily Usage Scenarios

| Exemplo | Conceito | Fluxos percorridos | Como passa pelo sistema |
|---|---|---|---|
| **Comprar guarda-roupa** | Tarefa | F3 → (F7) → F4 | Registra como tarefa (talvez com prazo); aparece em "pendentes"; ao comprar, conclui (F4). |
| **Consulta médica** | Evento | F2 → F7 | Registra como evento com data/horário; aparece em "eventos de hoje"/"próximos" no dia certo. |
| **Natação** | Evento | F2 → F7 | Cada sessão é um evento datado; aparece no dashboard do dia. *(Recorrência é futura — no MVP registra-se cada ocorrência.)* |
| **Comprar apartamento** | Meta | F5 → F6 → F7 | Registra como meta de longo prazo; atualiza progresso periodicamente; acompanha em "metas ativas". |
| **Concluir pós-graduação** | Meta | F5 → F6 → F7 | Meta de horizonte longo; progresso atualizado a cada avanço; eventos-marco (ex.: defesa) podem ser registrados via F2. |
| **Projeto RAIRE** | Meta | F5 → F6 → F7 (+ F3/F2) | Meta ampla; progresso atualizado ao longo do tempo; pode inspirar tarefas (F3) e eventos (F2), conceitualmente, sem vínculo explícito no MVP. |

> Todos os cenários usam apenas conceitos e fluxos aprovados; nenhum exige funcionalidade fora
> do escopo.

---

## 4. User Goals Mapping

| Fluxo | Objetivo do usuário | Problema da Task 1.1 que resolve | Valor entregue |
|---|---|---|---|
| F1 Login | Acessar seu espaço pessoal protegido | Informação pessoal dispersa/desprotegida | Espaço pessoal seguro |
| F2 Registrar Evento | Não esquecer compromissos datados | Compromissos na memória / dispersos | Compromissos recuperáveis e visíveis no tempo |
| F3 Registrar Tarefa | Capturar pendências | Pendências esquecidas/fragmentadas | Pendências sob controle |
| F4 Concluir Tarefa | Marcar o que foi feito | Falta de distinção feito × pendente | Sensação de progresso; clareza do que resta |
| F5 Registrar Meta | Tornar objetivos explícitos | Objetivos sem registro nem visibilidade | Objetivos acompanháveis |
| F6 Atualizar Progresso | Acompanhar evolução | Evolução de longo prazo invisível | Percepção de avanço; apoio à decisão |
| F7 Consultar Dashboard | Saber o que importa agora | Falta de visão consolidada | Clareza imediata; priorização |

**Verificação:** todos os fluxos rastreiam a um objetivo do usuário, a um problema da Task 1.1
e a um valor. Nenhum fluxo ficou sem valor claro — nada a questionar.

---

## 5. Frequency Analysis

| Fluxo | Frequência | Justificativa |
|---|---|---|
| **F7 Consultar Dashboard** | **Muito frequente** | É o principal mecanismo de valor; consultado uma ou várias vezes ao dia. |
| **F4 Concluir Tarefa** | **Frequente** | Tarefas são concluídas ao longo da rotina; ação rápida e recorrente. |
| **F3 Registrar Tarefa** | **Frequente** | Pendências surgem com regularidade no dia a dia. |
| **F2 Registrar Evento** | **Frequente / Ocasional** | Novos compromissos surgem com alguma regularidade, mas menos que tarefas. |
| **F1 Login** | **Ocasional** | Depende da sessão; não a cada interação de conteúdo. |
| **F6 Atualizar Progresso** | **Ocasional** | Metas avançam em ritmo mais lento; atualização periódica. |
| **F5 Registrar Meta** | **Raro** | Metas são poucas e duradouras; criadas esporadicamente. |

**Conclusão de design (conceitual):** os fluxos **F7 (consultar), F4 (concluir) e F3
(registrar tarefa)** são os que mais merecem **mínima fricção**, por serem os mais repetidos no
cotidiano. Registro de meta e atualização de progresso toleram um pouco mais de esforço por
serem raros/ocasionais.

---

## 6. Friction Analysis

| Atrito | Causa | Impacto | Mitigação conceitual |
|---|---|---|---|
| **Cadastro excessivo** | Pedir muitos dados ao registrar evento/tarefa/meta | Desistência de registrar; sistema incompleto | Manter o registro com o mínimo essencial; dados opcionais permanecem opcionais (prazo de tarefa, horário de evento). |
| **Atualização manual** | Tudo depende de o usuário alimentar (sem automações/integrações, fora do escopo) | Dados desatualizados; perda de confiança | Tornar concluir/atualizar ações de baixíssimo esforço; pedir só o necessário. |
| **Falta de clareza** | Dúvida sobre classificar como Evento/Tarefa/Meta | Hesitação; registros inconsistentes | Apoiar-se no guia de decisão da Task 1.3; fronteiras conceituais claras. |
| **Esquecimento de uso** | Sem notificações (fora do escopo), o usuário pode não voltar | Sistema esvazia; valor cai (risco R1 da Task 1.1) | Tornar o dashboard a porta de entrada e fonte de valor imediato, incentivando o hábito de consulta. |
| **Sobrecarga de informações** | Dashboard com itens demais ou listas longas | Ruído; perda da clareza que é o propósito | Manter o dashboard nos cinco blocos definidos; priorizar o que importa agora; evitar enriquecer além do escopo. |

> Nenhuma mitigação acima entra em implementação — são orientações conceituais para as próximas
> fases.

---

## 7. Product Usage Philosophy

**O sistema deve ser consultado ou alimentado constantemente?**
**Predominantemente consultado, com alimentação leve e contínua.** O valor (clareza) é colhido
na consulta ao dashboard; a alimentação existe para sustentar essa consulta e deve ser a menor
possível. Não é um sistema que exige "trabalho de manutenção" pesado.
*Justificativa:* a visão prioriza reduzir carga mental; um sistema que exige muita alimentação
aumentaria a carga em vez de reduzi-la.

**O usuário deve registrar tudo ou apenas o essencial?**
**Apenas o essencial.** Deve registrar o que de fato precisa lembrar, executar ou acompanhar —
não transformar o sistema num repositório de tudo.
*Justificativa:* princípios de simplicidade, foco no que importa e baixa carga cognitiva;
registrar tudo geraria ruído e sobrecarga (atrito da §6).

**O sistema deve reduzir ou aumentar o esforço de organização?**
**Reduzir.** O SibylSystem existe para diminuir o esforço de manter a vida organizada,
centralizando e dando clareza.
*Justificativa:* é o propósito declarado na Task 1.1; qualquer fluxo que aumente o esforço de
organização contraria a visão e deve ser revisto.

**Síntese da filosofia de uso:** *alimentar pouco e fácil, consultar muito e com clareza.* O
esforço de uso deve ser sempre menor do que o esforço mental que ele substitui.

---

## Conclusão

1. **Os fluxos estão coerentes com a visão do produto?**
   Sim. Os sete fluxos cobrem exatamente as funcionalidades aprovadas e convergem para o valor
   central (clareza com baixo esforço), com o dashboard como motor.

2. **Existe algum fluxo desnecessário?**
   Não. Todos rastreiam a um objetivo do usuário, a um problema da Task 1.1 e a um valor (§4).
   Editar/Excluir (Should Have da Task 1.2) são fluxos de manutenção implícitos, não listados
   como "mínimos" aqui, mas permanecem no escopo e não conflitam.

3. **Existe algum fluxo essencial ausente?**
   Nenhum essencial. Os fluxos de **editar** e **excluir** (eventos, tarefas, metas) existem no
   escopo e são fluxos de correção/manutenção; não foram detalhados por não estarem na lista
   mínima pedida, mas devem ser considerados disponíveis. *(Observação, não lacuna.)*

4. **O uso diário parece sustentável para um usuário único?**
   Sim, **desde que** a alimentação permaneça de baixo esforço e o dashboard entregue valor
   imediato. O principal risco à sustentabilidade é o esquecimento de uso (R1), mitigável
   conceitualmente tornando a consulta a fonte de valor e o registro leve.

**Recomendação: Prosseguir para a Task 1.5.** Os fluxos são coerentes, suficientes e
sustentáveis; os pontos em aberto são de regras funcionais e de hábito de uso, a tratar adiante.

---

## Observações Futuras

- **OF (1.4-a).** Fluxos de **editar/excluir** (Should Have) podem ser formalizados quando as
  regras funcionais forem definidas — sem ampliar escopo.
- **OF (1.4-b).** O risco de esquecimento de uso (R1) reabre, no futuro, a discussão sobre
  lembretes/notificações — explicitamente fora do MVP.
- **OF (1.4-c).** Recorrência de eventos reduziria a fricção de registrar ocorrências repetidas
  (ex.: natação) — evolução futura.
