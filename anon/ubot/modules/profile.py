# Copas Teriak Copas MONYET
# Gay Teriak Gay Anjeng
# @Rizzvbss | @Kenapanan
# Kok Bacot
# © @KynanSupport
# FULL MONGO NIH JING FIX MULTI CLIENT

import os
from asyncio import sleep
from io import BytesIO

from pyrogram import *
from pyrogram.enums import *
from pyrogram.types import *

from ubot import *
from ubot.config import *
from ubot.utils.utils import *

__MODULE__ = "Profile"
__HELP__ = """
Bantuan Untuk Profile

• Perintah: <code>{0}setgpic</code> [balas media]
• Penjelasan: Untuk mengubah foto grup.

• Perintah: <code>{0}adminlist</code>
• Penjelasan: Untuk melihat status admin grup anda.

• Perintah: <code>{0}setbio</code> [query]
• Penjelasan: Untuk mengubah bio Anda.

• Perintah: <code>{0}setname</code> [query]
• Penjelasan: Untuk mengubah Nama Anda.

• Perintah: <code>{0}setpp</code> [balas media]
• Penjelasan: Untuk mengubah Foto Akun Anda.

• Perintah: <code>{0}block</code> [balas pengguna]
• Penjelasan: Untuk blokir pengguna.

• Perintah: <code>{0}unblock</code> [query]
• Penjelasan: Untuk buka blokir pengguna.
"""


@KY.UBOT("adminlist")
async def list_admin(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    bacot = await message.reply(f"{emo.proses} **Processing...**")
    await sleep(2)
    a_chats = []
    me = await client.get_me()
    async for dialog in client.get_dialogs(limit=None):
        if dialog.chat.type == enums.ChatType.SUPERGROUP:
            gua = await dialog.chat.get_member(int(me.id))
            if gua.status in (
                enums.ChatMemberStatus.OWNER,
                enums.ChatMemberStatus.ADMINISTRATOR,
            ):
                a_chats.append(dialog.chat)

    text = ""
    j = 0
    for chat in a_chats:
        try:
            title = chat.title
        except Exception:
            title = "Private Group"
        if chat.username:
            text += f"<b>{j + 1}.</b>  [{title}](https://t.me/{chat.username})[`{chat.id}`]\n"
        else:
            text += f"<b>{j + 1}. {title}</b> [`{chat.id}`]\n"
        j += 1

    if not text:
        await bacot.edit_text(
            f"{emo.gagal} **Kamu tidak menjadi admin di grup manapun.**"
        )
    elif len(text) > 4096:
        with BytesIO(str.encode(text)) as out_file:
            out_file.name = "adminlist.text"
            await message.reply_document(
                document=out_file,
                disable_notification=True,
                quote=True,
            )
            await bacot.delete()
    else:
        await bacot.edit_text(
            f"**Kamu admin di `{len(a_chats)}` group:\n\n{text}**",
            disable_web_page_preview=True,
        )


@KY.UBOT("unblock")
async def unblock_user_func(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    user_id = await extract_user(message)
    tex = await message.reply(f"{emo.proses} <b>Processing...</b>")
    await sleep(2)
    if not user_id:
        return await tex.edit(
            f"{emo.gagal} **Berikan username atau reply pesan untuk membuka blokir.**"
        )
    if user_id == client.me.id:
        return await tex.edit(f"{emo.sukses} **Ok done .**")
    await client.unblock_user(user_id)
    umention = (await client.get_users(user_id)).mention
    await message.reply(f"{emo.sukses} <b>Berhasil membuka blokir</b> {umention}")


@KY.UBOT("block")
async def block_user_func(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    user_id = await extract_user(message)
    tex = await message.reply(f"{emo.proses} <b>Processing...</b>")
    await sleep(2)
    if not user_id:
        return await tex.edit(f"{emo.gagal} **Berikan username untuk di blok.**")
    if user_id == client.me.id:
        return await tex.edit(f"{emo.sukses} **Ok .**")
    await client.block_user(user_id)
    umention = (await client.get_users(user_id)).mention
    await tex.edit(f"{emo.sukses} <b>Berhasil Blokir</b> {umention}.")


@KY.UBOT("setname")
async def setname(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    tex = await message.reply(f"{emo.proses} <b>Processing...</b>")
    await sleep(2)
    if len(message.command) == 1:
        return await tex.edit(
            f"{emo.gagal} **Berikan text untuk diatur sebagai nama anda.**"
        )
    elif len(message.command) > 1:
        name = message.text.split(None, 1)[1]
        try:
            await client.update_profile(first_name=name)
            await tex.edit(
                f"{emo.sukses} <b>Berhasil mengganti nama menjadi</b> <code>{name}</code>"
            )
        except Exception as e:
            await tex.edit(f"{emo.gagal} <b>ERROR:</b> <code>{e}</code>")
    else:
        return await tex.edit(
            f"{emo.gagal} **Berikan text untuk diatur sebagai nama anda.**"
        )


@KY.UBOT("setbio")
async def set_bio(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    tex = await message.reply(f"{emo.proses} <b>Processing...</b>")
    await sleep(2)
    if len(message.command) == 1:
        return await tex.edit(f"{emo.gagal} **Berikan text untuk diatur sebagai bio.**")
    elif len(message.command) > 1:
        bio = message.text.split(None, 1)[1]
        try:
            await client.update_profile(bio=bio)
            await tex.edit(
                f"{emo.sukses} <b>Berhasil mengganti bio menjadi</b> <code>{bio}</code>"
            )
        except Exception as e:
            await tex.edit(f"<b>ERROR:</b> <code>{e}</code>")
    else:
        return await tex.edit(f"{emo.gagal} **Berikan text untuk diatur sebagai bio.**")


@KY.UBOT("setpp")
async def set_pfp(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    po = "ubot/resources/blank.png"
    xx = await message.reply(f"{emo.proses} **Processing...**")
    await sleep(1)
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
        await xx.delete()
        await sleep(1)
        await message.reply(f"{emo.sukses} **Foto Profil anda Berhasil Diubah.**")
    else:
        await xx.edit(
            f"{emo.gagal} **Balas ke foto apa pun untuk dipasang sebagai foto profile**"
        )
        await sleep(3)
        await message.delete()
