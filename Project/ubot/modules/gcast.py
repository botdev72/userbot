import asyncio
import os
from gc import get_objects

from pyrogram import *
from pyrogram.enums import ChatType
from pyrogram.errors import *
from pyrogram.types import *
from telegraph import upload_file

from ubot import *
from ubot.config import *
from ubot.utils import *

__MODULE__ = "Broadcast"
__HELP__ = """
Bantuan Untuk Broadcast

• Perintah: <code>{0}gucast</code> [text/reply to text/media]
• Penjelasan: Untuk mengirim pesan ke semua user

• Perintah: <code>{0}gcast</code> [text/reply to text/media]
• Penjelasan: Untuk mengirim pesan ke semua group

• Perintah: <code>{0}addbl</code>
• Penjelasan: Menambahkan grup kedalam anti Gcast.

• Perintah: <code>{0}delbl</code>
• Penjelasan: Menghapus grup dari daftar anti Gcast.

• Perintah: <code>{0}rmall</code>
• Penjelasan: Menghapus semua grup dari daftar anti Gcast.

• Perintah: <code>{0}listbl</code>
• Penjelasan: Melihat daftar grup anti Gcast.
"""


async def get_broadcast_id(client, query):
    chats = []
    chat_types = {
        "group": [ChatType.GROUP, ChatType.SUPERGROUP],
        "users": [ChatType.PRIVATE],
    }
    try:
        async for dialog in client.get_dialogs():
            if dialog.chat.type in chat_types[query]:
                chats.append(dialog.chat.id)
    except ChannelPrivate:
        pass

    return chats


def get_message(message):
    msg = (
        message.reply_to_message
        if message.reply_to_message
        else ""
        if len(message.command) < 2
        else " ".join(message.command[1:])
    )
    return msg


@KY.UBOT("gcast", sudo=True)
async def _(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()

    msg = await message.reply(f"{emo.proses} **Processing...**")
    send = get_message(message)
    if not send:
        await eor(
            message, f"{emo.gagal} **Silakan balas ke pesan atau berikan pesan.**"
        )
        return

    chats = await get_broadcast_id(client, "group")
    blacklist = await get_chat(client.me.id)

    done = 0
    failed = 0

    for chat_id in chats:
        if chat_id in blacklist:
            continue
        elif chat_id in BLACKLIST_CHAT:
            continue

        try:
            if message.reply_to_message:
                await send.copy(chat_id)
            else:
                await client.send_message(chat_id, send)
            await asyncio.sleep(0.2)
            done += 1
        except FloodWait:
            pass
            # await asyncio.sleep(e.value)
            # if message.reply_to_message:
            # await send.copy(chat_id)
            # else:
            # await client.send_message(chat_id, send)
            # done += 1
        except Exception:
            failed += 1

    await msg.delete()
    await client.send_message(
        # return await eor(
        # message,
        message.chat.id,
        f"{emo.alive} **Pesan Broadcast Terkirim :\n{emo.sukses} Berhasil di `{done}` Grup.\n{emo.gagal} Gagal di `{failed}` Grup.**",
    )


@KY.UBOT("gucast", sudo=True)
async def _(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()

    msg = await message.reply(f"{emo.proses} **Processing...**")

    send = get_message(message)
    if not send:
        return await msg.edit(
            f"{emo.gagal} **Silakan balas ke pesan atau berikan pesan.**"
        )

    chats = await get_broadcast_id(client, "users")
    blacklist = await get_chat(client.me.id)

    done = 0
    failed = 0
    for chat_id in chats:
        if chat_id in blacklist:
            continue
        elif chat_id in DEVS:
            continue

        try:
            if message.reply_to_message:
                await send.copy(chat_id)
            else:
                await client.send_message(chat_id, send)
            await asyncio.sleep(0.8)
            done += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            if message.reply_to_message:
                await send.copy(chat_id)
            else:
                await client.send_message(chat_id, send)
            done += 1
        except Exception:
            failed += 1
        except SlowmodeWait:
            pass

    # await msg.delete()
    # return await client.send_message(
    return await msg.edit(
        # message.chat.id,
        f"{emo.alive} **Pesan Broadcast Terkirim :\n{emo.sukses} Berhasil di `{done}` penguna.\n{emo.gagal} Gagal di `{failed}` pengguna.**",
    )


@KY.UBOT("addbl", sudo=True)
async def add_blaclist(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    Tm = await message.reply(f"{emo.proses} **Processing...**")
    await asyncio.sleep(2)
    chat_id = message.chat.id
    blacklist = await get_chat(client.me.id)
    if chat_id in blacklist:
        return await Tm.edit(f"{emo.sukses} **Grup ini sudah ada dalam blacklist**")
    add_blacklist = await add_chat(client.me.id, chat_id)
    if add_blacklist:
        await Tm.edit(
            f"{emo.sukses} **`{message.chat.title}` berhasil ditambahkan ke dalam blacklist.**"
        )
    else:
        await Tm.edit(f"{emo.gagal} **Error.**")


@KY.UBOT("delbl", sudo=True)
async def del_blacklist(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    Tm = await message.reply(f"{emo.proses} **Processing...**")
    await asyncio.sleep(2)
    try:
        if not get_arg(message):
            chat_id = message.chat.id
        else:
            chat_id = int(message.command[1])
        blacklist = await get_chat(client.me.id)
        if chat_id not in blacklist:
            return await Tm.edit(
                f"{emo.gagal} **`{message.chat.title}` tidak ada dalam daftar blacklist.**"
            )
        del_blacklist = await remove_chat(client.me.id, chat_id)
        if del_blacklist:
            await Tm.edit(
                f"{emo.sukses} **`{chat_id}` berhasil dihapus dari daftar blacklist.**"
            )
        else:
            await Tm.edit(f"{emo.gagal} **Error.**")
    except Exception as error:
        await Tm.edit(str(error))


@KY.UBOT("listbl", sudo=True)
async def get_blacklist(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    Tm = await message.reply(f"{emo.proses} **Processing...**")
    await asyncio.sleep(2)
    msg = (
        f"{emo.sukses} <b>• Total blacklist {len(await get_chat(client.me.id))}</b>\n\n"
    )
    for X in await get_chat(client.me.id):
        try:
            get = await client.get_chat(X)
            msg += f"<b>• {get.title} | <code>{get.id}</code></b>\n"
        except:
            msg += f"<b>• <code>{X}</code></b>\n"
    await Tm.delete()
    await message.reply(msg)


@KY.UBOT("rmall", sudo=True)
async def rem_all_blacklist(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    msg = await message.reply(f"{emo.proses} **Processing....**")
    await asyncio.sleep(2)
    get_bls = await get_chat(client.me.id)
    if len(get_bls) == 0:
        return await msg.edit(f"{emo.gagal} **Daftar hitam Anda kosong.**")
    for X in get_bls:
        await remove_chat(client.me.id, X)
    await msg.edit(f"{emo.sukses} **Semua daftar hitam telah berhasil dihapus.**")


@KY.UBOT("send", sudo=True)
@KY.BOT("send")
async def send_msg_cmd(client, message):
    if message.reply_to_message:
        chat_id = (
            message.chat.id if len(message.command) < 2 else message.text.split()[1]
        )
        try:
            if client.me.id != bot.me.id:
                if message.reply_to_message.reply_markup:
                    x = await client.get_inline_bot_results(
                        bot.me.username, f"get_send_ {id(message)}"
                    )
                    return await client.send_inline_bot_result(
                        chat_id, x.query_id, x.results[0].id
                    )
        except Exception as error:
            return await message.reply(error)
        else:
            try:
                return await message.reply_to_message.copy(chat_id)
            except Exception as t:
                return await message.reply(f"{t}")
    else:
        if len(message.command) < 3:
            return await message.reply("Ga gitu.")
        chat_id, chat_text = message.text.split(None, 2)[1:]
        try:
            if "/" in chat_id:
                to_chat, msg_id = chat_id.split("/")
                return await client.send_message(
                    to_chat, chat_text, reply_to_message_id=int(msg_id)
                )
            else:
                return await client.send_message(chat_id, chat_text)
        except Exception as t:
            return await message.reply(f"{t}")


@KY.INLINE("^get_send_")
async def send_inline(client, inline_query):
    try:
        _id = int(inline_query.query.split()[1])
        m = [obj for obj in get_objects() if id(obj) == _id][0]

        if m.reply_to_message.photo:
            m_d = await m.reply_to_message.download()
            photo_tg = upload_file(m_d)
            cp = m.reply_to_message.caption
            text = cp if cp else ""
            hasil = [
                InlineQueryResultPhoto(
                    photo_url=f"https://telegra.ph/{photo_tg[0]}",
                    title="get send!",
                    reply_markup=m.reply_to_message.reply_markup,
                    caption=text,
                ),
            ]
            os.remove(m_d)
        else:
            hasil = [
                InlineQueryResultArticle(
                    title="get send!",
                    reply_markup=m.reply_to_message.reply_markup,
                    input_message_content=InputTextMessageContent(
                        m.reply_to_message.text
                    ),
                )
            ]
        await client.answer_inline_query(
            inline_query.id,
            cache_time=0,
            results=hasil,
        )
    except Exception as e:
        print("Terjadi kesalahan:", str(e))
