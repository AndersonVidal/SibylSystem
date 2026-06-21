# Backlog Inicial do MVP — SibylSystem

> Artefato da **Task 1.7 (Fase 1 — Definição do Produto)**.
> Fontes: [`CLAUDE.md`](../CLAUDE.md) (fonte de verdade) e Tasks 1.1–1.6.
> Em caso de conflito, o CLAUDE.md prevalece.
> Escopo desta task: transformar as decisões da Fase 1 em backlog estruturado.
> **Não** trata de arquitetura, tecnologia, banco, implementação técnica, infraestrutura,
> testes automatizados, CI/CD ou deployment.
> O backlog representa **funcionalidades do produto**; usa exclusivamente funcionalidades
> aprovadas no escopo do MVP (Task 1.2).

---

## 1. Product Breakdown

### Épicos e Features

```
E1 — Autenticação
  F1.1  Login
  F1.2  Logout

E2 — Gestão de Eventos
  F2.1  Criar Evento
  F2.2  Listar Eventos
  F2.3  Editar Evento
  F2.4  Excluir Evento

E3 — Gestão de Tarefas
  F3.1  Criar Tarefa
  F3.2  Listar Tarefas
  F3.3  Concluir Tarefa
  F3.4  Editar Tarefa
  F3.5  Excluir Tarefa

E4 — Gestão de Metas
  F4.1  Criar Meta
  F4.2  Listar Metas
  F4.3  Atualizar Progresso da Meta
  F4.4  Editar Meta
  F4.5  Excluir Meta

E5 — Dashboard
  F5.1  Bloco: Eventos de Hoje
  F5.2  Bloco: Próximos Eventos
  F5.3  Bloco: Tarefas Pendentes
  F5.4  Bloco: Tarefas Atrasadas
  F5.5  Bloco: Metas Ativas
```

**Total:** 5 épicos · 16 features.

---

## 2. Epic Definition

### E1 — Autenticação

- **Objetivo:** proteger o acesso ao espaço pessoal do usuário único.
- **Valor para o usuário:** garantia de que as informações pessoais centralizadas são acessíveis
  apenas pelo proprietário.
- **Funcionalidades:** F1.1 Login, F1.2 Logout.

### E2 — Gestão de Eventos

- **Objetivo:** permitir ao usuário registrar e manter ocorrências datadas.
- **Valor para o usuário:** comprometer-se e acompanhar compromissos e ocorrências sem depender
  da memória; alimentar os blocos de eventos do dashboard.
- **Funcionalidades:** F2.1 Criar, F2.2 Listar, F2.3 Editar, F2.4 Excluir.

### E3 — Gestão de Tarefas

- **Objetivo:** permitir ao usuário registrar pendências e registrar sua conclusão.
- **Valor para o usuário:** nada essencial esquecido; clareza do que falta fazer e do que já foi
  feito; alimentar os blocos de tarefas do dashboard.
- **Funcionalidades:** F3.1 Criar, F3.2 Listar, F3.3 Concluir, F3.4 Editar, F3.5 Excluir.

### E4 — Gestão de Metas

- **Objetivo:** permitir ao usuário registrar objetivos e acompanhar seu progresso.
- **Valor para o usuário:** objetivos de curto/médio/longo prazo visíveis e com evolução
  rastreável; conecta o esforço cotidiano ao que se quer alcançar; alimenta o bloco de metas
  do dashboard.
- **Funcionalidades:** F4.1 Criar, F4.2 Listar, F4.3 Atualizar Progresso, F4.4 Editar,
  F4.5 Excluir.

### E5 — Dashboard

- **Objetivo:** apresentar uma visão consolidada do que importa agora, num único lugar.
- **Valor para o usuário:** clareza imediata para priorizar e decidir; é o motor de valor do
  produto (Task 1.4/1.5).
- **Funcionalidades:** F5.1–F5.5 (os cinco blocos definidos na Task 1.6).

---

## 3. Feature Breakdown

### E1 — Autenticação

| ID | Feature | Objetivo | Valor entregue | Dependências funcionais |
|---|---|---|---|---|
| F1.1 | **Login** | Autenticar o usuário e iniciar sessão | Acesso ao espaço pessoal | — (pré-requisito de tudo) |
| F1.2 | **Logout** | Encerrar a sessão | Controle de acesso | F1.1 |

### E2 — Gestão de Eventos

| ID | Feature | Objetivo | Valor entregue | Dependências funcionais |
|---|---|---|---|---|
| F2.1 | **Criar Evento** | Registrar ocorrência com data (e horário opcional) | Compromissos registrados, fora da memória | F1.1 |
| F2.2 | **Listar Eventos** | Ver todos os eventos registrados | Recuperação da informação; base para editar/excluir | F2.1 |
| F2.3 | **Editar Evento** | Corrigir ou atualizar dados de um evento | Dados confiáveis e atuais | F2.2 |
| F2.4 | **Excluir Evento** | Remover evento não mais relevante | Clareza; sem ruído | F2.2 |

### E3 — Gestão de Tarefas

| ID | Feature | Objetivo | Valor entregue | Dependências funcionais |
|---|---|---|---|---|
| F3.1 | **Criar Tarefa** | Registrar ação a executar (prazo opcional) | Pendência capturada, não perdida | F1.1 |
| F3.2 | **Listar Tarefas** | Ver tarefas e seus estados | Visão de pendências; base para concluir/editar/excluir | F3.1 |
| F3.3 | **Concluir Tarefa** | Marcar tarefa como realizada | Progresso visível; clareza do que resta | F3.2 |
| F3.4 | **Editar Tarefa** | Corrigir ou atualizar dados de uma tarefa | Dados confiáveis e atuais | F3.2 |
| F3.5 | **Excluir Tarefa** | Remover tarefa não mais relevante | Clareza; sem ruído | F3.2 |

### E4 — Gestão de Metas

| ID | Feature | Objetivo | Valor entregue | Dependências funcionais |
|---|---|---|---|---|
| F4.1 | **Criar Meta** | Registrar objetivo com horizonte (data-alvo opcional) | Objetivo explícito e acompanhável | F1.1 |
| F4.2 | **Listar Metas** | Ver metas e seu progresso | Visão dos objetivos; base para atualizar/editar/excluir | F4.1 |
| F4.3 | **Atualizar Progresso** | Registrar avanço (0–100%) em direção à meta | Evolução visível ao longo do tempo | F4.2 |
| F4.4 | **Editar Meta** | Corrigir ou atualizar dados de uma meta | Dados confiáveis e atuais | F4.2 |
| F4.5 | **Excluir Meta** | Remover meta não mais relevante | Clareza; sem ruído | F4.2 |

### E5 — Dashboard

> Cada bloco do dashboard depende funcionalmente de existirem dados dos conceitos correspondentes.
> Blocos sem dados exibem estado vazio — comportamento válido e esperado.

| ID | Feature | Objetivo | Valor entregue | Dependências funcionais |
|---|---|---|---|---|
| F5.1 | **Bloco: Eventos de Hoje** | Mostrar eventos com `data = hoje` | Clareza imediata do dia | F2.1 |
| F5.2 | **Bloco: Próximos Eventos** | Mostrar eventos nos próximos 7 dias | Antecipação da semana | F2.1 |
| F5.3 | **Bloco: Tarefas Pendentes** | Mostrar tarefas pendentes sem atraso | O que falta fazer (no prazo ou sem prazo) | F3.1, F3.3 |
| F5.4 | **Bloco: Tarefas Atrasadas** | Mostrar tarefas pendentes com prazo vencido | Destaque do urgente; apoio à priorização | F3.1, F3.3 |
| F5.5 | **Bloco: Metas Ativas** | Mostrar metas com progresso < 100% | Objetivos em andamento sempre visíveis | F4.1, F4.3 |

---

## 4. MVP Build Order

A ordem segue dois critérios: **dependências funcionais** (o que é pré-requisito de quê) e
**frequência de uso** (Task 1.4 — fluxos mais frequentes primeiro, para gerar valor mais cedo).

```
Etapa 1 — Autenticação
  F1.1 Login · F1.2 Logout
  Por quê primeiro: pré-requisito absoluto de todo o restante.

Etapa 2 — Gestão de Tarefas (Must Have)
  F3.1 Criar · F3.2 Listar · F3.3 Concluir
  Por quê: tarefas são o fluxo mais frequente (Task 1.4); o usuário já obtém valor imediato
  (pendências fora da memória) antes de qualquer outra funcionalidade.

Etapa 3 — Dashboard parcial (blocos de tarefas)
  F5.3 Tarefas Pendentes · F5.4 Tarefas Atrasadas
  Por quê: com tarefas existentes, os dois blocos de tarefas já entregam a visão consolidada
  parcial; o motor de valor (dashboard) entra cedo.

Etapa 4 — Gestão de Eventos (Must Have)
  F2.1 Criar · F2.2 Listar
  Por quê: segundo conceito mais frequente; alimenta os blocos de eventos do dashboard.

Etapa 5 — Dashboard expandido (blocos de eventos)
  F5.1 Eventos de Hoje · F5.2 Próximos Eventos
  Por quê: com eventos existentes, o dashboard ganha mais dois blocos; visão do dia e da semana.

Etapa 6 — Gestão de Metas (Must Have)
  F4.1 Criar · F4.2 Listar · F4.3 Atualizar Progresso
  Por quê: metas são o conceito de menor frequência de criação; entram após os dois mais
  frequentes.

Etapa 7 — Dashboard completo (bloco de metas)
  F5.5 Metas Ativas
  Por quê: com metas existentes, o dashboard atinge os 5 blocos completos. MVP funcionalmente
  completo nos Must Haves.

Etapa 8 — Gestão completa: Editar e Excluir
  F2.3/F2.4 (Eventos) · F3.4/F3.5 (Tarefas) · F4.4/F4.5 (Metas)
  Por quê: Should Have; necessários para manter os dados confiáveis. Entram após o núcleo
  funcional estar estabelecido.
```

**Qual sequência gera validação mais rápida?** A Etapa 3 (dashboard parcial com tarefas) é o
primeiro ponto de validação real do produto — o usuário já experimenta a centralização e a visão
consolidada, mesmo que com apenas um conceito. Cada etapa subsequente expande o dashboard e
enriquece o valor.

---

## 5. Release Strategy

Cada release entrega um produto **funcionalmente utilizável** — não um incremento invisível.

---

### Release 1 — Fundação Funcional

**Conteúdo:** E1 completo + E3 Must Have + Dashboard parcial (blocos de tarefas)

| Feature | Código |
|---|---|
| Login | F1.1 |
| Logout | F1.2 |
| Criar Tarefa | F3.1 |
| Listar Tarefas | F3.2 |
| Concluir Tarefa | F3.3 |
| Dashboard: Tarefas Pendentes | F5.3 |
| Dashboard: Tarefas Atrasadas | F5.4 |

**Valor entregue:** o usuário já pode usar o sistema como ferramenta de gestão de tarefas e
ver no dashboard o que está pendente e o que está atrasado. O principal fluxo (criar/concluir
tarefas + consultar dashboard) está disponível.

---

### Release 2 — Visão do Dia e da Semana

**Conteúdo:** E2 Must Have + Dashboard blocos de eventos

| Feature | Código |
|---|---|
| Criar Evento | F2.1 |
| Listar Eventos | F2.2 |
| Dashboard: Eventos de Hoje | F5.1 |
| Dashboard: Próximos Eventos | F5.2 |

**Valor entregue:** compromissos datados entram no sistema; o dashboard agora mostra também o
que ocorre hoje e nos próximos 7 dias. O usuário tem visão de tarefas **e** eventos num único
lugar.

---

### Release 3 — Visão Completa da Vida

**Conteúdo:** E4 Must Have + Dashboard completo

| Feature | Código |
|---|---|
| Criar Meta | F4.1 |
| Listar Metas | F4.2 |
| Atualizar Progresso da Meta | F4.3 |
| Dashboard: Metas Ativas | F5.5 |

**Valor entregue:** objetivos de curto/médio/longo prazo entram no sistema; o dashboard atinge
os 5 blocos completos. O produto entrega a visão consolidada total — propósito da visão do
produto. **MVP funcionalmente completo (Must Haves).**

---

### Release 4 — Gestão Plena

**Conteúdo:** Editar e Excluir para todos os conceitos

| Feature | Código |
|---|---|
| Editar Evento | F2.3 |
| Excluir Evento | F2.4 |
| Editar Tarefa | F3.4 |
| Excluir Tarefa | F3.5 |
| Editar Meta | F4.4 |
| Excluir Meta | F4.5 |

**Valor entregue:** o usuário pode corrigir e limpar seus dados; o sistema torna-se confiável
para uso de longo prazo. Completa todos os Should Haves e encerra o MVP.

---

## 6. Backlog Prioritization

| ID | Feature | Prioridade | Justificativa |
|---|---|---|---|
| F1.1 | Login | **Must Have** | Pré-requisito absoluto |
| F1.2 | Logout | **Must Have** | Controle de acesso; par do login |
| F2.1 | Criar Evento | **Must Have** | Core do conceito Evento; alimenta dashboard |
| F2.2 | Listar Eventos | **Must Have** | Recuperação da informação; base das demais ações |
| F2.3 | Editar Evento | **Should Have** | Mantém dados confiáveis; não é pré-requisito do valor central |
| F2.4 | Excluir Evento | **Should Have** | Clareza e manutenção; não é pré-requisito do valor central |
| F3.1 | Criar Tarefa | **Must Have** | Fluxo mais frequente (Task 1.4); core do conceito Tarefa |
| F3.2 | Listar Tarefas | **Must Have** | Recuperação; base de concluir/editar/excluir |
| F3.3 | Concluir Tarefa | **Must Have** | Eixo central da Tarefa; alimenta dashboard |
| F3.4 | Editar Tarefa | **Should Have** | Dados confiáveis; não é pré-requisito do valor central |
| F3.5 | Excluir Tarefa | **Should Have** | Clareza; não é pré-requisito do valor central |
| F4.1 | Criar Meta | **Must Have** | Core do conceito Meta; alimenta dashboard |
| F4.2 | Listar Metas | **Must Have** | Recuperação; base das demais ações |
| F4.3 | Atualizar Progresso | **Must Have** | Eixo central da Meta (acompanhamento) |
| F4.4 | Editar Meta | **Should Have** | Dados confiáveis; não é pré-requisito do valor central |
| F4.5 | Excluir Meta | **Should Have** | Clareza; não é pré-requisito do valor central |
| F5.1 | Dashboard: Eventos de Hoje | **Must Have** | Clareza imediata do dia; propósito central |
| F5.2 | Dashboard: Próximos Eventos | **Must Have** | Antecipação da semana; bloco de decisão |
| F5.3 | Dashboard: Tarefas Pendentes | **Must Have** | O que falta fazer; bloco de decisão central |
| F5.4 | Dashboard: Tarefas Atrasadas | **Must Have** | Priorização do urgente; bloco de decisão central |
| F5.5 | Dashboard: Metas Ativas | **Must Have** | Objetivos visíveis; completa os 5 blocos |

**Resumo:** 14 Must Have · 6 Should Have · 0 Could Have no escopo do MVP.
*(Não há Could Have: o MVP já está no mínimo necessário. Tudo que não entra é Fora do Escopo.)*

---

## 7. MVP Completeness Review

**Todas as funcionalidades do MVP estão representadas?**
Sim. Confrontando com o escopo da Task 1.2:

| Escopo Task 1.2 | Feature(s) no backlog |
|---|---|
| Login / Logout | F1.1, F1.2 ✓ |
| Criar/Editar/Excluir/Listar Eventos | F2.1–F2.4 ✓ |
| Criar/Editar/Excluir/Concluir/Listar Tarefas | F3.1–F3.5 ✓ |
| Criar/Editar/Excluir/Atualizar progresso/Listar Metas | F4.1–F4.5 ✓ |
| Dashboard: 5 blocos | F5.1–F5.5 ✓ |

**Existe funcionalidade redundante?** Não. Cada feature tem responsabilidade única; nenhum par
de features faz a mesma coisa.

**Existe funcionalidade faltando?** Não. Todos os blocos do dashboard e todas as operações dos
três conceitos estão representados.

**Existe algo que deveria ser removido?** Não. As 16 features rastreiam-se ao escopo da Task
1.2 e ao valor definido na Task 1.1; nenhuma foi criada além do aprovado.

---

## Conclusão

1. **O backlog representa integralmente o MVP da Task 1.2?**
   Sim. As 16 features cobrem as 5 áreas do escopo (autenticação, eventos, tarefas, metas,
   dashboard) sem omissão nem adição.

2. **Existe alguma inconsistência com decisões anteriores?**
   Não. O backlog é derivado diretamente das Tasks 1.1–1.6: conceitos (1.3), fluxos (1.4),
   telas (1.5) e regras funcionais (1.6) estão refletidos nas features e em suas dependências.

3. **O backlog está pronto para servir de entrada da Fase 2 (Arquitetura)?**
   Sim. A Fase 2 tem como insumos: os três conceitos com seus atributos e regras, os cinco
   blocos do dashboard com seus critérios, as cinco telas e sua navegação, e as 16 features com
   ordem de construção e prioridades. Todos disponíveis.

4. **Existe alguma decisão de produto ainda pendente?**
   Apenas as **decisões de produto reversíveis** registradas na Task 1.6 (janela de 7 dias para
   "Próximos Eventos"; progresso por percentual). São escolhas feitas e documentadas, não
   pendências — revisáveis após uso real, conforme previsto.

**Recomendação: Prosseguir para a Task 1.8** (ou para a Fase 2, caso a Task 1.8 seja a revisão
final da Fase 1). O backlog está completo, consistente e pronto como entrada da Fase 2.

---

## Observações Futuras

- **OF (1.7-a).** O Release 4 (editar/excluir) pode ser antecipado para o Release 1 ou 2 se o
  uso real mostrar que a ausência de edição gera atrito significativo logo de início.
- **OF (1.7-b).** As decisões reversíveis (janela 7 dias, progresso percentual) podem ser
  revisadas entre releases, sem impacto na estrutura do backlog.
- **OF (1.7-c).** Pós-MVP, os candidatos futuros listados na Task 1.2 (recorrência, vínculo
  Meta→Tarefa/Evento, notas, notificações etc.) poderão entrar como novos épicos e features em
  backlog de Fase 5.
