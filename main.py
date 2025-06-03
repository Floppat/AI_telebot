import telebot

from config import API_TOKEN, path
from ya import Ai
from db import DB_Manager


bot = telebot.TeleBot(API_TOKEN)
dab = DB_Manager(path)


def handle_AI(message, additional):
    bot.send_chat_action(message.chat.id,'typing')
    ai = Ai(dab.read(message.chat.id)) # загрузка памяти
    ai.new_prompt(additional + message.text) # вписываю запрос
    bot.reply_to(message, asis := ai.gpt()) # генерирую ответ
    ai.asis_ans(asis) # сохраняю ответ
    dab.update(message.chat.id, ai.get_history()) # обновляю бд

def check_reg(message):
    try:
        dab.read(message.chat.id)
    except IndexError:
        bot.reply_to(message, 'используй /start чтобы начать')
        return
    

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    try:
        dab.read(message.chat.id)
    except IndexError:
        if  message.from_user.id == message.chat.id:
            dab.new_id(message.chat.id, 'user') 
        else:
            dab.new_id(message.chat.id, 'chat')
    bot.reply_to(message, "Привет, чем я могу помочь?")
    
@bot.message_handler(func=lambda message: True)
def echo_message(message): # message: telebot.types.Message
    if message.from_user.id == message.chat.id: #проверка - групповой чат или лс
        check_reg(message)
        handle_AI(message, '')
    elif (message.text is not None and ("@" + str(bot.get_me().username)) in message.text) or (message.reply_to_message is not None and message.reply_to_message.from_user.id == bot.get_me().id): # нечто сложное что написал не я
        check_reg(message)
        handle_AI(message, f'{message.from_user.full_name} написал: ')
    else:
        pass


bot.infinity_polling()
