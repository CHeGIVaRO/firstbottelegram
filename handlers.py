from utils import get_keyboard, get_user_emo, is_cat
from datetime import datetime
from glob import glob
import ephem
from random import choice
import os
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler
from  bot import subscribers
from telegram.ext import messagequeue as mq

def anketa_start(bot, update, user_data):
    update.message.reply_text("Как вас зовут? Напишите имя и фамилию", reply_markup=ReplyKeyboardRemove())
    return "name"

def anketa_cancel_comment(bot, update, user_data):
    user_text = """
    <b>Имя фамилия: </b> {anketa_name}    
    <b>Оценка: </b> {anketa_rating} """.format(**user_data)
    update.message.reply_text(user_text, reply_markup=get_keyboard(), parse_mode=ParseMode.HTML)
    return ConversationHandler.END

def anketa_comment(bot, update, user_data):
    user_data["anketa_comment"] = update.message.text
    user_text= """
    <b>Имя фамилия: </b> {anketa_name}    
    <b>Оценка: </b> {anketa_rating} 
    <b>Комментарий: </b> {anketa_comment}""".format(**user_data)
    update.message.reply_text(user_text,reply_markup=get_keyboard(), parse_mode=ParseMode.HTML)
    return ConversationHandler.END

def anketa_get_name(bot, update, user_data):
    user_name = update.message.text
    if len(user_name.split(" ")) != 2:
        update.message.reply_text("Введите корректное имя и фамилию")
        return "name"
    else:
        user_data['anketa_name'] = user_name
        reply_keyboard = [["1", "2", "3", "4", "5"]]
        update.message.reply_text("Цените нашего бота от 1 до 5",
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return "rating"

def cat_sender(bot, update, user_data):
    cat_pic = choice(glob('images/*'))
    bot.send_photo(chat_id = update.message.chat.id, photo = open(cat_pic, 'rb'), reply_markup=get_keyboard())

def planet_answer(planet, planet_name):
    const = ephem.constellation(planet)
    answer = 'Планета {} на данный момент находится в созвездии {}.'.format(planet_name, const[1])
    return answer

def planet_talk(bot, update, user_data):
    planet_name = "зельдобаран"
    user_text = update.message.text.split(' ')
    user_planet = user_text[1]
    if user_planet == 'Меркурий':
        planet_name = 'Меркурий'
        planet = ephem.Mercury(datetime.now())
        update.message.reply_text(planet_answer(planet, planet_name), reply_markup=get_keyboard())
    if user_planet == 'Венера':
        planet_name = 'Венера'
        planet = ephem.Venus(datetime.now())
        update.message.reply_text(planet_answer(planet, planet_name), reply_markup=get_keyboard())
    if user_planet == 'Марс':
        planet_name = 'Марс'
        planet = ephem.Mars(datetime.now())
        update.message.reply_text(planet_answer(planet, planet_name), reply_markup=get_keyboard())
    if user_planet == 'Юпитер':
        planet_name = 'Юпитер'
        planet = ephem.Jupiter(datetime.now())
        update.message.reply_text(planet_answer(planet, planet_name), reply_markup=get_keyboard())
    if user_planet == 'Сатурн':
        planet_name = 'Сатурн'
        planet = ephem.Saturn(datetime.now())
        update.message.reply_text(planet_answer(planet, planet_name), reply_markup=get_keyboard())
    if user_planet == 'Уран':
        planet_name = 'Уран'
        planet = ephem.Uranus(datetime.now())
        update.message.reply_text(planet_answer(planet, planet_name), reply_markup=get_keyboard())
    if user_planet == 'Нептун':
        planet_name = 'Нептун'
        planet = ephem.Neptune(datetime.now())
        update.message.reply_text(planet_answer(planet, planet_name), reply_markup=get_keyboard())
    if user_planet == 'Плутон':
        update.message.reply_text("Плутон не Планета!!!!", reply_markup=get_keyboard())

def talk_to_me(bot, update, user_data):
    smile = get_user_emo(user_data)
    user_data['emo'] = smile
    user_text = "{}! {} Ты написал: {}".format(update.message.chat.first_name, user_data['emo'], update.message.text)
    update.message.reply_text(user_text, reply_markup=get_keyboard())

def greet_user(bot, update, user_data):
    print(update.message.chat_id)
    smile = get_user_emo(user_data)
    user_data['emo'] = smile
    text = 'Привет {}! {} Я тестовый бот и пока очень тупой, я всего лиш умею пофторять за тобой сообщения. Знаю комманду /start, результат которой ты сейчас наблюдаешь, а так же знаю команду /planet которая подскажет тебе в каком созвездии находится планета(прим: /planet Марс), так же я могу прислать тебе случайного котики /cat'.format(update.message.chat.first_name, smile)

    update.message.reply_text(text, reply_markup=get_keyboard())

def change_avatar(bot, update, user_data):
    if 'emo' in user_data:
        del user_data['emo']
    smile = get_user_emo(user_data)
    update.message.reply_text(f'Готово: {smile}', reply_markup=get_keyboard())

def get_contact(bot, update, user_data):
    print(update.message.contact)
    update.message.reply_text('Готово: {}'.format(get_user_emo(user_data)), reply_markup=get_keyboard())

def get_location(bot, update, user_data):
    print(update.message.location)
    update.message.reply_text('Готово: {}'.format(get_user_emo(user_data)), reply_markup=get_keyboard())

def check_user_photo(bot, update, user_data):
    update.message.reply_text("Обрабатываю фото")
    os.makedirs('downloads', exist_ok=True)
    photo_file = bot.getFile(update.message.photo[-1].file_id)
    filename = os.path.join('downloads', f'{photo_file.file_id}.jpg')
    photo_file.download(filename)
    if is_cat(filename):
        update.message.reply_text("Обнаружен котик, добавляю в библиотеку")
        new_filename = os.path.join('images', f'{photo_file.file_id}.jpg')
        os.rename(filename, new_filename)
    else:
        os.remove(filename)
        update.message.reply_text("Тревога, котик не обнаружен!!")

def anketa_rating(bot, update, user_data):
    user_data['anketa_rating'] = update.message.text
    update.message.reply_text("Введие комментария пожалуйста в свободной форме или /cancel что бы пропустить")
    return "comment"

def subscribe(bot, update):
    subscribers.add(update.message.chat_id)
    update.message.reply_text('Вы подписались.')
    print(subscribers)

@mq.queuedmessage
def send_updates(bot, job):
    for chat_id in subscribers:
        bot.sendMessage(chat_id=chat_id, text="Уведомление")

def unsubscribe(bot, update):
    if update.message.chat_id in subscribers:
        subscribers.remove(update.message.chat_id)
        update.message.reply_text('Вы описанны')
    else:
        update.message.reply_text('Вы и не подписанный')
    print(subscribers)

def set_alarm(bot, update, args, job_queue):
    try:
        seconds = abs(int(args[0]))
        job_queue.run_once(alarm, seconds, context=update.message.chat_id)
    except (IndexError, ValueError):
        update.message.reply_text("Введите число секунд после комманды /alarm")

@mq.queuedmessage
def alarm(bot, job):
    bot.send_message(chat_id=job.context, text='BUZZZZZZZZZ!')