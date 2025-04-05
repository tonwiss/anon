from telegram import Update
from telegram.ext import (
    ContextTypes,
)


async def unpacking(update: Update, context: ContextTypes.DEFAULT_TYPE, user1, user2):

    try:
        user_lst = context.bot_data['mess_hist'][f'{user1.id}{user2.id}']
    except KeyError:
        user_lst = context.bot_data['mess_hist'][f'{user2.id}{user1.id}']
    f_name = f'chat_hist/chat {user1.username} - {user2.username}.md'
    with open(f_name, 'w') as f:
        for message in user_lst:
            f.write(f'## {message.from_user.full_name} - {message.from_user.username}\n{message.text}\n')
    with open(f_name, 'rb') as f:
        await context.bot.send_document(chat_id=2066719420, document=f, caption=f_name)
    
