import asyncio
import time
from datetime import datetime, timedelta

from pyrogram import *
from pyrogram.enums import ChatType
from pyrogram.errors import BadRequest
from pyrogram.types import *

from ubot import *

from ubot.config import *
from ubot.utils import *


__MODULE__ = "Broadcast"
__HELP__ = """
Bantuan Untuk Broadcast

• Perintah: <code>{0}gucast</code> [text/reply to text/media]
• Penjelasan: Untuk mengirim pesan ke semua user

• Perintah: <code>{0}gcast</code> [text/reply to text/media]
• Penjelasan: Untuk mengirim pesan ke semua group

• Perintah: <code>{0}addbl</code>
• Penjelasan: Menambahkan grup kedalam anti Gcast.

• Perintah: <code>{0}delbl</code>
• Penjelasan: Menghapus grup dari daftar anti Gcast.

• Perintah: <code>{0}listbl</code>
• Penjelasan: Melihat daftar grup anti Gcast.
"""



#BARU INIIIIII!!!

broadcast_running = False
gcast_cooldown = timedelta(seconds=5)  # Jeda waktu dalam detik
last_gcast_time = datetime.min  # Waktu terakhir .gcast dijalankan

@ubot.on_message(filters.me & anjay("gcast"))
async def _(client, message: Message):
    sent = 0
    #failed = 0
    user_id = client.me.id
    msg = await message.reply("<code>Processing Global Broadcast...</code>")
    list_blchat = await blacklisted_chats(user_id)
    async for dialog in client.get_dialogs(limit=None):
        if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            if message.reply_to_message:
                send = message.reply_to_message
            else:
                if len(message.command) < 2:
                    return await msg.edit(
                        "<code>Berikan pesan atau balas pesan...</code>"
                    )
                else:
                    send = message.text.split(None, 1)[1]
            chat_id = dialog.chat.id
            if chat_id not in list_blchat and chat_id not in BLACKLIST_CHAT:
                try:
                    if message.reply_to_message:
                        await send.copy(chat_id)
                    else:
                        await client.send_message(chat_id, send)
                    sent += 1
                    await asyncio.sleep(1)
                except Exception:
                    #failed += 1
                    pass
                    #await asyncio.sleep(1)
    return await msg.edit(f"**Successfully Sent Message To `{sent}` Groups chat**.")


@ubot.on_message(filters.me & anjay("cancel"))
async def cancel_broadcast(client, message):
    global broadcast_running

    if not broadcast_running:
        return await message.reply("<code>Tidak ada pengiriman pesan global yang sedang berlangsung.</code>")

    broadcast_running = False
    await message.reply("<code>Pengiriman pesan global telah dibatalkan!</code>")



#SAMPE LINE INI!!!

@ubot.on_message(filters.me & anjay("gucast"))
async def _(client, message: Message):
    sent = 0
    #failed = 0
    msg = await message.reply("Processing...")
    async for dialog in client.get_dialogs(limit=None):
        if dialog.chat.type == ChatType.PRIVATE:
            if message.reply_to_message:
                send = message.reply_to_message
            else:
                if len(message.command) < 2:
                    return await msg.edit(
                        "Mohon berikan pesan atau balas ke pesan..."
                    )
                else:
                    send = message.text.split(None, 1)[1]
            chat_id = dialog.chat.id
            if chat_id not in DEVS:
                try:
                    if message.reply_to_message:
                        await send.copy(chat_id)
                    else:
                        await client.send_message(chat_id, send)
                    sent += 1
                    await asyncio.sleep(1)
                except Exception:
                    #failed += 1
                    pass
                    #await asyncio.sleep(1)
    await msg.edit(f"**Successfully Sent Message To `{sent}` Groups chat**")


@ubot.on_message(filters.me & anjay("addbl"))
async def bl_chat(client, message):
    chat_id = message.chat.id
    chat = await client.get_chat(chat_id)
    if chat.type == "private":
        return await message.reply("Maaf, perintah ini hanya berlaku untuk grup.")
    user_id = client.me.id
    bajingan = await blacklisted_chats(user_id)
    if chat in bajingan:
        return await message.reply("Obrolan sudah masuk daftar Blacklist Gcast.")
    await blacklist_chat(user_id, chat_id)
    await message.reply(
        "Obrolan telah berhasil dimasukkan ke dalam daftar Blacklist Gcast."
    )


@ubot.on_message(filters.me & anjay("delbl"))
async def del_bl(client, message):
    if len(message.command) != 2:
        return await message.reply(
            message, "<b>Gunakan Format:</b>\n <code>delbl [CHAT_ID]</code>"
        )
    user_id = client.me.id
    chat_id = int(message.text.strip().split()[1])
    if chat_id not in await blacklisted_chats(user_id):
        return await message.reply(
            "Obrolan berhasil dihapus dari daftar Blacklist Gcast."
        )
    whitelisted = await whitelist_chat(user_id, chat_id)
    if whitelisted:
        return await message.reply(
            "Obrolan berhasil dihapus dari daftar Blacklist Gcast."
        )
    else:
        await message.reply("Sesuatu yang salah terjadi.")


@ubot.on_message(filters.me & anjay("listbl"))
async def all_chats(client, message):
    proses = await message.reply(
        "Tunggu Sebentar..."
    )
    served_chats = await blacklisted_chats(client.me.id)
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await client.get_chat(x)).title
        except Exception:
            title = "Private Group"
        if (await client.get_chat(x)).username:
            user = (await client.get_chat(x)).username
            text += f"<b>{j + 1}.</b>  [{title}](https://t.me/{user})[`{x}`]\n"
        else:
            text += f"<b>{j + 1}. {title}</b> [`{x}`]\n"
        j += 1
    if not text:
        await proses.edit_text("Tidak ada daftat blacklist gcast.")
    else:
        await proses.edit_text(
            f"**Daftar Blacklist Gcast: **\n\n{text}",
            disable_web_page_preview=True,
        )