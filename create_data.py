from telegram import Update, ReplyKeyboardMarkup
import os
from telegram.ext import (
    ContextTypes,
)
from constants import CHATTING
from logging_file import logger
from start import start


async def check_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.bot_data.get("users_list"):
        context.bot_data["users_list"] = []
    context.bot_data["users_list"].append(update.effective_user)
    logger.info(f"{context.bot_data['users_list']}")
    keyboard = [["Прекратить поиск"]]
    markup = ReplyKeyboardMarkup(
        keyboard=keyboard,
    )
    if len(context.bot_data["users_list"]) == 1:
        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text="Ищем собеседника",
            reply_markup=markup,
        )
    else:
        user1 = context.bot_data["users_list"][0]
        user2 = context.bot_data["users_list"][1]
        if not context.bot_data.get("dialogs"):
            context.bot_data["dialogs"] = {}
        context.bot_data["dialogs"][user1.id] = user2
        context.bot_data["dialogs"][user2.id] = user1
        if not context.bot_data.get("mess_hist"):
            context.bot_data["mess_hist"] = {}
        context.bot_data["mess_hist"][f'{user1.id}{user2.id}'] = []
        if not os.path.isdir(f'chat_hist/chat_{user1.username}_{user2.username}'):
            os.mkdir(path=f'chat_hist/chat_{user1.username}_{user2.username}')
        context.bot_data[f'chat_hist/chat_{user1.username}_{user2.username}'] = 0
        await context.bot.send_message(
            chat_id=user1.id,
            text="Начинай общение",
        )
        await context.bot.send_message(
            chat_id=user2.id,
            text="Начинай общение",
        )
        context.bot_data["users_list"] = []
    return CHATTING


async def stop_searching(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.bot_data["users_list"] = []
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text=f"Если захотите общаться - только скажите! Хорошего дня, {update.effective_user.name}",
    )
    return await start(update, context)
