import os

import requests
from telegraph import upload_file

from .. import *

__MODULE__ = "OCR"
__HELP__ = f"""
Perintah:
         <code>{PREFIX[0]}ocr</code> [reply to media]
Penjelasan:
           Untuk membaca text pada media yang di reply
"""


@PY.UBOT("ocr", PREFIX)
async def _(client, message):
    reply = message.reply_to_message
    if not reply or not reply.photo and not reply.sticker:
        return await message.reply_text(f"{message.text} reply media")
    msg = await message.reply("Membaca pesan media....")
    try:
        file_path = await reply.download()
        if reply.sticker:
            file_path = await reply.download(f"ocr{message.from_user.id}.jpg")
        response = upload_file(file_path)
        url = f"https://telegra.ph{response[0]}"
        req = requests.get(
            f"https://script.google.com/macros/s/AKfycbwURISN0wjazeJTMHTPAtxkrZTWTpsWIef5kxqVGoXqnrzdLdIQIfLO7jsR5OQ5GO16/exec?url={url}"
        ).json()
        await msg.edit(f"<b>Hasil OCR:</b>\n<code>{req['text']}</code>")
        os.remove(file_path)
    except Exception as e:
        await msg.edit(str(e))
        os.remove(file_path)
