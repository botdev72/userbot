import asyncio

import wget
from pyrogram.enums import *
from pyrogram.types import *

from ubot import *

__MODULE__ = "Misc"
__HELP__ = """
Bantuan Untuk Misc

• Perintah: <code>{0}logger</code> [on/off]
• Penjelasan: Untuk mengetahui jika ada pesan masuk dari pengguna lain, atau ketika anda ditandai oleh orang lain.

- <code>{0}logger on</code> ->  Untuk menghidupkan grup log.
- <code>{0}logger off</code> ->  Untuk mematikan grup log.
- <code>{0}logger clear</code> ->  Untuk menghapus grup log.
"""


async def send_log(client, chat_id, message, message_text, msg):
    try:
        await client.send_message(chat_id, message_text, disable_web_page_preview=True)
        await message.forward(chat_id)
    except Exception as error:
        print(f"{msg} - {error}")


@KY.PC()
async def _(client, message):
    lognya = await get_var(client.me.id, "grup_log")
    status_log = await get_var(client.me.id, "logger_nya")
    if lognya and status_log:
        typenya = "<b>Private</b>"
        user_link = f"[{message.from_user.first_name} {message.from_user.last_name or ''}](tg://user?id={message.from_user.id})"
        message_link = (
            f"tg://openmessage?user_id={message.from_user.id}&message_id={message.id}"
        )
        pesan_nya = f"""
<b>💌 PESAN BARU</b>
<b>• Pesan Dari :</b> <code>{user_link}</code>
<b>• Pesan Tipe :</b> <code>{typenya}</code>
<b>• Lihat Pesan :</b> [Disini]({message_link})
"""
        await send_log(client, int(lognya), message, pesan_nya, "PC")


@KY.GC()
async def _(client, message):
    lognya = await get_var(client.me.id, "grup_log")
    status_log = await get_var(client.me.id, "logger_nya")
    if lognya and status_log:
        typenya = "<b>Group</b>"
        user_link = f"[{message.from_user.first_name} {message.from_user.last_name or ''}](tg://user?id={message.from_user.id})"
        message_link = message.link
        pesan_nya = f"""
<b>💌 PESAN BARU</b>

<b>• Pesan Dari :</b> <code>{user_link}</code>
<b>• Pesan Tipe :</b> <code>{typenya}</code>
<b>• Lihat Pesan :</b> [Disini]({message_link})
"""
        await send_log(client, int(lognya), message, pesan_nya, "GC")


@KY.UBOT("logger")
async def _(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    if len(message.command) < 2:
        return await message.reply(
            f"{emo.gagal} <b>Silakan lihat bantuan untuk menggunakan nya.</b>"
        )

    query = {"on": True, "off": False, "clear": False}
    command = message.command[1].lower()

    if command not in query:
        return await message.reply(
            f"{emo.gagal} <b>Silakan lihat bantuan untuk menggunakan nya.</b>"
        )

    value = query[command]

    vars = await get_var(client.me.id, "grup_log")

    if not vars:
        logs = await buat_lognya(client)
        await set_var(client.me.id, "grup_log", logs)

    if command == "clear" and vars:
        await client.delete_channel(vars)
        await set_var(client.me.id, "grup_log", value)

    await set_var(client.me.id, "logger_nya", value)
    return await message.reply(
        f"<b>{emo.sukses} Logger diatur ke :</b> <code>{value}</code>"
    )


async def buat_lognya(client):
    bot.me.username
    logs = await client.create_supergroup("Uputt-Userbot Logs 🇮🇩")
    url = wget.download("https://telegra.ph/file/6d909b4a1b7b0385c1dfe.jpg")
    desnya = "Group Log untuk Uputt-Userbot.\n\nHARAP JANGAN KELUAR DARI GROUP INI.\n\nPowered By ~ @UputtSupport"
    photo_video = {"video": url} if url.endswith(".mp4") else {"photo": url}
    await client.set_chat_photo(
        logs.id,
        **photo_video,
    )
    await asyncio.sleep(1)
    await client.set_chat_description(
        logs.id,
        desnya,
    )
    await asyncio.sleep(1)

    return logs.id
