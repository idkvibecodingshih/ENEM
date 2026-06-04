from openai import OpenAI
from rag import RAG
from datetime import datetime
import re

class IA:
    def __init__(self, bot, selfObj=None):
        self.Obj = selfObj
        self.bot = bot
        self.rag = RAG()
        self.behavior = ""

        for line in open("internals\\behavior.txt", "r", encoding="utf-8").readlines():
            self.behavior += line.strip() + "\n"

        self.client = OpenAI(
            api_key="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",
            base_url="https://api.groq.com/openai/v1"
        )

        print("IA Connection established - Ollama API")
    


    def ask(self, msg):
        # First, search the RAG for relevant information
        context, scores = self.rag.search(msg.text)
        for c, s in zip(context, scores):
            print(f"RAG Result (Score: {s}): {c}\n")
        
        context_str = "\n".join(context)
        print(f"\n\n{context_str}")

        memory_text = "\n".join(
            f"{m['role']}: {m['content']}"
            for m in self.Obj.memories.get(msg.chat.id, [])[-20:]
        )


        response = self.client.chat.completions.create(
            model="qwen/qwen3-32b",
            messages=[
                {
                    "role": "system",
                    "content": self.behavior
                },
                {
                    "role": "system",
                    "content": f"""INFORMAÇÕES INTERNAS

Prioridade das informações:

1. Mensagens recentes da conversa.
2. Memórias da conversa.
3. Contexto recuperado pelo RAG.
4. Conhecimento geral do modelo.

REGRAS DE USO DE MEMÓRIA E RAG

1. Considere primeiro a mensagem atual do usuário.

2. Utilize MEMÓRIAS apenas quando elas forem diretamente relevantes para responder à pergunta atual.

3. Utilize o CONTEXTO RAG apenas quando ele contiver informações relacionadas à pergunta atual.

4. Nunca trate o CONTEXTO RAG como sugestão. Considere-o uma fonte factual.

5. Quando utilizar informações do CONTEXTO RAG:

   * Responda apenas com informações presentes no contexto.
   * Não adicione detalhes próprios.
   * Não complete lacunas.
   * Não faça estimativas.
   * Não faça suposições.

6. Se a resposta não estiver explicitamente presente no CONTEXTO RAG:

   * Ignore o contexto.
   * Responda usando conhecimento geral apenas se a pergunta não depender do contexto.
   * Caso a pergunta dependa do contexto para ser respondida corretamente, diga que não possui informações suficientes.

7. Nunca invente:

   * Valores
   * Preços
   * Datas
   * Estatísticas
   * Quantidades
   * Nomes
   * Mecânicas
   * Requisitos
   * Rankings

8. Se houver dúvida entre duas interpretações, escolha a opção mais conservadora e admita incerteza.

9. É preferível responder "não sei" do que fornecer uma informação não presente nas memórias, no contexto ou no conhecimento confiável disponível.

10. Não transforme exemplos em fatos.

11. Não deduza relações que não estejam explicitamente descritas.

12. Se o contexto mencionar:
    "Dragon = 5.13B"
    e não mencionar outros valores,
    você NÃO pode afirmar quanto vale qualquer outro item.

13. Se o contexto não fornecer dados suficientes para comparar dois itens, informe que a comparação não pode ser feita com as informações disponíveis.


DATA ATUAL:
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

MEMÓRIAS:
{memory_text}

CONTEXTO FACTUAL (FONTE DE VERDADE)

As informações abaixo são a referência principal para responder.
Se houver conflito entre seu conhecimento e este contexto, utilize o contexto.

{context_str}"""
                },
                {
                    "role": "user",
                    "content": msg.text
                }
            ]
        )


        resposta_limpa = re.sub(r'<tool_call>.*?</tool_call>', '', response.choices[0].message.content, flags=re.DOTALL)

        return resposta_limpa.strip()
    


    def setup_memories(self, chat_id):
        if chat_id not in self.Obj.memories:
            self.Obj.memories[chat_id] = []

    def WipeMem(self, chat_id):
        if chat_id in self.Obj.memories:
            self.Obj.memories[chat_id] = []
        else:
            print(f"No memories found for chat {chat_id}.")

    def add_user_message(self, chat_id, message):
        if chat_id not in self.Obj.memories:
            self.Obj.memories[chat_id] = []
        self.Obj.memories[chat_id].append({"role": "user", "content": message})

    def add_assistant_message(self, chat_id, message):
        if chat_id not in self.Obj.memories:
            self.Obj.memories[chat_id] = []
        self.Obj.memories[chat_id].append({"role": "assistant", "content": message})