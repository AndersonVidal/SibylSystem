# Escopo do MVP — SibylSystem

> Artefato da **Task 1.2 (Fase 1 — Definição do Produto)**.
> Fontes: [`CLAUDE.md`](../CLAUDE.md) (fonte de verdade) e [`01-product-vision.md`](./01-product-vision.md) (Task 1.1).
> Em caso de conflito, o CLAUDE.md prevalece.
> Escopo desta task: o que entra/não entra no MVP e a menor versão capaz de entregar o valor.
> **Não** trata de arquitetura, tecnologia, banco de dados, telas, fluxos ou modelo de dados.
> Toda funcionalidade é justificada pelo problema definido na Task 1.1.

---

## 1. MVP Definition

O MVP do SibylSystem é a **menor versão capaz de centralizar eventos, tarefas e metas de um
único usuário e apresentá-los em uma visão consolidada (dashboard)**, substituindo a memória e
as ferramentas dispersas para esses três conceitos.

A menor versão possível que ainda entrega o valor principal da visão é composta por:

- **Autenticação** de usuário único (proteger o acesso ao espaço pessoal).
- **Gestão dos três conceitos** — Evento, Tarefa e Meta — com as operações mínimas para
  registrá-los e mantê-los atualizados.
- **Dashboard** que responde, numa única tela, "o que preciso fazer, o que está
  pendente/atrasado e quais metas estão ativas".

Sem qualquer um desses três blocos o produto não entrega o valor definido na Task 1.1:
sem autenticação não há espaço pessoal protegido; sem a gestão dos conceitos não há o que
centralizar; sem o dashboard não há a clareza consolidada que é o motor de valor.

---

## 2. Core Features

> Prioridades restritas a **Must Have / Should Have / Could Have**.
> Todas as funcionalidades abaixo já constam do escopo do MVP no CLAUDE.md; a priorização
> abaixo indica a ordem de valor dentro do próprio MVP, não exclusão.

### Autenticação

| Funcionalidade | Objetivo | Justificativa (problema da Task 1.1) | Prioridade |
|---|---|---|---|
| **Login** | Permitir acesso autenticado ao sistema | O espaço pessoal centraliza informações da vida do usuário e precisa ser protegido | **Must Have** |
| **Logout** | Encerrar a sessão de forma segura | Contraparte do login; controle básico de acesso ao espaço pessoal | **Must Have** |

### Eventos

| Funcionalidade | Objetivo | Justificativa | Prioridade |
|---|---|---|---|
| **Criar evento** | Registrar algo que ocorre em data específica | Centralizar compromissos hoje dispersos/na memória | **Must Have** |
| **Listar eventos** | Visualizar os eventos registrados | Sem listar não há recuperação da informação centralizada | **Must Have** |
| **Editar evento** | Corrigir/atualizar um evento | Manter a informação confiável e atual reduz carga mental | **Should Have** |
| **Excluir evento** | Remover evento que não é mais relevante | Evitar ruído e manter clareza do que importa | **Should Have** |

### Tarefas

| Funcionalidade | Objetivo | Justificativa | Prioridade |
|---|---|---|---|
| **Criar tarefa** | Registrar uma ação a ser executada | Centralizar pendências hoje dispersas/na memória | **Must Have** |
| **Listar tarefas** | Visualizar tarefas e seu estado | Recuperar pendências; base de "pendentes/atrasadas" | **Must Have** |
| **Concluir tarefa** | Marcar uma tarefa como realizada | Acompanhar execução e distinguir feito de pendente | **Must Have** |
| **Editar tarefa** | Corrigir/atualizar uma tarefa | Manter a informação confiável e atual | **Should Have** |
| **Excluir tarefa** | Remover tarefa não mais relevante | Reduzir ruído e preservar clareza | **Should Have** |

### Metas

| Funcionalidade | Objetivo | Justificativa | Prioridade |
|---|---|---|---|
| **Criar meta** | Registrar um objetivo a ser alcançado | Conectar o cotidiano aos objetivos de curto/médio/longo prazo | **Must Have** |
| **Listar metas** | Visualizar as metas e seu estado | Recuperar objetivos; base de "metas ativas" | **Must Have** |
| **Atualizar progresso da meta** | Refletir avanço em direção ao objetivo | Acompanhamento de evolução é valor central da visão | **Must Have** |
| **Editar meta** | Corrigir/atualizar uma meta | Manter a informação confiável e atual | **Should Have** |
| **Excluir meta** | Remover meta não mais relevante | Reduzir ruído e preservar clareza | **Should Have** |

### Dashboard

| Funcionalidade | Objetivo | Justificativa | Prioridade |
|---|---|---|---|
| **Eventos de hoje** | Mostrar o que ocorre no dia | Clareza imediata do "agora" | **Must Have** |
| **Próximos eventos** | Antecipar o que vem a seguir | Reduzir risco de esquecimento de compromissos | **Must Have** |
| **Tarefas pendentes** | Mostrar o que falta fazer | Visão consolidada da execução pendente | **Must Have** |
| **Tarefas atrasadas** | Destacar pendências vencidas | Apoiar priorização do que é urgente | **Must Have** |
| **Metas ativas** | Mostrar objetivos em andamento | Manter os objetivos visíveis no dia a dia | **Must Have** |

> Nota: a regra que define "próximos", "pendente", "atrasada" e "ativa" pertence às tasks de
> **Regras Funcionais** da Fase 1 (ver Observações Futuras). Aqui apenas confirmamos sua
> presença obrigatória no MVP.

---

## 3. Explicitly Out of Scope

### Exclusões herdadas do CLAUDE.md

| Item fora do escopo | Motivo da exclusão |
|---|---|
| Multiusuário | MVP é de usuário único; multiusuário adiciona complexidade sem necessidade atual |
| Compartilhamento | Depende de multiusuário; não atende ao usuário único |
| Aplicativo mobile | Amplia esforço e manutenção sem ser necessário para entregar o valor central |
| IA | Sofisticação prematura; contraria o princípio da simplicidade |
| Chat | Não resolve o problema central de centralização/clareza |
| Gamificação | Não essencial ao valor; adiciona complexidade e manutenção |
| Integrações externas | Complexidade e manutenção altas; o valor é entregue sem elas |
| Sincronização com calendários externos | Integração externa; fora do propósito mínimo do MVP |
| Notificações automáticas | Fora do escopo declarado; o dashboard cobre a visibilidade no MVP |
| Integração com e-mail | Integração externa não essencial ao valor central |
| Integração com WhatsApp | Integração externa não essencial ao valor central |

### Novas exclusões identificadas nesta análise

| Item fora do escopo | Motivo da exclusão |
|---|---|
| Recorrência de eventos | O CLAUDE.md a cita apenas como possibilidade *futura* ("Pode ser recorrente futuramente"); não consta do escopo do MVP. Incluir agora seria antecipar funcionalidade |
| Categorias/etiquetas/prioridade visual de itens | Não previstos no CLAUDE.md; adicionam estrutura e decisões sem justificativa pelo problema atual |
| Relatórios/histórico/analytics de evolução | Embora "evolução ao longo do tempo" seja parte da visão, no MVP isso é atendido pelo progresso de meta e pelo dashboard; relatórios são sofisticação adiável |
| Busca/filtros avançados | "Listar" cobre a recuperação mínima; filtros avançados são otimização não essencial |
| Anexos, notas livres ou campos ricos nos conceitos | Não previstos; ampliam escopo sem justificativa pelo problema da Task 1.1 |
| Subtarefas / vínculo explícito Meta→Tarefa/Evento | O CLAUDE.md diz que Meta "pode originar tarefas e eventos", mas não define vínculo no MVP; tratar como candidato futuro evita complexidade prematura |

---

## 4. User Value Mapping

| Funcionalidade | Problema que resolve (Task 1.1) | Valor para o usuário |
|---|---|---|
| Login / Logout | Informação pessoal dispersa e desprotegida | Espaço pessoal seguro e controlado |
| Criar/Listar evento | Compromissos na memória ou dispersos | Compromissos registrados e recuperáveis num só lugar |
| Editar/Excluir evento | Informação desatualizada gera ruído | Dados confiáveis e limpos |
| Criar/Listar tarefa | Pendências esquecidas ou fragmentadas | Pendências visíveis e sob controle |
| Concluir tarefa | Falta de distinção entre feito e pendente | Sensação de progresso e clareza do que resta |
| Editar/Excluir tarefa | Pendências obsoletas/incorretas | Lista de tarefas confiável |
| Criar/Listar meta | Objetivos sem registro nem visibilidade | Objetivos explícitos e acompanháveis |
| Atualizar progresso da meta | Evolução de longo prazo invisível | Percepção de avanço e apoio à decisão |
| Editar/Excluir meta | Objetivos desatualizados | Metas confiáveis e relevantes |
| Dashboard (5 blocos) | Falta de visão consolidada do que importa agora | Clareza imediata: o que fazer, o que está pendente/atrasado, quais metas estão ativas |

**Verificação de valor:** nenhuma funcionalidade do MVP ficou sem problema/valor claro. Todas
rastreiam diretamente a um problema da Task 1.1. Não há funcionalidade no MVP que deva ser
questionada por ausência de valor.

---

## 5. MVP Boundaries

### Ao final do MVP, o usuário **conseguirá**:

1. Autenticar-se (login) e encerrar a sessão (logout) como usuário único.
2. Criar, listar, editar e excluir **eventos**.
3. Criar, listar, editar, excluir e **concluir** **tarefas**.
4. Criar, listar, editar, excluir e **atualizar o progresso** de **metas**.
5. Abrir um **dashboard** e ver, numa única visão: eventos de hoje, próximos eventos, tarefas
   pendentes, tarefas atrasadas e metas ativas.

### Ao final do MVP, o usuário **NÃO conseguirá**:

1. Compartilhar dados ou ter mais de um usuário.
2. Acessar por aplicativo mobile dedicado.
3. Usar IA, chat ou gamificação.
4. Integrar/sincronizar com calendários, e-mail, WhatsApp ou qualquer serviço externo.
5. Receber notificações automáticas.
6. Configurar eventos recorrentes.
7. Categorizar, etiquetar, filtrar avançadamente ou buscar itens.
8. Gerar relatórios/históricos de evolução além do progresso de meta e do dashboard.
9. Vincular explicitamente metas a tarefas/eventos ou criar subtarefas.

---

## 6. Future Candidates

| Candidata | Motivo para ficar fora do MVP |
|---|---|
| Recorrência de eventos | Citada como possibilidade futura no CLAUDE.md; não essencial ao valor mínimo |
| Vínculo Meta → Tarefas/Eventos | Conceito previsto ("meta pode originar tarefas e eventos"), mas adiciona complexidade; validar valor após o MVP |
| Notificações/lembretes automáticos | Fora do escopo; reduziria o risco R1 (hábito) mas é adiável |
| Relatórios e histórico de evolução | "Evolução ao longo do tempo" pode ganhar visões dedicadas após validação |
| Categorias / etiquetas / prioridade | Organização adicional; só se o uso real demonstrar necessidade |
| Busca e filtros avançados | Útil conforme o volume de dados crescer |
| Aplicativo mobile | Ampliaria acesso; avaliar após validação do valor no MVP |
| Integrações externas (calendário, e-mail, WhatsApp) | Alto custo/manutenção; só com validação explícita |
| IA / chat | Sofisticação; só faz sentido após o núcleo provar valor |
| Gamificação | Engajamento; não essencial ao propósito central |

*(Registro apenas — sem detalhamento de implementação, conforme a task.)*

---

## 7. Risks of Scope Expansion

| Risco | Tipo de funcionalidade que ameaça | Princípio ameaçado |
|---|---|---|
| **Inflar os conceitos** com campos ricos, anexos, subtarefas, vínculos | "Seria bom ter" sem justificativa no problema | Simplicidade, Baixa manutenção |
| **Antecipar recorrência** de eventos | Funcionalidade marcada como futura sendo puxada para o MVP | Simplicidade, Rapidez de uso |
| **Adicionar relatórios/analytics** cedo | Visões sofisticadas de evolução | Simplicidade, Baixa manutenção |
| **Introduzir filtros/busca/categorias** prematuramente | Otimização de organização sem volume que a justifique | Clareza, Rapidez de uso |
| **Puxar integrações/notificações** | Itens explicitamente fora do escopo | Baixa manutenção, Simplicidade |
| **Enriquecer o dashboard** além dos 5 blocos | Mais informação na tela principal | Clareza, Rapidez de uso |
| **Generalizar para multiusuário** | Estrutura para além do usuário único | Simplicidade, Baixa manutenção |

Padrão comum a vigiar: funcionalidades adicionadas "porque seriam interessantes" e não porque
resolvem um problema da Task 1.1. O CLAUDE.md exige justificar pelo problema e, na dúvida,
escolher a solução simples.

---

## Conclusão

1. **O escopo do MVP está claro?**
   Sim. O MVP está delimitado pelos três blocos (Autenticação, Conceitos, Dashboard) já
   definidos no CLAUDE.md, com fronteiras objetivas e verificáveis (seção 5).

2. **Existem ambiguidades a resolver antes da Task 1.3?**
   Não no nível de *escopo*. Persistem ambiguidades de *regras funcionais* — definição de
   "próximos eventos", "tarefa pendente", "tarefa atrasada", "meta ativa", valores de status de
   tarefa e forma de medir progresso de meta. Elas **não bloqueiam** a Task 1.3 e pertencem às
   tasks de Conceitos Centrais / Regras Funcionais da Fase 1 (ver Observações Futuras).

3. **Há funcionalidade prevista que deveria ser removida do MVP?**
   Não. Todas as funcionalidades previstas no escopo do CLAUDE.md rastreiam a um problema da
   Task 1.1 e geram valor claro (seção 4). Nada deve ser removido.

4. **Há funcionalidade essencial ausente do MVP?**
   Não. O conjunto atual é suficiente para entregar o valor da visão. Itens como vínculo
   Meta→Tarefa/Evento e recorrência são desejáveis, porém **não essenciais**, e ficam como
   candidatos futuros.

**Recomendação: Prosseguir para a Task 1.3.** As definições em aberto são de regras funcionais
e devem ser tratadas no momento apropriado da Fase 1, sem bloquear o avanço.

---

## Observações Futuras

- **OF (Task 1.2-a).** Definir, em Regras Funcionais: valores de status da tarefa; regra de
  "tarefa atrasada"; janela de "próximos eventos"; critério de "meta ativa"; forma de medir
  "progresso" da meta.
- **OF (Task 1.2-b).** Avaliar, pós-MVP, o vínculo explícito Meta → Tarefas/Eventos
  (conceito previsto no CLAUDE.md, fora do MVP).
- **OF (Task 1.2-c).** Reposicionar formalmente a recorrência de eventos no roadmap de
  evoluções futuras (Fase 5).
