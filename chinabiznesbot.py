import config
import telebot
from telebot import types
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

bot = telebot.TeleBot(config.token) #должно быть в начале. Вызывает токен
cred = credentials.Certificate('C:/Users/Kokoto/Desktop/madeinchina/key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://chinabiznesbot.firebaseio.com/' })


@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    current = db.reference("/users/"+str(user_id)+"/current").get()
    
    db.reference("/users/"+str(user_id)).update({"current": "login"})
    bot.send_message(message.from_user.id,"Привет, я Дана, обучаю вас как работать с китайскими поставщиками. Введите свое ФИО:")
    
    
@bot.message_handler(content_types = ['text', 'contact'])
def start_dialog(message):
    user_id = message.from_user.id
    current = db.reference("/users/"+str(user_id)+"/current").get()
    if current == "login":
        db.reference("/users/"+str(user_id)).update({"login": message.text})
        db.reference("/users/"+str(user_id)).update({"current": "password"})
        bot.send_message(message.from_user.id,"Введите пароль:")
        
    elif current == "password":
        db.reference("/users/"+str(user_id)).update({"password": message.text})
        password = db.reference("/users/"+str(user_id)+"/password").get()
        if password == "12345":
            user_markup = telebot.types.ReplyKeyboardMarkup(True)
            user_markup.row("Введение", "Доставка товара")
            user_markup.row("Торговые площадки", "Посредники")
            user_markup.row("Ссылки", "Контакты")
            bot.send_message(user_id,"Принято! Выберите кнопку",reply_markup = user_markup)
            db.reference("/users/"+str(user_id)).update({"current": "buttons"})
        else:
            bot.send_message(message.from_user.id,"Ошибка! Введите снова")

    elif current == "buttons":
        db.reference("/users/"+str(user_id)).update({"buttons": message.text})
        buttons = db.reference("/users/"+str(user_id)+"/buttons").get()
        if buttons == "Введение":
            bot.send_message(message.from_user.id,"A")
        elif buttons == "Доставка товара":
            bot.send_message(message.from_user.id,"B")
        elif buttons == "Торговые площадки":
            inline = types.InlineKeyboardMarkup()
            url_button = types.InlineKeyboardButton(text = "Alibaba", url = "http://bitpine.ru/verta/")
            inline.add(url_button)
            url_button = types.InlineKeyboardButton(text = "Aliexpress", url = "http://bitpine.ru/verta/")
            inline.add(url_button)
            url_button = types.InlineKeyboardButton(text = "1688", url = "http://bitpine.ru/verta/")
            inline.add(url_button)
            url_button = types.InlineKeyboardButton(text = "Taobao", url = "http://bitpine.ru/verta/")
            inline.add(url_button)
            bot.send_message(message.from_user.id,"Ссылки на торговые площадки", reply_markup = inline)
        elif buttons == "Посредники":
            bot.send_message(message.from_user.id,"D")
        elif buttons == "Ссылки":
            bot.send_message(message.from_user.id,"E")
        elif buttons == "Контакты":
            bot.send_message(message.from_user.id,"F")
        


bot.polling(none_stop=True)
