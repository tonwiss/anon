from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ContextTypes,
)
from start import start
from unpack import unpacking
import os


async def message_processing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in context.bot_data["dialogs"]:
        return
    keyboard = [["Остановить общение"]]
    user1 = update.effective_user
    user2 = context.bot_data["dialogs"][user1.id]
    markup = ReplyKeyboardMarkup(
        keyboard=keyboard,
    )
    if update.effective_message.text:
        await context.bot.send_message(
            chat_id=context.bot_data["dialogs"][update.effective_user.id].id,
            text=update.effective_message.text,
            reply_markup=markup,
        )
        if f"{user1.id}{user2.id}" in context.bot_data[f"mess_hist"]:
            context.bot_data[f"mess_hist"][f"{user1.id}{user2.id}"].append(
                update.effective_message
            )
        else:
            context.bot_data[f"mess_hist"][f"{user2.id}{user1.id}"].append(
                update.effective_message
            )
    elif update.effective_message.photo:
        print("AAAAAAAAAAAAAAAAAAAAAAA")
        keyboard = [["Остановить общение"]]
        markup = ReplyKeyboardMarkup(
            keyboard=keyboard,
        )
        photo_file = await update.effective_message.photo[-1].get_file()
        if os.path.exists(f"chat_hist/chat_{user1.username}_{user2.username}"):
            f_path = f"chat_hist/chat_{user1.username}_{user2.username}"
        else:
            f_path = f"chat_hist/chat_{user2.username}_{user1.username}"
        photo_num = context.bot_data[f_path]
        await photo_file.download_to_drive(f"{f_path}/{photo_num}.png")
        context.bot_data[f_path] += 1
        with open(f"{f_path}/{photo_num}.png", "rb") as f:
            await context.bot.send_photo(
                chat_id=context.bot_data["dialogs"][update.effective_user.id].id,
                photo=f,
                reply_markup=markup,
            )
        if f"{user1.id}{user2.id}" in context.bot_data[f"mess_hist"]:
            context.bot_data[f"mess_hist"][f"{user1.id}{user2.id}"].append(
                update.effective_message
            )
        else:
            context.bot_data[f"mess_hist"][f"{user2.id}{user1.id}"].append(
                update.effective_message
            )


async def stop_messaging(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user2 = context.bot_data["dialogs"][update.effective_user.id]
    user1 = context.bot_data["dialogs"][user2.id]
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text="Вы остановили общение, но можете продолжить в то время, когда захотите",
    )
    keyboard = [["Искать новую пару"], ["Меню"]]
    markup = ReplyKeyboardMarkup(
        keyboard=keyboard,
    )
    await context.bot.send_message(
        chat_id=user2.id,
        text="Пользователь остановил общение. Уже ищем Вам новую пару...",
        reply_markup=markup,
    )
    del context.bot_data["dialogs"][update.effective_user.id]
    del context.bot_data["dialogs"][user2.id]
    await unpacking(update, context, user1, user2)
    return await start(update, context)
