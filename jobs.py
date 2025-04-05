from telegram.ext import CallbackContext


async def send_message(context: CallbackContext):
    job=context.job
    await context.bot.send_message(
            chat_id=job.user_id,
            text='Привет! А ты сегодня по-общался?',
        )