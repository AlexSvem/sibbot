import telebot
import random
from telebot import types
import wikipedia, re
import config
import tokenn
import time
import datetime

bot = telebot.TeleBot(tokenn.TOKEN)

wikipedia.set_lang("ru")
# Чистим текст статьи в Wikipedia и ограничиваем его тысячей символов
def getwiki(s):
    try:
        ny = wikipedia.page(s)
        # Получаем первую тысячу символов
        wikitext=ny.content[:1000]
        # Разделяем по точкам
        wikimas=wikitext.split('.')
        # Отбрасываем всЕ после последней точки
        wikimas = wikimas[:-1]
        # Создаем пустую переменную для текста
        wikitext2 = ''
        # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
        for x in wikimas:
            if not('==' in x):
                    # Если в строке осталось больше трех символов, добавляем ее к нашей переменной и возвращаем утерянные при разделении строк точки на место
                if(len((x.strip()))>3):
                   wikitext2=wikitext2+x+'.'
            else:
                break
        # Теперь при помощи регулярных выражений убираем разметку
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\{[^\{\}]*\}', '', wikitext2)
        # Возвращаем текстовую строку
        return wikitext2
    # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
    except Exception as e:
        return 'В энциклопедии нет информации об этом'


@bot.message_handler(commands=['start'])
def start(mess):
    with open('add_files\dino_work.webp', 'rb') as st:
        bot.send_sticker(mess.chat.id, st)
    time_now = datetime.datetime.now()
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton('Русский 🇷🇺', callback_data='rus')
    item2 = types.InlineKeyboardButton('English 🇬🇧', callback_data='eng')
    markup.add(item1, item2)
    bot.send_message(mess.chat.id, f'<b>Hi {mess.from_user.first_name}</b>\nСейчас: {time_now}\nClick '
                                   f'/functions to see my features\n<b>Choose the language⬇</b>',
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['functions', 'func'])
def func(mess):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    item1 = types.KeyboardButton('/search')
    item2 = types.KeyboardButton('/random_game')
    item3 = types.KeyboardButton('/help')
    item4 = types.KeyboardButton('/wiki')
    item5 = types.KeyboardButton('/')
    item6 = types.KeyboardButton('/about_us')
    markup.add(item1, item2, item3, item4, item5, item6)
    bot.send_message(mess.chat.id, 'Here are my functions', reply_markup=markup)


@bot.message_handler(commands=['about_us'])
def about(message):
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton('Наш GitHub', url='https://github.com/AlexSvem')
    item2 = types.InlineKeyboardButton('Наш сайт[beta]', url='https://yandex.com/')
    item3 = types.InlineKeyboardButton('Наш Vk', url='https://vk.com/')
    item4 = types.InlineKeyboardButton('Наш Тг канал', url='https://t.me/sibna_apps')
    markup.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id,
                     'Я <b>Sib.help</b> созданный командой Sibna для помощи в ознакомлении с нашими новыми сервисами',
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['wiki'])
def get_wiki(message):
    bot.send_message(message.chat.id, 'Пришлите мне слово которое хотите найти в wiki')
    time.sleep(15)
    bot.send_message(message.chat.id, getwiki(message.text))


@bot.message_handler(content_types=['text'])
def tolk(message):
    mess = message.text.lower()
    if 'привет' in mess:
        bot.send_message(message.chat.id, 'И тебе привет')
    elif 'как дела' in mess:
        mess1 = ["У меня все ок, а у тебя как?", "ХайЮ бро мои дела норм, а ты как"]
        rend = random.choice(mess1)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Все окей! 😜')
        item2 = types.KeyboardButton('Нормально 😐')
        item3 = types.KeyboardButton('Все плохо 😡')
        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, f"<b>{rend}</b>", parse_mode='html', reply_markup=markup)

    elif 'все окей' in mess:
        with open('fish_like.tgs', 'rb') as stk1:
            bot.send_sticker(message.chat.id, stk1)
        bot.send_message(message.chat.id, 'Я рад за тебя')
    elif 'нормально' in mess:
        with open('fish_cry.tgs', 'rb') as stk2:
            bot.send_sticker(message.chat.id, stk2)
        bot.send_message(message.chat.id, 'Ну ничего, я думаю мои веселые анекдоты поднимут твое настроение')
    elif 'все плохо' in mess:
        with open('fish_crying.tgs', 'rb') as stk3:
            bot.send_sticker(message.chat.id, stk3)
        bot.send_message(message.chat.id, 'Щя погоди на анекдот 😁')
        bot.send_message(message.chat.id,
                         'Встречаются две Акулы:\n–Ну, как дела?\n-Голодно, объявили запрет на купание…\n–А, я слышала, у вас дайвингистов развилось видимо-невидимо…\n-Да, они жесткие и резиной отдают…\n–Вот, дура, их же чистить надо!')
        with open('chameleo_happy.tgs', 'rb') as stk4:
            bot.send_sticker(message.chat.id, stk4)



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'rus':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Русский 🇷🇺",
                                      reply_markup=None)
                bot.send_message(call.message.chat.id, '<b>Привет</b>, весь остальной текст будет на русском',
                                 parse_mode='html')
                bot.answer_callback_query(callback_query_id=call.id, text="Выбран русский", show_alert=False)
            elif call.data == 'eng':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="English 🇬🇧",
                                      reply_markup=None)
                bot.send_message(call.message.chat.id, '<b>Hello</b>, all other text will be in English',
                                 parse_mode='html')
                bot.answer_callback_query(callback_query_id=call.id, text="English selected", show_alert=False)

    except Exception as e:
        print(repr(e))


@bot.message_handler(content_types=['sticker'])
def sticker(msg):
    d = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    r_stk = random.choice(d)
    try:
        if r_stk == 1:
            bot.send_sticker(msg.chat.id, config.stk1)
        elif r_stk == 2:
            bot.send_sticker(msg.chat.id, config.stk2)
        elif r_stk == 3:
            bot.send_sticker(msg.chat.id, config.stk3)
        elif r_stk == 4:
            bot.send_sticker(msg.chat.id, config.stk4)
        elif r_stk == 5:
            bot.send_sticker(msg.chat.id, config.stk5)
        elif r_stk == 6:
            bot.send_sticker(msg.chat.id, config.stk6)
        elif r_stk == 7:
            bot.send_sticker(msg.chat.id, config.stk7)
        elif r_stk == 8:
            bot.send_sticker(msg.chat.id, config.stk8)
        elif r_stk == 9:
            bot.send_sticker(msg.chat.id, config.stk9)
        elif r_stk == 10:
            bot.send_sticker(msg.chat.id, config.stk10)
        elif r_stk == 11:
            bot.send_sticker(msg.chat.id, config.stk11)
        elif r_stk == 12:
            bot.send_sticker(msg.chat.id, config.stk12)
        elif r_stk == 13:
            bot.send_sticker(msg.chat.id, config.stk13)
        elif r_stk == 14:
            bot.send_sticker(msg.chat.id, config.stk14)
        elif r_stk == 15:
            bot.send_sticker(msg.chat.id, config.stk15)
    except Exception:
        bot.send_message(msg.chat.id, 'Что-то пошло не так')


bot.polling(none_stop=True, interval=0)
