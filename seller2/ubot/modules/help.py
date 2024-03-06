import asyncio
import random
import re
from datetime import datetime
from time import time

from pyrogram import enums
from pyrogram.errors import *
from pyrogram.errors.exceptions import FloodWait
from pyrogram.raw.functions import Ping
from pyrogram.types import *

from ubot import *
from ubot.config import *
from ubot.core.functions.plugins import HELP_COMMANDS
from ubot.utils import *
from ubot.utils.misc import paginate_modules
from ubot.utils.unpack import unpackInlineMessage
from ubot.utils.waktu import get_time


def lewatin(func):
    @wraps(func)
    async def lepas(client, message, *args, **kwargs):
        try:
            return await func(client, message, *args, **kwargs)
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except MessageNotModified:
            pass

    return lepas


@KY.UBOT("help")
async def help_cmd(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    if not get_arg(message):
        try:
            x = await client.get_inline_bot_results(bot.me.username, "help")
            await message.reply_inline_bot_result(x.query_id, x.results[0].id)
        except Exception as error:
            await message.reply(error)
    else:
        nama = get_arg(message)
        if get_arg(message) in HELP_COMMANDS:
            prefix = await get_prefix(client.me.id)
            await eor(
                message,
                f"<b>{HELP_COMMANDS[get_arg(message)].__HELP__}</b>".format(
                    next((p) for p in prefix)
                )
                + f"\n<b>{emo.anu} {bot.me.mention}</b>",
            )
        else:
            await eor(
                message,
                f"<b>{emo.gagal} Tidak ada modul bernama <code>{nama}</code></b>",
            )


@KY.UBOT("alive")
async def _(client, message):
    try:
        x = await client.get_inline_bot_results(
            bot.me.username, f"user_alive_command {message.id} {message.from_user.id}"
        )
        await message.reply_inline_bot_result(x.query_id, x.results[0].id)
    except Exception as error:
        await message.reply(error)


@KY.INLINE("^user_alive_command")
async def _(client, inline_query):
    emo = Emo(client.me.id)
    await emo.initialize()
    get_id = inline_query.query.split()
    len(ubot._ubot)
    for my in ubot._ubot:
        if int(get_id[2]) == my.me.id:
            try:
                peer = my._get_my_peer[my.me.id]
                users = len(peer["pm"])
                group = len(peer["gc"])
            except Exception:
                users = random.randrange(await my.get_dialogs_count())
                group = random.randrange(await my.get_dialogs_count())
            get_exp = await get_expired_date(my.me.id)
            if get_exp is None:
                expired = ""
            else:
                exp = get_exp.strftime("%d-%m-%Y")
                expired = f"<code>{exp}</code>"
            if my.me.id in DEVS:
                status = "**SellerKeren**"
            elif my.me.id in await get_seles():
                status = "**SellerKeren**"
            else:
                status = "**SellerKeren**"
            antipm = None
            cekpc = await get_var(my.me.id, "ENABLE_PM_GUARD")
            if not cekpc:
                antipm = "disable"
            else:
                antipm = "enable"
            button = [[InlineKeyboardButton(text="close",
            callback_data=f"alv_cls {int(get_id[1])} {int(get_id[2])}")]]
            start = datetime.now()
            await my.invoke(Ping(ping_id=0))
            ping = (datetime.now() - start).microseconds / 1000
            b = await get_uptime(my.me.id)
            uptime = await get_time((time() - b))
            msg = f"""
<b>Seller-Keren</b>
     <b>status:</b> [{status}]
        <b>dc_id:</b> <code>{my.me.dc_id}</code>
        <b>ping_dc:</b> <code>{str(ping).replace('.', ',')} ms</code>
        <b>antipm:</b> <code>{antipm}</code>
        <b>device_uptime:</b> <code>{uptime}</code>
        <b>expired:</b> <code>{expired}</code>
"""
            await client.answer_inline_query(
                inline_query.id,
                cache_time=300,
                results=[
                    (
                        InlineQueryResultArticle(
                            title="💬",
                            reply_markup=InlineKeyboardMarkup(button),
                            input_message_content=InputTextMessageContent(msg),
                        )
                    )
                ],
            )


@KY.CALLBACK("^alv_cls")
async def _(cln, cq):
    get_id = cq.data.split()
    if not cq.from_user.id == int(get_id[2]):
        return await cq.answer(
            f"❌ JANGAN DI PENCET PENCET GUE JIJIK.{cq.from_user.first_name} {cq.from_user.last_name or ''}",
            True,
        )
    unPacked = unpackInlineMessage(cq.inline_message_id)
    for my in ubot._ubot:
        if cq.from_user.id == int(my.me.id):
            await my.delete_messages(
                unPacked.chat_id, [int(get_id[1]), unPacked.message_id]
            )


@KY.CALLBACK("^getid")
async def _(client, inline_query):
    chat_id = inline_query.query.lower().split()[1]
    try:
        get = await bot.get_chat(chat_id)
        name = f"{get.title}"
        if name == "None":
            get = await bot.get_users(chat_id)
            name = f"{get.first_name} {get.last_name or ''}"
        msg = f"<b>ID {name} Adalah:</b> <code>{get.id}</code>"
        await client.answer_inline_query(
            inline_query.id,
            cache_time=60,
            results=[
                (
                    InlineQueryResultArticle(
                        title="✅ GET ID",
                        input_message_content=InputTextMessageContent(msg),
                    )
                )
            ],
        )
    except BadRequest as why:
        await client.answer_inline_query(
            inline_query.id,
            cache_time=60,
            results=[
                (
                    InlineQueryResultArticle(
                        title="❌ ERROR",
                        input_message_content=InputTextMessageContent(why),
                    )
                )
            ],
        )


@KY.INLINE("^help")
@lewatin
async def _(client, inline_query):
    user_id = inline_query.from_user.id
    emut = await get_prefix(user_id)
    msg = "<b>Help Modules\n     Prefixes: `{}`\n     Commands: <code>{}</code></b>".format(
        " ".join(emut), len(HELP_COMMANDS)
    )
    await client.answer_inline_query(
        inline_query.id,
        cache_time=0,
        results=[
            (
                InlineQueryResultArticle(
                    title="Help Menu!",
                    reply_markup=InlineKeyboardMarkup(
                        paginate_modules(0, HELP_COMMANDS, "help")
                    ),
                    input_message_content=InputTextMessageContent(msg),
                )
            )
        ],
    )


@KY.CALLBACK(r"help_(.*?)")
@lewatin
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    mod_match = re.match(r"help_module\((.+?)\)", callback_query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", callback_query.data)
    next_match = re.match(r"help_next\((.+?)\)", callback_query.data)
    back_match = re.match(r"help_back", callback_query.data)
    prefix = await get_prefix(user_id)
    if mod_match:
        module = (mod_match.group(1)).replace(" ", "_")
        text = f"<b>{HELP_COMMANDS[module].__HELP__}</b>\n".format(
            next((p) for p in prefix)
        )

        button = [[InlineKeyboardButton("Back", callback_data="help_back")]]
        await callback_query.edit_message_text(
            text=text + f"\n<b>© {bot.me.mention}</b>",
            reply_markup=InlineKeyboardMarkup(button),
            disable_web_page_preview=True,
        )
    top_text = "<b>Help Modules\n     Prefixes: <code>{}</code>\n     Commands: <code>{}</code></b>".format(
        " ".join(prefix), len(HELP_COMMANDS)
    )
    if prev_match:
        curr_page = int(prev_match.group(1))
        await callback_query.edit_message_text(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(curr_page - 1, HELP_COMMANDS, "help")
            ),
            disable_web_page_preview=True,
        )
    if next_match:
        next_page = int(next_match.group(1))
        await callback_query.edit_message_text(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(next_page + 1, HELP_COMMANDS, "help")
            ),
            disable_web_page_preview=True,
        )
    if back_match:
        await callback_query.edit_message_text(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, HELP_COMMANDS, "help")
            ),
            disable_web_page_preview=True,
        )


SUPPORT = []


@KY.CALLBACK("^support")
async def _(client, callback_query):
    user_id = int(callback_query.from_user.id)
    full_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}"
    get = await bot.get_users(user_id)
    await callback_query.message.delete()
    SUPPORT.append(get.id)
    try:
        button = [
            [InlineKeyboardButton("❌ BATALKAN", callback_data=f"batal {user_id}")]
        ]
        pesan = await bot.ask(
            user_id,
            f"<b>✍️ SILAHKAN KIRIM PERTANYAAN ANDA: {full_name}</b>",
            reply_markup=InlineKeyboardMarkup(button),
            timeout=90,
        )
    except asyncio.TimeoutError as out:
        if get.id not in SUPPORT:
            return
        else:
            SUPPORT.remove(get.id)
            await pesan.delete()
            return await bot.send_message(user_id, "Pembatalan Otomatis")
    text = f"<b>💬 PERTANYAAN ANDA SUDAH TERKIRIM: {full_name}</b>"
    buttons = [
        [
            InlineKeyboardButton("👤 Profil", callback_data=f"profil {user_id}"),
            InlineKeyboardButton("Jawab 💬", callback_data=f"jawab_pesan {user_id}"),
        ],
    ]
    if get.id not in SUPPORT:
        return
    else:
        try:
            await pesan.copy(
                SKY,
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            SUPPORT.remove(get.id)
            await bot.edit_message_text(
                user_id,
                pesan.id - 1,
                f"<b>✍️ SILAHKAN KIRIM PERTANYAAN ANDA: {full_name}</b>",
            )
            await callback_query.message.delete()
            return await bot.send_message(user_id, text)
        except Exception as error:
            return await bot.send_message(user_id, error)


@KY.CALLBACK("^jawab_pesan")
async def _(client, callback_query):
    user_id = int(callback_query.from_user.id)
    full_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}"
    get = await bot.get_users(user_id)
    user_ids = int(callback_query.data.split()[1])
    SUPPORT.append(get.id)
    try:
        button = [
            [InlineKeyboardButton("❌ BATALKAN", callback_data=f"batal {user_id}")]
        ]
        pesan = await bot.ask(
            user_id,
            f"<b>✉️ SILAHKAN KIRIM BALASAN ANDA: {full_name}</b>",
            reply_markup=InlineKeyboardMarkup(button),
            timeout=300,
        )
    except asyncio.TimeoutError:
        if get.id not in SUPPORT:
            return
        else:
            SUPPORT.remove(get.id)
            await pesan.delete()
            return await bot.send_message(SKY, "Pembatalan Otomatis")
    text = f"<b>✅ PESAN BALASAN ANDA TELAH TERKIRIM: {full_name}</b>"
    if user_ids not in [DEVS]:
        buttons = [[InlineKeyboardButton("💬 Jawab Pesan 💬", f"jawab_pesan {user_id}")]]
    else:
        buttons = [
            [
                InlineKeyboardButton("👤 Profil", callback_data=f"profil {user_id}"),
                InlineKeyboardButton("Jawab 💬", callback_data=f"jawab_pesan {user_id}"),
            ],
        ]
    if get.id not in SUPPORT:
        return
    else:
        try:
            await pesan.copy(
                user_ids,
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            SUPPORT.remove(get.id)
            await bot.edit_message_text(
                user_id,
                pesan.id - 1,
                f"<b>✉️ SILAHKAN KIRIM BALASAN ANDA: {full_name}</b>",
            )
            await callback_query.message.delete()
            return await bot.send_message(user_id, text)
        except Exception as error:
            return await bot.send_message(user_id, error)


@KY.CALLBACK("^profil")
async def _(client, callback_query):
    user_id = int(callback_query.data.split()[1])
    try:
        get = await bot.get_users(user_id)
        first_name = f"{get.first_name}"
        last_name = f"{get.last_name}"
        full_name = f"{get.first_name} {get.last_name or ''}"
        username = f"{get.username}"
        msg = (
            f"<b>👤 <a href=tg://user?id={get.id}>{full_name}</a></b>\n"
            f"<b> ┣ ID Pengguna:</b> <code>{get.id}</code>\n"
            f"<b> ┣ Nama Depan:</b> {first_name}\n"
        )
        if last_name == "None":
            msg += ""
        else:
            msg += f"<b> ┣ Nama Belakang:</b> {last_name}\n"
        if username == "None":
            msg += ""
        else:
            msg += f"<b> ┣ UserName:</b> @{username}\n"
        msg += f"<b> ┗ Bot: {bot.me.mention}\n"
        buttons = [
            [
                InlineKeyboardButton(
                    f"{full_name}",
                    url=f"tg://openmessage?user_id={get.id}",
                )
            ]
        ]
        await callback_query.message.reply_text(
            msg, reply_markup=InlineKeyboardMarkup(buttons)
        )
    except RPCError as why:
        await callback_query.message.reply_text(why)


@KY.CALLBACK("^batal")
async def _(client, callback_query):
    user_id = int(callback_query.data.split()[1])
    get = await bot.get_users(user_id)
    if get.id in SUPPORT:
        try:
            SUPPORT.remove(get.id)
            await callback_query.message.delete()
            await bot.send_message(user_id, "<b>✅ Berhasil Dibatalkan!</b>")
        except RPCError as why:
            print(why)
            await callback_query.message.delete()
            await bot.send_message(user_id, "<b>❌ Gagal Dibatalkan!</b>")
