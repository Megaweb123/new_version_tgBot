import datetime


def polling_tgbot(bot):
    while True:
        try:
            bot.polling()
        except BaseException as error:
            print(datetime.datetime.now().strftime('%d-%m-%Y %H:%M'), error)
            continue
