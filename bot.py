import os
from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackQueryHandler,
)
from start import start
from create_data import check_user, stop_searching
from message_proc import message_processing, stop_messaging


from constants import CHATTING, CHECKING_DATA

load_dotenv()


if __name__ == "__main__":
    # persistence = PicklePersistence(filepath="anon")
    # application = (
    #     ApplicationBuilder().token(os.getenv("TOKEN")).persistence(persistence).build()
    # )
    application = ApplicationBuilder().token(os.getenv("TOKEN")).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHATTING: [
                MessageHandler(filters.Regex("^Остановить общение$"), stop_messaging),
                MessageHandler(filters.Regex("^Искать новую пару$"), check_user),
                MessageHandler(filters.Regex("^Меню$"), start),
                MessageHandler(filters.Regex("^Прекратить поиск$"), stop_searching),
                MessageHandler(filters.TEXT & ~filters.COMMAND, message_processing),
            ],
            CHECKING_DATA: [
                CallbackQueryHandler(check_user),
            ],

        },
        fallbacks=[CommandHandler("start", start)],
    )
    application.add_handler(conv_handler)
    #application.job_queue()

    application.run_polling()
