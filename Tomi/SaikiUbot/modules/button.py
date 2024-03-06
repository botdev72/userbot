from gc import get_objects

from pykeyboard import InlineKeyboard
from pyrogram.types import (InlineKeyboardButton, InlineQueryResultArticle,
                            InputTextMessageContent)

from .. import *


async def create_button(m):
    buttons = InlineKeyboard(row_width=2)
    keyboard = []
    if "|" not in m.text.split(None, 1)[1]:
        msg = []
        for X in m.text.split(None, 1)[1].split():
            keyboard.append(
                InlineKeyboardButton(X.split(":", 1)[0], url=X.split(":", 1)[1])
            )
            msg.append(X.split(":")[0])
        buttons.add(*keyboard)
        if m.reply_to_message:
            text_or_rep = m.reply_to_message.text
        else:
            msg_text = ""
            for Z in msg:
                msg_text += f"{Z} "
            text_or_rep = msg_text
    else:
        for X in m.text.split("|", 1)[1].split():
            keyboard.append(
                InlineKeyboardButton(X.split(":", 1)[0], url=X.split(":", 1)[1])
            )
        buttons.add(*keyboard)
        text_or_rep = m.text.split("|", 1)[0].split(None, 1)[1]
    return buttons, text_or_rep


@PY.UBOT("button", PREFIX)
async def _(client, message):
    if len(message.command) < 2:
        return await message.reply(f"{message.text} button_name:link_url")
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


@PY.INLINE("^get_button")
@Inline.query
async def _(client, inline_query):
    get_id = int(inline_query.query.split(None, 1)[1])
    m = [obj for obj in get_objects() if id(obj) == get_id][0]
    buttons, text_or_rep = await create_button(m)
    await client.answer_inline_query(
        inline_query.id,
        cache_time=0,
        results=[
            (
                InlineQueryResultArticle(
                    title="get button!",
                    reply_markup=buttons,
                    input_message_content=InputTextMessageContent(text_or_rep),
                )
            )
        ],
    )
