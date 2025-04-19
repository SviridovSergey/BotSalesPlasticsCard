from pickle import TRUE
import telebot
bot = telebot.TeleBot("8086181539:AAG8tdzVKEQONpcb9F8tldJiKaXxu9nypGs")

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id,"куку")
    print("func 1 is started")
@bot.message_handler(commands=["пися"])
def pisy(message):
    bot.send_message(message.chat.id,"попа член")




bot.polling(none_stop=True)