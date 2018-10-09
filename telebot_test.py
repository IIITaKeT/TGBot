import telebot
import time, re
import bot_supporter

# with open("C:\TGBot_config.txt", 'r') as conf:
#     middle = conf.readline()
#     bot_token = middle.split("=")[1]
#     conf.close()

bot = telebot.TeleBot(bot_token)

from telebot import apihelper
apihelper.proxy = {
    'https' : 'socks5h://telegram:telegram@u0k12.tgproxy.me:1080',
    'http' : 'socks5h://telegram:telegram@u0k12.tgproxy.me:1080'
}

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

if __name__ == '__main__':
    bot.polling(none_stop=True)