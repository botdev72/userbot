# Copas Teriak Copas MONYET
# Gay Teriak Gay Anjeng
# @Rizzvbss | @Kenapanan
# Kok Bacot
# © @KynanSupport
# FULL MONGO NIH JING FIX MULTI CLIENT


import glob
import os
import random
from PIL import *
from pyrogram import *
from pyrogram.types import *

from . import bot, ubot, anjay, eor, cobadah


__MODULE__ = "Write"
__HELP__ = """
Bantuan Untuk Write


• Perintah: <code>{0}nulis</code> [text/reply to text/media]
• Penjelasan: Buat kamu yang malas nulis.
"""


def text_set(text):
    lines = []
    if len(text) <= 55:
        lines.append(text)
    else:
        all_lines = text.split("\n")
        for line in all_lines:
            if len(line) <= 55:
                lines.append(line)
            else:
                k = len(line) // 55
                lines.extend(line[((z - 1) * 55) : (z * 55)] for z in range(1, k + 2))
    return lines[:25]

@ubot.on_message(filters.me & anjay("nulis"))
async def handwrite(client, message):
    if message.reply_to_message:
        naya = message.reply_to_message.text
    else:
        naya = message.text.split(None, 1)[1]
    nan = await eor(message, "Processing...")
    try:
        img = Image.open("ubot/resources/kertas.jpg")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("ubot/resources/fonts/assfont.ttf", 30)
        x, y = 150, 140
        lines = text_set(naya)
        line_height = font.getsize("hg")[1]
        for line in lines:
            draw.text((x, y), line, fill=(1, 22, 55), font=font)
            y = y + line_height - 5
        file = "nulis.jpg"
        img.save(file)
        if os.path.exists(file):
            await message.reply_photo(
                photo=file,
                caption=f"<b>Ditulis Oleh :</b> {client.me.mention}"
            )
            os.remove(file)
            await nan.delete()
    except Exception as e:
        return await message.reply(e)