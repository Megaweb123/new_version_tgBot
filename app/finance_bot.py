import telebot
import datetime
from data import token
from processing.reader import read_history
from processing.polling import polling_tgbot


def fin_bot():
    btns_names = ['История', 'Очистить', 'F.A.Q.']

    @bot.message_handler(commands=['start'])
    def start_message(message):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = telebot.types.KeyboardButton("История")
        btn2 = telebot.types.KeyboardButton("Очистить")
        btn3 = telebot.types.KeyboardButton("F.A.Q.")
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, 'Добро пожаловать!')
        bot.send_message(message.chat.id,
                         'Пишите мне свои траты в формате "Категория - Сумма", и я запишу их.'
                         .format(message.from_user), reply_markup=markup)

    @bot.message_handler(content_types=['text'])
    def write_message(message):
        if message.text not in btns_names:
            try:
                s = message.text.lower().split(' - ')
                int(s[1]) + 1
            except IndexError as error:
                print(message.chat.username, message.chat.id, datetime.datetime.now().strftime('%d-%m-%Y %H:%M'),
                      error, sep='\n', end='\n')
                bot.send_message(message.chat.id, 'Неверный формат данных.\n'
                                                  'Пишите мне свои траты в формате "Категория - Сумма", и я запишу их.')
            except ValueError as error:
                print(message.chat.username, message.chat.id, datetime.datetime.now().strftime('%d-%m-%Y %H:%M'),
                      error, sep='\n', end='\n')
                bot.send_message(message.chat.id, 'Неверный формат данных.\nСумма должна быть целым числом.')
            else:
                categories = read_history(message.chat.username, message.chat.id)
                if s[0].strip() not in categories:
                    categories[s[0].lower().strip()] = int(s[1].strip())
                else:
                    categories[s[0].lower().strip()] += int(s[1].strip())
                with open(
                        f'userdata/{message.chat.username}{message.chat.id}.txt',
                        'w', encoding='utf-8') as file:
                    for i in categories:
                        file.writelines(f'{i} - {categories[i]}\n')
                bot.send_message(message.chat.id,
                                 f'Записал!\nДля вывода информации о ваших тратах, нажмите кнопку "История".'
                                 )
        elif message.text == 'История':
            categories = read_history(message.chat.username, message.chat.id)
            history = ''.join(list(map(lambda item: f'{item.title()} - {categories[item]}руб\n', categories)))
            total = sum(list(map(lambda x: int(categories[x]), categories)))
            if history != '':
                history += f'\nВсего: {total} руб.'
                bot.send_message(message.chat.id, history)
            else:
                bot.send_message(message.chat.id, 'Вы пока что ничего не записывали.')

        elif message.text == 'Очистить':
            with open(f'userdata/{message.chat.username}{message.chat.id}.txt', 'w', encoding='utf-8') as file:
                file.write('')
                bot.send_message(message.chat.id, 'Готово!')
        elif message.text == 'F.A.Q.':
            bot.send_message(message.chat.id, 'Функционал в разработке.')

    polling_tgbot(bot)


bot = telebot.TeleBot(token)
