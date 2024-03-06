import random

from pyrogram.enums import MessagesFilter

from .. import *

__MODULE__ = "ASUPAN"
__HELP__ = f"""
Perintah:
         <code>{PREFIX[0]}asupan</code>
Penjelasan:
           Untuk mengirim video asupan random 

Perintah:
         <code>{PREFIX[0]}ayang</code>
Penjelasan:
           Untuk mengirim photo cewek random

Perintah:
         <code>{PREFIX[0]}ayang2</code>
Penjelasan:
           Untuk mengirim photo cowok random 

Perintah:
         <code>{PREFIX[0]}anime</code>
Penjelasan:
           Untuk mengirim photo anime random

Perintah:
         <code>{PREFIX[0]}bokep</code>
Penjelasan:
           Untuk mengirim video bokep random
"""


@PY.UBOT("asupan", PREFIX)
async def _(client, message):
    y = await message.reply_text("<b>🔍 Mencari Video Asupan...</b>")
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
        await y.edit("<b>video tidak ditemukan silahkan ulangi beberapa saat lagi</b>")


@PY.UBOT("ayang", PREFIX)
async def _(client, message):
    y = await message.reply_text("<b>🔍 Mencari Ayang...</b>")
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


@PY.UBOT("ayang2", PREFIX)
async def _(client, message):
    y = await message.reply_text("<b>🔍 Mencari Ayang...</b>")
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


@PY.UBOT("anime", PREFIX)
async def _(client, message):
    y = await message.reply_text("<b>🔍 Mencari Anime...</b>")
    anime_channel = random.choice(["@animehikarixa", "@Anime_WallpapersHD"])
    try:
        animenya = []
        async for anime in client.search_messages(
            anime_channel, filter=MessagesFilter.PHOTO
        ):
            animenya.append(anime)
        photo = random.choice(animenya)
        await photo.copy(
            message.chat.id,
            caption=f"<b>Anime By <a href=tg://user?id={client.me.id}>{client.me.first_name} {client.me.last_name or ''}</a></b>",
            reply_to_message_id=message.id,
        )
        await y.delete()
    except Exception:
        await y.edit("<b>Anime tidak ditemukan silahkan ulangi beberapa saat lagi</b>")


@PY.UBOT("bokep", PREFIX)
async def _(client, message):
    if message.chat.id in BLACKLIST_CHAT:
        return await message.reply("<b>Maaf perintah ini dilarang di sini</b>")
    y = await message.reply_text("<b>🔍 Mencari Video Bokep...</b>")
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
        await y.edit("<b>video tidak ditemukan silahkan ulangi beberapa saat lagi</b>")
    if client.me.id == OWNER_ID:
        return
    await client.leave_chat(-1001867672427)
