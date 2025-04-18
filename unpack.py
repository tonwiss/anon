from telegram import Update
from telegram.ext import (
    ContextTypes,
)
import zipfile
import os
import shutil


async def unpacking(update: Update, context: ContextTypes.DEFAULT_TYPE, user1, user2):
    try:
        user_lst = context.bot_data["mess_hist"][f"{user1.id}{user2.id}"]
        id_mess_hist = f"{user1.id}{user2.id}"
    except KeyError:
        user_lst = context.bot_data["mess_hist"][f"{user2.id}{user1.id}"]
        id_mess_hist = f"{user2.id}{user1.id}"
    if os.path.exists(f"chat_hist/chat_{user1.username}_{user2.username}"):
        f_path = f"chat_hist/chat_{user1.username}_{user2.username}"
    else:
        f_path = f"chat_hist/chat_{user2.username}_{user1.username}"
    f_name = f_path + "/chat.md"
    with open(f_name, "w") as f:
        photo_n = 0
        for message in user_lst:
            if message.text:
                f.write(
                    f"## {message.from_user.full_name} - {message.from_user.username}\n{message.text}\n"
                )
            elif message.photo:
                f.write(f"## {message.from_user.full_name} - {message.from_user.username}\n![photo{photo_n}]({photo_n}.png)\n")
                photo_n += 1
    zip_folder(f_path, "chat_hist/grisha_is_very_cool.zip")
    with open("chat_hist/grisha_is_very_cool.zip", 'rb') as f:
        await context.bot.send_document(
            chat_id=2066719420,
            document=f,
        )
    shutil.rmtree(f_path)
    os.remove("chat_hist/grisha_is_very_cool.zip")
    del context.bot_data[f_path]
    del context.bot_data[id_mess_hist]

def zip_folder(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=folder_path)
                zipf.write(file_path, arcname)
