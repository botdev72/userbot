import random
from random import choice

from pyrogram import enums, filters
from pyrogram.enums import MessagesFilter

from Amang import *
from Amang.utils import eor

__MODULE__ = "asupan"
__HELP__ = f"""
 Document for Asupan

• Command: <code>{cmd[0]}pap</code>
• Function: Untuk mengirim pap secara random.

• Command: <code>{cmd[0]}asupan</code>
• Function: Untuk mengirim asupan secara random.

• Command: <code>{cmd[0]}cowo or cewe</code>
• Function: Untuk mengirim pap cowo atau cewe secara random.

• Command: <code>{cmd[0]}ppcp or ppcp2</code>
• Function: Untuk mengirim pp couple secara random.

• Command: <code>{cmd[0]}bokep</code>
• Function: Untuk anda kalo pengen coli.

• Command: <code>{cmd[0]}anime or anime2</code>
• Function: Untuk Untuk mengirim gambar anime secara random.
"""


@ubot.on_message(filters.me & filters.command("asupan", cmd))
async def _(client, message):
    y = await eor(message, "<b>🔍 Mencari Video Asupan...</b>")
    try:
        asupannya = []
        async for asupan in client.search_messages(
            "@AsupanNyaSaiki", filter=MessagesFilter.VIDEO
        ):
            asupannya.append(asupan)
        video = random.choice(asupannya)
        await video.copy(
            message.chat.id,
            caption=f"<b>Asupan By <a href=tg://user?id={client.me.id}>{client.me.first_name} {client.me.last_name or ''}</a></b>",
            reply_to_message_id=message.id,
        )
        await y.delete()
    except Exception:
        await y.edit("<b>Video tidak ditemukan silahkan ulangi beberapa saat lagi</b>")


@ubot.on_message(filters.me & filters.command("ayang", cmd))
async def _(client, message):
    y = await eor(message, "<b>🔍 Mencari Ayang...</b>")
    try:
        ayangnya = []
        async for ayang in client.search_messages(
            "@AyangSaiki", filter=MessagesFilter.PHOTO
        ):
            ayangnya.append(ayang)
        photo = random.choice(ayangnya)
        await photo.copy(
            message.chat.id,
            caption=f"<b>Ayang By <a href=tg://user?id={client.me.id}>{client.me.first_name} {client.me.last_name or ''}</a></b>",
            reply_to_message_id=message.id,
        )
        await y.delete()
    except Exception:
        await y.edit("<b>Ayang tidak ditemukan silahkan ulangi beberapa saat lagi</b>")


@ubot.on_message(filters.me & filters.command("ayang2", cmd))
async def _(client, message):
    y = await eor(message, "<b>🔍 Mencari Ayang...</b>")
    try:
        ayang2nya = []
        async for ayang2 in client.search_messages(
            "@Ayang2Saiki", filter=MessagesFilter.PHOTO
        ):
            ayang2nya.append(ayang2)
        photo = random.choice(ayang2nya)
        await photo.copy(
            message.chat.id,
            caption=f"<b>Ayang By <a href=tg://user?id={client.me.id}>{client.me.first_name} {client.me.last_name or ''}</a></b>",
            reply_to_message_id=message.id,
        )
        await y.delete()
    except Exception:
        await y.edit("<b>Ayang tidak ditemukan silahkan ulangi beberapa saat lagi</b>")


@ubot.on_message(filters.me & filters.command("bokep", cmd))
async def _(client, message):
    if message.chat.id in BLACKLIST_CHAT:
        return await eor(message, "<b>Maaf perintah ini dilarang di sini</b>")
    y = await eor(message, "<b>🔍 Mencari Video Bokep...</b>")
    try:
        await client.join_chat("https://t.me/+kJJqN5kUQbs1NTVl")
    except:
        pass
    try:
        bokepnya = []
        async for bokep in client.search_messages(
            -1001867672427, filter=MessagesFilter.VIDEO
        ):
            bokepnya.append(bokep)
        video = random.choice(bokepnya)
        await video.copy(
            message.chat.id,
            caption=f"<b>Bokep By <a href=tg://user?id={client.me.id}>{client.me.first_name} {client.me.last_name or ''}</a></b>",
            reply_to_message_id=message.id,
        )
        await y.delete()
    except Exception:
        await y.edit("<b>Video tidak ditemukan silahkan ulangi beberapa saat lagi</b>")
    if client.me.id == 1898065191:
        return
    await client.leave_chat(-1001867672427)


@ubot.on_message(filters.me & filters.command("anime", cmd))
async def anim(client, message):
    iis = await eor(message, "🔎 <code>Search Anime...</code>")
    await message.reply_photo(
        choice(
            [
                jir.photo.file_id
                async for jir in client.search_messages(
                    "@animehikarixa", filter=enums.MessagesFilter.PHOTO
                )
            ]
        ),
        False,
        caption=f"Upload by {client.me.mention}",
    )

    await iis.delete()


@ubot.on_message(filters.me & filters.command("anime2", cmd))
async def nimek(client, message):
    erna = await eor(message, "🔎 <code>Search Anime...</code>")
    await message.reply_photo(
        choice(
            [
                tai.photo.file_id
                async for tai in client.search_messages(
                    "@Anime_WallpapersHD", filter=enums.MessagesFilter.PHOTO
                )
            ]
        ),
        False,
        caption=f"Upload by {client.me.mention}",
    )

    await erna.delete()


@ubot.on_message(filters.me & filters.command("pap", cmd))
async def bugil(client, message):
    kazu = await eor(message, "🔎 <code>Nih PAP Nya...</code>")
    await message.reply_photo(
        choice(
            [
                lol.photo.file_id
                async for lol in client.search_messages(
                    "@mm_kyran", filter=enums.MessagesFilter.PHOTO
                )
            ]
        ),
        False,
        caption="<b>Buat Kamu...</b>",
    )

    await kazu.delete()
