# CLAUDE.md

## Projeto

Nome: SibylSystem

Repositório: https://github.com/AndersonVidal/SibylSystem

---

# O que é o Sibyl

Organizador pessoal local para tarefas, eventos e metas.

Roda inteiramente no computador do usuário. O navegador é a interface. Os dados pertencem ao usuário. Não há dependência de servidores externos.

Usuário único. Qualquer adição de multiusuário, compartilhamento ou integração externa exige validação explícita antes de ser implementada.

---

# Arquitetura

**Monólito modular server-rendered.**

Django renderiza HTML no servidor. Sem SPA, sem API dedicada, sem microsserviços.

## Apps de domínio

```
apps/
    accounts/      autenticação, modelo User customizado, management commands
    events/        módulo de Eventos
    tasks/         módulo de Tarefas
    goals/         módulo de Metas
    dashboard/     painel consolidado (lê os demais módulos, não possui modelos próprios)
```

## Frontend

```
frontend/
    templates/     templates Django organizados por app (base.html + subdiretórios)
    static/
        css/       main.css (arquivo único)
        js/        htmx.min.js (carregado mas usado apenas quando necessário)
```

## Configuração

```
config/
    settings.py    configuração única — sem múltiplos arquivos de settings
    urls.py
    wsgi.py
```

## Operação local

```
scripts/
    run.sh                     Linux
    run-macos.sh               macOS
    run.ps1                    Windows
    install-launcher-linux.sh
    install-launcher-macos.sh
    install-launcher-windows.ps1

resources/
    linux/sibyl.desktop        template do launcher Linux
    macos/Sibyl.command        template do launcher macOS
```

## Testes

```
tests/
    base.py        SibylTestCase (classe base para todos os testes)
    factories.py   create_user
```

Testes de cada app ficam em `apps/<app>/tests.py`.

---

# Dados do usuário

O banco de dados **nunca** fica dentro do diretório do projeto.

`DATA_DIR` é resolvido em `config/settings.py` via `_data_dir()`:

| SO | Caminho padrão |
|---|---|
| Linux | `~/.local/share/sibyl/` (respeita `XDG_DATA_HOME`) |
| macOS | `~/Library/Application Support/Sibyl/` |
| Windows | `%LOCALAPPDATA%\Sibyl\` |

Estrutura criada automaticamente:

```
sibyl/
    database.sqlite3
    backups/
    logs/
```

Backup: `python manage.py backup` — cria cópia timestampada, mantém os 10 mais recentes.

---

# Configuração por variáveis de ambiente

`.env` na raiz do projeto (gitignored). Carregado via `load_dotenv(BASE_DIR / ".env")`.

| Variável | Obrigatória | Comportamento se ausente |
|---|---|---|
| `SECRET_KEY` | Sim | `RuntimeError` explícito — a app não sobe |
| `DEBUG` | Não | `False` por padrão |

`DEBUG` aceita: `true`, `1`, `yes`, `on` (case-insensitive). Qualquer outro valor → `False`.

Criar `.env` a partir de `.env.example`. Nunca commitar `.env`.

---

# Convenções de implementação

## Views

Function Based Views exclusivamente. Sem Class Based Views.

Padrão para listagem com criação inline:

```python
@login_required
def index(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            return redirect("app:index")
    else:
        form = MyForm()
    objects = MyModel.objects.filter(owner=request.user).order_by(...)
    return render(request, "app/index.html", {"form": form, "objects": objects, "active_nav": "app"})
```

Padrão para edição:

```python
@login_required
def edit(request, pk):
    obj = get_object_or_404(MyModel, pk=pk, owner=request.user)
    if request.method == "POST":
        form = MyForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("app:index")
    else:
        form = MyForm(instance=obj)
    return render(request, "app/edit.html", {"form": form, "obj": obj, "active_nav": "app"})
```

Padrão para exclusão (confirmação em GET, execução em POST):

```python
@login_required
def delete(request, pk):
    obj = get_object_or_404(MyModel, pk=pk, owner=request.user)
    if request.method == "POST":
        obj.delete()
        return redirect("app:index")
    return render(request, "app/delete.html", {"obj": obj, "active_nav": "app"})
```

## Proteção de owner

Sempre usar `get_object_or_404(Model, pk=pk, owner=request.user)`.

Nunca buscar por pk sem filtrar por owner.

O campo `owner` nunca aparece em `ModelForm` — é atribuído na view via `commit=False`.

## POST para ações destrutivas

Operações irreversíveis (deletar, concluir, atualizar progresso) sempre via POST.

GET nunca altera estado.

## QuerySets especializados

Regras de domínio ficam no QuerySet, não nas views:

```python
class TaskQuerySet(models.QuerySet):
    def overdue(self, today=None): ...
    def pending_not_overdue(self, today=None): ...

class Task(models.Model):
    objects = TaskQuerySet.as_manager()
```

## Ordenação com NULLs

Campos nullable sempre ordenados explicitamente:

```python
.order_by(F("due_date").asc(nulls_last=True), "title")
```

Nunca depender do comportamento padrão de NULL do banco.

## Owner obrigatório em todos os modelos de domínio

Todos os modelos (Event, Task, Goal) têm:

```python
owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, ...)
```

## Redirect após POST

Toda ação bem-sucedida termina com `redirect(...)`. Nunca renderizar diretamente após POST válido.

---

# Convenções de CSS

Classes compartilhadas entre módulos usam prefixo `entity-`:

- `entity-list`, `entity-item`, `entity-title`, `entity-meta`, `entity-date`

Classes específicas de um módulo usam o nome do módulo:

- `task-status`, `task-status--completed`, `task-overdue`

---

# Convenções de testes

Todos os testes herdam de `SibylTestCase` (em `tests/base.py`).

Métodos disponíveis: `make_user()`, `login()`, `today()`, `days_from_today(days)`.

Para testar comportamento dependente de data, usar `unittest.mock.patch` no target correto:

```python
patch("apps.tasks.models.timezone.localdate", return_value=fixed_date)
```

O banco de testes usa `:memory:` (SQLite em memória). Configurado em `settings.py`.

---

# Toolchain

- **Python 3.12** / **Django 6.0**
- **Black** — formatação
- **Ruff** — lint (E, F, I, W) + isort
- **pre-commit** — executa Black e Ruff antes de todo commit

Antes de commitar, o pre-commit roda automaticamente. Se Black reformatar um arquivo, o commit falha — re-adicionar e commitar.

---

# Inicialização local

```bash
# Linux
./scripts/run.sh

# macOS
./scripts/run-macos.sh

# Windows
.\scripts\run.ps1
```

Os scripts verificam o venv, aplicam migrations e sobem o servidor. Executáveis de qualquer diretório.

---

# Filosofia de desenvolvimento

- Uma task por vez. Nunca antecipar.
- Não implementar o que não foi solicitado.
- Quando houver dúvida entre simples e sofisticado, escolher o simples.
- Três linhas similares são melhores que uma abstração prematura.
- Mudanças em modelo de dados, arquitetura ou fluxos do usuário devem ser comunicadas antes de implementadas.
- Aguardar validação ao final de cada task.

---

# Orientações para IA

- Preservar as convenções acima. Consistência supera criatividade.
- Não introduzir CBVs, APIs REST, serializers, ou qualquer padrão ausente no projeto.
- Não adicionar dependências sem necessidade explícita.
- Não adicionar tratamento de erros para cenários impossíveis.
- Não adicionar comentários que repetem o que o código já diz.
- Não criar arquivos de documentação sem solicitação.
- Ao editar views, seguir exatamente o padrão FBV existente.
- Ao criar modelos, incluir `owner` obrigatoriamente.
- Ao criar QuerySets, colocar regras de domínio no QuerySet, não na view.
- Ao ordenar campos nullable, usar `F("campo").asc(nulls_last=True)`.
- Migrations nunca devem ser editadas manualmente.
- O `db.sqlite3` na raiz do projeto é um resíduo histórico — o banco real fica em `DATA_DIR`.

---

# Documentação do projeto

| Documento | Propósito |
|---|---|
| `CLAUDE.md` | Orientação para IA — arquitetura, convenções, padrões |
| `README.md` | Documentação do usuário — instalação, uso, operação |
| `docs/` | Documentação técnica detalhada — decisões, modelo de dados, retrospectivas |

Não duplicar conteúdo entre esses documentos.

---

# Fonte da verdade

Quando houver conflito entre uma task e este documento, o conflito deve ser explicitamente comunicado antes da implementação.

A implementação real sempre prevalece sobre documentação desatualizada.
