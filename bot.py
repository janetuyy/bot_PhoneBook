import telebot
from telebot import types
import db

API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btnmenu = types.KeyboardButton("/menu")
    markup.add(btnmenu)
    bot.reply_to(message, "heyy, " + message.from_user.first_name +
                 ", this is ur phonebook! send me /menu", reply_markup=markup)
    # bot.send_message(message.chat.id,
    # text="Привет, {0.first_name}! Я тестовый бот для твоей статьи для habr.com".format(
    #     message.from_user), reply_markup=markup)


@bot.message_handler(commands=['menu'])
def send_help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btnadd = types.KeyboardButton("/add")
    btndelete = types.KeyboardButton("/delete")
    btnmycontacts = types.KeyboardButton("/mycontacts")
    btnget = types.KeyboardButton("/get")

    markup.add(btnadd)
    markup.add(btndelete)
    markup.add(btnmycontacts)
    markup.add(btnget)
    bot.reply_to(message,
                 "1. to add contact use /add with name, phone number and note, \n"
                 "2. to delete contact use /delete with name, \n"
                 "3. to see all of ur contacts with /mycontacts, \n"
                 "4. to find contact, write /get and name \n", reply_markup=markup)


@bot.message_handler(commands=['add'])
def add(message):
    db.flag_add = True
    bot.reply_to(message, "give me name, number and note!")


def send_add(message):
    text = message.text.split()
    try:
        name = text[0]
        number = int(text[1])
        note = ""
        for i in range(2, len(text)):
            note += text[i] + " "
        chat_id = message.chat.id
        db.insert(chat_id, name, number, note)
        bot.reply_to(message, "done! u can see it using /mycontacts")
    except:
        try:
            name = text[0]
            number = int(text[1])
            note = ""
            chat_id = message.chat.id
            db.insert(chat_id, name, number, note)
            bot.reply_to(message, "done! u can see it using /mycontacts")
        except:
            bot.reply_to(message, "error! u should write /add with name, phone and information of contact")


@bot.message_handler(commands=['mycontacts'])
def send_contacts(message):
    contacts = db.select(message.chat.id)
    answer = ""
    for i in range(len(contacts)):
        answer += str(i + 1) + ". " + contacts[i][1] + "\n"
    bot.reply_to(message, "if u want to find contact, write /get and name \n" + answer)


@bot.message_handler(commands=['get'])
def get(message):
    bot.reply_to(message, "give me name!")
    db.flag_get = True


def get_contacts(message):
    try:
        contact = db.get(message.chat.id, message.text.split()[0])
        answer = contact[1] + " " + str(contact[2]) + " " + contact[3]
        bot.reply_to(message, answer)
    except:
        bot.reply_to(message, "error! tell me what u want with the right command")


@bot.message_handler(commands=['delete'])
def delete(message):
    db.flag_delete = True
    bot.reply_to(message, "give me name!")


def delete_contacts(message):
    try:
        if db.check(message.chat.id, message.text.split()[0]):
            db.delete(message.chat.id, message.text.split()[0])
            bot.reply_to(message, "done! check it with /mycontacts")
        else:
            bot.reply_to(message, "there is no contacts with this name")
    except:
        bot.reply_to(message, "try again!")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if db.flag_add:
        send_add(message)
        db.flag_add = False
    elif db.flag_get:
        get_contacts(message)
        db.flag_get = False
    elif db.flag_delete:
        delete_contacts(message)
        db.flag_delete = False
    # bot.reply_to(message, message.text)


markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btnadd = types.KeyboardButton("/add")
btndelete = types.KeyboardButton("/delete")
btnmycontacts = types.KeyboardButton("/mycontacts")
btnget = types.KeyboardButton("/get")
markup.add(btnadd)
markup.add(btndelete)
markup.add(btnmycontacts)
markup.add(btnget)
bot.infinity_polling()