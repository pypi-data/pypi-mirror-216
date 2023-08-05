import datetime
import telebot
from clubscore.objects.CONTAINER import *
import importlib
import xml.etree.ElementTree as ET
from io import BytesIO
import clubscore.utils as u
import json
import traceback
import requests
from telebot import types


def insertAction(bot, message, command):
    d = {}
    d["bot"] = bot
    d["user_id"] = message.from_user.id
    d["name"] = message.from_user.first_name
    d["lastname"] = message.from_user.last_name
    d["username"] = message.from_user.username
    d["command"] = command
    d["timestamp"] = datetime.datetime.now().isoformat()


    url = "https://clubscorestats.herokuapp.com/actions"
    payload = json.dumps(d)
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)




def run_telegram_bot(BOT, API_KEY, single_input, single_api):

    with open(single_input) as file:
        comandi_elite = json.load(file)

    with open(single_api) as file:
        singleapi = json.load(file)

    reply_markup = None
    print(comandi_elite)
    print(singleapi)

    reply_markup = types.ReplyKeyboardMarkup(row_width=2)

    button = types.InlineKeyboardButton(text="/start")
    reply_markup.add(button)
    button = types.InlineKeyboardButton(text="/help")
    reply_markup.add(button)
    button = types.InlineKeyboardButton(text="/teams")
    reply_markup.add(button)


    for command_data in singleapi:
        callback_data = "/" + command_data  # Remove the leading '/'
        button = types.InlineKeyboardButton(text=callback_data)
        reply_markup.add(button)

    for command_data in comandi_elite:
        button_text = f"{command_data}"
        callback_data = "/" + command_data  # Remove the leading '/'
        button = types.InlineKeyboardButton(text=callback_data)
        reply_markup.add(button)

    bot = telebot.TeleBot(API_KEY)

    def update_status(message):
        d[message.from_user.id] = message.text.replace('/', '')


    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        # Send a welcome message with the command menu
        bot.send_message(message.chat.id, f"Welcome in {BOT}!🤖\n A Clubscore® product!", reply_markup=reply_markup)


    @bot.message_handler(commands=['teams'])
    def teams(message):
        bot.send_message(message.chat.id, u.print_file_tree("teams"))

    @bot.message_handler(commands=['help'])
    def help(message):
        s = "You have the following commands:\n\n"
        s += "/start \n \help \n /teams\n"
        for e in sorted(comandi_elite):
            s += "/" + e + "\n"
        for e in sorted(singleapi):
            s += "/" + e + "\n"
        bot.send_message(message.chat.id, s)


    @bot.message_handler(commands=[k for k in comandi_elite])
    def risultati(message):
        m = message.text.replace('/', '')
        template = comandi_elite[m]
        #print(template)
        update_status(message)
        bot.send_message(message.chat.id, u.getTemplateGuide(template))

    @bot.message_handler(commands=[k for k in singleapi])
    def risultati(message):
        try:
            m = message.text.replace('/', '')
            template = singleapi[m]


            function_name = u.getTemplateText(template, "API").strip()
            params = u.getTemplateText(template, "PARAMETERS").strip().split("\n")

            module_name = "clubscore.API"
            module = importlib.import_module(module_name)
            function = getattr(module, function_name)

            lista = function(*params)

            root = ET.parse(template).getroot()
            width = int(root.attrib["width"])
            height = int(root.attrib["height"])

            image = Image.new('RGB', (width, height), color=(255, 255, 255))
            CONTAINER.interpretaTemplate(image, template, lista)

            img_io = BytesIO()
            image.save(img_io, 'PNG', quality=90)
            img_io.seek(0)

            bot.send_document(message.chat.id, document=img_io, visible_file_name="out.png", reply_markup=reply_markup)
            insertAction(BOT, message, m)

        except Exception as e:
            print("An exception occurred")
            traceback.print_exc()
            bot.send_message(message.chat.id, "C'è stato un problema, prova a rilanciare il comando")


    # todo rinominare: serve per far funzionare il message handler
    def risultato(message):
        if message.text != '':
            return True
        return False

    def send_photo_to_chat_(message, template):
        # todo al posto di message dovrebbe esserci un array o qualcosa di simile per accettare anche una foto da gestire nell'interprete
        root = ET.parse(template).getroot()
        width = int(root.attrib["width"])
        height = int(root.attrib["height"])

        image = Image.new('RGB', (width, height), color=(255, 255, 255))

        text = message.text.split('\n')

        CONTAINER.interpretaTemplate(image, template, text)

        img_io = BytesIO()
        image.save(img_io, 'PNG', quality=90)
        img_io.seek(0)

        bot.send_document(message.chat.id, document=img_io, visible_file_name="out.png", reply_markup=reply_markup)


    @bot.message_handler(func=risultato)
    def messaggi(message):
        user = message.from_user.id
        print(message)

        try:

            if user not in d or message.text[0] == '/':
                print(message.text.split('\n'))
                bot.send_message(message.chat.id, "Inserisci un comando valido")

            elif d[user] in comandi_elite:
                print(comandi_elite[d[user]])
                send_photo_to_chat_(message, comandi_elite[d[user]])
                insertAction(BOT, message, d[user])
                d[message.chat.id] = ''


            else:
                print(message.text)
                bot.send_message(message.chat.id, "Comando non riconosciuto")


        except Exception as e:
            print("An exception occurred")
            traceback.print_exc()
            bot.send_message(message.chat.id, "C'è stato un problema, manda un messaggio col formato corretto")

    # d: dizionario che associa la chiave utente con l'ultimo comando richiesto
    d = {}

    # info: associa la chiave dell'utente con le informazioni stringate necessarie
    info = {}

    bot.polling()


if __name__ == '__main__':
    run_telegram_bot()
