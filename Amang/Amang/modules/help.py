import re
from datetime import datetime

from pyrogram import enums, filters
from pyrogram.raw.functions import Ping
from pyrogram.types import *

from Amang import *
from Amang.config import *
from Amang.core.functions.plugins import HELP_COMMANDS
from Amang.modules.start import START_TIME, _human_time_duration
from Amang.utils.dbfunctions import get_expired_date, get_seles
from Amang.utils.misc import paginate_modules
from Amang.utils.unpack import unpackInlineMessage
from Amang.utils.dbfunctions import get_userbots

PEPEK = [1054295664, 2073506739]


@ubot.on_message(filters.me & filters.command(["alive", "help"], cmd))
async def _(client, message):
    if message.command[0] == "alive":
        text = f"user_alive_command {message.id} {message.from_user.id}"
    if message.command[0] == "help":
        text = "user_help_command"
    try:
        x = await client.get_inline_bot_results(bot.me.username, text)
        for m in x.results:
            await message.reply_inline_bot_result(x.query_id, m.id)
    except Exception as error:
        await message.reply(error)


@bot.on_inline_query(filters.regex("^user_alive_command"))
async def _(client, inline_query):
    user_id = inline_query.from_user.id
    get_id = inline_query.query.split()
    memek = len(ubot._ubot)
    if user_id in DEVS:
        status = "founder"
    elif user_id in await get_seles():
        status = "admin"
    else:
        status = "user"
    for my in ubot._ubot:
        get_exp = await get_expired_date(my.me.id)
        if get_exp is None:
            expired = ""
        else:
            exp = get_exp.strftime("%d.%m.%Y")
            expired = f"<code>{exp}</code>"
        button = [
            [
                InlineKeyboardButton(
                    text="close",
                    callback_data=f"closed {int(get_id[1])} {int(get_id[2])}",
                ),
            ],
        ]
        start = datetime.now()
        exp = await get_expired_date(user_id)
        habis = exp.strftime("%d.%m.%Y") if exp else None
        await my.invoke(Ping(ping_id=0))
        ping = (datetime.now() - start).microseconds / 1000
        uptime_sec = (datetime.utcnow() - START_TIME).total_seconds()
        uptime = await _human_time_duration(int(uptime_sec))
        msg = f"""
<b>AmangUbot</b>
         <b>status:</b> <code>Premium[{status}]</code>
             <b>expired:</b> <code>{habis}</code>
             <b>dc_id:</b> <code>{my.me.dc_id}</code>
             <b>ping_dc:</b> <code>{ping} ms</code>
             <b>peer_ubot:</b> <code>{memek} users</code>
             <b>uptime:</b> <code>{uptime}</code>
"""
        await client.answer_inline_query(
            inline_query.id,
            cache_time=300,
            results=[
                (
                    InlineQueryResultArticle(
                        title="alive",
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


@bot.on_inline_query(filters.regex("^user_help_command"))
async def _(client, inline_query):
    msg = f"<b>Help Module\nPrefixes: <code>. ! ,</code></b>"
    await client.answer_inline_query(
        inline_query.id,
        cache_time=300,
        results=[
            (
                InlineQueryResultArticle(
                    title="help",
                    reply_markup=InlineKeyboardMarkup(
                        paginate_modules(0, HELP_COMMANDS, "help")
                    ),
                    input_message_content=InputTextMessageContent(msg),
                )
            )
        ],
    )


@bot.on_callback_query(filters.regex(r"help_(.*?)"))
async def _(client, callback_query):
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
    top_text = f"<b>Help Module\nPrefixes: <code>{COMMAND}</code></b>"
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
            top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(next_page + 1, HELP_COMMANDS, "help")
            ),
            disable_web_page_preview=True,
        )
    if back_match:
        await callback_query.edit_message_text(
            top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, HELP_COMMANDS, "help")
            ),
            disable_web_page_preview=True,
        )
