import asyncio
import re
from datetime import datetime

import psutil
from pyrogram import enums, filters
from pyrogram.errors import *
from pyrogram.raw.functions import Ping
from pyrogram.types import *

from Amang import *
from Amang.config import *
from Amang.core.functions.plugins import HELP_COMMANDS
from Amang.modules.start import START_TIME, _human_time_duration
from Amang.utils import *
from Amang.utils.dbfunctions import *
from Amang.utils.waktu import get_time
from Amang.utils.misc import paginate_modules
from Amang.utils.unpack import unpackInlineMessage

from .start import PREM


def lewatin(func):
    @wraps(func)
    async def lepas(client, message, *args, **kwargs):
        try:
            return await func(client, message, *args, **kwargs)
        except MessageNotModified:
            pass
          
    return lepas


@ubot.on_message(filters.me & anjay("help"))
async def _(client, message):
    try:
        x = await client.get_inline_bot_results(bot.me.username, "help")
        await message.reply_inline_bot_result(x.query_id, x.results[0].id)
            
    except Exception as error:
        await message.reply(error)


@ubot.on_message(filters.me & anjay("alive"))
async def _(client, message):
    try:
        x = await client.get_inline_bot_results(bot.me.username, f"user_alive_command {message.id} {message.from_user.id}")
        await message.reply_inline_bot_result(x.query_id, x.results[0].id)
    except Exception as error:
        await message.reply(error)


@bot.on_inline_query(filters.regex("^user_alive_command"))
async def _(client, inline_query):
    get_id = inline_query.query.split()
    babi = len(ubot._ubot)
    if int(get_id[2]) in await get_ultraprem():
        status1 = "__Super__ __premium__"
    else:
        status1 = "__premium__"
    for my in ubot._ubot:
        get_exp = await get_expired_date(my.me.id)
        if get_exp is None:
            expired = ""
        else:
            exp = get_exp.strftime("%d.%m.%Y")
            expired = f"<code>{exp}</code>"
        if int(get_id[2]) == int(my.me.id):
            users = 0
            group = 0
            async for dialog in my.get_dialogs(limit=None):
                if dialog.chat.type == enums.ChatType.PRIVATE:
                    users += 1
                elif dialog.chat.type in (
                    enums.ChatType.GROUP,
                    enums.ChatType.SUPERGROUP,
                ):
                    group += 1
            if int(get_id[2]) in DEVS:
                status = "founder"
            elif int(get_id[2]) in await get_seles():
                status = "admin"
            else:
                status = "user"
            if int(get_id[2]) == OWNER:
                button = [
                    [
                        InlineKeyboardButton(
                            text="close",
                            callback_data=f"closed {int(get_id[1])} {int(get_id[2])}",
                        ),
                    ],
                ]
            else:
                button = [
                    [
                        InlineKeyboardButton(
                            text="close",
                            callback_data=f"closed {int(get_id[1])} {int(get_id[2])}",
                        ),
                    ]
                ]
            start = datetime.now()
            await my.invoke(Ping(ping_id=0))
            ping = (datetime.now() - start).microseconds / 1000
            uptime_sec = (datetime.utcnow() - START_TIME).total_seconds()
            uptime = await _human_time_duration(int(uptime_sec))
            msg = f"""
<b>AmangUserbot</b>
    <b>status:</b> <code>{status1} [{status}]</code>
      <b>expires_on:</b> <code>{expired}</code>
      <b>dc_id:</b> <code>{my.me.dc_id}</code>
      <b>ping_dc:</b> <code>{str(ping).replace('.', ',')} ms</code>
      <b>peer_users:</b> <code>{users} users</code>
      <b>peer_group:</b> <code>{group} group</code>
      <b>peer_ubot:</b> <code>{len(ubot._ubot)}</code>
      <b>ubot_uptime:</b> <code>{uptime}</code>
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


@bot.on_callback_query(filters.regex("^closed"))
async def _(cln, cq):
    get_id = cq.data.split()
    if not cq.from_user.id == int(get_id[2]):
        return await cq.answer(
            f"JANGAN PENCET PENCET, GUA JIJIK ANJING.",
            True,
        )
    unPacked = unpackInlineMessage(cq.inline_message_id)
    for my in ubot._ubot:
        if cq.from_user.id == int(my.me.id):
            await my.delete_messages(
                unPacked.chat_id, [int(get_id[1]), unPacked.message_id]
            )


@bot.on_callback_query(filters.regex("stats"))
async def _(client, callback_query):
    uptime_sec = (datetime.utcnow() - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    process = psutil.Process(os.getpid())
    stats = f"""
UPTIME: {uptime}
BOT: {round(process.memory_info()[0] / 1024 ** 2)} MB
CPU: {cpu}%
RAM: {mem}%
DISK: {disk}%
UBOT: {len(ubot._ubot)}
MODULES: {len(HELP_COMMANDS)}
"""
    await callback_query.answer(stats, True)



@bot.on_inline_query(filters.regex("^getid"))
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


@bot.on_inline_query(filters.regex("^help"))
@lewatin
async def _(client, inline_query):
    user_id = inline_query.from_user.id
    emut = await get_prefix(user_id)
    if emut is None or emut == ['']:
        msg = "<b>Help Modules\n     Prefixes: `None`</b>"
    else:
        msg = f"<b>Help Modules\n     Prefixes: <code>{emut[0]}</code></b>"
    msg = f"<b>Help Modules\n    Prefixes: <code>{emut}</code></b>"
    await client.answer_inline_query(
        inline_query.id,
        cache_time=60,
        results=[
            InlineQueryResultArticle(
                title="Help Menu!",
                reply_markup=InlineKeyboardMarkup(paginate_modules(0, HELP_COMMANDS, "help")),
                input_message_content=InputTextMessageContent(msg),
            )
        ],
    )


@bot.on_inline_query(filters.regex("^help"))
@lewatin
async def _(client, inline_query):
    user_id = inline_query.from_user.id
    emut = await get_pref(user_id)
    if emut is None or emut == [""]:
        msg = "<b>Help Modules\n     Prefixes: `None`</b>"
    else:
        msg = f"<b>Help Modules\n     Prefixes: <code>{emut[0]}</code></b>"
    await client.answer_inline_query(
        inline_query.id,
        cache_time=60,
        results=[
            InlineQueryResultArticle(
                title="Help Menu!",
                reply_markup=InlineKeyboardMarkup(paginate_modules(0, HELP_COMMANDS, "help")),
                input_message_content=InputTextMessageContent(msg),
            )
        ],
    )


@bot.on_callback_query(filters.regex(r"help_(.*?)"))
@lewatin
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    mod_match = re.match(r"help_module\((.+?)\)", callback_query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", callback_query.data)
    next_match = re.match(r"help_next\((.+?)\)", callback_query.data)
    back_match = re.match(r"help_back", callback_query.data)
    if mod_match:
        module = (mod_match.group(1)).replace(" ", "_")
        text = f"<b>{HELP_COMMANDS[module].__HELP__}</b>\n"
        button = [[InlineKeyboardButton("Back", callback_data="help_back")]]
        await callback_query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(button),
            disable_web_page_preview=True,
        )
    emut = await get_pref(user_id)
    if emut is None or emut == [""]:
        top_text = "<b>Help Modules\n     Prefixes: `None`</b>"
    else:
        top_text = f"<b>Help Modules\n     Prefixes: <code>{emut[0]}</code></b>"
    if prev_match:
        curr_page = int(prev_match.group(1))
        await callback_query.edit_message_text(
            top_text,
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


@bot.on_callback_query(filters.regex("^support"))
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
                LOGS,
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


@bot.on_callback_query(filters.regex("^jawab_pesan"))
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
            return await bot.send_message(LOGS, "Pembatalan Otomatis")
    text = f"<b>✅ PESAN BALASAN ANDA TELAH TERKIRIM: {full_name}</b>"
    if user_ids not in [PREM]:
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


@bot.on_callback_query(filters.regex("^profil"))
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


@bot.on_callback_query(filters.regex("^batal"))
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
