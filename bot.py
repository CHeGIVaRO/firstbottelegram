from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import setting

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO, filename='bot.log')

def talk_to_me(bot, update):

    user_text = "Привет {}! Ты написал: {}".format(update.message.chat.first_name, update.message.text)
    print(user_text)
    update.message.reply_text(user_text)

def greet_user(bot, update):
    text = 'Вызван старт!!'
    logging.info(text)
    update.message.reply_text(text)

def main():
    mybot = Updater(setting.API_KEY, request_kwargs=setting.PROXY)

    logging.info('Bot started')

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()

main()
