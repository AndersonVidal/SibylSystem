# Sibyl

Organizador pessoal local para tarefas, eventos e metas.

O Sibyl roda inteiramente no seu computador. Seus dados ficam no seu disco,
não existem servidores externos e o navegador é apenas a interface.

---

## Funcionalidades

- **Tarefas** — criar, editar, concluir e acompanhar com prazo
- **Eventos** — registrar compromissos com data e horário
- **Metas** — definir objetivos com horizonte temporal e progresso
- **Dashboard** — visão diária de eventos, tarefas pendentes, atrasadas e metas ativas
- **Backup local** — cópia do banco com retenção automática
- **Launcher Linux** — iniciar pelo menu de aplicações sem abrir terminal

---

## Requisitos

- Python 3.11 ou superior
- SQLite (embutido no Python)
- Linux, macOS ou Windows

---

## Instalação

**Linux / macOS:**

```bash
git clone https://github.com/AndersonVidal/SibylSystem.git
cd SibylSystem

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
```

**Windows (PowerShell):**

```powershell
git clone https://github.com/AndersonVidal/SibylSystem.git
cd SibylSystem

python -m venv venv
.\venv\Scripts\pip install -r requirements.txt

copy .env.example .env
```

Edite o arquivo `.env` e defina uma chave secreta:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

Cole o resultado no campo `SECRET_KEY` do arquivo `.env`.

---

## Inicialização

| Sistema | Comando |
|---|---|
| Linux | `./scripts/run.sh` |
| macOS | `./scripts/run-macos.sh` |
| Windows | `.\scripts\run.ps1` |

O script aplica as migrations, inicia o servidor e exibe:

```
Sibyl disponível em:
http://127.0.0.1:8000
```

Abra o endereço no navegador. Para encerrar, pressione `Ctrl+C` no terminal.

> **Windows:** na primeira execução pode ser necessário permitir a execução de scripts PowerShell:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

---

## Dados da aplicação

Os dados ficam separados do código, em um diretório próprio do usuário:

| Sistema | Caminho |
|---|---|
| Linux | `~/.local/share/sibyl/` |
| macOS | `~/Library/Application Support/Sibyl/` |
| Windows | `%LOCALAPPDATA%\Sibyl\` |

Estrutura criada automaticamente na primeira execução:

```
sibyl/
    database.sqlite3
    backups/
    logs/
```

O diretório do projeto pode ser movido ou atualizado sem afetar os dados.

---

## Backup

```bash
python manage.py backup
```

Cria uma cópia do banco com timestamp em `DATA_DIR/backups/`. Os 10 backups
mais recentes são mantidos automaticamente.

**Restaurar um backup:**

```bash
cp ~/.local/share/sibyl/backups/database-YYYYMMDD-HHMMSS.sqlite3 \
   ~/.local/share/sibyl/database.sqlite3
```

---

## Launcher Desktop (Linux)

Para iniciar o Sibyl pelo menu de aplicações:

```bash
./scripts/install-launcher.sh
```

O launcher aparece no menu do sistema e executa `scripts/run.sh` ao ser clicado.
A aplicação continua rodando localmente — o navegador continua sendo a interface.

Para remover:

```bash
rm ~/.local/share/applications/sibyl.desktop
```

Para reinstalar após mover o projeto de diretório, basta executar
`install-launcher.sh` novamente.

---

## Atualização

```bash
git pull
# em seguida execute o script do seu sistema operacional
./scripts/run.sh        # Linux
./scripts/run-macos.sh  # macOS
.\scripts\run.ps1       # Windows
```

O script aplica as migrations automaticamente. Os dados não são afetados.

---

## Estrutura do projeto

```
apps/          módulos de domínio (accounts, tasks, events, goals, dashboard)
config/        configurações do Django
frontend/      templates e assets estáticos
scripts/       scripts de operação (run.sh, run-macos.sh, run.ps1, install-launcher.sh)
resources/     arquivos de integração com o sistema operacional
docs/          documentação técnica detalhada
tests/         infraestrutura de testes compartilhada
```

---

## Documentação técnica

Detalhes de arquitetura, modelo de dados, decisões técnicas e roadmap estão em `docs/`.

---

## Roadmap

Possíveis evoluções futuras, sem prazo definido:

- Aplicativo desktop empacotado (Tauri ou similar)
- Backup automático agendado
- Sincronização entre dispositivos
- Suporte a múltiplos usuários
- Notificações locais
