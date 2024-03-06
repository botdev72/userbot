import asyncio
from gc import get_objects

from pyrogram.enums import ChatType
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent

from .. import *

__MODULE__ = "GCAST"
__HELP__ = f"""
Perintah:
         <code>{PREFIX[0]}ucast</code> [text/reply to text/media]
Penjelasan:
           Untuk mengirim pesan ke semua user 

Perintah:
         <code>{PREFIX[0]}gcast</code> [text/reply to text/media]
Penjelasan:
           Untuk mengirim pesan ke semua group 

Perintah:
         <code>{PREFIX[0]}send</code> [userid/username - text/reply]
Penjelasan:
           Untuk mengirim pesan ke user/group/channel 
"""


@PY.UBOT("gcast", PREFIX)
async def _(client, message):
    sent = 0
    failed = 0
    msg = await message.reply("Sedang Memproses")
    async for dialog in client.get_dialogs():
        if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            if message.reply_to_message:
                send = message.reply_to_message
            else:
                if len(message.command) < 2:
                    await msg.delete()
                    return await message.reply("mohon balas sesuatu atau ketik sesuatu")
                else:
                    send = message.text.split(None, 1)[1]
            chat_id = dialog.chat.id
            if chat_id not in BLACKLIST_CHAT:
                try:
                    if message.reply_to_message:
                        await send.copy(chat_id)
                    else:
                        await client.send_message(chat_id, send)
                    sent += 1
                    await asyncio.sleep(0.3)
                except Exception:
                    failed += 1
                    await asyncio.sleep(0.1)
    await msg.delete()
    return await message.reply(
        f"💬 Mengirim Pesan Selesai\n\n✅ Berhasil Terkirim: {sent} \n❌ Gagal Terkirim: {failed}"
    )


@PY.UBOT("ucast", PREFIX)
async def _(client, message):
    sent = 0
    failed = 0
    msg = await message.reply("Sedang Memproses")
    async for dialog in client.get_dialogs():
        if dialog.chat.type == ChatType.PRIVATE:
            if message.reply_to_message:
                send = message.reply_to_message
            else:
                if len(message.command) < 2:
                    await msg.delete()
                    return await message.reply("mohon balas sesuatu atau ketik sesuatu")
                else:
                    send = message.text.split(None, 1)[1]
            chat_id = dialog.chat.id
            if chat_id not in BLACKLIST_CHAT:
                try:
                    if message.reply_to_message:
                        await send.copy(chat_id)
                    else:
                        await client.send_message(chat_id, send)
                    sent += 1
                    await asyncio.sleep(0.3)
                except Exception:
                    failed += 1
                    await asyncio.sleep(0.1)
    await msg.delete()
    return await message.reply(
        f"💬 Mengirim Pesan Selesai\n\n✅ Berhasil Terkirim: {sent} \n❌ Gagal Terkirim: {failed}"
    )


@PY.UBOT("send", PREFIX)
async def _(client, message):
    if message.reply_to_message:
        if len(message.command) < 2:
            chat_id = message.chat.id
        else:
            chat_id = message.text.split()[1]
        if message.reply_to_message.reply_markup:
            try:
                x = await client.get_inline_bot_results(
                    bot.me.username, f"get_send {id(message)}"
                )
                msg = message.reply_to_message or message
                await client.send_inline_bot_result(
                    chat_id, x.query_id, x.results[0].id, reply_to_message_id=msg.id
                )
                tm = await message.reply(f"✅ Pesan Berhasil Dikirim Ke {chat_id}")
                await asyncio.sleep(5)
                await message.delete()
                await tm.delete()
            except Exception as error:
                await message.reply(error)
        else:
            try:
                await message.reply_to_message.copy(chat_id, protect_content=True)
                tm = await message.reply(f"✅ Pesan Berhasil Dikirim Ke {chat_id}")
                await asyncio.sleep(3)
                await message.delete()
                await tm.delete()
            except Exception as t:
                return await message.reply(f"{t}")
    else:
        if len(message.command) < 3:
            return await message.reply("ketik yang bener")
        chat_id = message.text.split(None, 2)[1]
        chat_text = message.text.split(None, 2)[2]
        try:
            await client.send_message(chat_id, chat_text, protect_content=True)
            tm = await message.reply(f"✅ Pesan Berhasil Dikirim Ke {chat_id}")
            await asyncio.sleep(3)
            await message.delete()
            await tm.delete()
        except Exception as t:
            return await message.reply(f"{t}")


@PY.INLINE("^get_send")
@Inline.query
async def _(client, inline_query):
    _id = int(inline_query.query.split()[1])
    m = [obj for obj in get_objects() if id(obj) == _id][0]
    await client.answer_inline_query(
        inline_query.id,
        cache_time=0,
        results=[
            (
                InlineQueryResultArticle(
                    title="get send!",
                    reply_markup=m.reply_to_message.reply_markup,
                    input_message_content=InputTextMessageContent(
                        m.reply_to_message.text
                    ),
                )
            )
        ],
    )
