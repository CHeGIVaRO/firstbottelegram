import logging
import setting
import ephem
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
from datetime import datetime
from glob import glob
from random import choice
from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO, filename='bot.log')

def cat_sender(bot, update, user_data):
    cat_pic = choice(glob('images/*'))
    bot.send_photo(chat_id = update.message.chat.id, photo = open(cat_pic, 'rb'), reply_markup=get_keyboard())

def get_user_emo(user_data):
    if 'emo' in user_data:
        return user_data['emo']
    else:
        user_data['emo'] = emojize(choice(setting.USER_EMOJI), use_aliases = True)
        return user_data['emo']

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

def get_keyboard():
    contact_button = KeyboardButton('Прислать контакты', request_contact = True)
    location_button = KeyboardButton('Прислать координаты', request_location = True)
    my_keyboard = ReplyKeyboardMarkup([
                                        ['Прислать котика', 'Сменить аватарку'],
                                        [contact_button, location_button]
                                        ], resize_keyboard=True)
    return my_keyboard

def main():
    mybot = Updater(setting.API_KEY, request_kwargs=setting.PROXY)

    logging.info('Bot started')

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user, pass_user_data = True))
    dp.add_handler(CommandHandler("planet", planet_talk, pass_user_data = True))
    dp.add_handler(CommandHandler("cat", cat_sender, pass_user_data = True))
    dp.add_handler(RegexHandler('^(Прислать котика)$', cat_sender, pass_user_data = True))
    dp.add_handler(RegexHandler('^(Сменить аватарку)$', change_avatar, pass_user_data = True))
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data = True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data = True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data = True))

    mybot.start_polling()
    mybot.idle()

main()