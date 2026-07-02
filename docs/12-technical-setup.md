# SibylSystem — Setup Técnico

> **Documento da Fase 2 (Arquitetura) — Task 2.5.**
> Fontes: PDD, CLAUDE.md (fonte de verdade), `08`–`11` (arquitetura, domínio, dados, UX).
> Em caso de conflito, o CLAUDE.md prevalece.
>
> **Propósito:** definir o setup técnico oficial do MVP — stack, estilo arquitetural, estrutura
> e padrões — sempre escolhendo a opção **mais simples capaz de atender o MVP**, e só aumentando
> a complexidade quando houver justificativa objetiva.
>
> **Restrições desta task:** não altera produto, domínio, modelo de dados nem UX; não cria
> funcionalidades; não antecipa requisitos futuros sem justificativa.
>
> **Nota de decisão:** o desenvolvedor principal não indicou preferência de stack e pediu a
> "mais adequada à aplicação". Portanto a recomendação abaixo é feita **pelos méritos técnicos
> frente aos requisitos do MVP**, não por familiaridade prévia.

---

## 1. Technical Requirements Analysis

Análise baseada exclusivamente no PDD.

| Dimensão | Evidência no PDD | Leitura técnica |
|---|---|---|
| **Escala esperada** | "menor versão capaz"; uso pessoal; consulta frequente + alimentação leve (Parte 6) | Carga mínima; picos inexistentes; nada de escala horizontal. |
| **Número de usuários** | "Inicialmente, um único usuário" (Parte 2); multiusuário fora de escopo (Parte 3) | **1 usuário.** Sem concorrência real, sem gestão de contas. |
| **Volume de dados** | Eventos, tarefas e metas de uma pessoa; "registrar apenas o essencial" (Parte 6) | Volume baixíssimo (ordem de dezenas/centenas de registros). |
| **Complexidade funcional** | CRUD de 3 conceitos + conclusão + progresso + dashboard de 5 blocos (Parte 3 e 7) | Baixa: CRUD + autenticação + uma visão consolidada com regras derivadas simples. |
| **Performance** | Sem requisitos de latência; ênfase em "rapidez de uso" como UX (Princípio 3) | Trivial de atender; nenhuma operação pesada. |
| **Disponibilidade** | Não há SLA; ferramenta pessoal | "Bom o suficiente"; indisponibilidade breve é tolerável. |
| **Segurança** | "Proteger o acesso ao espaço pessoal" (Parte 3, E1); login/logout | Autenticação de um usuário + proteção das rotas. Sem multiusuário/compartilhamento. |

**Qual é o nível real de complexidade técnica do SibylSystem?**

> **Baixo.** É essencialmente um **CRUD pessoal autenticado com uma tela de consolidação**, de
> usuário único e volume mínimo. Não há concorrência, escala, integrações nem requisitos de
> performance/disponibilidade que justifiquem qualquer sofisticação. O risco real do projeto é
> **overengineering**, não capacidade técnica.

---

## 2. Architecture Style

**Recomendado: Monólito Modular, server-rendered.**

- **Por que atende melhor o MVP:** uma única aplicação que renderiza HTML no servidor cobre
  exatamente as 5 telas e os fluxos rasos da Task 2.4, com o mínimo de partes móveis. Os módulos
  internos espelham 1:1 a arquitetura da Task 2.1 (Acesso, Eventos, Tarefas, Metas, Painel),
  preservando alta coesão e baixo acoplamento **sem** custo de rede entre serviços. Alinha-se
  diretamente à Filosofia Arquitetural do CLAUDE.md ("Monólito modular").

- **Estilos que seriam excessivos:**
  - **Microserviços** — sem escala, sem times, sem domínios independentes; introduz rede,
    orquestração e operação que não se justificam.
  - **Frontend SPA + Backend API separados** — duplicaria deploys, exigiria CORS, contrato de API
    e gestão de estado no cliente para uma UX que é lista/formulário rasa. Overengineering.
  - **Event Sourcing / CQRS** — explicitamente desaconselhados no CLAUDE.md; nada no domínio os
    pede.

> Decisão: **Monólito Modular server-rendered** — o ponto exato entre simplicidade e organização
> por módulos de negócio.

---

## 3. Backend Stack

**Recomendado: Python + Django.**

### Linguagem — Python
- **Vantagens:** sintaxe legível (aderente ao critério "Legibilidade" do CLAUDE.md); curva
  suave; ecossistema maduro; ótima para CRUD.
- **Desvantagens:** não é a linguagem do frontend (mas, sendo server-rendered, não há "segunda
  linguagem" relevante no cliente).
- **Justificativa:** prioriza velocidade de desenvolvimento e manutenção de um único dev, sem
  exigir tooling pesado.

### Framework — Django
- **Vantagens:** "batteries-included" — **autenticação de sessão pronta** (cobre E1 com
  quase nenhum código), **ORM + migrations** integrados (mapeiam direto as 4 estruturas da Task
  2.3), **admin** integrado (gestão e inspeção de dados de graça para um usuário único),
  templates server-rendered (casam com a UX rasa). Extremamente estável e documentado.
- **Desvantagens:** traz componentes que talvez não usemos a fundo (ex.: parte do admin);
  "monolítico" por natureza — aceitável e desejado aqui.
- **Justificativa:** entre os frameworks batteries-included equivalentes (Django, Rails,
  Laravel), Django é recomendado pelos méritos: auth/ORM/admin prontos reduzem ao mínimo o
  código próprio para login, persistência e CRUD — exatamente o núcleo do MVP. Rails e Laravel
  seriam escolhas de **mesma classe**; o desempate objetivo seria a familiaridade do dev, que
  não foi declarada.

### Estrutura do projeto — apps de domínio
- Um app por módulo de negócio (Acesso/contas, Eventos, Tarefas, Metas, Painel), refletindo a
  Task 2.1. Mantém coesão e fronteiras claras dentro do monólito.

### Estratégia de autenticação — sessão (cookie) com o sistema nativo do Django
- **Vantagens:** pronta, segura por padrão, sem dependências externas; adequada a um navegador e
  um usuário.
- **Desvantagens:** baseada em servidor (sessão) — irrelevante para um único usuário.
- **Justificativa:** JWT/OAuth/SSO seriam overengineering para usuário único sem integrações. O
  `ownerId` (Task 2.3) é preenchido a partir do usuário autenticado, sem UI.

### Estratégia de APIs — sem API dedicada no MVP
- **Vantagens:** menos código e nenhuma camada de contrato; formulários enviam dados e o servidor
  responde HTML renderizado — o caminho mais curto para a UX da Task 2.4.
- **Desvantagens:** um cliente externo (ex.: app mobile futuro) precisaria de uma API depois.
- **Justificativa:** mobile e integrações estão fora do escopo; criar API agora seria antecipar
  requisito futuro sem justificativa. Se vier, é adição incremental (ver §9/Evolução).

---

## 4. Frontend Stack

**Recomendado: templates server-rendered do Django + HTML/CSS simples.**

### Framework — Django Templates (sem framework SPA)
- **Vantagens:** zero build pipeline obrigatório, zero estado de cliente, uma só aplicação para
  manter; entrega HTML pronto e rápido.
- **Desvantagens:** menos interatividade rica — desnecessária aqui.
- **Justificativa:** a UX (Task 2.4) é lista/formulário rasa, mobile-agnóstica por empilhamento;
  não há nada que exija uma SPA.

### Estratégia de UI — HTML semântico + CSS mínimo
- Sem biblioteca de componentes nem identidade visual (fora do escopo desta task). Estrutura
  primeiro; estética depois.

### Navegação — navegação por páginas (server-side)
- Barra de navegação persistente e retorno ao Dashboard, exatamente como o mapa da Task 2.4.

### Estado da aplicação — no servidor (banco + sessão)
- **Justificativa:** não há estado de cliente a gerenciar; elimina toda uma categoria de
  complexidade (stores, sincronização).

### Comunicação com backend — submissões HTTP + **htmx** como padrão de interatividade
- **htmx adotado como padrão de interatividade do projeto.** O Dashboard é a principal
  experiência do produto e concentra ações frequentes de baixa granularidade (concluir tarefa,
  atualizar progresso, editar registros). O **htmx** (dependência leve, sem build) oferece uma
  UX mais fluida — atualizações parciais da página sem recarga completa — **preservando a
  simplicidade da arquitetura server-rendered e evitando a complexidade de uma SPA**.
- Formulários HTTP tradicionais permanecem disponíveis como base; o htmx os complementa nas
  interações do caminho quente (Task 2.4). Não se adota nada além disso para não inflar o cliente.

---

## 5. Persistence Layer

### Banco de dados recomendado — **SQLite** (MVP)
- **Justificativa:** arquivo único, zero configuração e zero processo separado; mais que
  suficiente para um usuário e volume baixíssimo. Custo operacional praticamente nulo.

### Estratégia de persistência — ORM do Django + migrations
- Mapeia as 4 estruturas da Task 2.3 (Usuário, Evento, Tarefa, Meta + `ownerId`); migrations
  versionam a evolução do schema.

### Estrutura geral de armazenamento
- Uma coleção por entidade (sem tabelas detalhadas aqui — Task 2.6/implementação). Sem
  relacionamentos entre conceitos; apenas a referência de propriedade (`ownerId`) ao Usuário.

### Estratégia de backups — cópia do arquivo
- **Justificativa:** com SQLite, backup = **copiar o arquivo** periodicamente (cópia agendada
  para um armazenamento externo). Simples, barato e suficiente para uso pessoal.

> **Caminho de evolução (não agora):** trocar SQLite por **PostgreSQL** é uma mudança de
> configuração no Django, justificável apenas se surgir concorrência/volume — o que o escopo
> atual não prevê.

---

## 6. Project Structure

Estrutura de alto nível (sem detalhar arquivos):

```
SibylSystem/
├── docs/                  # documentação das fases (já existente)
├── config/                # configurações do projeto (settings, rotas raiz)
├── accounts/              # módulo de Acesso (usuário único, login/logout)
├── events/                # módulo de Eventos
├── tasks/                 # módulo de Tarefas
├── goals/                 # módulo de Metas
├── dashboard/             # módulo de Painel (consolidação dos 5 blocos)
├── templates/             # telas server-rendered
├── static/                # CSS mínimo e assets
└── manage.py              # ponto de entrada de gestão do projeto
```

- **Justificativa:** um único repositório e uma única aplicação (sem `frontend/` + `backend/`
  separados, coerente com a decisão da §2). Os módulos de negócio são diretórios de primeiro
  nível, espelhando a Task 2.1 — fronteiras visíveis dentro do monólito, com baixo acoplamento.

---

## 6.1. Environment Variables

As variáveis de ambiente sensíveis são externalizadas e nunca commitadas.

| Variável | Obrigatória | Descrição |
|---|---|---|
| `SECRET_KEY` | **Sim** — a app falha explicitamente se ausente | Chave secreta do Django |
| `DEBUG` | Não (`False` por padrão) | `True` em desenvolvimento; omitir ou `False` em produção |

**Setup local:**

```bash
cp .env.example .env
# Editar .env com valores reais
python manage.py runserver
```

Gerar uma chave secreta segura:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

O arquivo `.env` é carregado automaticamente via `python-dotenv` no início do `settings.py`.
O `.env` está no `.gitignore` e nunca deve ser commitado.

---

## 7. Development Workflow

Adequado a **um desenvolvedor**, **evolução incremental** e **baixo custo operacional**.

- **Controle de versão:** Git, repositório no GitHub (já existente).
- **Estratégia de branches:** **trunk-based simplificado** — `main` sempre estável; uma branch
  curta por task/feature, integrada via PR (autorrevisão) e removida após o merge. Sem GitFlow
  (excessivo para um dev).
- **Ambiente local:** Python em ambiente virtual + SQLite + servidor de desenvolvimento do
  Django. Sem Docker obrigatório (adicionaria overhead sem ganho para um único dev; permanece
  como opção futura se a reprodutibilidade exigir).
- **Ambiente de produção:** uma única instância da aplicação com o arquivo SQLite em disco
  persistente.
- **Processo de releases:** seguir a estratégia de 4 releases do PDD (R1→R4); marcar cada
  release com uma tag Git. Releases são incrementais e pequenos, coerentes com a Filosofia de
  Desenvolvimento (uma task por vez).

---

## 8. Deployment Strategy

- **Como publicar o MVP:** empacotar a aplicação única e rodá-la em um processo, servindo HTTP.
- **Hospedagem recomendada:** **um VPS pequeno** ou uma **PaaS com volume persistente** (o
  volume persistente é necessário por causa do arquivo SQLite). Escolha pela menor combinação de
  custo e operação; ambas atendem.
- **Estratégia de atualização:** deploy por `git pull` + reinício do processo, ou deploy
  automático no push (se a PaaS oferecer). Migrations aplicadas no deploy.
- **Estratégia de monitoramento:** **mínima** — logs da plataforma + uma verificação simples de
  uptime. Sem stack de observabilidade.

**O que seria overengineering?** Kubernetes/containers orquestrados, múltiplos ambientes
(staging/QA), CI/CD elaborado, balanceadores, réplicas, cache (Redis), filas, APM/observabilidade
avançada, infraestrutura como código. Nada disso é justificável para um app pessoal de usuário
único.

**Qual a solução mais simples possível?** Uma instância, um arquivo SQLite em disco persistente,
deploy por push/pull com migrations no deploy e backup por cópia de arquivo.

---

## 9. Technical Risks

| # | Risco | Causa | Impacto | Mitigação |
|---|---|---|---|---|
| T1 | **Perda de dados (SQLite em FS efêmero)** | Hospedar SQLite em plataforma sem disco persistente | Perda do arquivo a cada deploy/reinício | Exigir **volume persistente** (VPS ou PaaS com disco) + **backups por cópia** agendados. |
| T2 | **Overengineering** | Tentação de adicionar SPA, API, containers, microserviços | Aumento de custo/manutenção sem ganho | Manter as decisões desta task; qualquer adição exige justificativa objetiva (Princípio 1). |
| T3 | **Limite de concorrência do SQLite** | SQLite serializa escritas | Irrelevante para 1 usuário; só importaria sob concorrência | Aceitar para o MVP; caminho documentado para PostgreSQL se o contexto mudar. |
| T4 | **Acoplamento entre módulos do monólito** | Módulos se referenciarem indevidamente | Erosão das fronteiras da Task 2.1 | Cada app de domínio coeso; o Painel apenas **lê** os conceitos (mitiga A1/A2 da Task 2.1). |
| T5 | **Dependência excessiva do admin do Django** | Usar o admin como substituto da UX definida | UX real (Task 2.4) ficaria secundária | Admin é ferramenta **auxiliar** (inspeção/manutenção do dev); a superfície do produto é a UX da Task 2.4. |
| T6 | **Ponto único de falha** | Uma só instância | Indisponibilidade temporária | Aceitável para uso pessoal; backups garantem recuperação; escalar só se justificado. |

---

## 10. Setup Review

- **A stack está alinhada ao MVP?** **Sim.** Complexidade técnica baixa (§1) → monólito modular
  server-rendered + SQLite, que é o mínimo viável que cobre auth, CRUD e dashboard.
- **Existe overengineering?** **Não.** Foram descartados SPA, API separada, microserviços,
  containers e observabilidade avançada por falta de justificativa.
- **Existe escolha desnecessariamente complexa?** **Não.** Todas as escolhas favorecem menos
  código e menos operação; o único "extra" (htmx) é uma dependência leve, sem build, adotada como
  padrão de interatividade — coerente com a arquitetura server-rendered, sem introduzir uma SPA.
- **O setup favorece evolução futura sem sacrificar simplicidade?** **Sim.** Caminhos de evolução
  são aditivos/localizados: SQLite→PostgreSQL (config), API para mobile (adição), módulo novo
  (ex.: Notas) como novo app — sem reescrever o existente, coerente com a análise de evolução das
  Tasks 2.2/2.3.

---

## Conclusão

1. **Stack oficial recomendada:**
   - **Linguagem/Framework:** Python + **Django** (monólito modular server-rendered).
   - **Persistência:** **SQLite** (MVP) via ORM + migrations do Django; evolução documentada para
     PostgreSQL.
   - **Autenticação:** sessão nativa do Django (usuário único).
   - **Frontend:** templates server-rendered + HTML/CSS mínimo; **htmx como padrão de
     interatividade** para as ações frequentes do Dashboard.
   - **APIs:** nenhuma dedicada no MVP (server-rendered).
   - **Versionamento/Deploy:** Git/GitHub; uma instância (VPS ou PaaS com volume persistente);
     backup por cópia do arquivo; monitoramento mínimo.

2. **Arquitetura técnica oficial:** **Monólito Modular server-rendered**, com apps de domínio
   espelhando a Task 2.1 (Acesso, Eventos, Tarefas, Metas, Painel).

3. **Solução mais simples capaz de atender o MVP:** uma aplicação Django única, com SQLite em
   disco persistente, telas server-rendered, autenticação de sessão e deploy por push/pull com
   backup por cópia de arquivo.

4. **O projeto está pronto para a Task 2.6 (Backlog Técnico)?** **Sim.** Stack, estilo
   arquitetural, persistência, estrutura, workflow e deploy estão definidos e justificados pelos
   requisitos reais do MVP, sem alterar produto, domínio, dados ou UX.

### Recomendação

> **Prosseguir para a Task 2.6 (Backlog Técnico).**
> O setup é o mais simples capaz de atender o MVP, com baixo custo operacional e velocidade de
> desenvolvimento, e mantém abertos caminhos de evolução incremental sem complexidade prematura.

---

*Documento produzido na Task 2.5 — Setup Técnico (Fase 2).*
