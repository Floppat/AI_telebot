import telebot
import config
import ya
import db

API_TOKEN = config.API_TOKEN

bot = telebot.TeleBot(API_TOKEN)

dab = db.DB_Manager(config.path)

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    print(type(message))
    try:
        dab.read(message.chat.id)
    except IndexError:
        if  message.from_user.id == message.chat.id:
            dab.new_user(message.chat.id) 
        else:
            dab.new_chat(message.chat.id)
    bot.reply_to(message, "Привет, чем я могу помочь?")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message): # message: telebot.types.Message
    try:
        dab.read(message.chat.id)
    except IndexError:
        bot.reply_to(message, 'используй /start чтобы начать')
        return
    if message.from_user.id == message.chat.id: #проверка - групповой чат или лс
        bot.send_chat_action(message.chat.id,'typing')
        ai = ya.Ai(dab.read(message.chat.id)['messages']) # загрузка памяти
        ai.new_prompt(message.text) # вписываю запрос
        bot.reply_to(message, asis := ai.gpt()) # генерирую ответ
        ai.asis_ans(asis) # сохраняю ответ
        dab.update(message.chat.id, ai.get_prompt()) # обновляю бд
    elif (message.text is not None and ("@" + str(bot.get_me().username)) in message.text) or (message.reply_to_message is not None and message.reply_to_message.from_user.id == bot.get_me().id): # нечто сложное что написал не я
        bot.send_chat_action(message.chat.id,'typing')
        ai = ya.Ai(dab.read(message.chat.id)['messages']) # загрузка памяти
        ai.new_prompt(f'{message.from_user.full_name} написал: {message.text}') # вписываю запрос
        bot.reply_to(message, asis := ai.gpt()) # генерирую ответ
        ai.asis_ans(asis) # сохраняю ответ
        dab.update(message.chat.id, ai.get_prompt()) # обновляю бд
    else:
        pass

bot.infinity_polling()
