import config
import voice
import database
import messages

import telebot
import sqlite3
from telebot import types
import random
import math
import numpy

bot = telebot.TeleBot(config.token)


database.create_users_db()
database.create_estabs_db()


def get_stage(message):
    database.create_users_db()
    # open connection
    conn = sqlite3.connect(config.db_name)
    cursor = conn.cursor()
    a = cursor.execute(f"SELECT reg_stage FROM {config.users_table} WHERE id='{message.chat.id}'").fetchall()
    if len(a) > 0:
        a = a[0][0]
        # close connection
        conn.commit()
        cursor.close()
        conn.close()
        return a
    # close connection
    conn.commit()
    cursor.close()
    conn.close()

# Register user
def create_user(message):
    # checking for existence
    database.create_users_db()
    # open connection
    conn = sqlite3.connect(config.db_name)
    cursor = conn.cursor()
    # Adding a new user if does not exist
    a = len(cursor.execute(f"SELECT * FROM {config.users_table} WHERE id='{message.chat.id}'").fetchall())
    if a == 0:
        cursor.execute(f"INSERT INTO {config.users_table} (id, rating, reg_stage) VALUES ('{message.chat.id}', {0}, {1})")
        bot.send_message(message.chat.id, messages.USERREG)
        bot.send_message(message.chat.id, messages.USERNAME)
    else:
        bot.send_message(message.chat.id, messages.HELP)
    # close connection
    conn.commit()
    cursor.close()
    conn.close()
def set_user_name(message):
    # open connection
    conn = sqlite3.connect(config.db_name)
    cursor = conn.cursor()
    # Writing name
    query = "UPDATE "+str(config.users_table)+" SET name='"+str(message.text)+"', reg_stage=2 WHERE id='"+str(message.chat.id)+"'"
    cursor.execute(query)
    # close connection
    conn.commit()
    cursor.close()
    conn.close()
    bot.send_message(message.chat.id, messages.USERAGE)
def set_user_age(message):
    # open connection
    conn = sqlite3.connect(config.db_name)
    cursor = conn.cursor()
    # Writing age
    query = "UPDATE "+str(config.users_table)+" SET age="+str(message.text)+", reg_stage=3 WHERE id='"+str(message.chat.id)+"'"
    cursor.execute(query)
    # close connection
    conn.commit()
    cursor.close()
    conn.close()
    # Sending buttons
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('Мужской', 'Женский')
    bot.send_message(message.from_user.id, messages.USERSEX, reply_markup=user_markup)
def set_user_sex(message):
    # open connection
    conn = sqlite3.connect(config.db_name)
    cursor = conn.cursor()
    # Writing age
    query = "UPDATE "+str(config.users_table)+" SET sex='"+str(message.text)+"', reg_stage=4 WHERE id='"+str(message.chat.id)+"'"
    cursor.execute(query)
    # close connection
    conn.commit()
    cursor.close()
    conn.close()
    bot.send_message(message.chat.id, messages.USERREGCOMPLETE)
    bot.send_message(message.chat.id, messages.HELP)

# different modes
def help_buttons(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row(config.choose)
    user_markup.row(config.add)
    user_markup.row(config.find)
    user_markup.row(config.tobe)
    user_markup.row(config.neighbour)
    bot.send_message(message.from_user.id, messages.help0, reply_markup=user_markup)

# price buttons
def send_prices(message):
    keyboard = types.ReplyKeyboardMarkup(True, True)
    keyboard.row(config.p1, config.p2, config.p3)
    keyboard.row(config.p4, config.p5, config.p6)
    keyboard.row(config.p7, config.p8, config.p9)
    bot.send_message(message.from_user.id, messages.ESTABAVGCHECK, reply_markup=keyboard)
# category buttons
def send_categories(message):
    keyboard = types.ReplyKeyboardMarkup(True, True)
    keyboard.row(config.cat1, config.cat2)
    keyboard.row(config.cat3, config.cat4)
    bot.send_message(message.from_user.id, messages.ESTABCATEGORY, reply_markup=keyboard)

# Register establishment
def create_estab(message):
    # checking for existence
    database.create_estabs_db()
    # open connection
    conn = sqlite3.connect(config.db_name)
    cursor = conn.cursor()
    # Adding new establishment
    cursor.execute(f"INSERT INTO {config.estabs_table} (holder_id) VALUES ('{message.chat.id}')")
    a = cursor.execute(f"SELECT id FROM {config.estabs_table} WHERE holder_id='{message.chat.id}'").fetchall()
    a = a[len(a)-1][0]
    # setting reg_stage
    cursor.execute(f"UPDATE {config.users_table} SET reg_stage=6, current={a} WHERE id='{message.chat.id}'")
    # close connection
    conn.commit()
    cursor.close()
    conn.close()
    bot.send_message(message.chat.id, messages.ESTABNAME)
def set_estab_name(message):
    # open connection
    conn = sqlite3.connect(config.db_name)
    cursor = conn.cursor()
    # writing establishment's name
    a = cursor.execute(f"SELECT current FROM {config.users_table} WHERE id='{message.chat.id}'").fetchall()
    a = a[0][0]
    query = "UPDATE " + str(config.estabs_table) + " SET name='" + str(message.text) + "' WHERE id=" + str(a)
    cursor.execute(query)
    # setting reg_stage
    cursor.execute(f"UPDATE {config.users_table} SET reg_stage=7 WHERE id='{message.chat.id}'")
    # close connection
    conn.commit()
    cursor.close()
    conn.close()
    send_prices(message)
def set_estab_avcheck(message):
    # open connection
    conn = sqlite3.connect(config.db_name)
    cursor = conn.cursor()
    # writing establishment's name
    a = cursor.execute(f"SELECT current FROM {config.users_table} WHERE id='{message.chat.id}'").fetchall()
    a = a[0][0]
    query = "UPDATE " + str(config.estabs_table) + " SET avcheck='" + str(message.text) + "' WHERE id=" + str(a)
    cursor.execute(query)
    # setting reg_stage
    cursor.execute(f"UPDATE {config.users_table} SET reg_stage=8 WHERE id='{message.chat.id}'")
    # close connection
    conn.commit()
    cursor.close()
    conn.close()
    bot.send_message(message.chat.id, messages.ESTABADDRESS)
def set_estab_address(message):
    # open connection
    conn = sqlite3.connect(config.db_name)
    cursor = conn.cursor()
    # writing establishment
    a = cursor.execute(f"SELECT current FROM {config.users_table} WHERE id='{message.chat.id}'").fetchall()
    a = a[0][0]
    query = "UPDATE " + str(config.estabs_table) + " SET address='" + str(message.text) + "' WHERE id=" + str(a)
    cursor.execute(query)
    # setting reg_stage
    cursor.execute(f"UPDATE {config.users_table} SET reg_stage=9 WHERE id='{message.chat.id}'")
    # close connection
    conn.commit()
    cursor.close()
    conn.close()
    # Sending buttons with categories
    send_categories(message)
def set_estab_category(message):
    # open connection
    conn = sqlite3.connect(config.db_name)
    cursor = conn.cursor()
    # writing establishment's name
    a = cursor.execute(f"SELECT current FROM {config.users_table} WHERE id='{message.chat.id}'").fetchall()
    a = a[0][0]
    query = "UPDATE " + str(config.estabs_table) + " SET category='" + str(message.text) + "' WHERE id=" + str(a)
    cursor.execute(query)
    # setting reg_stage
    cursor.execute(f"UPDATE {config.users_table} SET reg_stage=10 WHERE id='{message.chat.id}'")
    # close connection
    conn.commit()
    cursor.close()
    conn.close()
    bot.send_message(message.chat.id, messages.ESTABPHOTO)
def set_estab_photo(message):
    # open connection
    conn = sqlite3.connect(config.db_name)
    cursor = conn.cursor()
    # writing establishment's name
    a = cursor.execute(f"SELECT current FROM {config.users_table} WHERE id='{message.chat.id}'").fetchall()
    a = a[0][0]
    # Get photo_id
    photo_id = bot.get_file(message.photo[len(message.photo) - 1].file_id).file_id
    query = "UPDATE " + str(config.estabs_table) + " SET photo_id='" + str(photo_id) + "' WHERE id=" + str(a)
    cursor.execute(query)
    # setting reg_stage
    cursor.execute(f"UPDATE {config.users_table} SET reg_stage=11 WHERE id='{message.chat.id}'")
    # close connection
    conn.commit()
    cursor.close()
    conn.close()
    bot.send_message(message.chat.id, messages.ESTABLOCATION)
def set_estab_location(message):
    # open connection
    conn = sqlite3.connect(config.db_name)
    cursor = conn.cursor()
    a = cursor.execute(f"SELECT current FROM {config.users_table} WHERE id='{message.chat.id}'").fetchall()
    a = a[0][0]
    # Get lan and lon
    lon = message.location.longitude
    lat = message.location.latitude
    query = "UPDATE " + str(config.estabs_table) + " SET lon='" + str(lon) + "', lat='"+str(lat)+"' WHERE id=" + str(a)
    cursor.execute(query)
    # setting reg_stage
    cursor.execute(f"UPDATE {config.users_table} SET reg_stage=4 WHERE id='{message.chat.id}'")
    # close connection
    conn.commit()
    cursor.close()
    conn.close()
    bot.send_message(message.chat.id, messages.ESTABREGCOMPLETE)
    bot.send_message(message.chat.id, messages.HELP)

# Making choice
def send_estab(message, estab):
    bot.send_message(message.chat.id, messages.SENDINFO)
    bot.send_message(message.chat.id, messages.SENDNAME + estab[2])
    bot.send_message(message.chat.id, messages.SENDPHOTO)
    bot.send_photo(message.chat.id, estab[6])
    bot.send_message(message.chat.id, messages.SENDADDRESS + estab[4])
    bot.send_message(message.chat.id, messages.SENDLOCATION)
    bot.send_location(message.chat.id, latitude=estab[7], longitude=estab[8])
    bot.send_message(message.chat.id, messages.HELP)
def choose_estab(message):
    # open connection
    conn = sqlite3.connect(config.db_name)
    cursor = conn.cursor()
    # select all establishments
    user_budget = cursor.execute(f"SELECT budget FROM {config.users_table} WHERE id='{message.chat.id}'").fetchall()
    user_category = cursor.execute(f"SELECT category FROM {config.users_table} WHERE id='{message.chat.id}'").fetchall()
    user_budget = user_budget[0][0]
    user_category = user_category[0][0]
    # Looking for appropriate establishment
    all_estabs = cursor.execute(f"SELECT * FROM {config.estabs_table} WHERE avcheck='{user_budget}' AND category='{user_category}'").fetchall()
    if(len(all_estabs) == 0):
        bot.send_message(message.chat.id, messages.ESTABNOTFOUND)
        bot.send_message(message.chat.id, messages.HELP)
    else:
        send_estab(message, random.choice(all_estabs))
    # close connection
    conn.commit()
    cursor.close()
    conn.close()

# Writing criteria to make choice
def create_request(message):
    # open connection
    conn = sqlite3.connect(config.db_name)
    cursor = conn.cursor()
    # setting reg_stage
    cursor.execute(f"UPDATE {config.users_table} SET reg_stage=12  WHERE id='{message.chat.id}'")
    # close connection
    conn.commit()
    cursor.close()
    conn.close()
    send_categories(message)
def set_user_category(message):
    # open connection
    conn = sqlite3.connect(config.db_name)
    cursor = conn.cursor()
    # Writing name
    query = "UPDATE " + str(config.users_table) + " SET category='" + str(message.text) + "', reg_stage=13 WHERE id='" + str(message.chat.id) + "'"
    cursor.execute(query)
    # close connection
    conn.commit()
    cursor.close()
    conn.close()
    send_prices(message)
def set_user_budget(message):
    # open connection
    conn = sqlite3.connect(config.db_name)
    cursor = conn.cursor()
    # Writing name
    query = "UPDATE " + str(config.users_table) + " SET budget='" + str(message.text) + "', reg_stage=4 WHERE id='" + str(message.chat.id) + "'"
    cursor.execute(query)
    # close connection
    conn.commit()
    cursor.close()
    conn.close()
    bot.send_message(message.chat.id, 'Подбираем...')
    choose_estab(message)

# Couchsurfers mode
def set_surfer(message):
    # open connection
    conn = sqlite3.connect(config.db_name)
    cursor = conn.cursor()
    # looking for surfer
    all_surfers = cursor.execute(f"SELECT id FROM {config.users_table} WHERE reg_stage={15}").fetchall()
    if len(all_surfers) == 0:
        bot.send_message(message.chat.id, "К сожалению, не не удалось найти couchsurfer'а")
        cursor.execute(f"UPDATE {config.users_table} SET reg_stage=4 WHERE id='{message.chat.id}'")
    else:
        surfer = random.choice(all_surfers)[0]
        # set reg_status
        cursor.execute(f"UPDATE {config.users_table} SET reg_stage=17 WHERE id='{message.chat.id}'")
        cursor.execute(f"UPDATE {config.users_table} SET reg_stage=17 WHERE id='{surfer}'")
        # Set pair fields pair
        cursor.execute(f"UPDATE {config.users_table} SET pair_id='{surfer}' WHERE id='{message.chat.id}'")
        cursor.execute(f"UPDATE {config.users_table} SET pair_id='{message.chat.id}' WHERE id='{surfer}'")
        # send messages to pair
        bot.send_message(message.chat.id, "Couchsurfer найден!\nДиалог открыт!")
        bot.send_message(surfer, "Кому-то нужна ваща помощь!\nДиалог открыт!")
        bot.send_message(message.chat.id, '/stop_session - остановить сессию')
        bot.send_message(surfer, '/stop_session - остановить сессию')

    # close connection
    conn.commit()
    cursor.close()
    conn.close()
def set_status_tobe(message):
    # open connection
    conn = sqlite3.connect(config.db_name)
    cursor = conn.cursor()
    # set reg_status
    cursor.execute(f"UPDATE {config.users_table} SET reg_stage=15 WHERE id='{message.chat.id}'")
    # close connection
    conn.commit()
    cursor.close()
    conn.close()
    bot.send_message(message.chat.id, messages.SURFERSETTOBE)
def set_status_find(message):
    # open connection
    conn = sqlite3.connect(config.db_name)
    cursor = conn.cursor()
    # set reg_status
    cursor.execute(f"UPDATE {config.users_table} SET reg_stage=16 WHERE id='{message.chat.id}'")
    # close connection
    conn.commit()
    cursor.close()
    conn.close()
    bot.send_message(message.chat.id, messages.SURFERSETFIND)
    set_surfer(message)
def pair_mode(message, content_type):
    # open connection
    conn = sqlite3.connect(config.db_name)
    cursor = conn.cursor()
    # Get id of surfer
    to_id = cursor.execute(f"SELECT pair_id FROM {config.users_table} WHERE id={message.chat.id}").fetchall()
    to_id = to_id[0][0]
    if content_type == 'text':
        bot.send_message(to_id, message.text)
    elif content_type == 'photo':
        # get photo_id
        photo_id = bot.get_file(message.photo[len(message.photo) - 1].file_id).file_id
        bot.send_photo(to_id, photo_id)
    elif content_type == 'location':
        bot.send_location(to_id, longitude=message.location.longitude, latitude=message.location.latitude)
    elif content_type == 'voice':
        bot.send_voice(to_id, message.voice.file_id)
    # close connection
    conn.commit()
    cursor.close()
    conn.close()
def stop_session(message):
    # open connection
    conn = sqlite3.connect(config.db_name)
    cursor = conn.cursor()
    # Get id of surfer
    to_id = cursor.execute(f"SELECT pair_id FROM {config.users_table} WHERE id={message.chat.id}").fetchall()
    to_id = to_id[0][0]
    # close connection of surfers
    # set reg_status
    cursor.execute(f"UPDATE {config.users_table} SET reg_stage=4 WHERE id='{message.chat.id}'")
    cursor.execute(f"UPDATE {config.users_table} SET reg_stage=4 WHERE id='{to_id}'")
    # send messages to pairs
    bot.send_message(message.chat.id, "Сессия окончена!\nДиалог закрыт!")
    bot.send_message(to_id, "Сессия окончена!\nДиалог закрыт!")
    bot.send_message(message.chat.id, messages.HELP)
    bot.send_message(to_id, messages.HELP)
    # close connection
    conn.commit()
    cursor.close()
    conn.close()


# neighbour mode

def set_status_neighbour(message):
    # open connection
    conn = sqlite3.connect(config.db_name)
    cursor = conn.cursor()
    # set reg_status
    cursor.execute(f"UPDATE {config.users_table} SET reg_stage=19 WHERE id='{message.chat.id}'")
    # close connection
    conn.commit()
    cursor.close()
    conn.close()
    bot.send_message(message.chat.id, messages.USERLOCATION)

def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def find_neighbour(message):
    # open connection
    conn = sqlite3.connect(config.db_name)
    cursor = conn.cursor()
    # find neighbours
    all_neighbours = cursor.execute(f"SELECT lat, lon, id FROM {config.users_table} WHERE reg_stage=20 AND id!='{message.chat.id}'").fetchall()
    if len(all_neighbours) > 0:
        user_loc = cursor.execute(f"SELECT lat, lon FROM {config.users_table} WHERE id='{message.chat.id}'").fetchall()
        from_lat = float(user_loc[0][0])
        from_lon = float(user_loc[0][1])
        distances = []
        for i in range(0, len(all_neighbours)):
            to_lat = float(all_neighbours[i][0])
            to_lon = float(all_neighbours[i][1])
            distances.append(distance(from_lat, from_lon, to_lat, to_lon))
        # get surfer's id
        surfer = all_neighbours[numpy.argmin(distances)][2]
        # set reg_status
        cursor.execute(f"UPDATE {config.users_table} SET reg_stage=17 WHERE id='{message.chat.id}'")
        cursor.execute(f"UPDATE {config.users_table} SET reg_stage=17 WHERE id='{surfer}'")
        # Set pair fields pair
        cursor.execute(f"UPDATE {config.users_table} SET pair_id='{surfer}' WHERE id='{message.chat.id}'")
        cursor.execute(f"UPDATE {config.users_table} SET pair_id='{message.chat.id}' WHERE id='{surfer}'")
        # send messages to pair
        bot.send_message(message.chat.id, "Найден человек поблизости!\nДиалог открыт!")
        bot.send_message(surfer, "Найден человек поблизости!\nДиалог открыт!")
        bot.send_message(message.chat.id, '/stop_session - остановить сессию')
        bot.send_message(surfer, '/stop_session - остановить сессию')
    # close connection
    conn.commit()
    cursor.close()
    conn.close()

def cancel(message):
    # open connection
    conn = sqlite3.connect(config.db_name)
    cursor = conn.cursor()
    # set reg_status
    cursor.execute(f"UPDATE {config.users_table} SET reg_stage=4 WHERE id='{message.chat.id}'")
    # close connection
    conn.commit()
    cursor.close()
    conn.close()
    bot.send_message(message.chat.id, messages.HELP)

def set_user_location(message):
    # open connection
    conn = sqlite3.connect(config.db_name)
    cursor = conn.cursor()
    # write location
    # Get lan and lon
    lon = message.location.longitude
    lat = message.location.latitude
    cursor.execute(f"UPDATE {config.users_table} SET lon='{lon}', lat='{lat}' WHERE id='{message.chat.id}'")
    # change reg_stage
    cursor.execute(f"UPDATE {config.users_table} SET reg_stage=20 WHERE id='{message.chat.id}'")
    # close connection
    conn.commit()
    cursor.close()
    conn.close()
    bot.send_message(message.chat.id, 'Поиск людей поблизости...')
    # Дописать эту функцию
    find_neighbour(message)


def modes(message):
    if message.text in config.add_list:
        create_estab(message)
    elif message.text in config.choose_list:
        create_request(message)
    elif message.text in config.tobe_list:
        set_status_tobe(message)
    elif message.text in config.find_list:
        set_status_find(message)
    elif message.text in config.neighbour_list:
        set_status_neighbour(message)
    else:
        bot.send_message(message.chat.id, messages.VOICEERROR)


@bot.message_handler(commands=['start'])
def register(message):
    bot.send_message(message.chat.id, messages.INTRO)
    create_user(message)

@bot.message_handler(commands=['help'])
def user_help(message):
    stage = get_stage(message)
    if stage == 17:
        bot.send_message(message.chat.id, '/stop_session - остановить сессию')
    else:
        help_buttons(message)

@bot.message_handler(commands=['stop_session'])
def user_help(message):
    stage = get_stage(message)
    if stage == 17:
        stop_session(message)

@bot.message_handler(content_types=['text'])
def text_messages(message):
    stage = get_stage(message)
    if stage == 1:
        set_user_name(message)
    if stage == 2:
        set_user_age(message)
    if stage == 3:
        set_user_sex(message)
    if stage == 4:
        modes(message)
    if stage == 6:
        set_estab_name(message)
    if stage == 7:
        set_estab_avcheck(message)
    if stage == 8:
        set_estab_address(message)
    if stage == 9:
        set_estab_category(message)
    if stage == 12:
        set_user_category(message)
    if stage == 13:
        set_user_budget(message)
    if stage == 17:
        pair_mode(message, 'text')


@bot.message_handler(content_types=['location'])
def get_location(message):
    stage = get_stage(message)
    if stage == 11:
        set_estab_location(message)
    elif stage == 17:
        pair_mode(message, 'location')
    if stage == 19:
        set_user_location(message)

@bot.message_handler(content_types=['voice'])
def get_voice(message):
    if voice.voice_to_text(message) in config.cancel_list:
        cancel(message)
    else:
        stage = get_stage(message)
        if stage == 4:
            message.text = voice.voice_to_text(message)
            modes(message)
        if stage == 17:
            pair_mode(message, 'voice')


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    stage = get_stage(message)
    if stage == 10:
        set_estab_photo(message)
    elif stage == 17:
        pair_mode(message, 'photo')

bot.polling(none_stop=True)
