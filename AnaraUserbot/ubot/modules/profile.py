# Copas Teriak Copas MONYET
# Gay Teriak Gay Anjeng
# @Rizzvbss | @Kenapanan
# Kok Bacot
# © @KynanSupport
# FULL MONGO NIH JING FIX MULTI CLIENT

import os
from asyncio import sleep

from pyrogram import Client, filters
from pyrogram.types import Message

from . import bot, ubot, anjay, cobadah
from ubot.config import *
from ubot.utils.utils import *

__MODULE__ = "Profile"
__HELP__ = f"""
Bantuan Untuk Profile


• Perintah: <code>{cobadah}setgpic</code> [balas media]
• Penjelasan: Untuk mengubah foto grup.

• Perintah: <code>{cobadah}setbio</code> [query]
• Penjelasan: Untuk mengubah bio Anda.

• Perintah: <code>{cobadah}setname</code> [query]
• Penjelasan: Untuk mengubah Nama Anda.

• Perintah: <code>{cobadah}setpp</code> [balas media]
• Penjelasan: Untuk mengubah Foto Akun Anda.

• Perintah: <code>{cobadah}block</code> [balas pengguna]
• Penjelasan: Untuk blokir pengguna.

• Perintah: <code>{cobadah}unblock</code> [query]
• Penjelasan: Untuk buka blokir pengguna.


© {bot.me.first_name.split()[0]}
"""


@ubot.on_message(anjay(["unblock"]) & filters.me)
async def unblock_user_func(client, message):
    user_id = await extract_user(message)
    tex = await eor(message, "<code>Processing . . .</code>")
    if not user_id:
        return await eor(
            message, "Berikan username atau reply pesan untuk membuka blokir."
        )
    if user_id == client.me.id:
        return await tex.edit("Ok done ✅.")
    await client.unblock_user(user_id)
    umention = (await client.get_users(user_id)).mention
    await eor(message, f"<b>Berhasil membuka blokir</b> {umention}")


@ubot.on_message(anjay(["block"]) & filters.me)
async def block_user_func(client, message):
    user_id = await extract_user(message)
    tex = await eor(message, "<code>Processing . . .</code>")
    if not user_id:
        return await eor(message, "Berikan username untuk di blok.")
    if user_id == client.me.id:
        return await tex.edit("Ok ✅.")
    await client.block_user(user_id)
    umention = (await client.get_users(user_id)).mention
    await tex.edit(f"<b>Berhasil MemBlokir</b> {umention}")


@ubot.on_message(anjay(["setname"]) & filters.me)
async def setname(client: Client, message: Message):
    tex = await eor(message, "<code>Processing . . .</code>")
    if len(message.command) == 1:
        return await tex.edit("Berikan text untuk diatur sebagai nama anda.")
    elif len(message.command) > 1:
        name = message.text.split(None, 1)[1]
        try:
            await client.update_profile(first_name=name)
            await tex.edit(
                f"<b>Berhasil mengganti nama menjadi</b> <code>{name}</code>"
            )
        except Exception as e:
            await tex.edit(f"<b>ERROR:</b> <code>{e}</code>")
    else:
        return await tex.edit("Berikan text untuk diatur sebagai nama anda.")


@ubot.on_message(anjay(["setbio"]) & filters.me)
async def set_bio(client: Client, message: Message):
    tex = await eor(message, "<code>Processing . . .</code>")
    if len(message.command) == 1:
        return await tex.edit("Berikan text untuk diatur sebagai bio.")
    elif len(message.command) > 1:
        bio = message.text.split(None, 1)[1]
        try:
            await client.update_profile(bio=bio)
            await tex.edit(f"<b>Berhasil mengganti bio menjadi</b> <code>{bio}</code>")
        except Exception as e:
            await tex.edit(f"<b>ERROR:</b> <code>{e}</code>")
    else:
        return await tex.edit("Berikan text untuk diatur sebagai bio.")


@ubot.on_message(anjay(["setpp"]) & filters.me)
async def set_pfp(client, message):
    po = "ubot/resources/blank.png"
    replied = message.reply_to_message
    if (
        replied
        and replied.media
        and (
            replied.photo
            or (replied.document and "image" in replied.document.mime_type)
        )
    ):
        await client.download_media(message=replied, file_name=po)
        await client.set_profile_photo(photo=po)
        if os.path.exists(po):
            os.remove(po)
        await message.edit("**Foto Profil anda Berhasil Diubah.**")
    else:
        await message.edit(
            "`Balas ke foto apa pun untuk dipasang sebagai foto profile`"
        )
        await sleep(3)
        await message.delete()