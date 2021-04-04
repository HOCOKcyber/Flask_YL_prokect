from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
from data import db_session

SCORE = 0


def start(update, context):
    update.message.reply_text("Привет, я бот сделанный для проекта в YL. \n"
                              "С помощью меня ты можешь пограть в игру 'кликер'. \n"
                              "Но сначала скажи свое имя")
    return 1


def base_user(update, context):
    user = update.message.text
    print(user)
    reply_keyboard = [['Играть', 'Топ'],
                      ['Донат']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text(f"Хорошо.  Буду звать тебя, {user}", reply_markup=markup)
    return ConversationHandler.END


def game_info(update, context):
    reply_keyboard = [['+1']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text("Все что тебе нужно делать - это нажимать на кнопку.\n"
                              "Для выхода напиши /end", reply_markup=markup)
    return 1


def game(update, context):
    global SCORE
    SCORE += 1
    reply_keyboard = [['+1']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text(f"Твой счет: {SCORE}", reply_markup=markup)


def end_game(update, context):
    print(1)
    return ConversationHandler.END


def main():
    db_session.global_init("db/blogs.db")
    updater = Updater("1784802519:AAEbBDVSMfPdx2A0uAGXJ6c6SP1117I2b3E", use_context=True)
    dp = updater.dispatcher

    start_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            1: [MessageHandler(Filters.text, base_user)]
        },

        fallbacks=[CommandHandler('stop', start)]
    )
    game_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text, game_info)],

        states={
            1: [MessageHandler(Filters.text & ~Filters.command, game)]
        },

        fallbacks=[CommandHandler('end', end_game)]
    )

    dp.add_handler(start_handler)
    dp.add_handler(game_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
