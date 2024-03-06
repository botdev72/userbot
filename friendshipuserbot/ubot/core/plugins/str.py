import asyncio
from datetime import datetime
from gc import get_objects

from pyrogram.raw.functions import Ping
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ubot import *

PING = "🏓"
PONG = "🗿"


async def send_msg_to_owner(client, message):
    if message.from_user.id == OWNER_ID:
        return
    else:
        buttons = [
            [
                InlineKeyboardButton(
                    "👤 ᴘʀᴏꜰɪʟ", callback_data=f"profil {message.from_user.id}"
                ),
                InlineKeyboardButton(
                    "ᴊᴀᴡᴀʙ 💬", callback_data=f"jawab_pesan {message.from_user.id}"
                ),
            ],
        ]
        await client.send_message(
            OWNER_ID,
            f"<a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>\n\n<code>{message.text}</code>",
            reply_markup=InlineKeyboardMarkup(buttons),
        )


async def reak(client, message):
    await client.send_reaction(message.chat.id, message.id, "🗿")


async def ping_cmd(client, message):
    # uptime = await get_time((time() - start_time))
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    end = datetime.now()
    delta_ping = round((end - start).microseconds / 100000, 2)
    gua = client.me.is_premium
    ping = await get_var(client.me.id, "emoji1")
    cos_ping2 = ping if ping else PING
    ping_id = await get_var(client.me.id, "emoji_id1")
    cos_ping = ping_id if ping_id else "5269563867305879894"
    pong = await get_var(client.me.id, "emoji2")
    cos_pong2 = pong if pong else PONG
    pong_id = await get_var(client.me.id, "emoji_id2")
    cos_pong = pong_id if pong_id else "6183961455436498818"
    if gua == True:
        _ping = f"""
**<emoji id={cos_ping}>{cos_ping2}</emoji> Pong !!**
**<emoji id={cos_pong}>{cos_pong2}</emoji>`{str(delta_ping).replace('.', ',')}ms`**"""
    elif gua == False:
        _ping = f"""
**{cos_ping2} Pong !!**
**{cos_pong2} `{str(delta_ping).replace('.', ',')} ms`**"""
    await message.reply(_ping)


async def set_emoji(client, message):
    jing = await message.reply("`Processing...`")
    gua = client.me.is_premium
    emoji = get_arg(message)
    emoji_id = None
    if emoji:
        emojinya = emoji
    if gua == True:
        if message.entities:
            for entity in message.entities:
                if entity.custom_emoji_id:
                    emoji_id = entity.custom_emoji_id
                    break
            if emoji_id:
                await set_var(client.me.id, "emoji_id1", emoji_id)
                await jing.edit(
                    f"<b>Emoji 1 Diatur ke :</b> <emoji id={emoji_id}>{emojinya}</emoji>"
                )
    elif gua == False:
        await set_var(client.me.id, "emoji1", emojinya)
        await jing.edit(f"**Kostum emoji diatur ke `{emojinya}`**")


async def set_emoji2(client, message):
    jing = await message.reply("`Processing...`")
    gua = client.me.is_premium
    emoji = get_arg(message)
    emoji_id = None
    if emoji:
        emojinya = emoji
    if gua == True:
        if message.entities:
            for entity in message.entities:
                if entity.custom_emoji_id:
                    emoji_id = entity.custom_emoji_id
                    break
            if emoji_id:
                await set_var(client.me.id, "emoji_id2", emoji_id)
                await jing.edit(
                    f"<b>Emoji 2 Diatur ke: </b> <emoji id={emoji_id}>{emojinya}</emoji>"
                )
    elif gua == False:
        await set_var(client.me.id, "emoji2", emojinya)
        await jing.edit(f"**Kostum emoji 2 diatur ke `{emojinya}`**")


async def set_emoji3(client, message):
    jing = await message.reply("`Processing...`")
    user_id = client.me.id
    rep = message.reply_to_message
    emoji = get_arg(message)
    if rep:
        if rep.text:
            emojinya = rep.text
        else:
            return await jing.edit("`Silakan balas ke pesan untuk dijadikan emoji.`")
    elif emoji:
        emojinya = emoji
    else:
        return await jing.edit(
            "`Silakan balas ke pesan atau berikan pesan untuk dijadikan emoji`"
        )
    await set_var(user_id, "ICON_PONG", emojinya)
    await jing.edit(f"**Kostum emoji diatur ke `{emojinya}`**")


async def start_cmd(client, message):
    await add_served_user(message.from_user.id)
    await send_msg_to_owner(client, message)
    if len(message.command) < 2:
        buttons = Button.start(message)
        msg = MSG.START(message)
        await message.reply(msg, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        txt = message.text.split(None, 1)[1]
        msg_id = txt.split("_", 1)[1]
        send = await message.reply("<b>Tunggu Sebentar...</b>")
        if "secretMsg" in txt:
            try:
                m = [obj for obj in get_objects() if id(obj) == int(msg_id)][0]
            except Exception as error:
                return await send.edit(f"<b>❌ ᴇʀʀᴏʀ:</b> <code>{error}</code>")
            user_or_me = [m.reply_to_message.from_user.id, m.from_user.id]
            if message.from_user.id not in user_or_me:
                return await send.edit(
                    f"<b>❌ Jangan Di Klik Mas <a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>"
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
                return await send.edit(f"<b>❌ ᴇʀʀᴏʀ:</b> <code>{error}</code>")
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
