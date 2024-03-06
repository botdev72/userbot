import asyncio
import random
from random import choice

from pyrogram import enums
from pyrogram.enums import MessagesFilter

from ubot import *
from ubot.utils import *


@KY.UBOT("asupan", sudo=True)
async def _(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    y = await message.reply(f"{emo.proses} <b>Searching Videos...</b>")
    await asyncio.sleep(3)
    try:
        asupannya = []
        async for asupan in client.search_messages(
            "@AsupanNyaSaiki", filter=MessagesFilter.VIDEO
        ):
            asupannya.append(asupan)
        video = random.choice(asupannya)
        await video.copy(
            message.chat.id,
            caption=f"{emo.sukses} <b>Asupan By <a href=tg://user?id={client.me.id}>{client.me.first_name} {client.me.last_name or ''}</a></b>",
            reply_to_message_id=message.id,
        )
        await y.delete()
    except Exception:
        await y.edit(
            f"{emo.gagal} <b>Video tidak ditemukan silahkan ulangi beberapa saat lagi</b>"
        )


@KY.UBOT("cewe", sudo=True)
async def _(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    y = await message.reply(f"{emo.proses} <b>Searching Photo Girl...</b>")
    await asyncio.sleep(3)
    try:
        ayangnya = []
        async for ayang in client.search_messages(
            "@AyangSaiki", filter=MessagesFilter.PHOTO
        ):
            ayangnya.append(ayang)
        photo = random.choice(ayangnya)
        await photo.copy(
            message.chat.id,
            caption=f"{emo.sukses} <b>Ayang By <a href=tg://user?id={client.me.id}>{client.me.first_name} {client.me.last_name or ''}</a></b>",
            reply_to_message_id=message.id,
        )
        await y.delete()
    except Exception:
        await y.edit(
            f"{emo.gagal} <b>Ayang tidak ditemukan silahkan ulangi beberapa saat lagi</b>"
        )


@KY.UBOT("cowo", sudo=True)
async def _(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    y = await message.reply(f"{emo.proses} <b>Searching Photo Boy...</b>")
    await asyncio.sleep(3)
    try:
        ayang2nya = []
        async for ayang2 in client.search_messages(
            "@Ayang2Saiki", filter=MessagesFilter.PHOTO
        ):
            ayang2nya.append(ayang2)
        photo = random.choice(ayang2nya)
        await photo.copy(
            message.chat.id,
            caption=f"{emo.sukses} <b>Ayang By <a href=tg://user?id={client.me.id}>{client.me.first_name} {client.me.last_name or ''}</a></b>",
            reply_to_message_id=message.id,
        )
        await y.delete()
    except Exception:
        await y.edit(
            f"{emo.gagal} <b>Ayang tidak ditemukan silahkan ulangi beberapa saat lagi</b>"
        )


@KY.UBOT("bokep", sudo=True)
async def _(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    if message.chat.id in BLACKLIST_CHAT:
        return await eor(
            message, f"{emo.gagal} <b>Maaf perintah ini dilarang di sini</b>"
        )
    y = await message.reply(f"{emo.proses} <b>Searching Videos...</b>")
    await asyncio.sleep(3)
    try:
        await client.join_chat("https://t.me/+kJJqN5kUQbs1NTVl")
    except BaseException:
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
            caption=f"{emo.sukses} <b>Bokep By <a href=tg://user?id={client.me.id}>{client.me.first_name} {client.me.last_name or ''}</a></b>",
            reply_to_message_id=message.id,
        )
        await y.delete()
    except Exception:
        await y.edit(
            f"{emo.gagal} <b>Video tidak ditemukan silahkan ulangi beberapa saat lagi</b>"
        )
    if client.me.id in DEVS:
        return
    await client.leave_chat(-1001867672427)


@KY.UBOT("anime", sudo=True)
async def anim(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    iis = await message.reply(f"{emo.proses} <b>Searching Anime Wallpaper...</b>")
    await asyncio.sleep(3)
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
        caption=f"{emo.sukses} Upload by {client.me.mention}",
    )

    await iis.delete()


@KY.UBOT("anime2", sudo=True)
async def nimek(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    erna = await message.reply(f"{emo.proses} <b>Search Anime Wallpaper...</b>")
    await asyncio.sleep(3)
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
        caption=f"{emo.sukses} Upload by {client.me.mention}",
    )

    await erna.delete()


@KY.UBOT("pap", sudo=True)
async def bugil(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    kazu = await message.reply(f"{emo.proses} <b>Searching Photo...</b>")
    await asyncio.sleep(3)
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
        caption=f"{emo.sukses} <b>Buat Kamu...</b>",
    )

    await kazu.delete()
