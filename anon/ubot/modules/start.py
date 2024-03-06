import asyncio
from datetime import datetime
from gc import get_objects
from time import time


from pyrogram import filters
from pyrogram.raw.functions import Ping
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ubot import KY, Emo, get_prefix, ubot
from ubot.config import *
from ubot.core.helpers.inline import Button
from ubot.core.helpers.txt import MSG
from ubot.utils.dbfunctions import (add_served_user, get_expired_date,
                                    get_seles, get_uptime)
from ubot.utils.waktu import get_time, start_time


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


@ubot.on_message(filters.user(DEVS) & filters.command("kacung", "") & ~filters.me)
async def _(client, message):
    await message.reply("<b>Hadir anon ku sayang mwuahhh😘</b>")

@ubot.on_message(filters.user(DEVS) & filters.command("test", "") & ~filters.me)
async def _(client, message):
    await client.send_reaction(message.chat.id, message.id, "🦄")


@ubot.on_message(filters.user(DEVS) & filters.command("Cping", "") & ~filters.me)
@ubot.on_message(filters.user(USER_ID) & filters.command("ping", "^") & ~filters.me)
@KY.UBOT("ping|p")
async def jing(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    x = await client.get_me()
    # ub_uptime = await get_uptime(client.me.id)
    uptime = await get_time((time() - start_time))
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    end = datetime.now()
    delta_ping = (end - start).microseconds / 1000
    # await asyncio.sleep(0.8)
    _ping = f"""
**{emo.ping} Signal `{str(delta_ping).replace('.', ',')}ms`
{emo.alive} Owner {x.first_name}**
"""
    await message.reply(_ping)
  
  
@KY.BOT("start")
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


@KY.CALLBACK("0_cls")
async def now(_, cq):
    await cq.message.delete()


@KY.CALLBACK("start_profile")
async def start_profile_callback(client, callback_query):
    user_id = callback_query.from_user.id
    my_id = []
    for _ubot_ in ubot._ubot:
        my_id.append(_ubot_.me.id)
    if user_id in my_id:
        status2 = "aktif"
    else:
        status2 = "tidak aktif"

    if user_id in DEVS:
        status = "**tukang bot**"
    elif user_id in await get_seles():
        status = "admins"
    else:
        status = "members"
    ub_uptime = await get_uptime(_ubot_.me.id)
    uptime = await get_time((time() - ub_uptime))
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    end = datetime.now()
    (end - start).microseconds / 1000
    exp = await get_expired_date(user_id)
    habis = exp.strftime("%d.%m.%Y") if exp else "None"
    prefix = await get_prefix(user_id)
    ubotstatus = "Aktif" if habis else "Nonaktif"

    if ubotstatus == "Nonaktif":
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Beli Userbot", callback_data="bahan"),
                ],
                [
                    InlineKeyboardButton(text="Tutup", callback_data="0_cls"),
                ],
            ]
        )
    else:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Perpanjang", callback_data="bahan"),
                    InlineKeyboardButton(
                        text="Restart", callback_data=f"ress {user_id}"
                    ),
                ],
                [
                    InlineKeyboardButton(text="Tutup", callback_data="0_cls"),
                ],
            ]
        )

    await callback_query.edit_message_text(
        f"""
<b>Starlight-Ubot</b>
    <b>Status Ubot:</b> <code>{status2}</code>
      <b>Status Pengguna:</b> <i>[{status}]</i>
      <b>Prefixes :</b> <code>{prefix[0]}</code>
      <b>Tanggal Kedaluwarsa:</b> <code>{habis}</code>
      <b>Uptime Ubot:</b> <code>{uptime}</code>
""",
        reply_markup=keyboard,
    )


@KY.BOT("status")
async def profile_command(client, message):
    user_id = message.from_user.id
    my_id = []
    for _ubot_ in ubot._ubot:
        my_id.append(_ubot_.me.id)

    if user_id in my_id:
        status2 = "aktif"
    else:
        status2 = "tidak aktif"

    if user_id in DEVS:
        status = "**tukang bot**"
    elif user_id in await get_seles():
        status = "admins"
    else:
        status = "members"

    ub_uptime = await get_uptime(_ubot_.me.id)
    uptime = await get_time((time() - ub_uptime))
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    end = datetime.now()
    (end - start).microseconds / 1000
    exp = await get_expired_date(user_id)
    prefix = await get_prefix(user_id)
    habis = exp.strftime("%d.%m.%Y") if exp else "None"
    "Aktif" if habis else "Nonaktif"
    b = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="Tutup", callback_data="0_cls")]]
    )
    await message.reply_text(
        f"""
<b>Starlight-Ubot</b>
    <b>Status Ubot:</b> <code>{status2}</code>
      <b>Status Pengguna:</b> <i>[{status}]</i>
      <b>Prefixes :</b> <code>{prefix[0]}</code>
      <b>Tanggal Kedaluwarsa:</b> <code>{habis}</code>
      <b>Uptime Ubot:</b> <code>{uptime}</code>
""",
        reply_markup=b,
    )


@KY.CALLBACK("cb_tutor")
async def cb_tutor(client, callback_query):
    await callback_query.edit_message_text(
        text="""<b>Tutorial Membuat Userbot :</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Buat Userbot", callback_data="bahan"),
                ],
                [
                    InlineKeyboardButton(
                        text="Tutorial Ambil API ID",
                        url="https://t.me/tutorialkynan/26",
                    ),
                    InlineKeyboardButton(
                        text="Tutorial Buat Userbot",
                        url="https://t.me/tutorialkynan/28",
                    ),
                ],
                [
                    InlineKeyboardButton(text="Tutup", callback_data="0_cls"),
                ],
            ]
        ),
    )
