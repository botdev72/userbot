import re

from pyrogram.types import *

from .. import *


@PY.UBOT("help", PREFIX)
async def _(client, message):
    if len(message.command) < 2:
        x = await client.get_inline_bot_results(bot.me.username, "help")
        try:
            return await message.reply_inline_bot_result(x.query_id, x.results[0].id)
        except Exception as error:
            return await message.reply(error)
    else:
        if message.command[1] in HELP_COMMANDS:
            return await message.reply(
                f"<b>HELP {HELP_COMMANDS[message.command[1]].__MODULE__}\n{HELP_COMMANDS[message.command[1]].__HELP__}</b>"
            )
        elif message.command[1] in HelpText:
            return await message.reply(HelpText[message.command[1]])
        else:
            return await message.reply(
                f"<b>❌ Modules {message.command[1]} Tidak Ditemukan</b>"
            )


@PY.INLINE("^help")
@Inline.query
async def _(client, inline_query):
    msg = f"<b>HELP MENU OPEN\nPREFIXES: <code>{COMMAND}</code></b>"
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


@PY.CALLBACK("help_(.*?)")
@Inline.data
async def _(client, callback_query):
    mod_match = re.match(r"help_module\((.+?)\)", callback_query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", callback_query.data)
    next_match = re.match(r"help_next\((.+?)\)", callback_query.data)
    back_match = re.match(r"help_back", callback_query.data)
    top_text = f"<b>HELP MENU OPEN\nPREFIXES: <code>{COMMAND}</code></b>"
    if mod_match:
        module = (mod_match.group(1)).replace(" ", "_")
        text = f"<b>HELP {HELP_COMMANDS[module].__MODULE__}\n{HELP_COMMANDS[module].__HELP__}</b>\n"
        button = [[InlineKeyboardButton("• KEMBALI •", callback_data="help_back")]]
        if "ADMIN" in text:
            text = f"<b>HELP MENU OPEN\nPREFIXES: <code>{COMMAND}</code></b>"
            button = Button.admin()[0]
        if "STICKER" in text:
            text = f"<b>HELP MENU OPEN\nPREFIXES: <code>{COMMAND}</code></b>"
            button = Button.sticker()[0]
        await callback_query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(button),
            disable_web_page_preview=True,
        )
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


@PY.CALLBACK("^menu_help")
@Inline.data
async def _(client, callback_query):
    data = callback_query.data.split()[1]
    if data == "admin_gban":
        msg = HelpText["global"]
        button = Button.admin()[1]
    if data == "admin_restrict":
        msg = HelpText["restrict"]
        button = Button.admin()[1]
    if data == "admin_back":
        msg = f"<b>HELP MENU OPEN\n PREFIXES: <code>{COMMAND}</code></b>"
        button = Button.admin()[0]
    if data == "sticker_kang":
        msg = HelpText["kang"]
        button = Button.sticker()[1]
    if data == "sticker_memify":
        msg = HelpText["memify"]
        button = Button.sticker()[1]
    if data == "sticker_memes":
        msg = HelpText["memes"]
        button = Button.sticker()[1]
    if data == "sticker_quotly":
        msg = HelpText["quotly"]
        button = Button.sticker()[1]
    if data == "sticker_tiny":
        msg = HelpText["tiny"]
        button = Button.sticker()[1]
    if data == "sticker_back":
        msg = f"<b>HELP MENU OPEN\nPREFIXES: <code>{COMMAND}</code></b>"
        button = Button.sticker()[0]
    await callback_query.edit_message_text(
        msg, reply_markup=InlineKeyboardMarkup(button)
    )
