# Visão do Produto — SibylSystem

> Artefato da **Task 1.1 (Fase 1 — Definição do Produto)**.
> Fonte de verdade: [`CLAUDE.md`](../CLAUDE.md). Em caso de conflito, o CLAUDE.md prevalece.
> Escopo desta task: propósito, problema, usuário e valor. **Não** trata de arquitetura,
> tecnologia, banco de dados, telas, fluxos ou modelo de dados.

---

## 1. Product Vision

SibylSystem é uma plataforma pessoal de organização e acompanhamento de vida, destinada
inicialmente a um único usuário.

Seu propósito principal é **centralizar compromissos, tarefas e metas em um único lugar**,
oferecendo uma visão clara e organizada da vida pessoal para reduzir carga mental, aumentar
clareza e apoiar a tomada de decisões.

O sistema funciona como um painel pessoal de gestão da vida, permitindo que o usuário tenha
clareza sobre o que precisa fazer, o que está fazendo, o que pretende alcançar e como está
evoluindo ao longo do tempo.

---

## 2. Problem Statement

### Situação atual

O usuário gerencia compromissos, tarefas e objetivos de vida de forma dispersa — apoiado na
própria memória ou em múltiplas ferramentas desconexas (agenda, listas, anotações avulsas).
As informações relevantes para suas decisões ficam fragmentadas e sem uma visão unificada.

### Dificuldades encontradas

- Não há um lugar único que reúna **eventos** (o que ocorre em data específica), **tarefas**
  (o que precisa ser executado) e **metas** (o que se pretende alcançar).
- Falta visibilidade consolidada do "hoje" e do "próximo" — o que está pendente, o que está
  atrasado e o que está ativo.
- O acompanhamento de objetivos de curto, médio e longo prazo depende de esforço manual e
  memória, sem registro contínuo de progresso.
- A informação dispersa exige reconstrução mental constante do estado da vida.

### Consequências dessas dificuldades

- **Carga mental elevada**: o usuário precisa "segurar" mentalmente compromissos e pendências.
- **Perda de clareza e priorização**: dificuldade em distinguir o que realmente importa.
- **Risco de esquecimento**: tarefas sem prazo ou compromissos podem ser perdidos.
- **Acompanhamento frágil de metas**: objetivos de longo prazo avançam sem visibilidade,
  reduzindo a sensação de evolução e o apoio à decisão.

---

## 3. Target User

### Quem utilizará o sistema

Inicialmente, **um único usuário** — o próprio proprietário do sistema (uso pessoal). O
CLAUDE.md estabelece explicitamente usuário único e coloca multiusuário fora do escopo do MVP.

### Características

- Pessoa que lida simultaneamente com compromissos do dia a dia, tarefas práticas e objetivos
  de vida de diferentes horizontes (curto, médio e longo prazo).
- Valoriza simplicidade, rapidez de uso e baixa fricção.
- Busca clareza e redução de carga mental, não uma ferramenta sofisticada ou cheia de recursos.

### Necessidades

- Centralizar, em um só lugar, eventos, tarefas e metas.
- Enxergar rapidamente o que é relevante agora (hoje, próximos, pendentes, atrasados, ativos).
- Acompanhar a evolução dos próprios objetivos ao longo do tempo.
- Manter o esforço de manutenção do sistema baixo.

---

## 4. Value Proposition

O SibylSystem entrega **clareza com baixo esforço**: uma visão única e organizada da vida
pessoal que substitui a memória e as ferramentas dispersas por um ponto central de consulta
e decisão.

Por que usar o SibylSystem em vez de ferramentas dispersas ou da própria memória:

- **Centralização**: eventos, tarefas e metas convivem no mesmo lugar, eliminando a
  fragmentação entre múltiplas ferramentas.
- **Redução de carga cognitiva**: o sistema "lembra" pelo usuário, liberando atenção mental.
- **Visão consolidada**: um painel mostra o que importa agora (hoje, próximos, pendentes,
  atrasados, metas ativas), algo que ferramentas isoladas não oferecem de forma integrada.
- **Acompanhamento de longo prazo**: diferentemente de uma lista ou da memória, conecta o
  esforço cotidiano (tarefas e eventos) aos objetivos maiores (metas) e ao seu progresso.
- **Simplicidade e rapidez**: projetado para uso rápido e baixa manutenção, reduzindo a
  fricção que costuma levar ao abandono de ferramentas pessoais de organização.

---

## 5. Product Principles

Princípios derivados diretamente do CLAUDE.md, que devem orientar decisões futuras de produto:

1. **Simplicidade acima de sofisticação** — Na dúvida entre uma solução simples e uma
   sofisticada, escolher a simples. *Justificativa:* simplicidade sustenta baixa manutenção,
   rapidez de uso e longevidade do sistema pessoal.
2. **Clareza** — Cada informação apresentada deve aumentar o entendimento do usuário sobre sua
   própria vida. *Justificativa:* clareza é o valor central do produto; informação que não
   esclarece é ruído.
3. **Rapidez de uso** — O sistema deve ser ágil de operar no dia a dia. *Justificativa:*
   ferramentas pessoais lentas ou trabalhosas tendem a ser abandonadas.
4. **Baixa manutenção** — Minimizar o esforço para manter o sistema funcionando e atualizado.
   *Justificativa:* uso pessoal de um único usuário não comporta sobrecarga operacional.
5. **Evolução incremental** — Crescer de forma gradual e validada, uma etapa por vez.
   *Justificativa:* reduz risco, evita complexidade prematura e mantém o foco no essencial.
6. **Centralização das informações** — Reunir o que é relevante em um único ponto.
   *Justificativa:* a fragmentação é o problema central que o produto resolve.
7. **Redução de carga cognitiva** — Toda decisão deve aliviar a mente do usuário, não
   sobrecarregá-la. *Justificativa:* reduzir carga mental é o propósito declarado do produto.
8. **Foco no que importa** — Priorizar o essencial e ajudar o usuário a priorizar.
   *Justificativa:* o sistema existe para facilitar a priorização do que realmente importa.

---

## 6. MVP Success Criteria

Critérios objetivos e verificáveis que indicam que o MVP cumpriu seu propósito. Todos
derivam estritamente do escopo definido no CLAUDE.md.

**Capacidade funcional (verificável por uso):**

1. O usuário consegue **autenticar-se** (login e logout) como usuário único.
2. O usuário consegue **criar, editar, excluir e listar eventos**.
3. O usuário consegue **criar, editar, excluir, concluir e listar tarefas**.
4. O usuário consegue **criar, editar, excluir, atualizar progresso e listar metas**.
5. O **dashboard** apresenta, de forma consolidada: eventos de hoje, próximos eventos,
   tarefas pendentes, tarefas atrasadas e metas ativas.

**Critério de propósito (verificável por experiência de uso):**

6. A partir do dashboard, o usuário obtém em **uma única visão** a resposta para "o que preciso
   fazer, o que está pendente/atrasado e quais metas estão ativas", sem precisar consultar
   outras ferramentas.
7. O usuário consegue substituir o uso de ferramentas dispersas/memória para esses três
   conceitos (eventos, tarefas, metas) pelo SibylSystem.

> Observação: limiares quantitativos de sucesso (ex.: tempo de uso, frequência, satisfação)
> não estão definidos no CLAUDE.md. Ver §7 e a observação futura correspondente.

---

## 7. Risks and Assumptions

### Hipóteses assumidas (Assumptions)

- **H1.** Os três conceitos — Evento, Tarefa e Meta — são suficientes para representar o que o
  usuário precisa centralizar no MVP.
- **H2.** Um único usuário atende à necessidade real nesta fase (sem multiusuário).
- **H3.** Uma visão consolidada (dashboard) é o principal mecanismo de valor para reduzir carga
  mental.
- **H4.** Centralizar informação reduz, de fato, a carga cognitiva e melhora a priorização.
- **H5.** O usuário manterá o sistema atualizado manualmente — sem automações, notificações ou
  integrações externas — e ainda assim percebê-lo-á como útil.
- **H6.** Simplicidade e baixa manutenção são mais valiosas para este usuário do que riqueza de
  funcionalidades.

### Riscos de produto (nesta fase)

- **R1. Risco de adoção/hábito:** sem notificações ou integrações (explicitamente fora do
  escopo), o usuário pode esquecer de alimentar o sistema, esvaziando seu valor.
- **R2. Risco de definição:** conceitos com características ainda em aberto (ex.: status de
  tarefa, forma de medir progresso de meta, regra de "tarefa atrasada", janela de "próximos
  eventos") podem comprometer a clareza do dashboard se não forem definidos nas próximas tasks.
  *(Detalhamento pertence à Fase 1 — Regras Funcionais; não é objeto desta task.)*
- **R3. Risco de sucesso não mensurável:** o CLAUDE.md não define métricas quantitativas de
  sucesso; "redução de carga mental" e "clareza" são intrinsecamente subjetivos.
- **R4. Risco de escopo:** pressão por funcionalidades listadas em "Fora do Escopo" (IA, chat,
  integrações, multiusuário) pode desviar o foco da simplicidade que define o produto.
- **R5. Risco de valor sobre ferramentas existentes:** o usuário pode preferir manter
  ferramentas já consolidadas se o ganho de centralização não for percebido como significativo.

---

## Observações Futuras

Ideias surgidas durante a análise, **registradas para fases posteriores** (não fazem parte
desta task nem do escopo atual):

- **OF1.** Definir indicadores quantitativos de sucesso do MVP (ex.: frequência de uso,
  cobertura dos itens da vida no sistema) — pertinente à validação pós-MVP (Fase 5).
- **OF2.** As características em aberto dos conceitos (status de tarefa, progresso de meta,
  regra de atraso, janela de "próximos eventos", recorrência de eventos) devem ser tratadas
  nas tasks de **Regras Funcionais** da Fase 1.
- **OF3.** Recorrência de eventos é mencionada como possibilidade futura no CLAUDE.md; avaliar
  posicionamento (escopo futuro) sem antecipar implementação.

---

## Conclusão

A visão do produto está **clara e consistente** com o CLAUDE.md no nível exigido por esta task:
propósito, problema, usuário-alvo e proposta de valor estão bem definidos e alinhados à fonte
de verdade.

As ambiguidades identificadas (R2/OF2 — características em aberto dos conceitos e regras do
dashboard; R3/OF1 — ausência de métricas quantitativas) **não pertencem ao escopo da visão de
produto** e **não bloqueiam** o avanço. São insumos a serem resolvidos nas próximas tasks da
Fase 1 (Conceitos Centrais e Regras Funcionais).

**Recomendação:** a visão está suficientemente clara para **prosseguir para a Task 1.2**, desde
que as definições em aberto sejam tratadas no momento apropriado da Fase 1.
