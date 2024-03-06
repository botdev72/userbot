import asyncio
import os
from base64 import b64decode
from io import BytesIO

import requests
from pyrogram import *
from pyrogram.errors import FloodWait
from pyrogram.raw.functions.messages import DeleteHistory
from pyrogram.types import *

from ubot import *
from ubot.utils import extract_user_and_reason
from ubot.utils.quote import render_message, resize_image


@KY.UBOT("q", sudo=True)
async def quotly(client: Client, message: Message):
    emo = Emo(client.me.id)
    await emo.initialize()
    info = await message.reply(f"{emo.proses} **Processing...**")
    await asyncio.sleep(2)
    await client.unblock_user("@QuotLyBot")
    if message.reply_to_message:
        if len(message.command) < 2:
            msg = [message.reply_to_message]
        else:
            try:
                count = int(message.command[1])
            except Exception as error:
                await info.edit(error)
            try:
                msg = [
                    i
                    for i in await client.get_messages(
                        chat_id=message.chat.id,
                        message_ids=range(
                            message.reply_to_message.id,
                            message.reply_to_message.id + count,
                        ),
                        replies=-1,
                    )
                ]
            except FloodWait:
                pass
        try:
            for x in msg:
                await x.forward("@QuotLyBot")
        except Exception:
            pass
        await asyncio.sleep(9)
        await info.delete()
        async for quotly in client.get_chat_history("@QuotLyBot", limit=1):
            if not quotly.sticker:
                await eor(
                    message,
                    f"{emo.gagal} **Kesalahan saat membuat quote.**",
                )
            else:
                sticker = await client.download_media(quotly)
                await message.reply_sticker(sticker)
                os.remove(sticker)
    else:
        if len(message.command) < 2:
            return await info.edit(f"{emo.gagal} **Mohon balas ke teks.**")
        else:
            msg = await client.send_message(
                "@QuotLyBot", f"/qcolor {message.command[1]}"
            )
            await asyncio.sleep(1)
            try:
                get = await client.get_messages("@QuotLyBot", msg.id + 1)
                await info.edit(
                    f"{emo.sukses} **Warna latar belakang quote diganti ke: {get.text.split(':')[1]}**"
                )
            except FloodWait:
                pass
    user_info = await client.resolve_peer("@QuotLyBot")
    return await client.invoke(DeleteHistory(peer=user_info, max_id=0, revoke=True))


@KY.UBOT("qf", sudo=True)
async def fake_quote_cmd(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    xx = await message.reply(f"{emo.proses} **Processing...**")
    await asyncio.sleep(2)
    target_user, reason = await extract_user_and_reason(message)
    if target_user is None:
        return await xx.edit(f"{emo.gagal} **Invalid username format.**")

    target_user = str(target_user)
    if not target_user:
        return await xx.edit(f"{emo.gagal} **Invalid username format.**")
    try:
        user = await client.get_users(target_user)
    except errors.exceptions.bad_request_400.UsernameNotOccupied:
        return await xx.edit(f"{emo.gagal} **Not found a username.**")
    except IndexError:
        return await xx.edit(f"{emo.gagal} **Only for user.**")
    if message.reply_to_message:
        rep = message.reply_to_message.text
    else:
        rep = reason if reason else ""
    fake_quote_text = rep
    if not fake_quote_text:
        return await xx.edit(f"{emo.gagal} **Empty message.**")
    try:
        q_message = await client.get_messages(message.chat.id, message.id, replies=0)
    except FloodWait:
        pass
    q_message.text = fake_quote_text
    q_message.entities = None
    q_message.from_user.id = user.id
    q_message.from_user.first_name = user.first_name
    q_message.from_user.last_name = user.last_name
    q_message.from_user.username = user.username
    q_message.from_user.photo = user.photo
    url = "https://quotes.fl1yd.su/generate"
    user_auth_1 = b64decode(
        "Y2llIG1hbyBueW9sb25nIGNpaWUuLi4uLCBjb2xvbmcgYWphIGJhbmcgamFkaWluIHByZW0gdHJ1cyBqdWFsLCBrYWxpIGFqYSBiZXJrYWggaWR1cCBsdS4uLi4="
    )
    params = {
        "messages": [await render_message(client, q_message)],
        "quote_color": "#ffffff",
        "text_color": "#1e2729",
    }
    response = requests.post(url, json=params)
    if not response.ok:
        return await xx.edit(
            f"{emo.gagal} <b>Error!</b>\n" f"<code>{response.text}</code>"
        )
    resized = resize_image(BytesIO(response.content), img_type="webp")
    try:
        func = client.send_sticker
        chat_id = message.chat.id
        await func(chat_id, resized)
    except errors.RPCError as e:
        await xx.edit(e)
    else:
        await xx.delete()
