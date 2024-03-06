from gc import get_objects

from pyrogram import filters
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                            InlineQueryResultArticle, InputTextMessageContent)

from .. import *

__MODULE__ = "SECRET"
__HELP__ = f"""
Perintah:
         <code>{PREFIX[0]}msg</code> [reply to user - text]
Penjelasan:
           Untuk mengirim pesan secara rahasia
"""


@PY.UBOT("msg", PREFIX)
async def _(client, message):
    if not message.reply_to_message:
        return await message.reply(
            f"<code>{message.text}</code> [reply to user - text]"
        )
    text = f"secret {id(message)}"
    await message.delete()
    x = await client.get_inline_bot_results(bot.me.username, text)
    await message.reply_to_message.reply_inline_bot_result(x.query_id, x.results[0].id)


@bot.on_inline_query(filters.regex("^secret"))
@Inline.query
async def _(client, q):
    m = [obj for obj in get_objects() if id(obj) == int(q.query.split(None, 1)[1])][0]
    await client.answer_inline_query(
        q.id,
        cache_time=0,
        results=[
            (
                InlineQueryResultArticle(
                    title="pesan rahasia!",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="💬 Baca Pesan Rahasia 💬",
                                    url=f"https://t.me/{bot.me.username}?start=secretMsg_{int(q.query.split(None, 1)[1])}",
                                )
                            ],
                        ]
                    ),
                    input_message_content=InputTextMessageContent(
                        f"<b>👉🏻 Ada Pesan Rahasia Untuk Mu Nih:</b> <a href=tg://user?id={m.reply_to_message.from_user.id}>{m.reply_to_message.from_user.first_name} {m.reply_to_message.from_user.last_name or ''}</a>"
                    ),
                )
            )
        ],
    )
