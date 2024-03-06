import os

from pyrogram import *
from pyrogram.types import *

from ubot import *

from ubot.config import *
from ubot.utils import *



@ubot.on_message(anjay("curi") & filters.me)
async def pencuri(client, message):
    dia = message.reply_to_message
    if not dia:
        await client.send_message("me", "<b>Media tidak didukung</b>")
    anjing = dia.caption or None
    mmk = await message.edit_text("Processing...")
    await mmk.delete()
    if dia.text:
        await dia.copy("me")
        await message.delete()
    if dia.photo:
        anu = await client.download_media(dia)
        await client.send_photo("me", anu, anjing)
        await message.delete()
        os.remove(anu)
    if dia.video:
        anu = await client.download_media(dia)
        await client.send_video("me", anu, anjing)
        await message.delete()
        os.remove(anu)
    if dia.audio:
        anu = await client.download_media(dia)
        await client.send_audio("me", anu, anjing)
        await message.delete()
        os.remove(anu)
    if dia.voice:
        anu = await client.download_media(dia)
        await client.send_voice("me", anu, anjing)
        await message.delete()
        os.remove(anu)
    if dia.document:
        anu = await client.download_media(dia)
        await client.send_document("me", anu, anjing)
        await message.delete()
        os.remove(anu)
    try:
        await client.send_message("me", "<b>Pap nya kaka</b>")
    except Exception as e:
        print(e)
