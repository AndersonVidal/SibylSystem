# SibylSystem — Retrospectiva Arquitetural (Pós TE-2 + Dashboard Parte 1)

> **Documento produzido após a conclusão das Tasks T0.1–T5.2.**
> Fontes: PDD, CLAUDE.md (fonte de verdade), Tasks 2.1–2.7 e implementação T0.1–T5.2.
> Em caso de conflito, o CLAUDE.md prevalece.
>
> **Propósito:** validar criticamente a direção arquitetural ao final do primeiro domínio
> completo (Tarefas + Dashboard parcial), antes de iniciar o módulo de Eventos (TE-3).
>
> **Restrições:** documento de análise pura — sem implementação de código, sem modificação
> de arquivos, sem criação de tasks. Objetivo: validar ou corrigir a direção antes de
> replicar o padrão para Eventos e Metas.

---

## Contexto

Até este momento o projeto possui:

- **Fundação** (TE-0): scaffolding Django, layout base, navegação, htmx, qualidade (Ruff/Black/pre-commit)
- **Autenticação** (TE-1): login, logout, proteção de rotas, `AbstractUser`
- **Tarefas** (TE-2): modelo, QuerySet, formulário, criar, listar, concluir, regras de atraso
- **Dashboard parcial** (T5.1–T5.2): blocos "Tarefas Atrasadas" e "Tarefas Pendentes"

---

## Parte 1 — Arquitetura

### Separação de responsabilidades

O mapeamento entre módulos e responsabilidades está correto e fiel à Task 2.1:

- `apps/accounts/` — autenticação; sem conhecimento de nenhum conceito de negócio
- `apps/tasks/` — modelo, QuerySet, formulário e views de Tarefa; regras de status, atraso e ordenação residem aqui
- `apps/dashboard/` — consumidor puro; importa `Task` do domínio e chama métodos já implementados; não implementa regras

### Fronteiras entre módulos

Nenhum módulo atravessa a fronteira de outro. O Dashboard importa `apps.tasks.models.Task` — correto e esperado. Tarefas não conhece o Dashboard. Não há import circular.

### Acoplamento

O acoplamento Dashboard→Tasks é unidirecional e inerente ao propósito do Painel. Está controlado porque o Dashboard apenas chama métodos do QuerySet — não reimplementa regras, não filtra diretamente por campos raw.

### Coesão

`apps/tasks/` é altamente coeso: tudo que pertence ao conceito Tarefa está em um único lugar. O `TaskQuerySet` e o `@property is_overdue` são complementares e não duplicados (ver Parte 3).

### Reutilização

O botão "Concluir" no Dashboard posta para `tasks:complete`. O domínio não foi reimplementado. A regra de conclusão tem um único dono.

### Diagnóstico

| Questão | Resposta |
|---|---|
| Algum módulo assumindo responsabilidade de outro? | **Não** |
| Duplicação de regras? | **Não** — `overdue()` e `is_overdue` coexistem com propósitos complementares |
| Alguma camada crescendo além do esperado? | **Não** — Dashboard com dois blocos está simples; crescimento até cinco blocos é suportado |

---

## Parte 2 — Fluxo de Dados

### Fluxo de escrita — criar tarefa

```
POST /tasks/ → index → TaskForm.is_valid() → task.owner = request.user; task.save() → redirect("tasks:index")
```

Correto. O formulário valida, a view atribui `owner`, o modelo persiste.

### Fluxo de escrita — concluir tarefa

```
POST /tasks/<pk>/complete/ → complete → get_object_or_404(Task, pk=pk, owner=request.user) → task.status = COMPLETED → redirect("tasks:index")
```

Correto. O `owner=request.user` no `get_object_or_404` garante isolamento de dados.

### Fluxo de leitura — dashboard

```
GET / → index → Task.objects.filter(owner=request.user).overdue() + pending_not_overdue() → template
```

Correto. Sem etapas desnecessárias. A view não contém lógica de negócio.

### Inconsistência observada — redirect após `complete`

O `tasks:complete` sempre redireciona para `tasks:index`. Quando chamado a partir do Dashboard, o usuário é enviado para a página de Tarefas, não de volta ao Dashboard. A UX planejada (Task 2.4 §2, §3) descreve "ações diretas sobre itens do dashboard" como ocorrendo sem sair da tela.

Isso não quebra nada funcionalmente, mas é uma divergência entre o comportamento implementado e a intenção original. O htmx foi designado para resolver exatamente este caso (Task 2.5 §4). O problema é de *destino* do redirect, não de estrutura do fluxo.

**Responsabilidade mal posicionada?** Não.

---

## Parte 3 — QuerySets

### Faz sentido manter regras de consulta no QuerySet?

Sim. Duas justificativas se sustentam:

1. **Eficiência**: `overdue()` e `pending_not_overdue()` geram SQL com `WHERE` — uma query por bloco do Dashboard, sem N+1. Implementar a mesma lógica em Python (iterando instâncias) seria desnecessariamente caro.

2. **Unicidade da regra**: a definição de "atrasada" está em um único lugar. Se a regra mudar, muda em um arquivo e reflete em todos os consumidores.

### Avaliação de `overdue()`

```python
def overdue(self, today=None):
    if today is None:
        today = date.today()
    return self.filter(
        status=Task.Status.PENDING,
        due_date__isnull=False,
        due_date__lt=today,
    )
```

Correto. O parâmetro `today=None` com fallback é a decisão certa para testabilidade. Os três filtros correspondem exatamente à regra do domínio (PDD Parte 5).

### Avaliação de `pending_not_overdue()`

```python
def pending_not_overdue(self, today=None):
    if today is None:
        today = date.today()
    return self.filter(status=Task.Status.PENDING).filter(
        models.Q(due_date__isnull=True) | models.Q(due_date__gte=today)
    )
```

Correto. A lógica `sem prazo OR prazo >= hoje` é o complemento exato de `overdue()`. O anti-sobreposição entre os dois blocos do Dashboard é garantido por matemática (conjuntos disjuntos por construção), não por convenção.

### O `@property is_overdue` deveria sair do Model?

Não. É necessário para uso nos templates de `tasks/index.html` — permite `{% if task.is_overdue %}` sem query adicional por instância. Remover exigiria passar estado derivado como variável de contexto extra, aumentando complexidade da view.

### Alguma regra deveria sair do QuerySet?

Não. As únicas regras no QuerySet são de filtragem de dados — o lugar correto para elas.

---

## Parte 4 — Dashboard

### O Dashboard continua sendo apenas um consumidor?

Sim. `apps/dashboard/views.py` tem 10 linhas de código efetivo. Não contém nenhuma lógica condicional própria, nenhum `if`, nenhum filtro raw. Chama métodos nomeados do QuerySet e passa os resultados para o template.

### Risco de concentrar regras?

O risco existe estruturalmente (identificado como A1/A2 na Task 2.1) mas não se manifestou. O padrão atual — Dashboard chama métodos nomeados do QuerySet de cada domínio — cria uma barreira natural. Para violar o princípio, seria necessário escrever conscientemente `.filter(status="PENDING", due_date__lt=today)` no Dashboard em vez de chamar `.overdue()`.

### Dependências do Dashboard ao final do MVP

```
dashboard/views.py
  → apps.tasks.models.Task      (overdue, pending_not_overdue)     ← atual
  → apps.events.models.Event    (today, upcoming)                  ← TE-3
  → apps.goals.models.Goal      (active)                           ← TE-4
```

Esse acoplamento é inerente, unidirecional e esperado. Não é um risco — é o design.

### Prevenção antes de Eventos e Metas?

Nenhuma intervenção estrutural é necessária. O padrão é claro e replicável: cada módulo de conceito expõe métodos de QuerySet com nomes semânticos, e o Dashboard os chama.

---

## Parte 5 — Organização do Projeto

### Estrutura planejada vs. implementada

| Planejado (Task 2.5 §6) | Implementado | Avaliação |
|---|---|---|
| Apps no nível raiz | `apps/<nome>/` (namespace) | **Melhor** — evita colisão com pacotes Python; imports mais claros |
| `templates/` na raiz | `frontend/templates/` | **Melhor** — separa claramente o frontend |
| `static/` na raiz | `frontend/static/` | **Melhor** — mesmo motivo |

A estrutura implementada é superior ao esboço do planejado. Sem ação necessária.

### `TEMPLATES` com `DIRS` + `APP_DIRS: True`

```python
"DIRS": [BASE_DIR / "frontend" / "templates"],
"APP_DIRS": True,
```

Com `APP_DIRS: True`, o Django também procura templates em `<app>/templates/`. Atualmente nenhum app tem pasta `templates/` própria — todos os templates estão em `frontend/templates/`. A configuração funciona corretamente; `APP_DIRS: True` está inativo na prática. Sem impacto; sem ação necessária.

### Convenções a adotar antes do crescimento

A convenção de naming de templates está estabelecida: `frontend/templates/<app_name>/index.html`. Mantê-la em Eventos e Metas é suficiente.

---

## Parte 6 — Django

### Aproveitamento do framework

| Recurso | Uso | Avaliação |
|---|---|---|
| `AbstractUser` | `apps/accounts/models.py` | Correto |
| `LoginView` / `LogoutView` | `apps/accounts/views.py`, `urls.py` | Correto — delegação ao framework |
| `@login_required`, `@require_POST` | `apps/tasks/views.py` | Idiomático |
| `TextChoices` | `Task.Status` | Idiomático |
| `models.QuerySet` subclasse | `TaskQuerySet` | Padrão correto |
| `F("due_date").asc(nulls_last=True)` | `tasks/views.py` | Correto para ordenação null-safe |
| `get_object_or_404(Task, pk=pk, owner=request.user)` | `tasks/views.py` | Segurança idiomática |
| `ModelForm` com `fields` explícito | `TaskForm` | Mais seguro que `exclude` |

### Funcionalidade nativa ignorada

`django.contrib.messages` está no middleware mas não é utilizado. Após criar uma tarefa, o usuário não recebe feedback visual de sucesso. Para o MVP isso é aceitável, mas é um caso que o framework resolve nativamente sem código adicional.

### htmx — divergência com a arquitetura planejada

O arquivo `htmx.min.js` existe e o `base.html` carrega o script. Nenhuma view ou template usa atributos htmx atualmente. O backlog (T2.4) descrevia "Concluir Tarefa via htmx", mas a implementação usou plain form POST — simplificação pragmática e válida.

O htmx está *presente* mas *inativo*. Isso não causa problemas, mas representa uma divergência entre o planejado e o executado que deve ser registrada como decisão consciente (ver Parte 9 e Conclusão).

### `TIME_ZONE` e `date.today()` — risco de correctude

```python
# settings.py
TIME_ZONE = "UTC"
LANGUAGE_CODE = "en-us"

# apps/tasks/models.py
from datetime import date
today = date.today()    # usa o relógio do processo (UTC no servidor)
```

`datetime.date.today()` retorna a data segundo o relógio do processo. Em um servidor em UTC, para um usuário brasileiro (UTC-3), entre 21h e meia-noite, o servidor entenderia que já é "amanhã". Uma tarefa com prazo "hoje" poderia ser classificada como atrasada às 22h pelo servidor.

O Django oferece `django.utils.timezone.localdate()` que respeita `TIME_ZONE` do settings. A combinação correta é:

- `TIME_ZONE = "America/Sao_Paulo"` em `settings.py`
- `LANGUAGE_CODE = "pt-br"` em `settings.py`
- `from django.utils.timezone import localdate` nos models/querysets

Não bloqueia TE-3 (o problema só se manifesta em produção ao redor da meia-noite), mas deve ser corrigido antes ou durante T7.1.

---

## Parte 7 — Escalabilidade

### Projeção — TE-3 (Eventos)

```python
# apps/events/models.py  (padrão esperado)
class EventQuerySet(models.QuerySet):
    def today(self, today=None): ...
    def upcoming(self, today=None, days=7): ...
```

```python
# apps/dashboard/views.py
events_today    = Event.objects.filter(owner=request.user).today()
upcoming_events = Event.objects.filter(owner=request.user).upcoming()
```

Padrão idêntico ao de Tarefas. Sem atrito.

### Projeção — TE-4 (Metas)

```python
class GoalQuerySet(models.QuerySet):
    def active(self):
        return self.filter(progress__lt=100)
```

Mais simples ainda — sem dependência de "hoje".

### Dashboard completo (T5.3–T5.6)

A view do Dashboard terá cinco QuerySet calls. Para o volume do sistema (dezenas a centenas de registros de um usuário), cinco queries simples são triviais — sem necessidade de otimização.

### Primeiro ponto de atrito

O único ponto de atrito real é o redirect após `tasks:complete` → `tasks:index`. Quando o Dashboard for a principal tela de interação (cinco blocos, ações diretas), completar uma tarefa a partir do Dashboard e ser redirecionado para `tasks/` será perceptível.

Estruturalmente, a arquitetura suporta a evolução para Eventos e Metas sem reestruturação.

---

## Parte 8 — Código

### Decisões tomadas nas Tasks T0–T5 que seriam diferentes

**1. `TIME_ZONE = "UTC"` + `date.today()` (T0.1, T2.5)**

*Custo de alteração:* baixo. Uma linha em settings, duas linhas em `tasks/models.py`, sem alteração de schema.
*Recomendação:* **corrigir** antes do deploy. Pode ser feito no início de TE-3 ou reservado para T7.1.

**2. Redirect `tasks:complete` → `tasks:index` (T2.4)**

*Custo de alteração:* baixo. Adicionar parâmetro `next` opcional à view `complete` são 3–4 linhas. Não quebra comportamento atual (tasks:index permanece como default quando `next` está ausente).
*Recomendação:* **corrigir antes de T5.3**, quando o Dashboard passar a ter mais blocos e mais ações diretas.

**3. htmx não utilizado (T2.4, T5.1, T5.2)**

*Custo de alteração:* médio quando chegar o momento (reescrever views que hoje retornam redirect para retornar fragmentos HTML ou respostas htmx).
*Recomendação:* **não alterar agora**. Decidir em TE-5 se as ações diretas merecem htmx.

---

## Parte 9 — Riscos

| # | Risco | Causa | Impacto | Classificação |
|---|---|---|---|---|
| R1 | **`date.today()` retorna data UTC em servidor remoto** | `TIME_ZONE = "UTC"` + `datetime.date.today()` em vez de `localdate()` | Classificação incorreta de "atrasada/pendente" ao redor da meia-noite para usuário brasileiro | **Médio** — irrelevante em dev local; real em produção |
| R2 | **Redirect `tasks:complete` → `tasks:index` quando chamado do Dashboard** | View não é ciente do ponto de origem | Usuário sai do Dashboard ao concluir tarefa — UX inconsistente com o planejado | **Baixo** agora; **Médio** quando Dashboard for tela principal |
| R3 | **`SECRET_KEY` exposto no settings.py commitado** | Geração automática do Django no scaffolding | Chave de produção comprometida se settings.py for para produção sem alteração | **Baixo** agora (dev); **Alto** se for a produção sem mudança |
| R4 | **Ausência de testes para o QuerySet** | Nenhuma suite de testes foi criada | Regressões silenciosas se `overdue()` ou `pending_not_overdue()` forem modificados | **Baixo-Médio** — a lógica é simples mas é o coração das regras de negócio |
| R5 | **htmx presente mas inativo** | Simplificação pragmática das tasks T2.4, T5.1, T5.2 | Divergência entre arquitetura planejada e implementação; custo maior de adoção quando necessário | **Baixo** |
| R6 | **`APP_DIRS: True` redundante** | Configuração padrão do Django não revisada | Sem impacto prático atual; pode causar confusão em eventual template de nome conflitante | **Baixo** |

---

## Parte 10 — Conclusão

### 1. A arquitetura continua consistente?

**Sim.** As fronteiras entre módulos são respeitadas, o fluxo de dados é limpo, o Dashboard é um consumidor puro e as regras de domínio têm um único dono.

### 2. Existe alguma decisão que deve ser corrigida antes do módulo de Eventos?

**Uma:** `TIME_ZONE = "UTC"` + uso de `date.today()`. Não bloqueia TE-3, mas quanto mais tempo passa sem a correção, mais confuso fica o diagnóstico se um bug de "data errada" aparecer em produção. Custo de correção é baixo; o momento ideal é antes de implementar Eventos (que também dependem da data corrente).

### 3. Existe alguma oportunidade clara de simplificação?

**Não.** O código já está simples. O único item que se aproxima é o redirect de `tasks:complete`, mas a solução (parâmetro `next`) adiciona código, não remove.

### 4. O padrão utilizado em Tarefas pode ser replicado integralmente para Eventos e Metas?

**Sim.** O padrão é:

```
Model + QuerySet (regras de filtro)
  + @property (estado derivado por instância, onde aplicável)
  + ModelForm (campos editáveis)
  + views (index + ação de estado)
  + urls (app_name + rotas)
  + templates (index.html)
```

Para Eventos: sem `@property` de estado (eventos não têm ciclo de vida — Task 2.2 §4).
Para Metas: `@property is_active` substituindo `is_overdue`.

### 5. Existe alguma decisão que deveria ser documentada antes de continuar?

**Sim** — a decisão de não usar htmx nas tasks concluídas. O backlog (T2.4) descrevia "via htmx"; a implementação usou plain POST. Esta é uma decisão válida e pragmática, mas não estava registrada. Se não for definida antes de TE-3, há risco de inconsistência de convenção entre módulos.

**Decisão registrada aqui:** htmx será avaliado para adoção em TE-5 (Dashboard interativo), não antes. TE-3 e TE-4 seguem o mesmo padrão de plain form POST já estabelecido.

### 6. Estamos utilizando o Django de forma idiomática?

**Sim**, com uma lacuna: `django.contrib.messages` está disponível mas não utilizado para feedback de ações. Aceitável para MVP.

### 7. A arquitetura continua alinhada ao objetivo do SibylSystem?

**Sim.** Simplicidade, clareza, separação por conceito de negócio e Dashboard como consumidor puro estão preservados. O projeto está onde deveria estar ao final do primeiro domínio completo.

---

## Recomendação

**Realizar dois ajustes pontuais antes de iniciar TE-3, depois prosseguir:**

**Ajuste 1 — `TIME_ZONE` e `localdate()` (custo: ~10 min)**

Em `settings.py`:
```python
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
```

Em `apps/tasks/models.py`:
```python
# substituir
from datetime import date
date.today()
# por
from django.utils.timezone import localdate
localdate()
```

Sem alteração de schema, sem migration. Resolve o risco R1 antes do deploy.

**Ajuste 2 — Decisão sobre htmx (custo: apenas decisão)**

Registrado na Conclusão §5: htmx permanece inativo em TE-3 e TE-4; será avaliado em TE-5.

**Após esses dois itens: prosseguir para TE-3 sem alterações estruturais.** O padrão estabelecido em Tarefas é sólido, replicável e alinhado à arquitetura planejada. Não há débito técnico acumulado que justifique pausa.

---

*Documento produzido após Tasks T0.1–T5.2 — Retrospectiva Arquitetural Pós TE-2.*
*Próxima revisão recomendada: após conclusão de TE-4 (Metas) ou antes de TE-5 (Dashboard completo).*
