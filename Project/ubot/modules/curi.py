import os

from pyrogram import *
from pyrogram.types import *

from ubot import *
from ubot.config import *
from ubot.utils import *


@KY.UBOT("curi", sudo=True)
async def pencuri(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    dia = message.reply_to_message
    if not dia:
        return
    anjing = dia.caption or None
    mmk = await message.edit_text(f"{emo.proses} **Processing...**")
    await mmk.delete()
    lognya = await get_var(client.me.id, "grup_log")
    status_log = await get_var(client.me.id, "logger_nya")
    if lognya and status_log:
        if dia.text:
            await dia.copy(int(lognya))
            await message.delete()
        if dia.photo:
            anu = await client.download_media(dia)
            await client.send_photo(int(lognya), anu, anjing)
            await message.delete()
            os.remove(anu)
        if dia.video:
            anu = await client.download_media(dia)
            await client.send_video(int(lognya), anu, anjing)
            await message.delete()
            os.remove(anu)
        if dia.audio:
            anu = await client.download_media(dia)
            await client.send_audio(int(lognya), anu, anjing)
            await message.delete()
            os.remove(anu)
        if dia.voice:
            anu = await client.download_media(dia)
            await client.send_voice(int(lognya), anu, anjing)
            await message.delete()
            os.remove(anu)
        if dia.document:
            anu = await client.download_media(dia)
            await client.send_document(int(lognya), anu, anjing)
            await message.delete()
            os.remove(anu)
        try:
            await client.send_message(int(lognya), f"{emo.sukses} <b>Pap nya kaka</b>")
        except Exception as e:
            print(e)
    else:
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
            await client.send_message("me", f"{emo.sukses} <b>Pap nya kaka</b>")
        except Exception as e:
            print(e)
