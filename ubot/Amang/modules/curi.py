import os

from pyrogram import *
from pyrogram import filters
from pyrogram.types import *

from Amang import *
from Amang.config import *
from Amang.utils import *


@ubot.on_message(filters.command(["curi"], cmd) & filters.me)
async def pencuri(client, message):
    dia = message.reply_to_message
    client.me.id
    botlog = bot.me.username
    if not dia:
        await client.send_message(botlog, "<b>Media tidak didukung</b>")
    anjing = dia.caption or None
    mmk = await message.edit_text("Processing...")
    await mmk.delete()
    if dia.text:
        await dia.copy(botlog)
        await message.delete()
    if dia.photo:
        anu = await client.download_media(dia)
        await client.send_photo(botlog, anu, anjing)
        await message.delete()
        os.remove(anu)
    if dia.video:
        anu = await client.download_media(dia)
        await client.send_video(botlog, anu, anjing)
        await message.delete()
        os.remove(anu)
    if dia.audio:
        anu = await client.download_media(dia)
        await client.send_audio(botlog, anu, anjing)
        await message.delete()
        os.remove(anu)
    if dia.voice:
        anu = await client.download_media(dia)
        await client.send_voice(botlog, anu, anjing)
        await message.delete()
        os.remove(anu)
    if dia.document:
        anu = await client.download_media(dia)
        await client.send_document(botlog, anu, anjing)
        await message.delete()
        os.remove(anu)
    try:
        await client.send_message(botlog, "<b>Pap nya kaka</b>")
    except Exception as e:
        print(e)
