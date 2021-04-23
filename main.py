from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
from data import db_session
from data.users import User
from requests import get, post

CHAT_ID = None


def start(update, context):
    update.message.reply_text("Привет, я бот сделанный для проекта в YL. \n"
                              "С помощью меня ты можешь пограть в игру 'кликер'. \n"
                              "Но сначала скажи свое имя")
    return 1


def base_user(update, context):
    global CHAT_ID
    reply_keyboard = [['Играть', 'Топ'], ['Донат'], ['Инфо', 'Магазин']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    CHAT_ID = update.message.chat["id"]
    answer = post('http://127.0.0.1:8080/api/bot/register',
                  json={'name': update.message.text, 'score': 0, 'chat_id': CHAT_ID, 'lvl_click': 1}).json()
    update.message.reply_text(f"{answer['message']}", reply_markup=markup)
    return -1


def game_info(update, context):
    global CHAT_ID
    answer = get(f"http://127.0.0.1:8080/api/bot/game_info/{CHAT_ID}").json()
    reply_keyboard = [[f"+{answer['message']}"], ['Меню']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text("Все что тебе нужно делать - это нажимать на кнопку.", reply_markup=markup)
    return 1


def game(update, context):
    global CHAT_ID
    answer = get(f"http://127.0.0.1:8080/api/bot/game/{CHAT_ID}").json()
    update.message.reply_text(answer['message'])


def menu(update, context):
    reply_keyboard = [['Играть', 'Топ'], ['Донат'], ['Инфо', 'Магазин']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text('Куда пойдем на этот раз?', reply_markup=markup)


def stop(update, context):
    reply_keyboard = [['Играть', 'Топ'], ['Донат'], ['Инфо', 'Магазин']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text('Куда пойдем на этот раз?', reply_markup=markup)
    return -1


def top(update, context):
    reply_keyboard = [['Назад']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    answer = get(f"http://127.0.0.1:8080/api/bot/top").json()
    update.message.reply_text(f"{answer['message']}", reply_markup=markup)


def user_info(update, context):
    global CHAT_ID
    reply_keyboard = [['Назад']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    answer = get(f"http://127.0.0.1:8080/api/bot/user_info/{CHAT_ID}").json()
    update.message.reply_text(answer['message'], reply_markup=markup)


def upgrade(update, context):
    reply_keyboard = [['+2 за клик - 200'], ['+3 за клик - 400'], ['+4 за клик - 600'], ['+5 за клик - 800'], ['Меню']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text('Тут ты можешь потратить свои клики на улучшения', reply_markup=markup)
    return 1


def upgrade_db(update, context):
    global CHAT_ID
    ans_user = update.message.text
    answer = post('http://127.0.0.1:8080/api/bot/upgrade',
                  json={'ans_user': ans_user, 'chat_id': CHAT_ID}).json()
    update.message.reply_text(answer['message'])


def donate(update, context):
    update.message.reply_text('Если ты хочешь поддержать меня то перейди поэтой ссылке.\n'
                              'http://127.0.0.1:8080/donate')


def main():
    with open('Ключи.txt', 'rt') as f:
        Token = str(f.readline().split()[0])
    updater = Updater(Token, use_context=True)
    dp = updater.dispatcher

    start_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            1: [MessageHandler(Filters.text, base_user)]
        },

        fallbacks=[CommandHandler('stop', start)]
    )
    game_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('Играть'), game_info)],

        states={
            1: [MessageHandler(Filters.text & ~Filters.regex('Меню'), game)]
        },

        fallbacks=[MessageHandler(Filters.regex('Меню'), stop)]
    )
    upgrade_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('Магазин'), upgrade)],

        states={
            1: [MessageHandler(Filters.text & ~Filters.regex('Меню'), upgrade_db)]
        },
        fallbacks=[MessageHandler(Filters.regex('Меню'), stop)]
    )
    top_handler = MessageHandler(Filters.regex('Топ'), top)
    donate_handler = MessageHandler(Filters.regex('Донат'), donate)
    info_handler = MessageHandler(Filters.regex('Инфо'), user_info)
    menu_handler = MessageHandler(Filters.regex('Назад'), menu)

    dp.add_handler(donate_handler)
    dp.add_handler(top_handler)
    dp.add_handler(menu_handler)
    dp.add_handler(start_handler)
    dp.add_handler(game_handler)
    dp.add_handler(info_handler)
    dp.add_handler(upgrade_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    db_session.global_init("db/bot.db")
    main()
