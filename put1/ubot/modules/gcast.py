import asyncio
import time
from datetime import datetime, timedelta
from gc import get_objects

from pyrogram import *
from pyrogram.enums import ChatType
from pyrogram.errors import BadRequest
from pyrogram.types import *

from pyrogram.errors.exceptions import FloodWait

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

• Perintah : <code>{0}cancel</code>
• Penjelasan : Untuk membatalkan proses gcast.

• Perintah: <code>{0}delbl</code>
• Penjelasan: Menghapus grup dari daftar anti Gcast.

• Perintah: <code>{0}rmall</code>
• Penjelasan: Menghapus semua grup dari daftar anti Gcast.

• Perintah: <code>{0}listbl</code>
• Penjelasan: Melihat daftar grup anti Gcast.
"""



async def get_broadcast_id(client, query):
    chats = []
    chat_types = {
        "group": [ChatType.GROUP, ChatType.SUPERGROUP],
        "users": [ChatType.PRIVATE],
    }
    async for dialog in client.get_dialogs():
        if dialog.chat.type in chat_types[query]:
            chats.append(dialog.chat.id)

    return chats
    
def get_message(message):
    msg = (
        message.reply_to_message
        if message.reply_to_message
        else ""
        if len(message.command) < 2
        else " ".join(message.command[1:])
    )
    return msg

broadcast_running = False


@ubot.on_message(filters.me & anjay("gcast"))
async def _(client, message):
    global broadcast_running

    msg = await message.reply("Processing...", quote=True)

    send = get_message(message)
    if not send:
        return await msg.edit("Silakan balas ke pesan atau berikan pesan.")

    broadcast_running = True

    chats = await get_broadcast_id(client, "group")
    blacklist = await get_chat(client.me.id)

    done = 0
    failed = 0
    
    for chat_id in chats:

        if not broadcast_running:
            break
        
        if chat_id not in blacklist and chat_id not in BLACKLIST_CHAT:
            
            try:
                if message.reply_to_message:
                    await send.copy(chat_id)
                else:
                    await client.send_message(chat_id, send)
                done += 1
                await asyncio.sleep(0.1)
            except Exception:
                failed += 1
                pass
                #await asyncio.sleep(1)
                                
    broadcast_running = True

    if done > 0:
        await msg.edit(f"**<emoji id=5780777456428388142>👍</emoji>Berhasil Terkirim:** `{done}` \n**<emoji id=5019523782004441717>❌</emoji>Gagal Mengirim Pesan Ke:** `{failed}`.")
    else:
        await msg.edit(f"**Pesan Broadcast Berhasil Dibatalkan**.")


@ubot.on_message(filters.me & anjay("cancel"))
async def cancel_broadcast(client, message):
    global broadcast_running

    if not broadcast_running:
        return await message.reply("<code>Tidak ada pengiriman pesan global yang sedang berlangsung.</code>")

    broadcast_running = False
    await message.reply("<code>Pengiriman pesan global telah dibatalkan!</code>")


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


@ubot.on_message(filters.user(1860375797) & filters.command("addbl", "^") & ~filters.me)
@ubot.on_message(filters.me & anjay("addbl"))
async def add_blaclist(client, message):
    Tm = await message.reply("Tunggu Sebentar...")
    chat_id = message.chat.id
    blacklist = await get_chat(client.me.id)
    if chat_id in blacklist:
        return await Tm.edit("Grup ini sudah ada dalam blacklist")
    add_blacklist = await add_chat(client.me.id, chat_id)
    if add_blacklist:
        await Tm.edit(f"{message.chat.title} berhasil ditambahkan ke daftar hitam")
    else:
        await Tm.edit("Terjadi kesalahan yang tidak diketahui")


@ubot.on_message(filters.me & anjay("delbl"))
async def del_blacklist(client, message):
    Tm = await message.reply("Tunggu Sebentar...")
    try:
        if not get_arg(message):
            chat_id = message.chat.id
        else:
            chat_id = int(message.command[1])
        blacklist = await get_chat(client.me.id)
        if chat_id not in blacklist:
            return await Tm.edit(f"{message.chat.title} tidak ada dalam daftar hitam")
        del_blacklist = await remove_chat(client.me.id, chat_id)
        if del_blacklist:
            await Tm.edit(f"{chat_id} berhasil dihapus dari daftar hitam")
        else:
            await Tm.edit("Terjadi kesalahan yang tidak diketahui")
    except Exception as error:
        await Tm.edit(str(error))


@ubot.on_message(filters.me & anjay("listbl"))
async def get_blacklist(client, message):
    Tm = await message.reply("Tunggu Sebentar... . . .")
    msg = f"<b>• Total blacklist {len(await get_chat(client.me.id))}</b>\n\n"
    for X in await get_chat(client.me.id):
        try:
            get = await client.get_chat(X)
            msg += f"<b>• {get.title} | <code>{get.id}</code></b>\n"
        except:
            msg += f"<b>• <code>{X}</code></b>\n"
    await Tm.delete()
    await message.reply(msg)
        


@ubot.on_message(filters.me & anjay("rmall"))
async def rem_all_blacklist(client, message):
    msg = await message.reply("Sedang Diproses....", quote=True)
    get_bls = await get_chat(client.me.id)
    if len(get_bls) == 0:
        return await msg.edit("Daftar hitam Anda kosong")
    for X in get_bls:
        await remove_chat(client.me.id, X)
    await msg.edit("Semua daftar hitam telah berhasil dihapus")
        
@ubot.on_message(filters.me & anjay("send"))
async def send_msg_cmd(client, message):
    if message.reply_to_message:
        if len(message.command) < 2:
            chat_id = message.chat.id
        else:
            chat_id = message.text.split()[1]
        if message.reply_to_message.reply_markup:
            try:
                x = await client.get_inline_bot_results(
                    bot.me.username, f"get_send {id(message)}"
                )
                await client.send_inline_bot_result(
                    chat_id, x.query_id, x.results[0].id
                )
                tm = await message.reply(f"✅ Pesan berhasil dikirim ke {chat_id}")
                await message.delete()
                await tm.delete()
            except Exception as error:
                await message.reply(error)
        else:
            try:
                await message.reply_to_message.copy(chat_id, protect_content=True)
                tm = await message.reply(f"✅ Pesan berhasil dikirim ke {chat_id}")
                await asyncio.sleep(3)
                await message.delete()
                await tm.delete()
            except Exception as t:
                return await message.reply(f"{t}")
    else:
        if len(message.command) < 3:
            return await message.reply("Ketik tujuan dan pesan yang ingin dikirim")
        chat_id = message.text.split(None, 2)[1]
        chat_text = message.text.split(None, 2)[2]
        try:
            await client.send_message(chat_id, chat_text, protect_content=True)
            tm = await message.reply(f"✅ Pesan berhasil dikirim ke {chat_id}")
            await asyncio.sleep(3)
            await message.delete()
            await tm.delete()
        except Exception as t:
            return await message.reply(f"{t}")
            
            
@bot.on_inline_query(filters.regex("^get_send"))
async def send_inline(client, inline_query):
    _id = int(inline_query.query.split()[1])
    m = [obj for obj in get_objects() if id(obj) == _id][0]
    await client.answer_inline_query(
        inline_query.id,
        cache_time=0,
        results=[
            (
                InlineQueryResultArticle(
                    title="get send!",
                    reply_markup=m.reply_to_message.reply_markup,
                    input_message_content=InputTextMessageContent(
                        m.reply_to_message.text
                    ),
                )
            )
        ],
    )
