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
        self.internal_info = ""

        for line in open("internals\\behavior.txt", "r", encoding="utf-8").readlines():
            self.behavior += line.strip() + "\n"

        for line in open("internals\\internal_info.txt", "r", encoding="utf-8").readlines():
            self.internal_info += line.strip() + "\n"

        self.client = OpenAI(
            api_key="COLOQUE SUA API KEY GROQ",
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
                    "content": self.internal_info.format(
                        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        memories=memory_text,
                        context=context_str
                    )
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
