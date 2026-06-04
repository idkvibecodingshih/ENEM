# TelAI - RAG Powered Telegram Assistant

TelAI é um assistente inteligente para Telegram desenvolvido em Python, integrando modelos de linguagem, memória conversacional e Retrieval-Augmented Generation (RAG).

O projeto foi criado com foco em experimentação prática de sistemas de IA, gerenciamento de contexto e personalização de comportamento de modelos através de conhecimento externo.

## Funcionalidades

* Integração com Telegram Bot API
* Suporte a múltiplos provedores de IA compatíveis com OpenAI API
* Sistema de memória por usuário
* Base de conhecimento utilizando RAG
* Recuperação semântica através de embeddings
* Comportamento customizável via prompts externos
* Gerenciamento de contexto dinâmico
* Arquitetura modular e extensível

## Arquitetura

```text
Telegram User
      │
      ▼
 Telegram Bot
      │
      ▼
 Message Processor
      │
      ├── Conversation Memory
      ├── RAG Search Engine
      └── Prompt Builder
              │
              ▼
         Language Model
              │
              ▼
           Response
```

## Tecnologias Utilizadas

* Python 3.11+
* PyTelegramBotAPI
* ChromaDB
* Sentence Transformers
* OpenAI SDK
* Ollama
* Groq API

## Sistema RAG

O mecanismo de Retrieval-Augmented Generation permite que o modelo consulte uma base de conhecimento indexada antes de responder ao usuário.

Fluxo:

1. Usuário envia mensagem
2. Geração de embedding da consulta
3. Busca semântica na base vetorial
4. Recuperação dos trechos mais relevantes
5. Construção do contexto
6. Geração da resposta

## Memória Conversacional

Cada chat possui um histórico independente que é utilizado para manter contexto entre mensagens.

Recursos:

* Histórico por usuário
* Limpeza manual de conversa
* Persistência durante execução
* Contexto dinâmico para respostas

## Objetivo do Projeto

Este projeto foi desenvolvido para estudar e implementar conceitos utilizados em assistentes modernos, incluindo:

* RAG (Retrieval-Augmented Generation)
* Engenharia de Prompt
* Embeddings
* Bancos Vetoriais
* Sistemas de Memória
* Integração de LLMs
* Arquiteturas de Agentes

## Status

Projeto em desenvolvimento ativo.

Atualmente possui:

* Sistema de memória
* Integração com Telegram
* Recuperação semântica via RAG
* Suporte a modelos locais e cloud
* Estrutura preparada para expansão futura

## Autor

Desenvolvido por Bernardo Gomes.
