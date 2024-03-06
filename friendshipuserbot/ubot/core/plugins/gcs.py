import asyncio
from gc import get_objects

from pyrogram.enums import ChatType
from pyrogram.errors.exceptions import *

from ubot import *


def get_message(message):
    msg = (
        message.reply_to_message
        if message.reply_to_message
        else ""
        if len(message.command) < 2
        else " ".join(message.command[1:])
    )
    return msg


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


"""
async def broadcast_group_cmd(client, message):
    msg = await message.reply("Processing...", quote=True)
    blacklist = await get_chat(client.me.id)
    done = 0
    async for dialog in client.get_dialogs(limit=None):
        if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            if message.reply_to_message:
                send = message.reply_to_message
            else:
                if len(message.command) < 2:
                    return await msg.edit(
                        "Silakan balas ke pesan atau berikan pesan.")
                else:
                    send = message.text.split(None, 1)[1]
            chat_id = dialog.chat.id
            if chat_id not in blacklist and chat_id not in BLACKLIST_CHAT:
                try:
                    if message.reply_to_message:
                        await send.copy(chat_id)
                    else:
                        await client.send_message(chat_id, send)
                    done += 1
                except Exception:
                    pass
                
    return await msg.edit(f"**Successfully Sent Message To `{done}` Groups chat**.")
"""

broadcast_running = False


async def broadcast_group_cmd(client, message):

    msg = await message.reply("sabar sudah pakde proses....", quote=True)

    send = get_message(message)
    if not send:
        return await msg.edit("Silakan balas ke pesan atau berikan pesan.")

    chats = await get_broadcast_id(client, "group")
    blacklist = await get_chat(client.me.id)

    done = 0
    failed = 0

    for chat_id in chats:
        if chat_id in blacklist:
            continue
        elif chat_id in BLACKLIST_CHAT:
            continue
        try:
            if message.reply_to_message:
                await send.copy(chat_id)
            else:
                await client.send_message(chat_id, send)
            await asyncio.sleep(0.2)
            done += 1
        except FloodWait:
            continue
        except SlowmodeWait:
            continue
        except Exception:
            continue
        except BaseException:
            failed += 1
    await msg.edit(
            f"**pesan broadcast Anda terkirim ke {done} grup. gagal: {failed}**."
        )
        
        
async def continuous_broadcast(client, message):
    tasks = [broadcast_group_cmd(client, message) for _ in range(5)]  # Membuat 5 tugas broadcast
    await asyncio.gather(*tasks)
    await asyncio.sleep(0.2)

    msg = await message.reply("Sedang memproses, mohon bersabar...")

    send = get_message(message)
    if not send:
        return await msg.edit("Mohon balas sesuatu atau ketik sesuatu")

    chats = await get_broadcast_id(client, "group")
    blacklist = await get_chat(client.me.id)

    done = 0
    for chat_id in chats:
        if chat_id in blacklist or chat_id in BLACKLIST_CHAT:
            continue

        try:
            if message.reply_to_message:
                await send.copy(chat_id)
            else:
                await client.send_message(chat_id, send)
            done += 1
            await asyncio.sleep(0.2)  # Tambahkan penundaan kecil setelah setiap pesan

        except FloodWait as e:
            # Handle SlowmodeWait separately
            if e.x >= 1:
                await asyncio.sleep(e.x + 1)  # Tambahkan waktu tambahan untuk menghindari kemungkinan SlowmodeWait
            else:
                await asyncio.sleep(1)  # Jika tidak ada informasi waktu yang diberikan
            if message.reply_to_message:
                await send.copy(chat_id)
            else:
                await client.send_message(chat_id, send)
            done += 1
        except Exception:
            pass

    return await msg.edit(f"<b>pesan broadcast Anda terkirim ke {done} grup</b>")
        

async def broadcast_users_cmd(client, message):
    msg = await message.reply("sabar pakde kirim surat cintamu....")
    blacklist = await get_chat(client.me.id)
    done = 0
    async for dialog in client.get_dialogs(limit=None):
        if dialog.chat.type == ChatType.PRIVATE:
            if message.reply_to_message:
                send = message.reply_to_message
            else:
                if len(message.command) < 2:
                    return await msg.edit("Silakan balas ke pesan atau berikan pesan")
                else:
                    send = message.text.split(None, 1)[1]
            chat_id = dialog.chat.id
            if chat_id not in blacklist and chat_id not in DEVS:
                try:
                    if message.reply_to_message:
                        await send.copy(chat_id)
                    else:
                        await client.send_message(chat_id, send)
                    done += 1
                except Exception:
                    pass

    await msg.edit(f"**🐒 berhasil kirim pesan ke {done} orang gabut.**")


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
                tm = await message.reply(f"✅Pesan berhasil dikirim ke {chat_id}")
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


async def gcast_inline(client, inline_query):
    get_id = int(inline_query.query.split(None, 1)[1])
    m = [obj for obj in get_objects() if id(obj) == get_id][0]
    buttons, text = await gcast_create_button(m)
    await client.answer_inline_query(
        inline_query.id,
        cache_time=0,
        results=[
            (
                InlineQueryResultArticle(
                    title="get button!",
                    reply_markup=buttons,
                    input_message_content=InputTextMessageContent(text),
                )
            )
        ],
    )
