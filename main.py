from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

from Token import *
from data import *


def give_result(update, context):
    data = list(answers[update.effective_user['id']].values())
    res = []
    chat_id = update.effective_chat.id
    for i in editors_list:
        ed = editors_data[i]
        if all(e in ed["tags"] for e in data):
            res.append(f"{i}:\n{ed['link']}\n")
    context.bot.send_message(text="Вот список редакторов, что могут вам подойти:",
                             chat_id=chat_id, reply_markup=ReplyKeyboardRemove())
    for i in res:
        context.bot.send_message(text=i, chat_id=chat_id)


def text_chat_handler(update, context):
    text = update.message.text
    if text == "Назад↩":
        index = len(answers[update.effective_user['id']])
        answers[update.effective_user['id']].pop(f"q{index}")
        markup = ReplyKeyboardMarkup(keyboards[f"q{index}"][1], resize_keyboard=True)
        update.message.reply_text("Предыдущий вопрос↩", reply_markup=markup)
    elif len(answers[update.effective_user['id']]) == 0 and text in ["Растровый◼", "Векторный↗"]:
        markup = ReplyKeyboardMarkup(keyboards["q2"][1], resize_keyboard=True)
        if text == "Растровый◼":
            answers[update.effective_user['id']]["q1"] = "Растровый"
        elif text == "Векторный↗":
            answers[update.effective_user['id']]["q1"] = "Векторный"
        update.message.reply_text("Следующий вопрос⚙", reply_markup=markup)
        context.bot.send_message(text=keyboards["q2"][0], chat_id=update.effective_chat.id)
    elif len(answers[update.effective_user['id']]) == 1 and text in ["Windows🪟", "Linux/macOS🌐"]:
        markup = ReplyKeyboardMarkup(keyboards["q3"][1], resize_keyboard=True)
        if text == "Windows🪟":
            answers[update.effective_user['id']]["q2"] = "Windows"
        elif text == "Linux/macOS🌐":
            answers[update.effective_user['id']]["q2"] = "Linux/macOS"
        update.message.reply_text("Следующий вопрос⚙", reply_markup=markup)
        context.bot.send_message(text=keyboards["q3"][0], chat_id=update.effective_chat.id)
    elif len(answers[update.effective_user['id']]) == 2 and text in ["Да. Важна✅", "Нет. Не важна❌"]:
        markup = ReplyKeyboardMarkup(keyboards["q4"][1], resize_keyboard=True)
        if text == "Да. Важна✅":
            answers[update.effective_user['id']]["q3"] = "Плагины"
        elif text == "Нет. Не важна❌":
            answers[update.effective_user['id']]["q3"] = "Любой"
        update.message.reply_text("Следующий вопрос⚙", reply_markup=markup)
        context.bot.send_message(text=keyboards["q4"][0], chat_id=update.effective_chat.id)
    elif len(answers[update.effective_user['id']]) == 3 and text in ["Бесплатный🔶", "Платный🟥", "Любой🔷"]:
        markup = ReplyKeyboardMarkup(keyboards["q5"][1], resize_keyboard=True)
        if text == "Бесплатный🔶":
            answers[update.effective_user['id']]["q4"] = "Бесплатный"
        elif text == "Платный🟥":
            answers[update.effective_user['id']]["q4"] = "Платный"
        elif text == "Любой🔷":
            answers[update.effective_user['id']]["q4"] = "Любой"
        update.message.reply_text("Последний Вопрос⚙", reply_markup=markup)
        context.bot.send_message(text=keyboards["q5"][0], chat_id=update.effective_chat.id)
    elif len(answers[update.effective_user['id']]) == 4 and text in ["Необходима🔧", "Не важно◼"]:
        if text == "Необходима🔧":
            answers[update.effective_user['id']]["q5"] = "Анимации"
        elif text == "Не важно◼":
            answers[update.effective_user['id']]["q5"] = "Любой"
        update.message.reply_text("Результаты:", reply_markup=ReplyKeyboardRemove())
        give_result(update, context)


def start(update, context):
    markup = ReplyKeyboardMarkup(keyboards["q1"][1], resize_keyboard=True)
    update.message.reply_text("Приветствую, я бот. Я помогу Вам в выборе графического редактора."
                              "Ответьте на вопросы и получите результат.", reply_markup=markup)
    context.bot.send_message(text=keyboards["q1"][0], chat_id=update.effective_chat.id)
    answers[update.effective_user['id']] = {}


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("res", give_result))
    text_handler = MessageHandler(Filters.text & ~Filters.command, text_chat_handler)
    dp.add_handler(text_handler)
    updater.start_polling()
    print("Старт!")
    updater.idle()


if __name__ == "__main__":
    main()
