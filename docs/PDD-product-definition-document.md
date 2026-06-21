# SibylSystem — Product Definition Document (PDD)

> **Documento de consolidação da Fase 1 (Definição do Produto).**
> Produzido na Task 1.8. Fontes: CLAUDE.md (fonte de verdade) e artefatos das Tasks 1.1–1.7.
> Em caso de conflito entre qualquer seção deste documento e o CLAUDE.md, o CLAUDE.md prevalece.
>
> **Propósito:** este documento representa a versão consolidada e oficial da Fase 1.
> Um novo colaborador deve conseguir compreender completamente o produto lendo apenas este
> documento, sem necessidade de consultar os artefatos individuais.
>
> **Restrições:** não cria funcionalidades, não altera decisões aprovadas, não altera escopo,
> conceitos ou regras funcionais. Não adiciona opiniões nem sugestões futuras.
> Consolida, organiza e verifica consistência.

---

## Parte 1 — Consistency Review

### Metodologia

Foram revisados: CLAUDE.md e os sete artefatos das Tasks 1.1 a 1.7. A revisão verificou
contradições, decisões duplicadas, regras conflitantes, definições inconsistentes e termos
com significados diferentes entre documentos.

### Resultado

**Nenhum conflito, contradição ou regra conflitante foi encontrado.**

Os documentos formam uma cadeia coerente onde cada task constrói sobre as anteriores sem
reescrever ou contrariar decisões já aprovadas.

### Checklist de consistência

| Item verificado | Resultado | Observação |
|---|---|---|
| Definição de Evento em 1.3 vs regras em 1.6 | Consistente | Regras operacionalizam o conceito sem contradizê-lo |
| Definição de Tarefa em 1.3 vs regras em 1.6 | Consistente | Status Pendente/Concluída é coerente com "execução e conclusão" |
| Definição de Meta em 1.3 vs regras em 1.6 | Consistente | Progresso percentual e data-alvo opcional derivam do conceito |
| Escopo (1.2) vs features no backlog (1.7) | Consistente | 16 features cobrem 100% do escopo, sem adição |
| Prioridade Should Have de editar/excluir em 1.2 vs 1.7 | Consistente | Classificação idêntica em ambos |
| Fluxos em 1.4 vs responsabilidades de telas em 1.5 | Consistente | Cada tela suporta os fluxos correspondentes |
| Dashboard blocos em 1.2 vs regras de bloco em 1.6 | Consistente | 1.6 especifica os critérios sem alterar os blocos de 1.2 |
| "Horizonte temporal" de Meta em CLAUDE.md vs 1.3 e 1.6 | Consistente | Interpretado como qualitativo; data-alvo opcional em 1.6 |
| Filosofia de uso em 1.4 vs estrutura de telas em 1.5 | Consistente | Dashboard como central nos dois documentos |
| "Informações relevantes" no CLAUDE.md vs escopo em 1.2 | Não conflita | 1.3 identificou a lacuna e decidiu não criar conceito; fora do MVP |
| Terminologia "Pendente/Concluída" ao longo da Fase 1 | Consistente | Uso uniforme de 1.3 a 1.7 |
| Terminologia "Ativa" para Meta ao longo da Fase 1 | Consistente | Formalizada em 1.6 como progresso < 100% |

### Observação sobre nomes de arquivo

A instrução da Task 1.8 referencia `05-screen-structure.md` e `07-initial-backlog.md`. Os
arquivos efetivamente produzidos são `05-screens.md` e `07-mvp-backlog.md`. O conteúdo é o
mesmo — a divergência é apenas nos nomes citados na instrução, não nos documentos.

---

## Parte 2 — Product Summary

### Nome do Produto

**SibylSystem**

### Missão

SibylSystem é um sistema pessoal de organização e apoio à tomada de decisões. Seu objetivo é
centralizar informações relevantes da vida do usuário para reduzir carga mental, aumentar
clareza e facilitar o acompanhamento de objetivos de curto, médio e longo prazo, através de
Planejamento, Execução, Acompanhamento e Reflexão.

### Problema Resolvido

O usuário gerencia compromissos, tarefas e objetivos de vida de forma dispersa — apoiado na
própria memória ou em múltiplas ferramentas desconexas. Isso gera:

- **Carga mental elevada**: o usuário precisa "segurar" mentalmente compromissos e pendências.
- **Perda de clareza e priorização**: dificuldade em distinguir o que realmente importa.
- **Risco de esquecimento**: tarefas e compromissos podem ser perdidos.
- **Acompanhamento frágil de metas**: objetivos de longo prazo avançam sem visibilidade.

### Público-Alvo

Inicialmente, **um único usuário** — o próprio proprietário do sistema (uso pessoal). Pessoa
que lida simultaneamente com compromissos do dia a dia, tarefas práticas e objetivos de vida
de diferentes horizontes; valoriza simplicidade, rapidez de uso e baixa fricção; busca clareza
e redução de carga mental.

### Proposta de Valor

**Clareza com baixo esforço**: uma visão única e organizada da vida pessoal que substitui a
memória e as ferramentas dispersas por um ponto central de consulta e decisão. O sistema
"lembra" pelo usuário, apresenta o que importa agora num único lugar e conecta o esforço
cotidiano aos objetivos de longo prazo.

### Princípios do Produto

| # | Princípio | Justificativa |
|---|---|---|
| 1 | **Simplicidade acima de sofisticação** | Na dúvida, a solução simples. Simplicidade sustenta manutenção e longevidade. |
| 2 | **Clareza** | Cada informação deve aumentar o entendimento do usuário. O que não esclarece é ruído. |
| 3 | **Rapidez de uso** | Ferramentas pessoais lentas ou trabalhosas tendem a ser abandonadas. |
| 4 | **Baixa manutenção** | Uso pessoal de usuário único não comporta sobrecarga operacional. |
| 5 | **Evolução incremental** | Crescer de forma gradual e validada; evitar complexidade prematura. |
| 6 | **Centralização das informações** | A fragmentação é o problema central que o produto resolve. |
| 7 | **Redução de carga cognitiva** | Toda decisão deve aliviar a mente do usuário, não sobrecarregá-la. |
| 8 | **Foco no que importa** | O sistema existe para facilitar a priorização do que realmente importa. |

---

## Parte 3 — MVP Definition

### Escopo do MVP

O MVP é a **menor versão capaz de centralizar eventos, tarefas e metas de um único usuário e
apresentá-los em uma visão consolidada (dashboard)**, composta por três blocos indispensáveis:

| Bloco | O que faz | Por que é indispensável |
|---|---|---|
| **Autenticação** | Protege o acesso ao espaço pessoal | Sem ela não há espaço pessoal protegido |
| **Gestão dos três conceitos** | Permite registrar e manter Eventos, Tarefas e Metas | Sem eles não há o que centralizar |
| **Dashboard** | Apresenta visão consolidada dos 5 blocos | Sem ele não há a clareza que é o motor de valor |

**Capacidades do MVP:**

1. Autenticar-se (login) e encerrar a sessão (logout) como usuário único.
2. Criar, listar, editar e excluir **Eventos**.
3. Criar, listar, editar, excluir e **concluir** **Tarefas**.
4. Criar, listar, editar, excluir e **atualizar o progresso** de **Metas**.
5. Consultar um **Dashboard** com: eventos de hoje, próximos eventos, tarefas pendentes,
   tarefas atrasadas e metas ativas.

### Fora do Escopo

| Item | Motivo |
|---|---|
| Multiusuário | MVP é de usuário único; complexidade sem necessidade atual |
| Compartilhamento | Depende de multiusuário |
| Aplicativo mobile | Amplia esforço e manutenção sem ser necessário ao valor central |
| IA | Sofisticação prematura; contraria simplicidade |
| Chat | Não resolve o problema central |
| Gamificação | Não essencial ao valor; adiciona complexidade |
| Integrações externas | Complexidade e manutenção altas |
| Sincronização com calendários externos | Integração externa desnecessária ao MVP |
| Notificações automáticas | O dashboard cobre a visibilidade |
| Integração com e-mail / WhatsApp | Integrações externas não essenciais |
| Recorrência de eventos | Citada como possibilidade futura no CLAUDE.md; não no MVP |
| Categorias/etiquetas/prioridade visual | Adicionam estrutura sem justificativa pelo problema |
| Relatórios/histórico/analytics | Sofisticação adiável |
| Busca/filtros avançados | "Listar" cobre a recuperação mínima |
| Anexos, notas livres ou campos ricos | Não previstos; ampliam escopo sem justificativa |
| Subtarefas / vínculo explícito Meta→Tarefa/Evento | Candidato futuro; evita complexidade prematura |

### Limites do MVP

**O usuário NÃO conseguirá:**
compartilhar dados; ter mais de um usuário; acessar por mobile; usar IA, chat ou gamificação;
integrar/sincronizar com qualquer serviço externo; receber notificações automáticas; configurar
eventos recorrentes; categorizar, etiquetar, filtrar avançadamente ou buscar itens; gerar
relatórios além do dashboard/progresso; vincular metas a tarefas/eventos; criar subtarefas.

### Critérios de Sucesso

**Capacidade funcional (verificável por uso):**

1. O usuário consegue autenticar-se e encerrar sessão como usuário único.
2. O usuário consegue criar, editar, excluir e listar eventos.
3. O usuário consegue criar, editar, excluir, concluir e listar tarefas.
4. O usuário consegue criar, editar, excluir, atualizar progresso e listar metas.
5. O dashboard apresenta, de forma consolidada, os 5 blocos: eventos de hoje, próximos
   eventos, tarefas pendentes, tarefas atrasadas e metas ativas.

**Critério de propósito (verificável por experiência de uso):**

6. A partir do dashboard, o usuário obtém em uma única visão a resposta para "o que preciso
   fazer, o que está pendente/atrasado e quais metas estão ativas", sem consultar outras
   ferramentas.
7. O usuário consegue substituir ferramentas dispersas/memória pelo SibylSystem para os três
   conceitos.

---

## Parte 4 — Domain Definition

### Evento

- **Definição:** algo que **ocorre** em uma data específica (podendo ter horário). É ancorado
  no tempo e existe independentemente de uma ação do usuário — acontece quando chega a data.
  Um evento não é "concluído": simplesmente ocorre, passa e fica no passado.
- **Propósito no sistema:** registrar compromissos e ocorrências datadas para que o usuário
  saiba o que acontece hoje e a seguir. Alimenta "Eventos de Hoje" e "Próximos Eventos" no
  dashboard.
- **Limites conceituais:**
  - *Não é* uma ação a executar com conclusão (isso é Tarefa).
  - *Não é* um objetivo de longo prazo (isso é Meta).
  - O horário é opcional; sem horário, o evento pertence ao dia inteiro.
  - Recorrência é funcionalidade futura; no MVP cada ocorrência é um evento distinto.

### Tarefa

- **Definição:** uma **ação que precisa ser executada** pelo usuário. Pode ter prazo ou não.
  Possui dois estados: Pendente e Concluída. Seu eixo central é a execução e a conclusão —
  uma tarefa não "acontece sozinha": exige ação deliberada.
- **Propósito no sistema:** registrar pendências para que nada essencial seja esquecido e para
  que o usuário acompanhe o que falta fazer. Alimenta "Tarefas Pendentes" e "Tarefas
  Atrasadas" no dashboard.
- **Limites conceituais:**
  - *Não é* uma ocorrência datada independente do usuário (isso é Evento).
  - *Não é* um objetivo amplo com horizonte e progresso (isso é Meta).
  - O prazo é opcional. Tarefa sem prazo nunca é considerada atrasada.
  - Apenas dois estados: Pendente (criada e não concluída) e Concluída (ação explícita do
    usuário). Não existem estados intermediários no MVP.

### Meta

- **Definição:** um **objetivo a ser alcançado**, com horizonte temporal (curto/médio/longo
  prazo) e noção de **progresso**. É um estado futuro desejado, geralmente alcançado por meio
  de múltiplas ações ao longo do tempo. O progresso é representado como percentual de 0% a
  100%.
- **Propósito no sistema:** dar visibilidade aos objetivos de vida e à evolução em direção a
  eles, conectando o esforço cotidiano ao que o usuário pretende alcançar. Alimenta "Metas
  Ativas" no dashboard.
- **Limites conceituais:**
  - *Não é* uma ação única e pontual (isso é Tarefa).
  - *Não é* uma ocorrência datada (isso é Evento).
  - A data-alvo é opcional; o horizonte temporal como natureza qualitativa está sempre
    presente.
  - Uma meta com progresso = 100% torna-se concluída e sai de "Metas Ativas". O progresso
    elimina a necessidade de um campo de estado separado.

### Relações entre os conceitos

- **Meta → Tarefas e Eventos (conceitual):** uma Meta é o "porquê" de longo prazo; Tarefas e
  Eventos são o "como" e o "quando" no cotidiano. Uma meta pode inspirar tarefas e eventos,
  mas **no MVP não há vínculo explícito implementado** — a relação é conceitual.
- **Tarefa ↔ Evento:** independentes entre si, complementares na linha do tempo do usuário.
- **Horizonte temporal compartilhado:** Evento marca *quando ocorre*, Tarefa marca *quando
  precisa estar feito* (se houver prazo), Meta marca *até quando se quer alcançar*.

### Guia de Classificação (árvore de decisão)

```
O que você quer registrar?
│
├─ É um objetivo amplo, que você quer ALCANÇAR ao longo do tempo,
│  e faz sentido acompanhar PROGRESSO?
│        └─ SIM ──────────────────────────────────────► META
│
├─ (não) É uma OCORRÊNCIA com data definida, que vai ACONTECER
│  naquele momento e não precisa ser "concluída"?
│        └─ SIM ──────────────────────────────────────► EVENTO
│
└─ (não) É uma AÇÃO que VOCÊ precisa EXECUTAR e marcar como
   concluída (com ou sem prazo)?
         └─ SIM ─────────────────────────────────────► TAREFA
```

**Perguntas de desempate:**
- "Acontece num momento ou precisa ser feito por mim?" → ocorrência = Evento; ação = Tarefa.
- "Resolvo com um esforço e marco como feito, ou avanço aos poucos até alcançar?" →
  conclusão única = Tarefa; progresso = Meta.
- "Tem data em que ocorre, ou horizonte até quando quero chegar lá?" → data de ocorrência =
  Evento; horizonte de objetivo = Meta.

---

## Parte 5 — Functional Rules

> Convenção: **"hoje"** é a data corrente do usuário. As regras usam comparação por **data**
> (dia), não por instante, salvo quando o horário existir e for relevante.
> Princípio comum ao dashboard: **nenhum item aparece em dois blocos** (evita ruído).

### Eventos

| Classificação temporal | Regra |
|---|---|
| Evento de hoje | `data = hoje` |
| Evento futuro | `data > hoje` |
| Evento passado | `data < hoje` |

- **Sem horário:** o evento pertence ao **dia inteiro**; sem posição específica na linha do
  tempo do dia.
- **Eventos passados:** não aparecem no dashboard; permanecem acessíveis na tela de Eventos.
- **Janela "Próximos Eventos":** eventos com `data` entre **amanhã** e **hoje + 7 dias**
  (inclusive). Decisão de produto reversível.
- **Limite de quantidade no dashboard:** nenhum artificial — a janela de 7 dias limita
  naturalmente.

### Tarefas

| Regra | Definição |
|---|---|
| **Status** | Dois: **Pendente** (padrão ao criar) e **Concluída** (por ação do usuário) |
| **Prazo** | Opcional. Tarefa sem prazo nunca é atrasada. |
| **Atrasada** | Pendente **e** possui prazo **e** `prazo < hoje` |
| **Pendente para hoje** | Pendente com `prazo = hoje` → é pendente, **não** atrasada |
| **Concluída** | Status alterado por ação explícita do usuário; sai de todos os blocos do dashboard |
| **Atrasada no dashboard** | Aparece **somente** em "Tarefas Atrasadas", não em "Tarefas Pendentes" |

### Metas

| Regra | Definição |
|---|---|
| **Progresso** | Percentual de **0% a 100%** (atualizado pelo usuário) |
| **Data-alvo** | Opcional. Meta pode existir sem prazo específico. |
| **Horizonte temporal** | Sempre presente como natureza qualitativa (curto/médio/longo prazo); não é campo obrigatório. |
| **Meta ativa** | Progresso < 100% |
| **Meta concluída** | Progresso = 100%; sai de "Metas Ativas" |

### Dashboard — Regras dos Blocos

| Bloco | Inclusão | Exclusão | Objetivo |
|---|---|---|---|
| **Eventos de Hoje** | `data = hoje` | Passados e futuros | Clareza imediata do dia |
| **Próximos Eventos** | `data` entre amanhã e hoje+7 | Hoje, passados, além de 7 dias | Antecipar a semana |
| **Tarefas Pendentes** | Pendentes sem atraso (sem prazo, ou `prazo ≥ hoje`) | Concluídas e atrasadas | O que falta fazer e ainda está no prazo |
| **Tarefas Atrasadas** | Pendentes com prazo e `prazo < hoje` | Concluídas, sem prazo, `prazo ≥ hoje` | Destacar o urgente; apoiar priorização |
| **Metas Ativas** | Progresso < 100% | Concluídas (100%) | Manter objetivos visíveis |

### Edge Cases

| Caso | Comportamento |
|---|---|
| Evento sem horário | Pertence ao dia inteiro; entra em "Eventos de Hoje" se `data = hoje` |
| Tarefa sem prazo | Válida; permanece em "Tarefas Pendentes" até ser concluída; nunca entra em "Atrasadas" |
| Meta sem data-alvo | Válida; permanece ativa enquanto progresso < 100% |
| Meta com progresso 100% | Torna-se concluída; sai de "Metas Ativas" |
| Evento no mesmo dia (hoje) | Entra em "Eventos de Hoje"; não entra em "Próximos Eventos" |
| Tarefa concluída após o prazo | Ao concluir, sai do dashboard; o MVP não registra "concluída com atraso" |
| Tarefa com `prazo = hoje` | É pendente (não atrasada); entra em "Tarefas Pendentes" |
| Evento passado | Fora do dashboard; acessível na tela de Eventos |

---

## Parte 6 — User Experience Model

### Jornada do Usuário

**Começo:** autenticação → carga inicial (tirar da memória eventos próximos, tarefas
pendentes e metas atuais). É o momento de maior volume de cadastro.

**Manutenção:** adicionar itens à medida que surgem, concluir tarefas ao realizá-las,
atualizar progresso de metas periodicamente. Incremental e de baixo volume.

**Valor diário:** consultar o dashboard como ponto de partida do dia e quantas vezes
necessário.

**Padrão ao longo do tempo:** alta alimentação inicial → manutenção leve contínua →
consulta frequente.

### Fluxos Principais

| ID | Fluxo | Gatilho | Resultado esperado | Frequência |
|---|---|---|---|---|
| F1 | **Login** | Quer usar o sistema | Sessão ativa; acesso ao dashboard | Ocasional |
| F2 | **Registrar Evento** | Surge compromisso com data | Evento disponível em hoje/próximos | Frequente/Ocasional |
| F3 | **Registrar Tarefa** | Surge uma pendência | Tarefa registrada como pendente | Frequente |
| F4 | **Concluir Tarefa** | Executou a ação | Tarefa concluída; sai do dashboard | Frequente |
| F5 | **Registrar Meta** | Define objetivo de curto/médio/longo prazo | Meta registrada como ativa | Raro |
| F6 | **Atualizar Progresso** | Houve avanço na meta | Progresso atualizado; evolução visível | Ocasional |
| F7 | **Consultar Dashboard** | Quer saber o que importa agora | Visão consolidada; priorização clara | Muito frequente |

> Fluxos de editar/excluir (Should Have) existem no escopo e são disponíveis como manutenção;
> não detalhados acima por não estarem na lista mínima de fluxos do produto.

**Implicação de frequência:** F7, F4 e F3 são os que mais exigem mínima fricção — são o
caminho quente do dia a dia.

### Filosofia de Uso

- **Predominantemente consultado, com alimentação leve e contínua.** O valor é colhido na
  consulta; a alimentação deve ser a menor possível.
- **Registrar apenas o essencial** — o que de fato precisa ser lembrado, executado ou
  acompanhado.
- **Reduzir o esforço de organização**, não aumentá-lo. O esforço de uso deve ser sempre
  menor do que o esforço mental que ele substitui.
- **Síntese:** *alimentar pouco e fácil, consultar muito e com clareza.*

### Estrutura de Navegação

```
Login
  └─► Dashboard (tela inicial após autenticação)
        ├─► Eventos  (criar / editar / excluir / listar)
        ├─► Tarefas  (criar / editar / excluir / concluir / listar)
        ├─► Metas    (criar / editar / excluir / atualizar progresso / listar)
        └─► (ações diretas sobre itens do dashboard, ex.: concluir tarefa)
Logout ◄── (acessível de forma persistente) ──► volta ao Login
```

**Filosofia de navegação:** rasa (tudo a um passo do dashboard), poucas telas bem definidas,
resolver rápido e navegar pouco.

### Estrutura de Telas

| Tela | Objetivo | Deve aparecer | NÃO deve aparecer | Classe |
|---|---|---|---|---|
| **Login** | Autenticar o usuário único | Entrada de credenciais + ação autenticar | Dados pessoais ou navegação do sistema | Administração |
| **Dashboard** | Visão consolidada do que importa agora | Os 5 blocos + acesso às telas de conceito | Formulários completos, listagens exaustivas, histórico | Essencial |
| **Eventos** | Ver e gerenciar eventos | Lista de eventos + ações criar/editar/excluir | Tarefas, metas, blocos do dashboard | Essencial |
| **Tarefas** | Ver e gerenciar/concluir tarefas | Lista de tarefas + ações criar/editar/excluir/concluir | Eventos, metas, blocos do dashboard | Essencial |
| **Metas** | Ver e gerenciar metas e progresso | Lista de metas + ações criar/editar/excluir/atualizar progresso | Eventos, tarefas, blocos do dashboard | Essencial |

> Criar/editar ocorre **dentro** da tela de cada conceito (não são telas autônomas).
> Logout é ação persistente, não tela. Não há tela de configurações no MVP.
> **Princípio anti-sobreposição:** dashboard agrega e resume; telas de conceito detalham e
> gerenciam um único conceito cada.

### Papel do Dashboard

O dashboard é **a experiência principal do produto** — não uma tela comum. É a tela inicial,
a mais frequente e onde se concentra o maior parte do valor de consulta. Sem ele, o produto
vira um conjunto de listas dispersas, que é exatamente o problema que a visão combate.
O usuário deve passar mais tempo no dashboard (consultando) do que nas telas de cadastro
(alimentando).

---

## Parte 7 — Product Backlog

### Épicos

| ID | Épico | Objetivo | Valor para o usuário |
|---|---|---|---|
| E1 | **Autenticação** | Proteger o acesso ao espaço pessoal | Informações acessíveis apenas pelo proprietário |
| E2 | **Gestão de Eventos** | Registrar e manter ocorrências datadas | Compromissos fora da memória; alimenta o dashboard |
| E3 | **Gestão de Tarefas** | Registrar pendências e sua conclusão | Nada esquecido; clareza do que falta e do que foi feito |
| E4 | **Gestão de Metas** | Registrar objetivos e acompanhar progresso | Objetivos visíveis e com evolução rastreável |
| E5 | **Dashboard** | Visão consolidada do que importa agora | Clareza imediata para priorizar e decidir |

### Features

| ID | Feature | Épico | Prioridade | Dependências |
|---|---|---|---|---|
| F1.1 | Login | E1 | **Must Have** | — |
| F1.2 | Logout | E1 | **Must Have** | F1.1 |
| F2.1 | Criar Evento | E2 | **Must Have** | F1.1 |
| F2.2 | Listar Eventos | E2 | **Must Have** | F2.1 |
| F2.3 | Editar Evento | E2 | **Should Have** | F2.2 |
| F2.4 | Excluir Evento | E2 | **Should Have** | F2.2 |
| F3.1 | Criar Tarefa | E3 | **Must Have** | F1.1 |
| F3.2 | Listar Tarefas | E3 | **Must Have** | F3.1 |
| F3.3 | Concluir Tarefa | E3 | **Must Have** | F3.2 |
| F3.4 | Editar Tarefa | E3 | **Should Have** | F3.2 |
| F3.5 | Excluir Tarefa | E3 | **Should Have** | F3.2 |
| F4.1 | Criar Meta | E4 | **Must Have** | F1.1 |
| F4.2 | Listar Metas | E4 | **Must Have** | F4.1 |
| F4.3 | Atualizar Progresso da Meta | E4 | **Must Have** | F4.2 |
| F4.4 | Editar Meta | E4 | **Should Have** | F4.2 |
| F4.5 | Excluir Meta | E4 | **Should Have** | F4.2 |
| F5.1 | Dashboard: Eventos de Hoje | E5 | **Must Have** | F2.1 |
| F5.2 | Dashboard: Próximos Eventos | E5 | **Must Have** | F2.1 |
| F5.3 | Dashboard: Tarefas Pendentes | E5 | **Must Have** | F3.1, F3.3 |
| F5.4 | Dashboard: Tarefas Atrasadas | E5 | **Must Have** | F3.1, F3.3 |
| F5.5 | Dashboard: Metas Ativas | E5 | **Must Have** | F4.1, F4.3 |

**Total:** 5 épicos · 16 features · 14 Must Have · 6 Should Have · 0 Could Have.

### Ordem de Construção

| Etapa | Conteúdo | Fundamento |
|---|---|---|
| 1 | Auth (F1.1, F1.2) | Pré-requisito absoluto de todo o restante |
| 2 | Tarefas Must Have (F3.1, F3.2, F3.3) | Fluxo mais frequente; valor imediato para o usuário |
| 3 | Dashboard parcial (F5.3, F5.4) | Primeiro ponto de validação real do produto |
| 4 | Eventos Must Have (F2.1, F2.2) | Segundo conceito mais frequente |
| 5 | Dashboard expandido (F5.1, F5.2) | Dashboard ganha visão do dia e da semana |
| 6 | Metas Must Have (F4.1, F4.2, F4.3) | Menor frequência de criação; entra após os demais |
| 7 | Dashboard completo (F5.5) | MVP Must Have finalizado; 5 blocos completos |
| 8 | Editar/Excluir tudo (F2.3, F2.4, F3.4, F3.5, F4.4, F4.5) | Should Have; confiabilidade de longo prazo |

### Estratégia de Releases

| Release | Conteúdo | Valor entregue |
|---|---|---|
| **R1 — Fundação Funcional** | Auth + Tarefas (criar/listar/concluir) + Dashboard (tarefas) | Pendências fora da memória; visão consolidada parcial |
| **R2 — Visão do Dia e da Semana** | Eventos (criar/listar) + Dashboard (eventos) | Compromissos registrados; dashboard com 4 de 5 blocos |
| **R3 — Visão Completa da Vida** | Metas (criar/listar/progresso) + Dashboard completo | 5 blocos; **MVP Must Have finalizado** |
| **R4 — Gestão Plena** | Editar/Excluir para todos os conceitos | Dados confiáveis; **MVP encerrado** |

---

## Parte 8 — Open Decisions

Decisões de produto **explicitamente classificadas como reversíveis** nos artefatos da Fase 1.
Não são ambiguidades — são escolhas feitas, documentadas e sujeitas a revisão após uso real.

| # | Decisão | Classificação | Origem |
|---|---|---|---|
| D1 | **Janela "Próximos Eventos" = 7 dias** — constante fixa que pode tornar-se ajustável após uso real | Reversível | Task 1.6 |
| D2 | **Progresso de Meta por percentual (0–100%)** — alternativa por marcos avaliável pós-MVP | Reversível | Task 1.6 |

Nenhuma outra decisão de produto permanece aberta ou pendente no escopo do MVP.

---

## Parte 9 — Fase 1 Closure Report

| Item | Status | Justificativa |
|---|---|---|
| **Escopo está definido?** | **Sim** | MVP com fronteiras objetivas e verificáveis (16 features, 5 épicos, lista completa de fora do escopo) |
| **Conceitos estão definidos?** | **Sim** | Evento, Tarefa e Meta com definição, propósito, limites e guia de classificação |
| **Fluxos estão definidos?** | **Sim** | 7 fluxos principais com objetivo, gatilho, passos e resultado; análise de frequência e fricção |
| **Telas estão definidas?** | **Sim** | 5 telas com objetivo, responsabilidades, navegação e papel do dashboard |
| **Regras funcionais estão definidas?** | **Sim** | Todas as ambiguidades identificadas nas Tasks 1.1–1.5 foram resolvidas na Task 1.6 |
| **Backlog está definido?** | **Sim** | 16 features priorizadas, com ordem de construção e estratégia de 4 releases |
| **Existem bloqueios para iniciar a Fase 2?** | **Não** | Conceitos, regras, telas e backlog estão completos; as únicas pendências são decisões reversíveis documentadas |

---

## Status da Fase 1

```
╔═══════════════════════════════════════╗
║   Status da Fase 1: APROVADA          ║
╚═══════════════════════════════════════╝
```

**Justificativa:**

Todos os entregáveis da Fase 1 (Definição do Produto) estão completos, consistentes entre si
e com o CLAUDE.md:

- A revisão de consistência não encontrou conflitos, contradições nem regras conflitantes.
- O domínio funcional está estabilizado: conceitos com limites claros, regras para todos os
  casos (incluindo edge cases), e backlog integral do MVP.
- As únicas decisões não fechadas são reversíveis por escolha explícita, não por omissão.
- Um novo colaborador pode compreender o produto integralmente a partir deste documento.

A Fase 2 (Arquitetura) pode ser iniciada com os seguintes insumos disponíveis:

1. Três conceitos de domínio com atributos e regras de negócio.
2. Cinco telas e estrutura de navegação.
3. 16 features com prioridade e dependências.
4. Estratégia de 4 releases com valor incremental.
5. Regras dos 5 blocos do dashboard com critérios precisos.

---

*Documento produzido na Task 1.8 — Consolidação da Fase 1.*
*Fase 1 concluída em: 2026-06-21.*
