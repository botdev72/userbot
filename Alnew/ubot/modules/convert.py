import asyncio
import os
import shutil

from py_extract import Video_tools
from pyrogram import enums, filters
from pyrogram.raw.functions.messages import DeleteHistory
from pyrogram.types import *

from ubot import *
from ubot.utils import *


__MODULE__ = "Convert"
__HELP__ = """
Bantuan Untuk Convert

• Perintah: <code>{0}toaudio</code> [reply to video]
• Penjelasan: Untuk merubah video menjadi audio mp3.

• Perintah: <code>{0}toanime</code> [reply to photo]
• Penjelasan: Untuk merubah foto menjadi anime.

• Perintah: <code>{0}mtoi</code> [reply to sticker]
• Penjelasan: Untuk merubah sticker menjadi gambar/foto.

• Perintah: <code>{0}togif</code> [reply to sticker]
• Penjelasan: Untuk merubah sticker menjadi stiker.
"""


@ubot.on_message(filters.me & anjay("toanime"))
async def _(client, message):
    if not message.reply_to_message:
        return await message.reply("`Mohon Balas Ke Foto`")
    bot = "qq_neural_anime_bot"
    if message.reply_to_message:
        cot = await message.reply("`Processing...`")
        await client.unblock_user(bot)
        ba = await message.reply_to_message.copy(bot)
        await asyncio.sleep(30)
        await ba.delete()
        await cot.delete()
        get_photo = []
        async for Toanime in client.search_messages(
            bot, filter=enums.MessagesFilter.PHOTO
        ):
            get_photo.append(InputMediaPhoto(Toanime.photo.file_id))
        await client.send_media_group(
            message.chat.id,
            media=get_photo,
            reply_to_message_id=message.id,
        )
        user_info = await client.resolve_peer(bot)
        return await client.invoke(DeleteHistory(peer=user_info, max_id=0, revoke=True))


@ubot.on_message(filters.me & anjay("toaudio"))
async def extract_all_aud(client, message):
    replied_msg = message.reply_to_message
    ajg = await message.reply("`Downloading Video . . .`")
    ext_out_path = os.getcwd() + "/" + "ubot/resources/"
    if not replied_msg:
        await ajg.edit("`Mohon Balas Ke Video`")
        return
    if not replied_msg.video:
        await ajg.edit("`Mohon Balas Ke Video`")
        return
    if os.path.exists(ext_out_path):
        await ajg.edit("`Processing...`")
        return
    replied_video = replied_msg.video
    try:
        await ajg.edit("`Downloading...`")
        ext_video = await client.download_media(message=replied_video)
        await ajg.edit("`Converting...`")
        exted_aud = Video_tools.extract_all_audio(
            input_file=ext_video, output_path=ext_out_path
        )
        await ajg.edit("`Uploading...`")
        for nexa_aud in exted_aud:
            await message.reply_audio(
                audio=nexa_aud, caption=f"`Extracted by` {client.me.mention}"
            )
        await ajg.edit("`Extracting Finished!`")
        shutil.rmtree(ext_out_path)
    except Exception as e:
        await ajg.edit(f"**Error:** `{e}`")


@ubot.on_message(anjay("togif") & filters.me)
async def togif(client, message):
    mk = await message.reply("<code>Processing...</code>")
    if not message.reply_to_message:
        return await mk.edit("<code>Balas ke Stiker...</code>")
    await mk.edit("<code>Downloading Sticker. . .</code>")
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
