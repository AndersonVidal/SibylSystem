# CLAUDE.md

## Projeto

Nome: SibylSystem

Repositório:
https://github.com/AndersonVidal/SibylSystem

---

# Visão

SibylSystem é uma plataforma pessoal de organização e acompanhamento de vida.

Seu objetivo é centralizar compromissos, tarefas, metas e informações relevantes para auxiliar o usuário na tomada de decisões e no acompanhamento de seus objetivos.

O sistema deve funcionar como um painel pessoal de gestão da vida, permitindo que o usuário tenha clareza sobre:

* O que precisa fazer
* O que está fazendo
* O que pretende alcançar
* Como está evoluindo ao longo do tempo

Inicialmente o sistema possuirá apenas um usuário.

---

# Missão do Produto

SibylSystem é um sistema pessoal de organização e apoio à tomada de decisões.

Seu objetivo é centralizar informações relevantes da vida do usuário para reduzir carga mental, aumentar clareza e facilitar o acompanhamento de objetivos de curto, médio e longo prazo.

Fornecer uma visão clara e organizada da vida pessoal através de:

* Planejamento
* Execução
* Acompanhamento
* Reflexão

O sistema deve reduzir carga mental e facilitar a priorização do que realmente importa.

---

# Princípios do Produto

Toda decisão funcional deve priorizar:

1. Simplicidade
2. Clareza
3. Rapidez de uso
4. Baixa manutenção
5. Evolução incremental
6. Centralização das informações
7. Redução de carga cognitiva

Quando houver dúvida entre uma solução simples e uma sofisticada, a simples deve ser escolhida.

---

# Conceitos Fundamentais

## Evento

Representa algo que ocorre em uma data específica.

Exemplos:

* Natação
* Academia
* Consulta médica
* Aula de inglês
* Reunião

Características:

* Possui data
* Pode possuir horário
* Pode ser recorrente futuramente

---

## Tarefa

Representa uma ação que precisa ser executada.

Exemplos:

* Comprar guarda-roupa
* Pagar conta
* Organizar apartamento
* Comprar perfume

Características:

* Pode possuir prazo
* Pode não possuir prazo
* Possui status

---

## Meta

Representa um objetivo a ser alcançado.

Exemplos:

* Comprar apartamento
* Concluir pós-graduação
* Melhorar tempo nos 50m livre
* Construir o RAIRE
* Ser aprovado em concurso

Características:

* Possui horizonte temporal
* Possui progresso
* Pode originar tarefas e eventos

---

# Escopo do MVP

O MVP deve conter apenas:

## Autenticação

* Login
* Logout
* Usuário único

## Eventos

* Criar
* Editar
* Excluir
* Listar

## Tarefas

* Criar
* Editar
* Excluir
* Concluir
* Listar

## Metas

* Criar
* Editar
* Excluir
* Atualizar progresso
* Listar

## Dashboard

* Eventos de hoje
* Próximos eventos
* Tarefas pendentes
* Tarefas atrasadas
* Metas ativas

---

# Fora do Escopo do MVP

Não implementar sem validação explícita:

* Multiusuário
* Compartilhamento
* Aplicativo mobile
* IA
* Chat
* Gamificação
* Integrações externas
* Sincronização com calendários externos
* Notificações automáticas
* Integração com e-mail
* Integração com WhatsApp

---

# Filosofia Arquitetural

A arquitetura deve permanecer simples.

Preferir:

* Monólito modular
* Componentes desacoplados
* Código legível
* Baixo acoplamento
* Alta coesão

Evitar:

* Microserviços
* Event Sourcing
* CQRS sem necessidade
* Complexidade prematura

---

# Filosofia de Desenvolvimento

O projeto será desenvolvido de forma iterativa.

Regras:

* Trabalhar uma task por vez
* Não antecipar tarefas futuras
* Não implementar funcionalidades não solicitadas
* Sempre explicar decisões importantes
* Aguardar validação ao final de cada task

---

# Gestão de Mudanças

Mudanças que afetem:

* Modelo de dados
* Arquitetura
* Fluxos do usuário
* Conceitos fundamentais

Devem ser comunicadas antes da implementação.

---

# Critérios de Qualidade

Todo código deve priorizar:

* Legibilidade
* Testabilidade
* Simplicidade
* Consistência
* Manutenibilidade

Comentários devem explicar decisões e não repetir código.

---

# Roadmap

## Fase 0

Fundação do Projeto

* CLAUDE.md
* Visão do produto
* Processo de desenvolvimento

## Fase 1

Definição do Produto

* Escopo do MVP
* Conceitos centrais
* Fluxos
* Telas
* Regras funcionais

## Fase 2

Arquitetura

* Stack tecnológica
* Modelo de dados
* Estrutura dos módulos

## Fase 3

Setup Técnico

* Ambiente de desenvolvimento
* Banco de dados
* Autenticação
* Estrutura inicial

## Fase 4

Implementação do MVP

* Eventos
* Tarefas
* Metas
* Dashboard

## Fase 5

Evoluções Futuras

Definidas após validação do MVP.

---

# Fonte da Verdade

Este documento é a principal referência para decisões do projeto.

Quando houver conflito entre uma task e este documento, o conflito deve ser explicitamente informado antes da implementação.
