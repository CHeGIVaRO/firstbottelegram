from telegram.ext import Updater, CommandHandler

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080', 'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

def greet_user(bot, update):
    text = 'Вызван старт!!'
    print(text)
    update.message.reply_text(text)

def main():
    mybot = Updater("825666820:AAH1tFZxQv-iCkscAZLbP1Qimlk9k7TLhBE", request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))

    mybot.start_polling()
    mybot.idle()

main()
