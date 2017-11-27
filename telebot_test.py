import telebot
import time, re
import bot_supporter

bot_token = ""
bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def start(massage):
    bot.send_message(massage.chat.id,"Здравствуйте. Я знаю цены на все продукты, могу их вам подсказать")

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    query = re.findall("\w+", message.text)
    bot.send_message(message.chat.id, 'Окей, ищу')
    if len(query) >= 2:
        answer = bot_supporter.GetQuery("{x[0]}+{x[1]}".format(x = query))
    else:
        answer = bot_supporter.GetQuery(query[0])
    if not answer:
        bot.send_message(message.chat.id, 'Сорян, ничего нет')
    else:
        bot.send_message(message.chat.id,
                 """
                 Вот что нашел:
         <b>Средняя цена - {z[1]}р.</b>
                
         <b>Минимальная цена - {z[0][1]}р.</b>
    <i>{z[0][0]}</i>
         <b>Максимальная цена - {z[2][1]}р.</b>
    <i>{z[2][0]}</i>
                 """.format(z = answer), parse_mode="HTML")

bot.polling()
