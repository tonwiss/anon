from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import (
    ContextTypes,
)
import datetime
from jobs import send_message
from constants import CHECKING_DATA
import pytz

from logging_file import logger


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Пользователь {update.effective_user} запустил бота")
    if update.effective_message.text == "/start":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Привет, {update.effective_user.first_name}\nЭто первая версия анонимки",
            reply_markup=ReplyKeyboardRemove(),
        )
    keyboard = [[InlineKeyboardButton("Начать общение", callback_data="start_talk")]]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Начни прямо сейчас!",
        reply_markup=markup,
    )
    context.job_queue.run_daily(
        send_message,
        datetime.time(hour=20, tzinfo=pytz.timezone("ETC/GMT-3")),
        user_id=update.effective_user.id,
    )
    return CHECKING_DATA
