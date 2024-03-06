import asyncio
from datetime import datetime
from gc import get_objects
from time import time

from pyrogram.raw.functions import Ping
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .. import *


async def add_broadcast_bot(client, message):
    if message.from_user.id == OWNER_ID:
        return
    else:
        buttons = [
            [
                InlineKeyboardButton(
                    "👤 Profil", callback_data=f"profil {message.from_user.id}"
                ),
                InlineKeyboardButton(
                    "Jawab 💬", callback_data=f"jawab_pesan {message.from_user.id}"
                ),
            ],
        ]
        await client.send_message(
            OWNER_ID,
            f"<a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>\n\n<code>{message.text}</code>",
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@PY.UBOT("ping", PREFIX)
async def _(client, message):
    uptime = await get_time((time() - start_time))
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    end = datetime.now()
    delta_ping = (end - start).microseconds / 1000
    _ping = f"""
<b>❏ PONG:</b> 
 <b>├• Pinger:</b> <code>{delta_ping} ms</code>
 <b>├• Uptime:</b> <code>{uptime}</code>
 <b>└• Owner:</b> <a href=tg://user?id={client.me.id}>{client.me.first_name} {client.me.last_name or ''}</a>
"""
    await message.reply(_ping)


@PY.BOT("start")
async def _(client, message):
    await add_broadcast_bot(client, message)
    if len(message.command) < 2:
        buttons = Button.start()
        msg = f"""
<b>👋🏻 HALO <a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>!

💬 @{bot.me.username} ADALAH BOT YANG DAPAT MEMBUAT USERBOT DENGAN MUDAH

👉🏻 KLIK TOMBOL DIBAWAH UNTUK MEMBUAT USERBOT 
"""
        await message.reply(msg, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        txt = message.text.split(None, 1)[1]
        msg_id = txt.split("_", 1)[1]
        send = await message.reply("<b>Tunggu Sebentar...</b>")
        if "secretMsg" in txt:
            try:
                m = [obj for obj in get_objects() if id(obj) == int(msg_id)][0]
            except Exception as error:
                return await send.edit(f"<b>❌ ERROR:</b> <code>{error}</code>")
            user_or_me = [m.reply_to_message.from_user.id, m.from_user.id]
            if message.from_user.id not in user_or_me:
                return await send.edit(
                    f"<b>❌ Pesan ini bukan untukmu <a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>"
                )
            else:
                text = await client.send_message(
                    message.chat.id,
                    m.text.split(None, 1)[1],
                    protect_content=True,
                    reply_to_message_id=message.id,
                )
                await send.delete()
                await asyncio.sleep(120)
                await message.delete()
                await text.delete()
        elif "copyMsg" in txt:
            try:
                m = [obj for obj in get_objects() if id(obj) == int(msg_id)][0]
            except Exception as error:
                return await send.edit(f"<b>❌ ERROR:</b> <code>{error}</code>")
            id_copy = int(m.text.split()[1].split("/")[-1])
            if "t.me/c/" in m.text.split()[1]:
                chat = int("-100" + str(m.text.split()[1].split("/")[-2]))
            else:
                chat = str(m.text.split()[1].split("/")[-2])
            try:
                get = await client.get_messages(chat, id_copy)
                await get.copy(message.chat.id, reply_to_message_id=message.id)
                await send.delete()
            except Exception as error:
                await send.edit(error)
        elif "InfoLagu" in txt:
            search = YouTubeSearch(f"https://youtu.be/{msg_id}")
            title = search[1]
            duration = search[2]
            url = search[3]
            views = search[4]
            thumbnail = search[6]
            await message.reply_photo(
                thumbnail,
                caption="💡 <b>Informasi Trek</b>\n\n🏷 <b>Nama:</b> {judul}\n⏱ <b>Durasi:</b> {durasi}\n👀 <b>Dilihat:</b> {views}\n🔗 <b>Tautan:</b> {link}\n\n⚡ <b>Powered By:</b> @{bot_username}".format(
                    judul=title,
                    durasi=duration,
                    views=views,
                    link=url,
                    bot_username=bot.me.username,
                ),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "🗑 Tutup 🗑",
                                callback_data="0_cls",
                            )
                        ],
                    ]
                ),
            )
            await send.delete()
