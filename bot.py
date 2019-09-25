import setting
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler
from telegram.ext import messagequeue as mq
from handlers import *
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO, filename='bot.log')

subscribers = set()



def my_test(bot, job):
    #bot.sendMessage(chat_id=307570156, text="Spam,Spam,Spam!!")
    job.interval += 5
    if job.interval > 20:
        bot.sendMessage(chat_id=307570156, text="Poka!")
        job.schedule_removal()

def main():
    mybot = Updater(setting.API_KEY, request_kwargs=setting.PROXY)
    mybot.bot._msg_queue = mq.MessageQueue()
    mybot.bot._is_messages_queued_default = True

    logging.info('Bot started')

    dp = mybot.dispatcher

    mybot.job_queue.run_repeating(my_test, interval=5)
    mybot.job_queue.run_repeating(send_updates, interval=5)

    dp.add_handler(CommandHandler('alarm', set_alarm, pass_args=True, pass_job_queue=True))
    dp.add_handler(CommandHandler('subscribe', subscribe))
    dp.add_handler(CommandHandler('unsubscribe', unsubscribe))
    dp.add_handler(CommandHandler("start", greet_user, pass_user_data = True))
    dp.add_handler(CommandHandler("planet", planet_talk, pass_user_data = True))
    dp.add_handler(CommandHandler("cat", cat_sender, pass_user_data = True))
    dp.add_handler(RegexHandler('^(Прислать котика)$', cat_sender, pass_user_data = True))
    dp.add_handler(RegexHandler('^(Сменить аватарку)$', change_avatar, pass_user_data = True))
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data = True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data = True))
    dp.add_handler(MessageHandler(Filters.photo, check_user_photo, pass_user_data=True))
    anketa = ConversationHandler(
        entry_points=[RegexHandler('^(Заполнить анкету)$', anketa_start, pass_user_data=True)],
        states={
            "name": [MessageHandler(Filters.text, anketa_get_name, pass_user_data=True)],
            "rating": [RegexHandler('^(1|2|3|4|%)$', anketa_rating, pass_user_data=True)],
            "comment": [MessageHandler(Filters.text, anketa_comment, pass_user_data=True),
                        CommandHandler('cancel', anketa_cancel_comment, pass_user_data=True)]
        },
        fallbacks=[]
    )
    dp.add_handler(anketa)
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()