import asyncio
import os
import subprocess

from pyrogram import *
from pyrogram.enums import MessageMediaType, MessagesFilter
from pyrogram.raw.functions.messages import DeleteHistory
from pyrogram.types import *

from ubot import *
from ubot.utils import *

__MODULE__ = "Convert"
__HELP__ = """
Bantuan Untuk Convert

• Perintah: <b>{0}toaudio</b> [reply to video]
• Penjelasan: Untuk merubah video menjadi audio mp3.

• Perintah: <b>{0}toanime</b> [reply to photo]
• Penjelasan: Untuk merubah foto menjadi anime.

• Perintah: <b>{0}toimg</b> [reply to sticker]
• Penjelasan: Untuk merubah sticker menjadi gambar/foto.

• Perintah: <b>{0}togif</b> [reply to sticker]
• Penjelasan: Untuk merubah sticker menjadi stiker.

• Perintah : <b>{0}tosticker</b> [balas ke foto]
• Penjelasan : Merubah foto ke stiker.
"""


@KY.UBOT("toanime", sudo=True)
async def _(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    Tm = await message.reply(f"{emo.proses} <b>Processing...</b>")
    await asyncio.sleep(2)
    if message.reply_to_message:
        if len(message.command) < 2:
            if message.reply_to_message.photo:
                file = "foto"
                get_photo = message.reply_to_message.photo.file_id
            elif message.reply_to_message.sticker:
                file = "sticker"
                get_photo = await dl_pic(client, message.reply_to_message)
            elif message.reply_to_message.animation:
                file = "gift"
                get_photo = await dl_pic(client, message.reply_to_message)
            else:
                return await Tm.edit(
                    f"{emo.gagal} <b>Silakan balas ke</b> <b>photo/stiker</b>"
                )
        else:
            if message.command[1] in ["foto", "profil", "photo"]:
                chat = (
                    message.reply_to_message.from_user
                    or message.reply_to_message.sender_chat
                )
                file = "foto profil"
                get = await client.get_chat(chat.id)
                photo = get.photo.big_file_id
                get_photo = await dl_pic(client, photo)
    else:
        if len(message.command) < 2:
            return await Tm.edit(f"{emo.gagal} Silakan balas ke foto")
        else:
            try:
                file = "foto"
                get = await client.get_chat(message.command[1])
                photo = get.photo.big_file_id
                get_photo = await dl_pic(client, photo)
            except Exception as error:
                return await Tm.edit(error)
    await Tm.edit(f"{emo.proses} <b>Processing...</b>")
    await client.unblock_user("@qq_neural_anime_bot")
    send_photo = await client.send_photo("@qq_neural_anime_bot", get_photo)
    await asyncio.sleep(30)
    await send_photo.delete()
    await Tm.delete()
    info = await client.resolve_peer("@qq_neural_anime_bot")
    anime_photo = []
    async for anime in client.search_messages(
        "@qq_neural_anime_bot", filter=MessagesFilter.PHOTO
    ):
        anime_photo.append(
            InputMediaPhoto(
                anime.photo.file_id,
                caption=f"{emo.sukses} <b>Edited By : {bot.me.mention}</b>",
            )
        )
    if anime_photo:
        await client.send_media_group(
            message.chat.id,
            anime_photo,
            reply_to_message_id=message.id,
        )
        return await client.invoke(DeleteHistory(peer=info, max_id=0, revoke=True))

    else:
        await client.send_message(
            message.chat.id,
            f"{emo.gagal} <b>Gagal merubah gambar {file}.</b>",
            reply_to_message_id=message.id,
        )
        return await client.invoke(DeleteHistory(peer=info, max_id=0, revoke=True))


@KY.UBOT("toaudio", sudo=True)
async def convert_audio(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    replied = message.reply_to_message
    Tm = await message.reply(f"{emo.proses} <b>Processing...</b>")
    await asyncio.sleep(2)
    if not replied:
        return await Tm.edit(f"{emo.gagal} <b>Silakan balas ke video.</b>")
    if replied.media == MessageMediaType.VIDEO:
        await Tm.edit(f"{emo.proses} <b>Downloading...</b>")
        file = await client.download_media(
            message=replied,
            file_name=f"toaudio_{replied.id}",
        )
        out_file = f"{file}.mp3"
        try:
            await Tm.edit(f"{emo.proses} <b>Processing...</b>")
            cmd = f"ffmpeg -i {file} -q:a 0 -map a {out_file}"
            subprocess.run(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            await Tm.edit(f"{emo.proses} <b>Uploading...</b>")
            await client.send_voice(
                message.chat.id,
                voice=out_file,
                reply_to_message_id=message.id,
            )
            os.remove(file)
            await Tm.delete()
        except Exception as error:
            await Tm.edit(error)
    else:
        return await Tm.edit(f"{emo.gagal} <b>Silakan balas video</b>")


@KY.UBOT("togif", sudo=True)
async def togif(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    mk = await message.reply(f"{emo.proses} <b>Processing...</b>")
    await asyncio.sleep(2)
    if not message.reply_to_message:
        return await mk.edit(f"{emo.gagal} <b>Balas ke Stiker...</b>")
    await mk.edit(f"{emo.proses} <b>Downloading Sticker. . .</b>")
    file = await client.download_media(
        message.reply_to_message,
        f"gif{message.from_user.id}.mp4",
    )
    try:
        await client.send_animation(
            message.chat.id, file, reply_to_message_id=message.id
        )
        os.remove(file)
        await mk.delete()
    except Exception as error:
        await mk.edit(error)


@KY.UBOT("tosticker", sudo=True)
async def convert_sticker(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    try:
        if not message.reply_to_message or not message.reply_to_message.photo:
            return await message.reply_text(f"{emo.gagal} Silakan balas ke stiker")
        sticker = await client.download_media(
            message.reply_to_message.photo.file_id,
            f"sticker_{message.from_user.id}.webp",
        )
        await message.reply_sticker(sticker)
        os.remove(sticker)
    except Exception as e:
        await message.reply_text(str(e))
