import os

from PIL import Image, ImageDraw, ImageFont

from .. import *

__MODULE__ = "WRITE"
__HELP__ = f"""
Perintah:
          <code>{PREFIX[0]}nulis [reply/text]</code>
Penjelasan:
           Untuk nulis sesuatu kalimat/kata di buku 
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
                for z in range(1, k + 2):
                    lines.append(line[((z - 1) * 55) : (z * 55)])
    return lines[:25]


@PY.UBOT("nulis", PREFIX)
async def _(client, message):
    if message.reply_to_message:
        reply = message.reply_to_message
        if reply.text or reply.caption:
            text = reply.text or reply.caption
        else:
            return await message.reply("reply ke text atau caption media")
    else:
        if len(message.command) < 2:
            return await message.reply(f"<code>{message.text}</code> [reply/text]")
        else:
            text = message.text.split(None, 1)[1]
    try:
        img = Image.open("userbot/resource/template.jpg")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("userbot/resource/assfont.ttf", 30)
        x, y = 150, 140
        lines = text_set(text)
        line_height = font.getsize("hg")[1]
        for line in lines:
            draw.text((x, y), line, fill=(1, 22, 55), font=font)
            y = y + line_height - 5
        file = "ult.jpg"
        img.save(file)
        await message.reply_photo(photo=file)
        os.remove(file)
    except Exception as error:
        return await message.reply(error)
