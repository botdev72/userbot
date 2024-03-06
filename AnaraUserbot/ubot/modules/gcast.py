import asyncio

from pyrogram import *
from pyrogram.enums import ChatType
from pyrogram.errors import BadRequest
from pyrogram.types import *

from . import bot, ubot, anjay, cobadah
from ubot.config import *
from ubot.utils import *

from . import BLACKLIST_CHAT

__MODULE__ = "Broadcast"
__HELP__ = f"""
Bantuan Untuk Broadcast


• Perintah: <code>{cobadah}gucast</code> [text/reply to text/media]
• Penjelasan: Untuk mengirim pesan ke semua user

• Perintah: <code>{cobadah}gcast</code> [text/reply to text/media]
• Penjelasan: Untuk mengirim pesan ke semua group

• Perintah: <code>{cobadah}cancel</code> [text/reply to text/media]
• Penjelasan: Untuk membatalkan proses gcast.

• Perintah: <code>{cobadah}addbl</code>
• Penjelasan: Menambahkan grup kedalam anti Gcast.

• Perintah: <code>{cobadah}delbl</code>
• Penjelasan: Menghapus grup dari daftar anti Gcast.

• Perintah: <code>{cobadah}listbl</code>
• Penjelasan: Melihat daftar grup anti Gcast.


© {bot.me.first_name.split()[0]}
"""



#BARU INIIIIII!!!

broadcast_running = False
gcast_cooldown = timedelta(seconds=5)  # Jeda waktu dalam detik
last_gcast_time = datetime.min  # Waktu terakhir .gcast dijalankan

@ubot.on_message(filters.me & anjay("gcast"))
async def _(client, message: Message):
    global broadcast_running, last_gcast_time

    if len(message.command) < 2 and not message.reply_to_message:
        return await eor(message, "<code>Berikan pesan atau balas pesan...</code>")

    current_time = datetime.now()
    if broadcast_running or (current_time - last_gcast_time) < gcast_cooldown:
        remaining_time = (last_gcast_time + gcast_cooldown - current_time).total_seconds()
        return await eor(message, f"<code>Mohon tunggu {remaining_time:.0f} detik sebelum menggunakan .gcast lagi.</code>")

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
    last_gcast_time = datetime.now()

    if sent > 0:
        await msg.edit(f"✅ Berhasil Terkirim: {sent} \n❌ Gagal Terkirim: {failed}")
    else:
        await msg.edit("<b>Tidak ada grup atau supergrup yang tersedia untuk dikirimkan pesan.</b>")


@ubot.on_message(filters.me & anjay("cancel"))
async def cancel_broadcast(client, message):
    global broadcast_running

    if not broadcast_running:
        return await eor(message, "<code>Tidak ada pengiriman pesan global yang sedang berlangsung.</code>")

    broadcast_running = False
    await eor(message, "<b>Pengiriman pesan global telah dibatalkan!</b>")



#SAMPE LINE INI!!!

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