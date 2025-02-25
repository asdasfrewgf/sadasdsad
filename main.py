#import telebot
import threading
from glob import glob
from tabnanny import verbose
import telebot
from telebot import types
import time
from time import sleep
#import file
from config import *
#import random
import random
from random import randint
#import module db
import sqlite3
import re
import string
import subprocess
import sys
import os

#course
from pycoingecko import CoinGeckoAPI

bot = telebot.TeleBot(token, parse_mode="HTML")
print("BOT START")
api = CoinGeckoAPI()
print("API START")

# Получаем абсолютный путь к файлам
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
photo_path = os.path.join(BASE_DIR, 'startPhoto.jpg')
card_ru_path = os.path.join(BASE_DIR, 'cardRU.txt')
card_ua_path = os.path.join(BASE_DIR, 'cardUA.txt')
crypto_photo_path = os.path.join(BASE_DIR, 'crypto.jpg')
about_file_path = os.path.join(BASE_DIR, 'about.txt')

def read_file_content(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    return "Файл не найден"

def send_photo_safe(chat_id, file_path, caption):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as photo:
            bot.send_photo(chat_id, photo, caption=caption)
    else:
        bot.send_message(chat_id, "Ошибка: изображение не найдено")

@bot.message_handler(commands=["start", "menu"])
def start(message):
    db = sqlite3.connect(os.path.join(BASE_DIR, 'users.db'))
    sql = db.cursor()
    sql.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER,
            username TEXT,
            cash BIGINT,
            verif BOOL,
            sdelka INTEGER,
            luck INTEGER,
            val TEXT,
            mindep INTEGER
        )
    """)
    db.commit()
    sql.execute("""CREATE TABLE IF NOT EXISTS valute( 
        valute TEXT,
        stat BOOL
        )""")
    db.commit()
    sql.execute(f"SELECT valute FROM valute")
    data = sql.fetchone()
    if data is None:
        print("Create new table val")
        sql.execute(f"INSERT OR IGNORE INTO valute (valute, stat) VALUES('UAH','True');")
        db.commit()
    print(f"{message.chat.id} conected to db")
    sql.execute("""CREATE TABLE IF NOT EXISTS promo( 
        id INTEGER,
        prom TEXT,
        sum INTAGER
        )""")
    db.commit()
    sql.execute(f"SELECT id FROM promo")
    data = sql.fetchone()
    if data is None:
        print("Create new table promo")
        sql.execute(f"INSERT OR IGNORE INTO promo (id,prom, sum) VALUES({0},'0',{0});")
        db.commit()

    people_id = message.chat.id
    username = message.from_user.username
    sql.execute(f"SELECT id FROM users WHERE id = {people_id}")
    data = sql.fetchone()
    if data is None:
        sql.execute(f"INSERT OR IGNORE INTO users VALUES('{people_id}', '{username}', {0}, 'False', {0}, {0},'{0}', {500});")
        bot.send_message(chatAlert, f"🎯<b>Пользователь @{username} запустил бота</b>")

        db.commit() 
        print(f"{message.chat.id} новый юзер")
    sql.execute(f"SELECT * FROM users WHERE id = {people_id}")
    excepts = sql.fetchone()
    print(excepts)
    if excepts[6] == '0': 
        sql.execute("SELECT * FROM valute WHERE stat = 'True' ")
        datV = sql.fetchall()
        markups = types.InlineKeyboardMarkup(row_width=2)
        buttons = []
        for i in datV:
            button = types.InlineKeyboardButton(text= str(i[0]), callback_data = f"newwal_{i[0]}")
            buttons.append(button)
        markups.add(*buttons)
        bot.send_message(message.chat.id, "<b>💱Установите желаемую валюту</b>",reply_markup=markups)
    
    
    else:
        t = "❌"
        if excepts[3] == 'False':
            t = "❌"
        if excepts[3] == 'True':
            t = "✅"
        activity_user = random.randint(340,720)
        markup = types.InlineKeyboardMarkup(row_width = 2)
        but = types.InlineKeyboardButton("📈ECN счёт", callback_data="inv")
        but1 = types.InlineKeyboardButton("💰Кошелек", callback_data="wallet")
        but2 = types.InlineKeyboardButton("❓info", callback_data="info")
        but3 = types.InlineKeyboardButton("⚙️Настройки", callback_data="setings")
        but4 = types.InlineKeyboardButton("🛠Поддержка", url=f"https://t.me/{support}")
        markup.add(but,but1,but2,but3,but4)   
        markups = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        menu = types.KeyboardButton("🖱Главное меню")
        markups.add(menu)  
        bot.send_message(message.chat.id, "<b>🖱Главное меню</b>",reply_markup=markups)

        bot.send_photo(
            message.chat.id,
            open(os.path.abspath('startPhoto.jpg'), 'rb'),
            caption=f"👤Мой профиль\n\n🗣Имя: {message.from_user.first_name}\n🦾Верификация: {t}\n🤝Совершенных сделок: {excepts[4]}\n🏦Баланс {excepts[2]} {excepts[6]}\n🧑🏻‍💻Трейдеров онлайн: {activity_user}",
            reply_markup=markup
        )
    #referals
    referal = message.text.split(' ')[-1]
    db = sqlite3.connect('users.db')
    sql = db.cursor()
    sql.execute("""CREATE TABLE IF NOT EXISTS worker( 
        idW INTEGER,
        refid INTEGER,
        refusernames TEXT,
        refcash INTAGER,
        refverif BOOL,
        refsdelka INTAGER,
        refluck INTAGER,
        mindep INTAGER

        )""")
    db.commit() 
    sql.execute(f"SELECT refid FROM worker WHERE refid = {message.chat.id}")
    data = sql.fetchone()
    if data is None:
        print("Create new users")
        sql.execute(f"INSERT OR IGNORE INTO worker (idW, refid, refusernames, refcash, refverif, refsdelka, refluck, mindep) VALUES({0}, {0}, '{0}' ,{0}, '0', {0}, {0}, {500});")
        print(referal)
        db.commit() 

    if referal != '/start': 
        db = sqlite3.connect('users.db')
        sql = db.cursor()
        db.commit()
        sql.execute(f"SELECT refid FROM worker WHERE refid = {message.chat.id}")
        dats = sql.fetchone()
        if dats is None:
            sql.execute(f"SELECT * FROM users WHERE id = {message.chat.id}")
            exts = sql.fetchone()
            sql.execute(f"INSERT OR IGNORE INTO worker (idW,refid,refusernames,refcash,refverif,refsdelka,refluck) VALUES ('{referal}',{message.chat.id}, '{message.from_user.username}' ,{exts[2]}, '{exts[3]}', {exts[4]},{exts[5]});")
            print(referal)
            print(message.chat.id)
            print(exts[3])
            db.commit()
            sql.execute(f"SELECT username FROM users WHERE id = {message.chat.id}")
            data = sql.fetchone()
            bot.send_message(referal, f"➕ Новый рефирал зашел: @{message.from_user.username}\n🏡Перейти в меню мамонта: /{message.chat.id}")
            bot.send_message(chatAlert, f"👻<b>Реферал {message.from_user.username} зашел в бота\n👤Воркер: @{data[0]}</b>")
        else: 
            bot.send_message(message.chat.id,"Вы уже зарегистрированы")
    
    





def depositSumData(message):
    db = sqlite3.connect(os.path.join(BASE_DIR, 'users.db'))
    sql = db.cursor()
    sql.execute(f"SELECT * FROM users WHERE id = {message.chat.id}")
    datatU = sql.fetchone()
    dep = int(message.text)
    if dep < datatU[7]:
        bot.send_message(message.chat.id, f"❕Минимальный депозит {datatU[7]} {datatU[6]}</b>")
    if dep == datatU[7]:
        bot.send_message(message.chat.id,f"❕<b>Минимальный депозит {datatU[7]} {datatU[6]}</b>")
    if dep >= datatU[7]:
        if datas is None:
            if datatU[6] == 'RUB':
                cardW = open("cardRU.txt", "r")
                card = cardW.read()
                cardW.close()
                markup = types.InlineKeyboardMarkup(row_width = 2)
                but = types.InlineKeyboardButton("✅ Я оплатил", callback_data=f"YesDep_{dep}")
                markup.add(but)
                bot.send_photo(message.chat.id, open('CardPhoto.jpg', 'rb'), f"<b>🤵 Для пополнения баланса\n\n💳 Реквизиты : <code>{card}</code>\n💸Сумма к оплате: {dep} RUB\n💬 Комментарий : t{message.chat.id}\n\n⚠️Нажмите на реквизиты или комментарий, чтобы скопировать!\n\n⚠️Если вы не можете указать комментарий, после оплаты пришлите чек/скриншот или же квитанцию в техническую поддержку.\n\n⚠️ 🛠 Тех.Поддержка - @{support}</b>",reply_markup=markup)        
                bot.send_message(chatAlert, f"<b>🔔 Мамонт @{message.from_user.username} на моменте пополнения\nСумма: {dep} RUB</b>")
            if datatU[6] == 'UAH':
                cardW = open("cardUA.txt", "r")
                card = cardW.read()
                cardW.close()
                markup = types.InlineKeyboardMarkup(row_width = 2)
                but = types.InlineKeyboardButton("✅ Я оплатил", callback_data=f"YesDep_{dep}")
                markup.add(but)
                bot.send_photo(message.chat.id, open('CardPhoto.jpg', 'rb'), f"<b>🤵 Для пополнения баланса\n\n💳 Реквизиты : <code>{card}</code>\n💸Сумма к оплате: {dep} UAH\n💬 Комментарий : t{message.chat.id}\n\n⚠️Нажмите на реквизиты или комментарий, чтобы скопировать!\n\n⚠️Если вы не можете указать комментарий, после оплаты пришлите чек/скриншот или же квитанцию в техническую поддержку.\n\n⚠️ 🛠 Тех.Поддержка - @{support}</b>",reply_markup=markup)        
                bot.send_message(chatAlert, f"<b>🔔 Мамонт @{message.from_user.username} на моменте пополнения\nСумма: {dep} UAH</b>")
        else:
            if datatU[6] == 'RUB':
                idWork = datas[0]
                print(datas[0])
                cardW = open("cardRU.txt", "r")
                card = cardW.read()
                cardW.close()
                markup = types.InlineKeyboardMarkup(row_width = 2)
                but = types.InlineKeyboardButton("✅ Я оплатил", callback_data=f"YesDep_{dep}")
                markup.add(but)
                bot.send_message(idWork, f"❕<b>Информация по мамонту: @{datas[2]}</b>\n🔅<i>Мамонт зашел на пополнение баланса!</i>")
                bot.send_photo(message.chat.id, open('CardPhoto.jpg', 'rb'), f"<b>🤵 Для пополнения баланса\n\n💳 Реквизиты : <code>{card}</code>\n💸Сумма к оплате: {dep} RUB\n💬 Комментарий : t{message.chat.id}\n\n⚠️Нажмите на реквизиты или комментарий, чтобы скопировать!\n\n⚠️Если вы не можете указать комментарий, после оплаты пришлите чек/скриншот или же квитанцию в техническую поддержку.\n\n⚠️ 🛠 Тех.Поддержка - @{support}</b>",reply_markup=markup)        
                bot.send_message(chatAlert, f"<b>🔔 Мамонт @{message.from_user.username} на моменте пополнения\nСумма: {dep} RUB</b>")
            if datatU[6] == 'UAH':
                idWork = datas[0]
                print(datas[0])
                cardW = open("cardUA.txt", "r")
                card = cardW.read()
                cardW.close()
                markup = types.InlineKeyboardMarkup(row_width = 2)
                but = types.InlineKeyboardButton("✅ Я оплатил", callback_data=f"YesDep_{dep}")
                markup.add(but)
                bot.send_message(idWork, f"❕<b>Информация по мамонту: @{datas[2]}</b>\n🔅<i>Мамонт зашел на пополнение баланса!</i>")
                bot.send_photo(message.chat.id, open('CardPhoto.jpg', 'rb'), f"<b>🤵 Для пополнения баланса\n\n💳 Реквизиты : <code>{card}</code>\n💸Сумма к оплате: {dep} UAH\n💬 Комментарий : t{message.chat.id}\n\n⚠️Нажмите на реквизиты или комментарий, чтобы скопировать!\n\n⚠️Если вы не можете указать комментарий, после оплаты пришлите чек/скриншот или же квитанцию в техническую поддержку.\n\n⚠️ 🛠 Тех.Поддержка - @{support}</b>",reply_markup=markup)        
                bot.send_message(chatAlert, f"<b>🔔 Мамонт @{message.from_user.username} на моменте пополнения\nСумма: {dep} UAH</b>")



@bot.message_handler(commands=["coder"])
def coder(message):
    db = sqlite3.connect('users.db')
    sql = db.cursor()
    markup = types.InlineKeyboardMarkup(row_width = 2)
    but = types.InlineKeyboardButton("ОчиститьБД", callback_data="cleardb")
    but1 = types.InlineKeyboardButton("Рассылка воркерам", callback_data="alertWork")
    markup.add(but,but1)
    bot.send_message(message.chat.id,"Кодер панель!",reply_markup=markup)

def alertW(message):
    msg = message.text
    bot.send_message(chatPay, f"<b>{msg}</b>")
    bot.send_message(message.chat.id, "Готово")
@bot.message_handler(commands=["admin"])
def admin(message):
    if message.chat.id in admins:
        markup = types.InlineKeyboardMarkup(row_width = 1)
        but = types.InlineKeyboardButton("Установить🇷🇺💳", callback_data="setCardRu")
        but1 = types.InlineKeyboardButton("Установить🇺🇦💳", callback_data="setCardUA")
        but2 = types.InlineKeyboardButton("💱Установить Валюты💱", callback_data="setWal")
        markup.add(but,but1,but2)
        bot.send_message(message.chat.id,"🤴Панель администратора🤴",reply_markup=markup)
        
            

def SetCardData(message):
    try:
        cards = int(message.text)
        files = open('cardUA.txt', 'w')
        files.write(str(cards))
        files.close()
        bot.send_message(message.chat.id,f"<b>✅Карта: {cards} успешно установленна!</b>")
    except:
        markup = types.InlineKeyboardMarkup(row_width = 2)
        but = types.InlineKeyboardButton("💳Установить карту💳", callback_data="setCard")
        markup.add(but)
        bot.send_message(message.chat.id, "<b>🤦Ты даун?Цифры вводи!🤦</b>",reply_markup=markup)


def SetCardDataRU(message):
    try:
        cardss = int(message.text)
        files = open('cardRU.txt', 'w')
        files.write(str(cardss))
        files.close()
        bot.send_message(message.chat.id,f"<b>✅Карта: {cardss} успешно установленна!</b>")
    except:
        markup = types.InlineKeyboardMarkup(row_width = 2)
        but = types.InlineKeyboardButton("💳Установить карту💳", callback_data="setCard")
        markup.add(but)
        bot.send_message(message.chat.id, "<b>🤦Ты даун?Цифры вводи!🤦</b>",reply_markup=markup)



@bot.message_handler(content_types=['text'])
def opensMamonts(message):
    if message.text == "/worker":
        menu_worker(message)
    if message.text == "🖱Главное меню":
        db = sqlite3.connect('users.db')
        sql = db.cursor()
        sql.execute(f"SELECT * FROM users WHERE id = {message.from_user.id}")
        excepts = sql.fetchone()
        s = "❌"
        if excepts[3] == 'False':
            s = "❌"
        if excepts[3] == 'True':
            s = "✅"
        activity_user = random.randint(340, 720)
        markup = types.InlineKeyboardMarkup(row_width=2)
        but = types.InlineKeyboardButton("📈ECN счёт", callback_data="inv")
        but1 = types.InlineKeyboardButton("💰Кошелек💰", callback_data="wallet")
        but2 = types.InlineKeyboardButton("❓info❓", callback_data="info")
        but3 = types.InlineKeyboardButton("⚙️Настройки", callback_data="setings")
        but4 = types.InlineKeyboardButton("🛠Поддержка", url=f"https://t.me/{support}")

        markup.add(but, but1, but2, but3, but4)

        # Получаем абсолютный путь к файлу
        photo_path = os.path.abspath('startPhoto.jpg')

        # Отправляем фото с проверкой
        send_photo_with_check(
            bot,
            message.chat.id,
            photo_path,
            f"👤Мой профиль\n\n🗣Имя: {message.from_user.first_name}\n🦾Верификация: {s}\n🤝Совершенных сделок: {excepts[4]}\n🧑🏻‍💻Трейдеров онлайн: {activity_user}",
            reply_markup=markup
        )

    else:
        db = sqlite3.connect('users.db')
        sql = db.cursor()
        idMamont = message.text.split('/')[-1]
        sql.execute(f"SELECT refid FROM worker")
        dataa = sql.fetchall()
        print(dataa)
        try:
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sql.execute(f"SELECT * FROM worker WHERE refid = {idMamont}")
            dataMamont = sql.fetchone()
            sql.execute(f"SELECT * FROM users WHERE id = {idMamont}")
            dataWork = sql.fetchone()
            sql.execute(f"SELECT refid FROM worker WHERE idW = {message.chat.id}") 
            idWorks = message.chat.id
            data = sql.fetchall()
            for idWorks in data:
                print(dataMamont[4])
                ver = "ERROR"
                if dataMamont[4] == "False":
                    ver = "✖️"
                if dataMamont[4] == "True":
                    ver = "✔️"
                lucks = "ERROR"
                if dataMamont[6] == 0:
                    lucks = "Only Win👍"
                if dataMamont[6] == 1:
                    lucks = "Only Lose👎"
                if dataMamont[6] == 2:
                    lucks = "Верификация🔞"

                markup = types.InlineKeyboardMarkup(row_width = 1)
                balance = types.InlineKeyboardButton("💰баланс", callback_data=f"balanceMamont_{idMamont}")
                verifickation = types.InlineKeyboardButton("🖥верификация", callback_data=f"verMamont_{idMamont}")
                luck = types.InlineKeyboardButton("☘️удача", callback_data=f"luckMamont_{idMamont}")
                setDep = types.InlineKeyboardButton("💱МинДеп", callback_data=f"SetMinDep_{idMamont}")
                alert = types.InlineKeyboardButton("💭смс мамонту", callback_data=f"alertmamont_{idMamont}")
                buton_dell_mamunt = types.InlineKeyboardButton("🚮Удалить Мамонта", callback_data=f"delMamonts_{idMamont}")
                markup.add(balance,verifickation,luck,setDep,alert,buton_dell_mamunt)
            sql.execute(f"SELECT * FROM users WHERE id = {idMamont}")
            datatU = sql.fetchone()
            bot.send_message(message.chat.id, f"<b>🦣Мамонт @{dataMamont[2]}\n💰Баланс: {dataMamont[3]} {datatU[6]}\n🖥Верификация: {ver}\n☘️Удача: {lucks}\n⚜️Минимальный депозит: {dataMamont[7]} {dataWork[6]}</b>",reply_markup=markup)
        except:
            pass
        

@bot.message_handler(commands=["worker"])
def menu_worker(message):
    db = sqlite3.connect('users.db')
    sql = db.cursor()
    db.commit()
    sql.execute(f"SELECT COUNT(refid) FROM worker WHERE idW = {message.chat.id}")
    uid = sql.fetchone()
    markup = types.InlineKeyboardMarkup(row_width = 2)
    but = types.InlineKeyboardButton("🦣 Мои мамонты", callback_data=f"MyMamont")
    but1 = types.InlineKeyboardButton("➕ Создать промокод", callback_data=f"AddPromo")
    but4 = types.InlineKeyboardButton("Реф.Ссылка", url=f"https://t.me/{botName}?start={message.chat.id}")
    markup.add(but,but1,but4)
    bot.send_message(message.chat.id, f"<b>⚜️Панель воркера:\n\n🦣Мамонтов: {uid[0]}\n💳Карта для вывода:: 5169155129365688\n🧊Cсылка:</b><code>https://t.me/{botName}?start={message.chat.id}</code>",reply_markup=markup)
    
        
def myMamont(message):
    db = sqlite3.connect('users.db')
    sql = db.cursor()
    ref_text = f"Мои рефералы: \n"
    data = sql.execute(f"SELECT refid,refusernames,refcash,refverif,refsdelka,refluck FROM worker WHERE idW = {message.chat.id}").fetchall()
    for user in data:
        id = user[0]
        username = user[1]
        ref_text = ref_text + f"🆔: <b>/{id}</b>--- 👨‍🦱: @{username}---\n\n"
    markup = types.InlineKeyboardMarkup(row_width = 2)
    buton_mamunt = types.InlineKeyboardButton("➕Добавить мамонтов", callback_data="menuMamont")
    buton_dell_mamunt = types.InlineKeyboardButton("➖Удалить Мамонта", callback_data="delMamont")
    markup.add(buton_mamunt,buton_dell_mamunt) 
    bot.send_message(message.chat.id, ref_text,reply_markup=markup) 
    

def setDepMin(message, idd):
    db = sqlite3.connect('users.db')
    sql = db.cursor()
    msg = int(message.text)
    sql.execute(f"UPDATE worker SET mindep = {msg} WHERE refid = {idd}")
    sql.execute(f"UPDATE users SET mindep = {msg} WHERE id = {idd}")
    db.commit()
    bot.send_message(message.chat.id, "<b>✅Готово</b>")

def alertM(message,idd):
    msg = message.text
    bot.send_message(idd,f"🔔<b>Новове сообщение</b>:\n\n {msg}")
    bot.send_message(message.chat.id, "<b>✅Готово</b>")
def menuMamont(message):
    idMamont = bot.send_message(message.chat.id, "Введите id мамонта: ")
    bot.register_next_step_handler(idMamont,setDataMamontMenu)

def delMamont(message):
    idMamont = bot.send_message(message.chat.id, "Введите id мамонта: ")
    bot.register_next_step_handler(idMamont,setDataMamontDell)

def setDataMamontDell(message):
    try:
        idMamont = message.text
        db = sqlite3.connect('users.db')
        sql = db.cursor()
        sql.execute(f"DELETE FROM worker WHERE refid = {idMamont}")
        db.commit()
        sql.execute(f"SELECT * FROM users WHERE id = {idMamont}")
        name = sql.fetchone()
        print(name[1])
        bot.send_message(message.chat.id, f"🗑<b>Мамонт @{name[1]} Успешно удален</b>")
    except:
        bot.send_message(message.chat.id, f"<b>Ошибка удаления</b>")

def setDataMamontMenu(message):
    try:
        idMamont = message.text 
        db = sqlite3.connect('users.db')
        sql = db.cursor()
        sql.execute(f"SELECT username FROM users WHERE id = {idMamont}")
        datsUs = sql.fetchone()
        sql.execute(f"SELECT refid FROM worker WHERE refid = {idMamont}")
        data = sql.fetchone()
        if data is None:
            sql.execute(f"INSERT OR IGNORE INTO worker (idW, refid, refusernames, refcash, refverif, refsdelka, refluck, mindep) VALUES({message.chat.id}, {idMamont}, '{datsUs[0]}', {0}, 'False', {0}, {0}, {500});")
            db.commit() 
        bot.send_message(message.chat.id, f"✅<b>Мамонт @{datsUs[0]} успешно добавлен!\n🏡Чтобы зайти в меню мамонта нажми не => /{idMamont}</b>")
    except:
        bot.send_message(message.chat.id, "❌Мамонт не запустил бота!❌")



@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    req = call.data.split('_')
    if call.message:
        if call.data == "alertWork":
            msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Введи текст рассылки:")
            bot.register_next_step_handler(msg, alertW)
        if call.data == "menu":
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sql.execute(f"SELECT * FROM users WHERE id = {call.from_user.id}")
            excepts = sql.fetchone()
            s = "❌"
            if excepts[3] == 'False':
                s = "❌"
            if excepts[3] == 'True':
                s = "✅"
            activity_user = random.randint(340, 720)
            markup = types.InlineKeyboardMarkup(row_width=2)
            but = types.InlineKeyboardButton("📈ECN счёт", callback_data="inv")
            but1 = types.InlineKeyboardButton("💰Кошелек💰", callback_data="wallet")
            but2 = types.InlineKeyboardButton("❓info❓", callback_data="info")
            but3 = types.InlineKeyboardButton("⚙️Настройки", callback_data="setings")
            but4 = types.InlineKeyboardButton("🛠Поддержка", url=f"https://t.me/{support}")

            markup.add(but, but1, but2, but3, but4)

            # Получаем абсолютный путь к файлу
            photo_path = os.path.abspath('startPhoto.jpg')

            # Отправляем фото с проверкой
            send_photo_with_check(
                bot,
                call.message.chat.id,
                photo_path,
                f"👤Мой профиль\n\n🗣Имя: {call.from_user.first_name}\n🦾Верификация: {s}\n🤝Совершенных сделок: {excepts[4]}\n🧑🏻‍💻Трейдеров онлайн: {activity_user}",
                reply_markup=markup
            )
        if call.data == "RUB":
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sql.execute(f"UPDATE users SET val = 'RUB' WHERE id = {call.from_user.id}")
            db.commit()
            markup = types.InlineKeyboardMarkup(row_width = 2)
            menu = types.InlineKeyboardButton("Меню👉🏻", callback_data=f"menu")
            markup.add(menu) 
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text=f"👍 Валюта успешно установленна!",reply_markup=markup)
        if req[0] == "newwal":
            vals = req[1]
            print(vals)
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sql.execute(f"UPDATE users SET val = '{vals}' WHERE id = {call.from_user.id}")
            db.commit()
            markup = types.InlineKeyboardMarkup(row_width = 2)
            menu = types.InlineKeyboardButton("Меню👉🏻", callback_data=f"menu")
            markup.add(menu) 
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text=f"👍 Валюта успешно установленна!",reply_markup=markup)
        if call.data == "cleardb":
            try:
                db = sqlite3.connect('users.db')
                sql = db.cursor()
                sql.execute(f"DELETE FROM worker WHERE refid = {0}")
                db.commit()
                bot.send_message(call.message.chat.id,"БД успешно очищенна!")
            except:
                bot.send_message(call.message.chat.id,"ДАУН?")
        if call.data == "setCardUA":
            cards = bot.send_message(call.message.chat.id, "Вводи новую карту: ")
            bot.register_next_step_handler(cards, SetCardData)
        if call.data == "setCardRu":
            cardss = bot.send_message(call.message.chat.id, "Вводи новую карту: ")
            bot.register_next_step_handler(cardss, SetCardDataRU)
        if call.data == "inv":
            markup = types.InlineKeyboardMarkup(row_width = 2)
            but = types.InlineKeyboardButton("Bitcoin", callback_data="BTC")
            but1 = types.InlineKeyboardButton("Ethereum", callback_data="ETH")
            but2 = types.InlineKeyboardButton("Tether", callback_data="TRC")
            but3 = types.InlineKeyboardButton("BNB", callback_data="BNB")
            but4 = types.InlineKeyboardButton("Ripple", callback_data="Ripple")
            but5 = types.InlineKeyboardButton("Nano", callback_data="Nano")
            but6 = types.InlineKeyboardButton("Dash", callback_data="Dash")
            but7 = types.InlineKeyboardButton("USD", callback_data="USD")
            but8 = types.InlineKeyboardButton("Cardano", callback_data="Cardano")
            markup.add(but,but1,but2,but3,but4,but5,but6,but7,but8)
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_photo(call.message.chat.id, open('crypto.jpg', 'rb'))
            bot.send_message(call.message.chat.id, "<b>📈Ваш личный ECN счет!\n\n💠Выберите монету, в которую хотите инвестировать средства:</b>",reply_markup=markup)
        if call.data == "Nano":
            t = api.get_price(ids='nano', vs_currencies='usd')['nano']['usd']
            r = random.randint(1,3)
            b = random.randint(1,2)
            s = "Даун"
            print(b)
            if b == 1:
                s = 'long📈'
            if b == 2:
                s = 'short📉'
            markup = types.InlineKeyboardMarkup(row_width = 2)
            but = types.InlineKeyboardButton("👉🏻Войти в сделку", callback_data=f"invs_{'Nano'}")
            markup.add(but)
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sql.execute(f"SELECT * FROM users WHERE id = {call.message.chat.id}")
            datatU = sql.fetchone()
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text=f"<b>🪙Монета: Nano\n\n💱Курс: {t} USD\n📈Последнее движение курса: {s}\n💸Изменение курса: {r}{datatU[6]}</b>",reply_markup=markup)

        
        if call.data == "Ripple":
            t = api.get_price(ids='ripple', vs_currencies='usd')['ripple']['usd']
            r = random.randint(18,50)
            b = random.randint(1,2)
            s = "Даун"
            print(b)
            if b == 1:
                s = 'long📈'
            if b == 2:
                s = 'short📉'
            markup = types.InlineKeyboardMarkup(row_width = 2)
            but = types.InlineKeyboardButton("👉🏻Войти в сделку", callback_data=f"invs_{'Ripple'}")
            markup.add(but)
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sql.execute(f"SELECT * FROM users WHERE id = {call.message.chat.id}")
            datatU = sql.fetchone()
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text=f"<b>🪙Монета: Ripple\n\n💱Курс: {t} USD\n📈Последнее движение курса: {s}\n💸Изменение курса: {r}{datatU[6]}</b>",reply_markup=markup)

        if call.data == "Dash":
            t = api.get_price(ids='dash', vs_currencies='usd')['dash']['usd']
            r = random.randint(22,32)
            b = random.randint(1,2)
            s = "Даун"
            print(b)
            if b == 1:
                s = 'long📈'
            if b == 2:
                s = 'short📉'
            markup = types.InlineKeyboardMarkup(row_width = 2)
            but = types.InlineKeyboardButton("👉🏻Войти в сделку", callback_data=f"invs_{'Dash'}")
            markup.add(but)
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sql.execute(f"SELECT * FROM users WHERE id = {call.message.chat.id}")
            datatU = sql.fetchone()
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text=f"<b>🪙Монета: Dash\n\n💱Курс: {t} USD\n📈Последнее движение курса: {s}\n💸Изменение курса: {r}{datatU[6]}</b>",reply_markup=markup)
        if call.data == "USD":
            t = api.get_price(ids='usd', vs_currencies='usd')['usd']['usd']
            r = random.uniform(0.5,1)
            b = random.randint(1,2)
            s = "Даун"
            print(b)
            if b == 1:
                s = 'long📈'
            if b == 2:
                s = 'short📉'
            markup = types.InlineKeyboardMarkup(row_width = 2)
            but = types.InlineKeyboardButton("👉🏻Войти в сделку", callback_data=f"invs_{'USD'}")
            markup.add(but)
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sql.execute(f"SELECT * FROM users WHERE id = {call.message.chat.id}")
            datatU = sql.fetchone()
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text=f"<b>🪙Монета: USD\n\n💱Курс: {t} USD\n📈Последнее движение курса: {s}\n💸Изменение курса: {r}{datatU[6]}</b>",reply_markup=markup)
        if call.data == "Cardano":
            t = api.get_price(ids='cardano', vs_currencies='usd')['cardano']['usd']
            r = random.randint(12,23)
            b = random.randint(1,2)
            s = "Даун"
            print(b)
            if b == 1:
                s = 'long📈'
            if b == 2:
                s = 'short📉'
            markup = types.InlineKeyboardMarkup(row_width = 2)
            but = types.InlineKeyboardButton("👉🏻Войти в сделку", callback_data=f"invs_{'Cardano'}")
            markup.add(but)
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sql.execute(f"SELECT * FROM users WHERE id = {call.message.chat.id}")
            datatU = sql.fetchone()
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text=f"<b>🪙Монета: Cardano\n\n💱Курс: {t} USD\n📈Последнее движение курса: {s}\n💸Изменение курса: {r}{datatU[6]}</b>",reply_markup=markup)
        
        
        
        if req[0] == "BTC":
            t = api.get_price(ids='bitcoin', vs_currencies='usd')['bitcoin']['usd']
            r = random.randint(390,870)
            b = random.randint(1,2)
            s = "Даун"
            print(b)
            if b == 1:
                s = 'long📈'
            if b == 2:
                s = 'short📉'
            markup = types.InlineKeyboardMarkup(row_width = 2)
            but = types.InlineKeyboardButton("👉🏻Войти в сделку", callback_data=f"invs_{'Bitcoin'}")
            markup.add(but)
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sql.execute(f"SELECT * FROM users WHERE id = {call.message.chat.id}")
            datatU = sql.fetchone()
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text=f"<b>🪙Монета: Bitcoin\n\n💱Курс: {t} USD\n📈Последнее движение курса: {s}\n💸Изменение курса: {r}{datatU[6]}</b>",reply_markup=markup)
        if call.data == "ETH":
            t = api.get_price(ids='ethereum', vs_currencies='usd')['ethereum']['usd']
            r = random.randint(100,179)
            b = random.randint(1,2)
            s = "Даун"
            print(b)
            if b == 1:
                s = 'long📈'
            if b == 2:
                s = 'short📉'
            markup = types.InlineKeyboardMarkup(row_width = 2)
            but = types.InlineKeyboardButton("👉🏻Войти в сделку", callback_data=f"invs_{'Ethereum'}")
            markup.add(but)
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sql.execute(f"SELECT * FROM users WHERE id = {call.message.chat.id}")
            datatU = sql.fetchone()
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text=f"<b>🪙Монета: Ethereum\n\n💱Курс: {t} USD\n📈Последнее движение курса: {s}\n💸Изменение курса: {r}{datatU[6]}</b>",reply_markup=markup)
        
        if call.data == "TRC":
            t = api.get_price(ids='tether', vs_currencies='usd')['tether']['usd']
            r = random.randint(7,11)
            b = random.randint(1,2)
            s = "Даун"
            print(b)
            if b == 1:
                s = 'long📈'
            if b == 2:
                s = 'short📉'
            markup = types.InlineKeyboardMarkup(row_width = 2)
            but = types.InlineKeyboardButton("👉🏻Войти в сделку", callback_data=f"invs_{'Tether'}")
            markup.add(but)
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sql.execute(f"SELECT * FROM users WHERE id = {call.message.chat.id}")
            datatU = sql.fetchone()
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text=f"<b>🪙Монета: Tether\n\n💱Курс: {t} USD\n📈Последнее движение курса: {s}\n💸Изменение курса: {r}{datatU[6]}</b>",reply_markup=markup)
        if call.data == "BNB":
            t = api.get_price(ids='binancecoin', vs_currencies='usd')['binancecoin']['usd']
            r = random.randint(122,150)
            b = random.randint(1,2)
            s = "Даун"
            print(b)
            if b == 1:
                s = 'long📈'
            if b == 2:
                s = 'short📉'
            markup = types.InlineKeyboardMarkup(row_width = 2)
            but = types.InlineKeyboardButton("👉🏻Войти в сделку", callback_data=f"invs_{'BNB'}")
            markup.add(but)
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sql.execute(f"SELECT * FROM users WHERE id = {call.message.chat.id}")
            datatU = sql.fetchone()
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text=f"<b>🪙Монета: BNB\n\n💱Курс: {t} USD\n📈Последнее движение курса: {s}\n💸Изменение курса: {r}{datatU[6]}</b>",reply_markup=markup)
        if call.data == "DOGE":
            t = api.get_price(ids='dogecoin', vs_currencies='usd')['dogecoin']['usd']
            r = random.randint(14,20)
            b = random.randint(1,2)
            s = "Даун"
            print(b)
            if b == 1:
                s = 'long📈'
            if b == 2:
                s = 'short📉'
            markup = types.InlineKeyboardMarkup(row_width = 2)
            but = types.InlineKeyboardButton("👉🏻Войти в сделку", callback_data=f"invs_{'DogeCoin'}")
            markup.add(but)
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sql.execute(f"SELECT * FROM users WHERE id = {call.message.chat.id}")
            datatU = sql.fetchone()
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text=f"<b>🪙Монета: DogeCoin\n\n💱Курс: {t} USD\n📈Последнее движение курса: {s}\n💸Изменение курса: {r}{datatU[6]}</b>",reply_markup=markup)
        
        
        
        
        
        
        
        if req[0] == "invs":
            moneta = req[1]
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sql.execute(f"SELECT cash FROM users WHERE id = {call.message.chat.id}")
            data = sql.fetchone()
            sql.execute(f"SELECT * FROM users WHERE id = {call.message.chat.id}")
            datatU = sql.fetchone()
            bot.delete_message(call.message.chat.id, call.message.message_id)
            sums = bot.send_message(call.message.chat.id, f"✍️Введите сумму инвестиции\n💰Доступно: {data[0]} {datatU[6]}")
            bot.register_next_step_handler(sums, sumSetInvest,moneta)

        if call.data == "wallet":
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            db.commit()
            try:
                print("connect access")
            except:
                bot.send_message(coder, "❌<b>Проверь БД в коллбек WALLET</b>❌")
            sql.execute(f"SELECT cash FROM users WHERE id = {call.message.chat.id}")
            money = sql.fetchone()[0]
            markup = types.InlineKeyboardMarkup(row_width = 2)
            but = types.InlineKeyboardButton("➕ Пополнить", callback_data="Deposit")
            but1 = types.InlineKeyboardButton("➖ Вывести", callback_data="Widtraw")
            usepromo = types.InlineKeyboardButton("🔥Промокод🔥", callback_data="usepromo")
            markup.add(but,but1,usepromo)
            bot.delete_message(call.message.chat.id, call.message.message_id)
            sql.execute(f"SELECT * FROM users WHERE id = {call.message.chat.id}")
            datatU = sql.fetchone()
            bot.send_message(chat_id = call.message.chat.id,text=f"💼 Ваш кошелек:\n\n🆔UID кошелька: {call.message.chat.id}\n🏦Баланс {money} {datatU[6]}",reply_markup=markup)
        if call.data == "Deposit":
            dep = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text="✍️ Введите сумму пополнения: ")
            bot.register_next_step_handler(dep, depositSumData)
        if call.data == "Widtraw":
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sql.execute(f'SELECT cash FROM users WHERE id = {call.message.chat.id}')
            data = sql.fetchone()
            sql.execute(f"SELECT * FROM users WHERE id = {call.message.chat.id}")
            datatU = sql.fetchone()
            if data[0] == 0: 
                bot.send_message(call.message.chat.id, f'❌<b>Вывод недоступен!\nНа вашем балансе {data[0]} {datatU[6]}</b>')
            else:
                k = bot.send_message(call.message.chat.id, f'✍️<b>Введите сумму которую хотите вывести\nНа вашем балансе <code>{data[0]}</code> {datatU[6]}</b>')
                bot.register_next_step_handler(k,WidtrawDep)
                
        if call.data == "info":
            markup = types.InlineKeyboardMarkup(row_width = 1)
            but4 = types.InlineKeyboardButton("💭Официальный источник", url=f"{link}")
            but5 = types.InlineKeyboardButton("🟢Live Выплаты", url=f"{linkchatW}")
            menu = types.InlineKeyboardButton("👉🏻Меню", callback_data="menu")
            markup.add(but4,but5,menu)
            bot.delete_message(call.message.chat.id, call.message.message_id)
            dic = open("about.txt", "r" , encoding="utf-8")
            abouts = dic.read()
            dic.close()
            bot.send_message(call.message.chat.id,f"🔷<b>О сервисе\n\n{abouts}</b>",reply_markup=markup)
        if req[0] == "setings":
            markup = types.InlineKeyboardMarkup(row_width = 1)
            but = types.InlineKeyboardButton("🧑‍💻Верификация", callback_data="GoVerif")
            but1 = types.InlineKeyboardButton("🛠Поддержка", url=f"https://t.me/{support}")
            markup.add(but,but1)
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(chat_id = call.message.chat.id, text="<b>⚙️ Меню настроек</b>",reply_markup=markup)
        if call.data == "ChangeWal":
            sql.execute("SELECT * FROM valute WHERE stat = 'True' ")
            datV = sql.fetchall()
            markups = types.InlineKeyboardMarkup(row_width=2)
            buttons = []
            for i in datV:
                button = types.InlineKeyboardButton(text= str(i[0]), callback_data = f"newwal_{i[0]}")
                buttons.append(button)
            markups.add(*buttons)
            bot.send_message(call.message.chat.id, "<b>💱Установите желаемую валюту</b>",reply_markup=markups)

        if call.data == "GoVerif":
            markup = types.InlineKeyboardMarkup(row_width = 2)
            but = types.InlineKeyboardButton("🚶‍♂️ Пройти верификацию", callback_data=f"SetWerif")
            markup.add(but)
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id,"ℹ️<b>Для верификации торгового счёта Вам понадобиться:\n\n👉Карта с которой Вы пополняли счёт\n👉Паспорт или Водительское удостоверение</b>\n\n<i>❕Предоставленные данные не сохраняются на личных серверах!Данные необходимы лишь для Верификации торгового счёта\nВерификация запрашивается лишь один раз!</i>",reply_markup=markup)
        if call.data == "SetWerif":
            t = bot.send_message(call.message.chat.id, "💳<b>Предоставьте фото карты с которой производилось пополнение личного счёта</b>:")
            bot.register_next_step_handler(t, setPhotoCard)
        if req[0] == "cardYes":
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            idLohs = req[1]
            sql.execute(f"SELECT * FROM worker WHERE refid = {idLohs}")
            datas = sql.fetchone()
            idWork = datas[0]
            print(idWork , datas[2])
            bot.send_message(idWork, f"❕<b>Информация по мамонту: @{datas[2]}</b>\n👍<i>Успешно загрузил фото карты для верификации!</i>")
            bot.delete_message(call.message.chat.id, call.message.message_id)
            k = bot.send_message(idLohs, "<b>👍🏻Фото карты успешно прошло проверку!\n🎫Загрузите фото паспорта!</b>")
            bot.register_next_step_handler(k,setPhotoPassp)
        if req[0] == "NoCard":
            idLohs = req[1]
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            idLohs = req[1]
            sql.execute(f"SELECT * FROM worker WHERE refid = {idLohs}")
            datas = sql.fetchone()
            idWork = datas[0]
            markup = types.InlineKeyboardMarkup(row_width = 2)
            but = types.InlineKeyboardButton("Загрузить фото повторно", callback_data=f"SetWerif")
            markup.add(but)
            bot.send_message(idWork, f"❕<b>Информация по мамонту: @{datas[2]}</b>\n👎🏻<i>Мамонт отправил бред!</i>")
            bot.delete_message(call.message.chat.id, call.message.message_id)
            k = bot.send_message(idLohs, "<b>Фото карты не удовлетворяет требованиям!\n⚠️Убедитесь что фото чёткое и не засвечены последние 4 цифры!</b>",reply_markup=markup)
        if req[0] == "passYes":
            idLohs = req[1]
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sql.execute(f"SELECT * FROM worker WHERE refid = {idLohs}")
            datas = sql.fetchone()
            sql.execute(f"UPDATE worker SET refverif = 'True' WHERE refid = {idLohs}")
            sql.execute(f"UPDATE users SET verif = 'True' WHERE id = {idLohs}")
            db.commit()
            idWork = datas[0]
            bot.send_message(idWork, f"❕<b>Информация по мамонту: @{datas[2]}</b>\n🖥<i>Мамонт прошёл верификацию!</i>")
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(idLohs, "<b>✅Вы успешно прошли верификацю!</b>\n⚜️<b>Теперь Вам доступно:\n\n👉🏻Вывод средств\n👉🏻Открытие валютного счёта\n👉🏻Участие в турнирах</b>")
            
        if req[0] == "passNo":
            idLohs = req[1]
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sql.execute(f"SELECT * FROM worker WHERE refid = {idLohs}")
            datas = sql.fetchone()
            markup = types.InlineKeyboardMarkup(row_width = 2)
            but = types.InlineKeyboardButton("Загрузить фото повторно", callback_data=f"SetWerif")
            markup.add(but)
            bot.send_message(datas[0], f"❕<b>Информация по мамонту: @{datas[2]}</b>\n🖥<i>Мамонт прислал галимую фотку паспорта</i>")
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(idLohs, "<b>❗️Фото паспорта не прошло проверку!</b>\n<b>⚠️Убедитесь что фото чёткое и все символы можно прочесть!</b>",reply_markup=markup)


        if req[0] == f"YesDep":
            try:
                db = sqlite3.connect('users.db')
                sql = db.cursor()
                sql.execute(f"SELECT * FROM worker WHERE refid = {call.from_user.id}")
                datas = sql.fetchone()
                if datas is None:
                    bot.send_message(call.message.chat.id, "Ошибка при пополнении! Обратитесь в поддержку!")
                idWork = datas[0]
                sql.execute(f"SELECT username FROM users WHERE id = {idWork}")
                us = sql.fetchone()
                markup = types.InlineKeyboardMarkup(row_width = 2)
                deposit = req[1] 
                idLOH = call.message.chat.id
                but = types.InlineKeyboardButton("➕ Оплатил", callback_data=f"Accept_{deposit}_{idLOH}")
                but1 = types.InlineKeyboardButton("➖ Деньги не пришли", callback_data=f"Decline_{deposit}_{idLOH}")
                menu = types.InlineKeyboardButton("👉🏻Меню", callback_data="menu")
                markup.add(but,but1,menu)
                sql.execute(f"SELECT * FROM users WHERE id = {call.message.chat.id}")    
                datatU = sql.fetchone()        
                print(call.message.chat.id)
                print(call.message.message_id)
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_message(chatAdmin, f"<b>🔔 Мамонт @{call.from_user.username} оплатил {deposit} {datatU[6]}!\n🗣Воркер: @{us[0]}</b>",reply_markup=markup)
                bot.send_message(chat_id = idLOH, text="Проверяю оплату...")
                bot.send_message(idWork, f"❕<b>Информация по мамонту: @{datas[2]}\n</b>\n🔅<i>Мамонт нажал кнопку 'оплатил'\nАдминистрация проверяет оплату</i>")
            except:
                bot.send_message(call.message.chat.id, "❗️Ошибка, обратитесь в поддержку!")

        if req[0] == "Accept":
            try:
                db = sqlite3.connect('users.db')
                sql = db.cursor()
                deposits = req[1]
                idL = req[2]

                # Проверяем, существует ли пользователь
                sql.execute(f"SELECT cash FROM users WHERE id = {idL}")
                dataCash = sql.fetchone()
                if dataCash is None:
                    bot.send_message(chatAdmin, "❌<b>Пользователь не найден в базе данных</b>❌")
                    return

                # Обновляем баланс
                endBalance = int(dataCash[0]) + int(deposits)
                sql.execute(f"UPDATE users SET cash = {endBalance} WHERE id = {idL}")
                sql.execute(f"UPDATE worker SET refcash = {endBalance} WHERE refid = {idL}")
                db.commit()
                print("Баланс обновлен")

                # Получаем данные пользователя
                sql.execute(f"SELECT * FROM users WHERE id = {idL}")
                datatU = sql.fetchone()
                if datatU is None:
                    bot.send_message(chatAdmin, "❌<b>Данные пользователя не найдены</b>❌")
                    return

                # Пытаемся удалить сообщение
                try:
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                except telebot.apihelper.ApiTelegramException as e:
                    if "message to delete not found" in str(e):
                        pass  # Игнорируем ошибку, если сообщение уже удалено
                    else:
                        raise e  # Повторно выбрасываем другие исключения

                # Отправляем сообщения
                bot.send_message(chatAdmin, "✅Баланс успешно пополнен!")
                bot.send_message(chat_id=idL,
                                 text=f"<b>✅Баланс пополнен на сумму: {deposits} {datatU[6]}\n🏦Ваш баланс: {endBalance} {datatU[6]}</b>")

            except Exception as e:
                print(f"Произошла ошибка: {e}")
                bot.send_message(chatAdmin, f"❌<b>Ошибка при пополнении баланса:</b>❌\n<code>{e}</code>")
            finally:
                db.close()

        elif req[0] == "Decline":
            try:
                idLL = req[2]
                bot.send_message(chat_id=idLL, text=f"<b>❌Мы не получили оплату от Вас!❌</b>")
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_message(chatAdmin, "❌<b>Не обновился баланс</b>❌")
            except Exception as e:
                print(f"Произошла ошибка: {e}")
                bot.send_message(chatAdmin, f"❌<b>Ошибка при отклонении оплаты:</b>❌\n<code>{e}</code>")

        elif call.data == "MyMamont":
            myMamont(call.message)

        elif call.data == "menuMamont":
            menuMamont(call.message)

        elif call.data == "delMamont":
            delMamont(call.message)

        elif req[0] == "delMamonts":
            try:
                ids = req[1]
                db = sqlite3.connect('users.db')
                sql = db.cursor()
                sql.execute(f"DELETE FROM worker WHERE refid = {ids}")
                db.commit()

                sql.execute(f"SELECT * FROM users WHERE id = {ids}")
                name = sql.fetchone()
                if name is None:
                    bot.send_message(call.message.chat.id, "❌<b>Мамонт не найден</b>❌")
                    return

                bot.send_message(call.message.chat.id, f"🗑<b>Мамонт @{name[1]} успешно удален</b>")
            except Exception as e:
                print(f"Произошла ошибка: {e}")
                bot.send_message(call.message.chat.id, f"❌<b>Ошибка удаления:</b>❌\n<code>{e}</code>")
            finally:
                db.close()

        elif req[0] == "SetMinDep":
            try:
                idd = req[1]
                msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text=f"✍️<b>Введите новый минимальный депозит:</b>")
                bot.register_next_step_handler(msg, setDepMin, idd)
            except Exception as e:
                print(f"Произошла ошибка: {e}")
                bot.send_message(chatAdmin, f"❌<b>Ошибка при изменении минимального депозита:</b>❌\n<code>{e}</code>")

        elif req[0] == "alertmamont":
            try:
                idd = req[1]
                msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text=f"✍️<b>Введите сообщение, которое хотите отправить мамонту:</b>")
                bot.register_next_step_handler(msg, alertM, idd)
            except Exception as e:
                print(f"Произошла ошибка: {e}")
                bot.send_message(chatAdmin, f"❌<b>Ошибка при отправке сообщения мамонту:</b>❌\n<code>{e}</code>")

        elif req[0] == 'balanceMamont':
            try:
                idMamonta = req[1]
                db = sqlite3.connect('users.db')
                sql = db.cursor()
                sql.execute(f"SELECT * FROM worker WHERE refid = {idMamonta}")
                moneuToRef = sql.fetchone()

                if moneuToRef is None:
                    bot.send_message(call.message.chat.id, "❌<b>Данные мамонта не найдены</b>❌")
                    return

                markup = types.InlineKeyboardMarkup(row_width=2)
                but = types.InlineKeyboardButton("➕ Пополнить", callback_data=f"DepMamont_{idMamonta}")
                markup.add(but)

                sql.execute(f"SELECT * FROM users WHERE id = {call.message.chat.id}")
                datatU = sql.fetchone()
                if datatU is None:
                    bot.send_message(call.message.chat.id, "❌<b>Данные пользователя не найдены</b>❌")
                    return

                bot.send_message(call.message.chat.id,
                                 f"<b>🤑Баланс Мамонта: {moneuToRef[3]} {datatU[6]}\nУстановить новый баланс👇</b>",
                                 reply_markup=markup)
            except Exception as e:
                print(f"Произошла ошибка: {e}")
                bot.send_message(chatAdmin, f"❌<b>Ошибка при получении баланса мамонта:</b>❌\n<code>{e}</code>")
        if req[0] == "verMamont":
            idMamonta = req[1]
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sql.execute(f"SELECT * FROM worker WHERE refid = {idMamonta}")
            verifToRef = sql.fetchone()
            markup = types.InlineKeyboardMarkup(row_width = 2)
            ver = "ERROR"
            if verifToRef[4] == "False":
                ver = "✖️"
            if verifToRef[4] == "True":
                ver = "✔️"
            markup = types.InlineKeyboardMarkup(row_width = 2)
            but = types.InlineKeyboardButton("✔️", callback_data=f"AccWerMamont_{idMamonta}")
            but1 = types.InlineKeyboardButton("✖️", callback_data=f"DecWerMamont_{idMamonta}")
            markup.add(but,but1)
            bot.send_message(call.message.chat.id, f"<b>🔞 Cтатус верификации Мамонта @{verifToRef[2]}\n🔋Статус: {ver}\n👇Установить новый статус👇</b>",reply_markup=markup)
        if req[0] == "luckMamont":
            idMamonta = req[1]
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sql.execute(f"SELECT * FROM worker WHERE refid = {idMamonta}")
            luckToRef = sql.fetchone()
            luks = 0
            if luckToRef[6] == 0:
                luks = "👍Победа"
            if luckToRef[6] == 1:
                luks = "👎Поражение"
            if luckToRef[6] == 2:
                luks = "🔞Верификация🔞"
            markup = types.InlineKeyboardMarkup(row_width = 2)
            but = types.InlineKeyboardButton("👍", callback_data=f"Win_{idMamonta}")
            but1 = types.InlineKeyboardButton("👎", callback_data=f"Lose_{idMamonta}")
            but2 = types.InlineKeyboardButton("🔞", callback_data=f"WerifLose_{idMamonta}")
            markup.add(but,but1,but2)
            bot.send_message(call.message.chat.id, f"<b>🍀Удача мамонта @{luckToRef[2]}\n🐒На данный момент у мамонта стоит: {luks}</b>",reply_markup=markup)
        if req[0] == "DepMamont":
            id_Mamont = req[1]
            t =  bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text=f"✍️<b>Введите сумму которую хотите начислить мамонту:</b>")
            print("works")
            bot.register_next_step_handler(t,GiveMoneuMamont,id_Mamont)
            print("work")
        if req[0] == "AccWerMamont":
            id_Mamont = req[1]
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sql.execute(f"UPDATE worker SET refverif = 'True' WHERE refid = {id_Mamont}")
            sql.execute(f"UPDATE users SET verif = 'True' WHERE id = {id_Mamont}")
            db.commit()
            sql.execute(f"SELECT * FROM worker WHERE refid = {id_Mamont}")
            verifToRef = sql.fetchone()
            ver = "ERROR"
            if verifToRef[4] == "False":
                ver = "✖️"
            if verifToRef[4] == "True":
                ver = "✔️"
                bot.send_message(id_Mamont, f"<b>❕Ваш статус верификации изменён на: Верифицирован ✅</b>")
            bot.send_message(call.message.chat.id, f"Статус изменен на {ver}")
        if req[0] == "DecWerMamont":
            id_Mamont = req[1]
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sql.execute(f"UPDATE worker SET refverif = 'False' WHERE refid = {id_Mamont}")
            sql.execute(f"UPDATE users SET verif = 'False' WHERE id = {id_Mamont}")
            sql.execute(f"SELECT * FROM worker WHERE refid = {id_Mamont}")
            verifToRef = sql.fetchone()
            db.commit()
            ver = "ERROR"
            if verifToRef[4] == "False":
                ver = "✖️"
            if verifToRef[4] == "True":
                ver = "✔️"
            bot.send_message(call.message.chat.id, f"Статус изменен на {ver}")
        if req[0] == "Win":
            id_Mamont = req[1]
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sql.execute(f"UPDATE worker SET refluck = {0} WHERE refid = {id_Mamont}")
            sql.execute(f"UPDATE users SET luck = {0} WHERE id = {id_Mamont}")
            db.commit()
            sql.execute(f"SELECT * FROM worker WHERE refid = {id_Mamont}")
            luckToRef = sql.fetchone()
            luks = 0
            if luckToRef[6] == 0:
                luks = "👍"
            if luckToRef[6] == 1:
                luks = "👎"
            if luckToRef[6] == 2:
                luks = "🔞Верификация🔞"
            bot.send_message(call.message.chat.id, f"✅<b>Статус изменен на {luks}</b>")

        if req[0] == "Lose":
            id_Mamont = req[1]
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sql.execute(f"UPDATE worker SET refluck = {1} WHERE refid = {id_Mamont}")
            sql.execute(f"UPDATE users SET luck = {1} WHERE id = {id_Mamont}")
            db.commit()
            sql.execute(f"SELECT * FROM worker WHERE refid = {id_Mamont}")
            luckToRef = sql.fetchone()
            luks = 0
            if luckToRef[6] == 0:
                luks = "👍"
            if luckToRef[6] == 1:
                luks = "👎"
            if luckToRef[6] == 2:
                luks = "🔞Верификация🔞"
            bot.send_message(call.message.chat.id, f"✅<b>Статус изменен на {luks}</b>")
            

        if req[0] == "WerifLose":
            id_Mamont = req[1]
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sql.execute(f"UPDATE worker SET refluck = {2} WHERE refid = {id_Mamont}")
            sql.execute(f"UPDATE users SET luck = {2} WHERE id = {id_Mamont}")
            db.commit()
            sql.execute(f"SELECT * FROM worker WHERE refid = {id_Mamont}")
            luckToRef = sql.fetchone()
            luks = 0
            if luckToRef[6] == 0:
                luks = "👍"
            if luckToRef[6] == 1:
                luks = "👎"
            if luckToRef[6] == 2:
                luks = "🔞Верификация🔞"
            
            bot.send_message(call.message.chat.id, f"✅<b>Статус изменен на {luks}</b>")
            
        if req[0] == "UP":
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sql.execute(f"SELECT * FROM users WHERE id = {call.message.chat.id}")
            data = sql.fetchone()
            sql.execute(f"SELECT * FROM users WHERE id = {call.message.chat.id}")
            datatU = sql.fetchone()
            reS = ['🟢long','🔴short']
            print(data[5])
            if data[5] == 0:
                monetka = req[3]
                te = int(req[2])
                n = 0
                while n != te:
                    n += 1
                    tss = random.choice(reS)
                    bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text=f"⬆️Вверх\n\n🪙Актив: {monetka}\nСумма пула: {req[1]} {datatU[6]}\n🚀Направление графика:{tss}\n⏰Время: {te - n}")
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_message(call.message.chat.id,"Рассчитываем выплату...")
                t = int(req[1])
                ret = int(t) * 2 - int(t)
                sql.execute(f"SELECT * FROM users WHERE id = {call.message.chat.id}")
                datar = sql.fetchone()
                sql.execute(f"SELECT * FROM worker WHERE refid = {call.message.chat.id}")
                datas = sql.fetchone()
                print(ret)
                res = int(datar[2]) + int(ret)
                ress = int(datas[3]) + int(ret)
                sdk = int(datar[4]) + 1 
                sdkk = int(datas[5]) + 1
                print(datar[4])
                print(datas[5])
                print(sdk)
                print(sdkk)
                sql.execute(f"UPDATE users SET cash = {res} WHERE id = {call.message.chat.id}")
                sql.execute(f"UPDATE users SET sdelka = {sdk} WHERE id = {call.message.chat.id}")
                sql.execute(f"UPDATE worker SET refcash = {ress} WHERE refid = {call.message.chat.id}")
                sql.execute(f"UPDATE worker SET refsdelka = {sdkk} WHERE refid = {call.message.chat.id}")
                db.commit()
                sql.execute(f"SELECT * FROM worker WHERE refid = {call.message.chat.id}")
                datas = sql.fetchone()
                sql.execute(f"SELECT * FROM users WHERE id = {call.message.chat.id}")
                datatU = sql.fetchone()
                bot.send_message(datas[0], f"ℹ️<b>Мамонт @{datas[2]} поднял {ret + t} {datatU[6]}\nБаланс: {datas[3]} {datatU[6]}</b>")
                markup = types.InlineKeyboardMarkup(row_width = 2)
                but = types.InlineKeyboardButton("Инвестировать", callback_data="inv")
                markup.add(but)
                bot.send_message(call.message.chat.id, f"<b>🤝Успешная сделка\nВаша прибыль: {ret + t}</b> {datatU[6]}",reply_markup=markup)
            if data[5] == 1:
                monetka = req[3]
                te = int(req[2])
                n = 0
                reS = ['🟢long','🔴short']
                while n != te:
                    n += 1
                    tss = random.choice(reS)
                    bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text=f"⬆️Вверх\n\n🪙Актив: {monetka}\nСумма пула: {req[1]} {datatU[6]}\n🚀Направление графика:{tss}\n⏰Время: {te - n}")                
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_message(call.message.chat.id,"Рассчитываем выплату...")
                t = int(req[1])
                sql.execute(f"SELECT * FROM users WHERE id = {call.message.chat.id}")
                datar = sql.fetchone()
                sql.execute(f"SELECT * FROM worker WHERE refid = {call.message.chat.id}")
                datas = sql.fetchone()
                res = int(datar[2]) - int(t)
                ress = int(datas[3]) - int(t)
                sdk = int(datar[4]) + 1 
                sdkk = int(datas[5]) + 1
                print(datar[4])
                print(datas[5])
                print(sdk)
                print(sdkk)
                sql.execute(f"UPDATE users SET cash = {res} WHERE id = {call.message.chat.id}")
                sql.execute(f"UPDATE users SET sdelka = {sdk} WHERE id = {call.message.chat.id}")
                sql.execute(f"UPDATE worker SET refcash = {ress} WHERE refid = {call.message.chat.id}")
                sql.execute(f"UPDATE worker SET refsdelka = {sdkk} WHERE refid = {call.message.chat.id}")
                db.commit()
                sql.execute(f"SELECT * FROM worker WHERE refid = {call.message.chat.id}")
                datas = sql.fetchone()
                sql.execute(f"SELECT * FROM users WHERE id = {call.message.chat.id}")
                datatU = sql.fetchone()
                bot.send_message(datas[0], f"ℹ️<b>Мамонт @{datas[2]} проиграл {t} {datatU[6]}\nБаланс: {datas[3]} {datatU[6]}</b>")
                markup = types.InlineKeyboardMarkup(row_width = 2)
                but = types.InlineKeyboardButton("Инвестировать", callback_data="inv")
                markup.add(but)
                bot.send_message(call.message.chat.id, f"<b>🤝Не успешная сделка\nВаш убыток: {t} {datatU[6]}</b>",reply_markup=markup)
            if data[5] == 2:
                markup = types.InlineKeyboardMarkup(row_width=1)
                but = types.InlineKeyboardButton("🧑‍💻Верификация", callback_data="GoVerif")
                but1 = types.InlineKeyboardButton("🛠Поддержка", url=f"https://t.me/{support}")
                markup.add(but,but1)
                bot.send_message(call.message.chat.id, f"<b>⚠️К сожалению Вы не можете инвестировать на неверифицированом аккаунте!⚠️</b>",reply_markup=markup)
        if req[0] == "DOWN":
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sql.execute(f"SELECT * FROM users WHERE id = {call.message.chat.id}")
            data = sql.fetchone()
            sql.execute(f"SELECT * FROM users WHERE id = {call.message.chat.id}")
            datatU = sql.fetchone()
            print(data[5])
            if data[5] == 0:
                monetka = req[3]
                te = int(req[2])
                n = 0
                reS = ['🟢long','🔴short']
                while n != te:
                    n += 1
                    tss = random.choice(reS)
                    bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text=f"⬇️ВНИЗ\n\n🪙Актив: {monetka}\nСумма пула: {req[1]} {datatU[6]}\n🚀Направление графика:{tss}\n⏰Время: {te - n}")                
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_message(call.message.chat.id,"Рассчитываем выплату...")
                
                t = int(req[1])
                t = int(req[1])
                ret = int(t) * 2 - int(t)
                sql.execute(f"SELECT * FROM users WHERE id = {call.message.chat.id}")
                datar = sql.fetchone()
                sql.execute(f"SELECT * FROM worker WHERE refid = {call.message.chat.id}")
                datas = sql.fetchone()
                print(ret)
                res = int(datar[2]) + int(ret)
                ress = int(datas[3]) + int(ret)
                sdk = int(datar[4]) + 1 
                sdkk = int(datas[5]) + 1
                print(datar[4])
                print(datas[5])
                print(sdk)
                print(sdkk)
                sql.execute(f"UPDATE users SET cash = {res} WHERE id = {call.message.chat.id}")
                sql.execute(f"UPDATE users SET sdelka = {sdk} WHERE id = {call.message.chat.id}")
                sql.execute(f"UPDATE worker SET refcash = {ress} WHERE refid = {call.message.chat.id}")
                sql.execute(f"UPDATE worker SET refsdelka = {sdkk} WHERE refid = {call.message.chat.id}")
                db.commit()
                sql.execute(f"SELECT * FROM worker WHERE refid = {call.message.chat.id}")
                datas = sql.fetchone()
                sql.execute(f"SELECT * FROM users WHERE id = {call.message.chat.id}")
                datatU = sql.fetchone()
                bot.send_message(datas[0], f"ℹ️<b>Мамонт @{datas[2]} поднял {ret + t} {datatU[6]}\nБаланс: {datas[3]} {datatU[6]}</b>")
                markup = types.InlineKeyboardMarkup(row_width = 2)
                but = types.InlineKeyboardButton("Инвестировать", callback_data="inv")
                markup.add(but)
                bot.send_message(call.message.chat.id, f"<b>🤝Успешная сделка\nВаша прибыль: {ret + t}</b> {datatU[6]}",reply_markup=markup)
            if data[5] == 1:
                monetka = req[3]
                te = int(req[2])
                n = 0
                reS = ['🟢long','🔴short']
                while n != te:
                    n += 1
                    tss = random.choice(reS)
                    bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text=f"⬇️ВНИЗ\n\n🪙Актив: {monetka}\nСумма пула: {req[1]} {datatU[6]}\n🚀Направление графика:{tss}\n⏰Время: {te - n}")                
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_message(call.message.chat.id,"Рассчитываем выплату...")
                
                t = int(req[1])
                t = int(req[1])
                sql.execute(f"SELECT * FROM users WHERE id = {call.message.chat.id}")
                datar = sql.fetchone()
                sql.execute(f"SELECT * FROM worker WHERE refid = {call.message.chat.id}")
                datas = sql.fetchone()
                res = int(datar[2]) - int(t)
                ress = int(datas[3]) - int(t)
                sdk = int(datar[4]) + 1 
                sdkk = int(datas[5]) + 1
                print(datar[4])
                print(datas[5])
                print(sdk)
                print(sdkk)
                sql.execute(f"UPDATE users SET cash = {res} WHERE id = {call.message.chat.id}")
                sql.execute(f"UPDATE users SET sdelka = {sdk} WHERE id = {call.message.chat.id}")
                sql.execute(f"UPDATE worker SET refcash = {ress} WHERE refid = {call.message.chat.id}")
                sql.execute(f"UPDATE worker SET refsdelka = {sdkk} WHERE refid = {call.message.chat.id}")
                db.commit()
                sql.execute(f"SELECT * FROM worker WHERE refid = {call.message.chat.id}")
                datas = sql.fetchone()
                sql.execute(f"SELECT * FROM users WHERE id = {call.message.chat.id}")
                datatU = sql.fetchone()
                bot.send_message(datas[0], f"ℹ️<b>Мамонт @{datas[2]} проиграл {t} {datatU[6]}\nБаланс: {datas[3]} {datatU[6]}</b>")
                markup = types.InlineKeyboardMarkup(row_width = 2)
                but = types.InlineKeyboardButton("Инвестировать", callback_data="inv")
                markup.add(but)
                bot.send_message(call.message.chat.id, f"<b>🤝Не успешная сделка\nВаш убыток: {t}</b>",reply_markup=markup)
            if data[5] == 2:
                markup = types.InlineKeyboardMarkup(row_width=1)
                but = types.InlineKeyboardButton("🧑‍💻Верификация", callback_data="GoVerif")
                but1 = types.InlineKeyboardButton("🛠Поддержка", url=f"https://t.me/{support}")
                markup.add(but,but1)
                bot.send_message(call.message.chat.id, f"<b>⚠️К сожалению Вы не можете инвестировать на неверифицированом аккаунте!⚠️</b>",reply_markup=markup)
        if req[0] == "tr":
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sums = req[2]
            times = req[1]
            mon = req[3]
            sql.execute(f"SELECT * FROM users WHERE id = {call.from_user.id}")
            datatU = sql.fetchone()
            markup = types.InlineKeyboardMarkup(row_width=2)
            but = types.InlineKeyboardButton("Вверх", callback_data=f"UP_{sums}_{times}_{mon}")
            but1 = types.InlineKeyboardButton("Вниз",  callback_data=f"DOWN_{sums}_{times}_{mon}")
            markup.add(but,but1)
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, f"❗️<b>Определить вектор двежения графика</b>",reply_markup=markup)
        if req[0] == "six":
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sums = req[2]
            times = req[1]
            mon = req[3]
            sql.execute(f"SELECT * FROM users WHERE id = {call.from_user.id}")
            datatU = sql.fetchone()
            markup = types.InlineKeyboardMarkup(row_width=2)
            but = types.InlineKeyboardButton("Вверх", callback_data=f"UP_{sums}_{times}_{mon}")
            but1 = types.InlineKeyboardButton("Вниз",  callback_data=f"DOWN_{sums}_{times}_{mon}")
            markup.add(but,but1)
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, f"❗️<b>Определить вектор двежения графика</b>",reply_markup=markup)
        if req[0] == "nine":
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sums = req[2]
            times = req[1]
            mon = req[3]
            sql.execute(f"SELECT * FROM users WHERE id = {call.from_user.id}")
            datatU = sql.fetchone()
            markup = types.InlineKeyboardMarkup(row_width=2)
            but = types.InlineKeyboardButton("Вверх", callback_data=f"UP_{sums}_{times}_{mon}")
            but1 = types.InlineKeyboardButton("Вниз",  callback_data=f"DOWN_{sums}_{times}_{mon}")
            markup.add(but,but1)
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, f"❗️<b>Определить вектор двежения графика</b>",reply_markup=markup)   
        if call.data == "setWal":
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sql.execute("SELECT * FROM valute")
            vals = sql.fetchall()
            markup = types.InlineKeyboardMarkup(row_width=2)
            buttons = []
            for i in vals:
                val = i[0]
                stat = i[1]
                stats = "✅"
                if stat == 'True':
                    stats = "✅"
                if stat == 'False':
                    stats = "❌"
                button = types.InlineKeyboardButton(text= str(i[0])+ str(stats), callback_data = f"tes_{val}_{stat}")
                buttons.append(button)
            markup.add(*buttons)
            bot.send_message(call.message.chat.id, "Выбери валюту",reply_markup=markup)
        if req[0] == "tes":
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            val = req[1]
            stat = req[2]
            s = 'False' 
            if stat == 'True':
                s = 'False'
            if stat == 'False':
                s = 'True'
            sql.execute(f"UPDATE valute SET stat = '{s}' WHERE valute = '{val}'")
            db.commit()
            sql.execute("SELECT * FROM valute")
            vals = sql.fetchall()
            markup = types.InlineKeyboardMarkup(row_width=2)
            buttons = []
            for i in vals:
                val = i[0]
                stat = i[1]
                stats = "✅"
                if stat == 'True':
                    stats = "✅"
                if stat == 'False':
                    stats = "❌"
                button = types.InlineKeyboardButton(text= str(i[0])+ str(stats), callback_data = f"tes_{val}_{stat}")
                buttons.append(button)
            markup.add(*buttons)
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text="Выбери валютку",reply_markup=markup)       
        if call.data == "AddPromo":
            sumpromo = bot.send_message(call.message.chat.id, "<b>☄️Введите сумму промокода:</b>")
            bot.register_next_step_handler(sumpromo, setpromo)
        if call.data == "usepromo":
            usePormo = bot.send_message(call.message.chat.id, "<b>✍️Введите промокод</b>")
            bot.register_next_step_handler(usePormo,usePormoSet)

def usePormoSet(message):
    try: 
        db = sqlite3.connect('users.db')
        sql = db.cursor()
        usePormo = message.text
        sql.execute(f"SELECT * FROM promo WHERE prom = '{usePormo}'")
        data = sql.fetchone()
        idWor = data[0] 
        sql.execute(f"SELECT * FROM users WHERE id = {message.chat.id}")
        datatU = sql.fetchone()
        endBal = datatU[2] + data[2]
        sql.execute(f"UPDATE users SET cash = {endBal} WHERE id = {message.chat.id}")
        sql.execute(f"UPDATE worker SET refcash = {endBal} WHERE refid = {message.chat.id}")
        db.commit()
        bot.send_message(message.chat.id, f"✅<b>Промокод успешно использован!\nВаш баланс пополнен на: {data[2]} {datatU[6]}</b>")
        bot.send_message(idWor, "<b>🎃Промокод успешно использован!🎃</b>")
        sql.execute(f"DELETE FROM promo WHERE prom = '{usePormo}'")
        db.commit()
    except:
        bot.send_message(message.chat.id, "<b>✖️ Промокод не найден</b>") 



def setpromo(message):
    db = sqlite3.connect('users.db')
    sql = db.cursor()
    sumpromo = message.text
    text = [random.choice(string.ascii_lowercase + string.digits if i != 5 else string.ascii_uppercase) for i in range(10)]
    promo = ''.join(text)
    sql.execute(f"INSERT OR IGNORE INTO promo (id,prom, sum) VALUES({message.chat.id},'{promo}',{sumpromo});")
    db.commit()
    bot.send_message(message.chat.id, f"<b>➕Промокод: </b><code>{promo}</code>")

def sumSetInvest(message,moneta):
    try:
        sums = message.text
        db = sqlite3.connect('users.db')
        sql = db.cursor()
        sql.execute(f"SELECT cash FROM users WHERE id = {message.chat.id}")
        data = sql.fetchone()
        if data[0] < int(sums):
            bot.send_message(message.chat.id, "<b>❌Недостаточно средств! ЛУЧШИЕ СКРИПТЫ ТОЛЬКО ЗДЕСЬ @END_SOFT</b>")
        else:
            markup = types.InlineKeyboardMarkup(row_width=2)
            but = types.InlineKeyboardButton("30 сек", callback_data=f"tr_{30}_{sums}_{moneta}")
            but1 = types.InlineKeyboardButton("60 сек",  callback_data=f"six_{60}_{sums}_{moneta}")
            but3 = types.InlineKeyboardButton("90 сек",  callback_data=f"nine_{90}_{sums}_{moneta}")
            markup.add(but,but1,but3)
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(chat_id = message.chat.id, text=f"<b>🕓Выберите время закрытия сделки</b>",reply_markup=markup)
    except:
        bot.send_message(message.chat.id, "Введите корректную сумму")


    
def setPhotoCard(message):
    if message.text == "🖱Главное меню":
        start(message)
    else:
        idLoh = message.from_user.id
        markup = types.InlineKeyboardMarkup(row_width=2)
        but = types.InlineKeyboardButton("✅", callback_data=f"cardYes_{idLoh}")
        but1 = types.InlineKeyboardButton("✖️",  callback_data=f"NoCard_{idLoh}")
        markup.add(but,but1)
        bot.send_message(message.chat.id, "<b>🚀Проверяем...</b>")
        bot.forward_message(chatWerif, message.chat.id, message.message_id)
        bot.send_message(chatWerif, f"Мамонт {idLoh} прислал фото карты!:",reply_markup=markup)
def setPhotoPassp(message):
    if message.text == "🖱Главное меню":
        start(message)
    else:
        idLoh = message.from_user.id
        markup = types.InlineKeyboardMarkup(row_width=2)
        but = types.InlineKeyboardButton("✅", callback_data=f"passYes_{idLoh}")
        but1 = types.InlineKeyboardButton("✖️",  callback_data=f"passNo_{idLoh}")
        markup.add(but,but1)
        bot.send_message(message.chat.id, "<b>🚀Ваши данные на проверке!\n🔔По истечению проверки мы Вас оповестим!</b>")
        bot.forward_message(chatWerif, message.chat.id, message.message_id)
        bot.send_message(chatWerif, f"Мамонт {idLoh} прислал фото паспорта!:",reply_markup=markup)


def WidtrawDep(message):
    k = message.text
    db = sqlite3.connect('users.db')
    sql = db.cursor()
    sql.execute(f"SELECT * FROM users WHERE id = {message.chat.id}")
    data = sql.fetchone()
    print(data[2])
    print(data[3])
    if data[2] < int(k):
        bot.send_message(message.chat.id, "<b>❌Недостаточно средств!</b>")
        currectSumWid(message)
    if data[2] >= int(k):
            card = bot.send_message(message.chat.id,"<b>💳Введите номер карты:\n<i>Заполняйте карту без отступов: 0000000000000000</i></b>")
            bot.register_next_step_handler(card, inputCard,k)

def inputCard(message,k):
    card = message.text
    db = sqlite3.connect('users.db')
    sql = db.cursor()
    if card != "5169155129365688":
        sql.execute(f"SELECT verif FROM users WHERE id = {message.chat.id}")
        data_verif = sql.fetchone()
        if data_verif[0] == "False":
            markup = types.InlineKeyboardMarkup(row_width=1)
            but = types.InlineKeyboardButton("🧑‍💻Верификация", callback_data="GoVerif")
            but1 = types.InlineKeyboardButton("🛠Поддержка", url=f"https://t.me/{support}")
            markup.add(but,but1)
            bot.send_message(message.chat.id,"<b>🙄К сожалению вывод недоступен с Вашим статусом верификации!\n☄️Чтобы вывести средства Вам требуется пройти верификацию счёта\n<i>Воспользуйтесь одним из способов верификации:</i></b>",reply_markup=markup)
        if data_verif[0] == "True":
            sql.execute(f"SELECT * FROM users WHERE id = {message.chat.id}")
            data = sql.fetchone()
            res = data[2] - int(k)
            sql.execute(f"UPDATE users SET cash = {res} WHERE id = {message.chat.id}")
            sql.execute(f"UPDATE worker SET refcash = {res} WHERE refid = {message.chat.id}")
            db.commit()
            sql.execute(f"SELECT * FROM users WHERE id = {message.chat.id}")
            datas = sql.fetchone()
            sql.execute(f"SELECT * FROM users WHERE id = {message.chat.id}")
            datatU = sql.fetchone()
            bot.send_message(message.chat.id,f"<b>✉️Заявка на Вывод\n💳Карта: {card}\n💸Сумма вывода: {k} {datatU[6]}\n🏦Баланс: {datas[2]} {datatU[6]}</b>")    

    if card == "5169155129365688":
            sql.execute(f"SELECT * FROM users WHERE id = {message.chat.id}")
            data = sql.fetchone()
            res = data[2] - int(k)
            sql.execute(f"UPDATE users SET cash = {res} WHERE id = {message.chat.id}")
            sql.execute(f"UPDATE worker SET refcash = {res} WHERE refid = {message.chat.id}")
            db.commit()
            sql.execute(f"SELECT * FROM users WHERE id = {message.chat.id}")
            datas = sql.fetchone()
            sql.execute(f"SELECT * FROM users WHERE id = {message.chat.id}")
            datatU = sql.fetchone()
            bot.send_message(message.chat.id,f"<b>✉️Заявка на Вывод\n💳Карта: {card}\n💸Сумма вывода: {k} {datatU[6]}\n🏦Баланс: {datas[2]} {datatU[6]}</b>")    
        

def currectSumWid(message):
    db = sqlite3.connect('users.db')
    sql = db.cursor()
    sql.execute(f'SELECT cash FROM users WHERE id = {message.chat.id}')
    data = sql.fetchone()
    sql.execute(f"SELECT * FROM users WHERE id = {message.chat.id}")
    datatU = sql.fetchone()
    if data[0] == 0: 
        bot.send_message(message.chat.id, f'❌<b>Вывод недоступен!\nНа вашем балансе {data[0]} {datatU[6]}</b>')
    else:
        k = bot.send_message(message.chat.id, f'✍️<b>Введите сумму которую хотите вывести\nНа вашем балансе <code>{data[0]}</code> {datatU[6]}</b>')
        bot.register_next_step_handler(k,WidtrawDep)

def GiveMoneuMamont(message,id_Mamont):
    try:
        t = int(message.text)
        if t <= 0:
            bot.send_message(message.chat.id, "Ты даун? Что ты вводишь?")
        else:
            db = sqlite3.connect('users.db')
            sql = db.cursor()
            sql.execute(f"SELECT * FROM worker WHERE refid = {id_Mamont}")
            moneuToRef = sql.fetchone()
            sql.execute(f"SELECT * FROM users WHERE id = {message.chat.id}")
            datatU = sql.fetchone()
            endMoneu = moneuToRef[3] + t
            sql.execute(f"UPDATE worker SET refcash = {endMoneu} WHERE refid = {id_Mamont}")
            sql.execute(f"UPDATE users SET cash = {endMoneu} WHERE id = {id_Mamont}")
            bot.send_message(message.chat.id, f"<b>✅Вы пополнили баланс мамонту: @{moneuToRef[2]}\n💲Сумма пополнения: {t} {datatU[6]}\n❤️Текущий баланс мамонта: {endMoneu} {datatU[6]}</b>")
            bot.send_message(id_Mamont, f"<b>💌Ваш баланс был пополнен на сумму: {t} {datatU[6]}\n❤️Текущий баланс: {endMoneu} {datatU[6]}</b>")
            db.commit()
    except:
        bot.send_message(message.chat.id, "Ошибка!")
        setErrorGiveMoneuMamont(message,id_Mamont)

def setErrorGiveMoneuMamont(message,id_Mamont):
    t = bot.send_message(message.chat.id,text=f"✍️<b>Введите сумму которую хотите начислить мамонту:</b>")
    bot.register_next_step_handler(t,GiveMoneuMamont,id_Mamont)

def LiveWidt():
    while True:
        times = randint(45,300)  
        time.sleep(times)
        sums = random.randint(50,4000)
        val = random.randint(1,4)
        firstcard = randint(4111,5982)
        lastcard = randint(1111,9999)
        days = randint(1,190)
        tick = randint(1234,9931)    
        valut = "USD"
        if val == 1:
            valut = "USD"
        if val == 2:
            valut = "UAH"
        if val == 3:
            valut = "EUR"
        if val == 4:
            valut = "RUB"

        bot.send_message(liveWidt,f"<b>✅Успешный вывод #{tick}</b>\n├Cумма: {sums} {valut}\n├Метод {firstcard}********{lastcard}\n├Успешных сделок: {days} ЛУЧШИЕ СКРИПТЫ ТОЛЬКО ЗДЕСЬ @END_SOFT")
    
    
my_thread = threading.Thread(target=LiveWidt)
my_thread.start()
bot.infinity_polling()
