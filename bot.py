import logging
import setting
import ephem
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
from datetime import datetime
from glob import glob
from random import choice
from utils import get_keyboard, get_user_emo
from handlers import *

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO, filename='bot.log')

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

if __name__ == '__main__':
    main()