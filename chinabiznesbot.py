import config
import telebot
from telebot import types
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

bot = telebot.TeleBot(config.token) #должно быть в начале. Вызывает токен
cred = credentials.Certificate('C:/Users/Kokoto/Documents/Github/madeinchina/key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://chinabiznesbot.firebaseio.com/' })


@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    current = db.reference("/users/"+str(user_id)+"/current").get()
    
    db.reference("/users/"+str(user_id)).update({"current": "login"})
    bot.send_message(message.from_user.id,"Привет, я ваш виртуальный помощник, обучаю вас как работать с китайскими поставщиками. Введите свое ФИО:")
    bot.send_message(message.from_user.id,"Хотите такого же бота? Пишите @vertaa_bot")
    
    
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
            user_markup.row("Предисловие", "Крупные рынки Китая")
            user_markup.row("Топ 10 товаров  из Китая")
            user_markup.row("Заключение")
            user_markup.row("Хочу задать вопрос")
            bot.send_message(user_id,"Принято! Выберите кнопку: ",reply_markup = user_markup)
            db.reference("/users/"+str(user_id)).update({"current": "buttons"})
        else:
            bot.send_message(message.from_user.id,"Ошибка! Введите снова")
    elif current == "buttons":
        db.reference("/users/"+str(user_id)).update({"buttons": message.text})
        buttons = db.reference("/users/"+str(user_id)+"/buttons").get()
        if buttons == "Предисловие":
            bot.send_message(message.from_user.id,"https://docs.google.com/document/d/18yPmG83qW6EKNE2Mg1eTrO-aSaBJ6k62rQlvjJW0fgk/edit?usp=sharing")
        elif buttons == "Крупные рынки Китая":
            user_markup = telebot.types.ReplyKeyboardMarkup(True)
            user_markup.row("Торговые площадки", "Как заказать товар")
            user_markup.row("Видео обучение", "Получить контакты посредников")
            user_markup.row("Назад")
            bot.send_message(user_id,"Крупные рынки Китая. Выберите интересующий вас пункт:",reply_markup = user_markup)
            db.reference("/users/"+str(user_id)).update({"current": "buttons2"})
            
        elif buttons == "Топ 10 товаров  из Китая":
            user_markup = telebot.types.ReplyKeyboardMarkup(True)
            user_markup.row("Список товаров")
            user_markup.row("Новинки товаров", "Видео")
            user_markup.row("Назад")
            bot.send_message(user_id,"Топ 10 товаров  из Китая. Выберите интересующий вас пункт:",reply_markup = user_markup)
            db.reference("/users/"+str(user_id)).update({"current": "buttons3"})
            
        elif buttons == "Заключение":
            bot.send_message(message.from_user.id,"https://docs.google.com/document/d/1PKHELQm48x2w5AhYC5v5egKQbOzIcaUKZD6HGjEMnVc/edit?usp=sharing")
        elif buttons == "Хочу задать вопрос":
            bot.send_message(message.from_user.id,"Чтобы задать вопрос, звоните или пишите на номер 87715987539")

    
    elif current == "buttons2":
        db.reference("/users/"+str(user_id)).update({"buttons2": message.text})
        buttons2 = db.reference("/users/"+str(user_id)+"/buttons2").get()
        if buttons2 == "Торговые площадки":
            bot.send_message(message.from_user.id,"http://bitpine.ru/themes/zwiebl-zwiebl_stellar/assets/images/рынки%20китая.png")
        elif buttons2 == "Как заказать товар":
            bot.send_message(message.from_user.id,"https://docs.google.com/document/d/1yNFw0m20ThwsVEyhoMRYKCGsCFldIKYPOY55moKFvVw/edit?usp=sharing")
        elif buttons2 == "Видео обучение":
            bot.send_message(message.from_user.id,"https://cloud.mail.ru/public/3DrN/1hPWngZT5")
            bot.send_message(message.from_user.id,"https://cloud.mail.ru/public/AFE7/xtGM9YALx")    
        elif buttons2 == "Получить контакты посредников":
            bot.send_message(message.from_user.id,"http://bitpine.ru/themes/zwiebl-zwiebl_stellar/assets/images/посредники%20номер.png")
        elif buttons2 == "Назад":
            user_markup = telebot.types.ReplyKeyboardMarkup(True)
            user_markup.row("Предисловие", "Крупные рынки Китая")
            user_markup.row("Топ 10 товаров  из Китая")
            user_markup.row("Заключение")
            user_markup.row("Хочу задать вопрос")
            bot.send_message(user_id,"Принято! Выберите кнопку: ",reply_markup = user_markup)
            db.reference("/users/"+str(user_id)).update({"current": "buttons"})

    elif current == "buttons3":
        db.reference("/users/"+str(user_id)).update({"buttons3": message.text})
        buttons3 = db.reference("/users/"+str(user_id)+"/buttons3").get()
        if buttons3 == "Список товаров":
            bot.send_message(message.from_user.id,"https://docs.google.com/spreadsheets/d/114tTBfmutAjVCyeckxONyOfDBjtd3nCwgbo20xlmMYI/edit?usp=sharing")
        elif buttons3 == "Новинки товаров":
            bot.send_message(message.from_user.id,"https://www.wish.com/   -  новинки товара ")
        elif buttons3 == "Видео":
            bot.send_message(message.from_user.id,"https://cloud.mail.ru/stock/e79L7t2E2nkbGviQRE4p8kBX")
        elif buttons3 == "Назад":
            user_markup = telebot.types.ReplyKeyboardMarkup(True)
            user_markup.row("Предисловие", "Крупные рынки Китая")
            user_markup.row("Топ 10 товаров  из Китая")
            user_markup.row("Заключение")
            user_markup.row("Хочу задать вопрос")
            bot.send_message(user_id,"Принято! Выберите кнопку",reply_markup = user_markup)
            db.reference("/users/"+str(user_id)).update({"current": "buttons"})

            
bot.polling(none_stop=True)
