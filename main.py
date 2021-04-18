from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
from data import db_session
from data.users import User
import os

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
    db_sess = db_session.create_session()
    CHAT_ID = update.message.chat["id"]
    bd = db_sess.query(User).filter(User.chat_id == CHAT_ID).first()
    if bd:
        update.message.reply_text(f"Шучу, я знаю, что тебя зовут, {bd.name}", reply_markup=markup)
    else:
        user_db = User(name=update.message.text, score=0, chat_id=CHAT_ID, lvl_click=1)
        db_sess.add(user_db)
        db_sess.commit()
        update.message.reply_text(f"Хорошо. Буду звать тебя, {update.message.text}", reply_markup=markup)
    return -1


def game_info(update, context):
    global CHAT_ID
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.chat_id == CHAT_ID).first()
    reply_keyboard = [[f'+{user.lvl_click}'], ['Меню']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text("Все что тебе нужно делать - это нажимать на кнопку.\n", reply_markup=markup)
    return 1


def game(update, context):
    global CHAT_ID
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.chat_id == CHAT_ID).first()
    user.score += user.lvl_click
    update.message.reply_text(f"Твой счет: {user.score}")
    db_sess.commit()


def menu(update, context):
    reply_keyboard = [['Играть', 'Топ'], ['Донат'], ['Инфо', 'Магазин']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text('Куда пойдем на этот раз?', reply_markup=markup)
    db_sess = db_session.create_session()
    user = db_sess.query(User.score, User.name)
    for i in user:
        print(i.name, i.score)
    a = update.message.chat["id"]
    print(a)


def stop(update, context):
    reply_keyboard = [['Играть', 'Топ'], ['Донат'], ['Инфо', 'Магазин']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text('Куда пойдем на этот раз?', reply_markup=markup)
    return -1


def top(update, context):
    reply_keyboard = [['Назад']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    db_sess = db_session.create_session()
    user = db_sess.query(User.score, User.name)
    top = {}
    ms = 'Топ лучших \n'
    for i in user:
        top[i.name] = i.score
    list_keys = list(top.keys())
    list_keys.sort()
    for i in list_keys[::-1]:
        ms += f"{i} : {top[i]} \n"
    update.message.reply_text(f'{ms}', reply_markup=markup)


def user_info(update, context):
    global CHAT_ID
    reply_keyboard = [['Назад']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.chat_id == CHAT_ID).first()
    update.message.reply_text(
        f' Твое имя: {user.name} \nТвой счет: {user.score} \nТвой прирост за клик: {user.lvl_click}',
        reply_markup=markup)


def upgrade(update, context):
    reply_keyboard = [['+2 за клик - 200'], ['+3 за клик - 400'], ['+4 за клик - 600'], ['+5 за клик - 800'], ['Меню']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text('Тут ты можешь потратить свои клики на улучшения', reply_markup=markup)
    return 1


def upgrade_dp(update, context):
    global CHAT_ID
    ans_user = update.message.text
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.chat_id == CHAT_ID).first()
    if ans_user == '+2 за клик - 200' and user.score >= 200:
        user.lvl_click += 2
        user.score -= 200
        update.message.reply_text(f'Успешно.  На твоем счету осталось {user.score}')
    elif ans_user == '+3 за клик - 400' and user.score >= 400:
        user.lvl_click += 3
        user.score -= 400
        update.message.reply_text(f'Успешно.  На твоем счету осталось {user.score}')
    elif ans_user == '+4 за клик - 600' and user.score >= 600:
        user.lvl_click += 4
        user.score -= 600
        update.message.reply_text(f'Успешно.  На твоем счету осталось {user.score}')
    elif ans_user == '+5 за клик - 800' and user.score >= 800:
        user.lvl_click += 5
        user.score -= 800
        update.message.reply_text(f'Успешно.  На твоем счету осталось {user.score}')
    else:
        update.message.reply_text('У тебя не кликов на эту покупку')
    db_sess.commit()


def donate(update, context):
    update.message.reply_text('Если ты хочешь поддержать меня то перейди поэтой ссылке.\n'
                              'http://127.0.0.1:8080/donate')

    # os.system('python flask_main.py')


def main():
    db_session.global_init("db/blogs.db")
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
            1: [MessageHandler(Filters.text & ~Filters.regex('Меню'), upgrade_dp)]
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
    main()
