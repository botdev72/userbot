import os
from datetime import datetime
from time import time

import psutil
from pyrogram.raw.functions import Ping
from pyrogram.types import *

from .. import *


@PY.UBOT("alive", PREFIX)
async def _(client, message):
    try:
        x = await client.get_inline_bot_results(
            bot.me.username, f"alive {message.id} {message.from_user.id}"
        )
        await message.reply_inline_bot_result(x.query_id, x.results[0].id)
    except Exception as error:
        await message.reply(error)


@PY.INLINE("^alive")
@Inline.query
async def _(client, inline_query):
    get_id = inline_query.query.split()
    for my in ubot._ubot:
        if int(get_id[2]) == my.me.id:
            peer = get_my_peer[my.me.id]
            get_exp = await get_expired_date(my.me.id)
            if get_exp is None:
                expired = ""
            else:
                exp = get_exp.strftime("%d-%m-%Y")
                expired = f"\n      <b>expired:</b> <code>{exp}</code>"
            if my.me.id == OWNER_ID:
                status = "founder"
            elif my.me.id in await get_seles():
                status = "admin"
            else:
                status = "member"
            if int(get_id[2]) == OWNER_ID:
                button = Button.alive(get_id)[0]
            else:
                button = Button.alive(get_id)[1]
            start = datetime.now()
            await my.invoke(Ping(ping_id=0))
            ping = (datetime.now() - start).microseconds / 1000
            uptime = await get_time((time() - start_time))
            msg = f"""
<b>{bot.me.username}</b>
   <b>status:</b> <code>[{status}]</code> {expired} 
      <b>dc_id:</b> <code>{my.me.dc_id}
      <b>ping_dc:</b> <code>{ping} ms</code>
      <b>peer_users:</b> <code>{peer['users']} users</code>
      <b>peer_group:</b> <code>{peer['group']} group</code>
      <b>{bot.me.first_name.split()[0]}_uptime:</b> <code>{uptime}</code>
"""
            await client.answer_inline_query(
                inline_query.id,
                cache_time=0,
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


@PY.CALLBACK("stats")
@Inline.data
async def _(client, callback_query):
    if not callback_query.from_user.id == OWNER_ID:
        return await callback_query.answer(
            f"❌ TOMBOL INI BUKAN UNTUK MU {callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}",
            True,
        )
    uptime = await get_time((time() - start_time))
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
MODULES: {len(HELP_COMMANDS) + len(HelpText)}
"""
    await callback_query.answer(stats, True)


@PY.CALLBACK("^alv_cls")
@Inline.data
async def _(cln, cq):
    get_id = cq.data.split()
    if not cq.from_user.id == int(get_id[2]):
        return await cq.answer(
            f"❌ TOMBOL INI BUKAN UNTUK MU {cq.from_user.first_name} {cq.from_user.last_name or ''}",
            True,
        )
    unPacked = unpackInlineMessage(cq.inline_message_id)
    for my in ubot._ubot:
        if cq.from_user.id == int(my.me.id):
            await my.delete_messages(
                unPacked.chat_id, [int(get_id[1]), unPacked.message_id]
            )
