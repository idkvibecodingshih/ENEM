import telebot
import pyfiglet
import webview

from IA import IA
TOKEN = "8859790251:AAHrMnvttZDkWAIfoMJv6uds3Rn82bpSQL0"

class Bot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.IA = IA(self.bot, selfObj=self)
        self.Object = self
        self.memories = {}


        pyfiglet.print_figlet("TelAI", font="slant")
        print("Ai powered Telegram Bot - Version 1.6.6")
    


    def start(self):
        @self.bot.message_handler(commands=['newchat'])
        def newchat(msg):
            self.IA.WipeMem(msg.chat.id)
            self.bot.reply_to(msg, "New chat started! Memories cleared.")


        @self.bot.message_handler(func=lambda msg: True)
        def handle_message(msg):
            self.IA.setup_memories(msg.chat.id)
            

            response = self.IA.ask(msg)
            self.IA.add_user_message(msg.chat.id, msg.text)
            self.IA.add_assistant_message(msg.chat.id, response)

            print(response)
            self.bot.reply_to(msg, response)

        self.bot.polling()


if __name__ == "__main__":
    bot = Bot(TOKEN)
    bot.start()