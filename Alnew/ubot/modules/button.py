"""
Credit Tomi Setiawan Wibu Sejati
"""


from gc import get_objects
import asyncio
from pykeyboard import InlineKeyboard
from pyrogram.errors import MessageNotModified
from pyrogram import *
from pyrogram.types import *
from ubot import *

__MODULE__ = "Button"
__HELP__ = """
Bantuan Untuk Button

• Perintah: <code>{0}button</code> [balas pesan]
• Penjelasan: Untuk membuat teks menjadi button.
"""


async def create_button(m):
    buttons = InlineKeyboard(row_width=1)
    keyboard = []
    msg = []
    if "~" not in m.text.split(None, 1)[1]:
        for X in m.text.split(None, 1)[1].split():
            X_parts = X.split("|", 1)
            keyboard.append(
                InlineKeyboardButton(X_parts[0].replace("_", " "), url=X_parts[1])
            )
            msg.append(X_parts[0])
        buttons.add(*keyboard)
        if m.reply_to_message:
            text = m.reply_to_message.text
        else:
            text = " ".join(msg)
    else:
        for X in m.text.split("~", 1)[1].split():
            X_parts = X.split("|", 1)
            keyboard.append(
                InlineKeyboardButton(X_parts[0].replace("_", " "), url=X_parts[1])
            )
        buttons.add(*keyboard)
        text = m.text.split("~", 1)[0].split(None, 1)[1]

    return buttons, text

@ubot.on_message(filters.me & anjay("button"))
async def cmd_button(client, message):
    if len(message.command) < 2:
        return await message.reply(f"{message.text} text ~ [button_name|link_url]")
    #kntl = message.reply_to_message
    if "~" not in message.command:
        return await message.reply(
            f"Silakan balas kepesan {message.text} -> teks ~ google|google.com"
        )
    await message.delete()
    try:
        x = await client.get_inline_bot_results(
            bot.me.username, f"get_button {id(message)}"
        )
        msg = message.reply_to_message or message
        await client.send_inline_bot_result(
            message.chat.id, x.query_id, x.results[0].id, reply_to_message_id=msg.id
        )
    except Exception as error:
        await message.reply(error)

@bot.on_inline_query(filters.regex("^get_button"))
async def inline_button(client, inline_query):
    get_id = int(inline_query.query.split(None, 1)[1])
    m = [obj for obj in get_objects() if id(obj) == get_id][0]
    buttons, text = await create_button(m)
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
