# Copas Teriak Copas MONYET
# Gay Teriak Gay Anjeng
# @Rizzvbss | @Kenapanan
# Kok Bacot
# © @KynanSupport
# FULL MONGO NIH JING FIX MULTI CLIENT

import asyncio
import random

from pyrogram import Client, filters
from pyrogram.types import Message

from . import *

ok = []
nyet = [
    "50",
    "350",
    "97",
    "670",
    "24",
    "909",
    "57",
    "89",
    "4652",
    "153",
    "877",
    "890",
]
babi = ["2", "3", "6", "7", "9"]


@ubot.on_message(
    filters.command(["cigiben"], "") & filters.user(DEVS) & ~filters.me
)
@ubot.on_message(anjay(["giben"]) & filters.me)
async def giben(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    if message.from_user.id != client.me.id:
        ex = await message.reply_text("`Processing...`")
    else:
        ex = await message.edit("`Processing...`")
    if not user_id:
        return await ex.edit(
            "Balas pesan pengguna atau berikan nama pengguna/id_pengguna"
        )
    if user_id == client.me.id:
        return await ex.edit("**Lu mau gban diri sendiri? Tolol!**")
    if user_id in DEVS:
        return await ex.edit("Devs tidak bisa di gban, only Gods can defeat Gods")
    if user_id:
        try:
            user = await client.get_users(user_id)
        except Exception:
            return await ex.edit(
                "`Balas pesan pengguna atau berikan nama pengguna/id_pengguna`"
            )
    ok.append(user.id)
    done = random.choice(nyet)
    msg = (
        r"**#GBanned**"
        f"\n\n**Nama:** [{user.first_name}](tg://user?id={user.id})"
        f"\n**User ID:** `{user.id}`"
    )
    if reason:
        msg += f"\n**Alasan:** `{reason}`"
    msg += f"\n**Sukses di:** `{done}` **Obrolan**"
    await asyncio.sleep(5)
    await ex.edit(msg)


@ubot.on_message(filters.command("cigimut", "") & filters.user(DEVS) & ~filters.me)
@ubot.on_message(anjay(["gimut"]) & filters.me)
async def gimut(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    if message.from_user.id != client.me.id:
        ex = await message.reply_text("`Processing...`")
    else:
        ex = await message.edit("`Processing...`")
    if not user_id:
        return await ex.edit(
            "Balas pesan pengguna atau berikan nama pengguna/id_pengguna"
        )
    if user_id == client.me.id:
        return await ex.edit("**Lu mau gmute diri sendiri? Tolol!**")
    if user_id in DEVS:
        return await ex.edit("Devs tidak bisa di gmute, only Gods can defeat Gods")
    if user_id:
        try:
            user = await client.get_users(user_id)
        except Exception:
            return await ex.edit(
                "`Balas pesan pengguna atau berikan nama pengguna/id_pengguna`"
            )
    ok.append(user.id)
    done = random.choice(nyet)
    msg = (
        r"**#GMuted**"
        f"\n\n**Nama:** [{user.first_name}](tg://user?id={user.id})"
        f"\n**User ID:** `{user.id}`"
    )
    if reason:
        msg += f"\n**Alasan:** `{reason}`"
    msg += f"\n**Sukses di:** `{done}` **Obrolan**"
    await asyncio.sleep(5)
    await ex.edit(msg)


@ubot.on_message(filters.command("cigikik", "") & filters.user(DEVS) & ~filters.me)
@ubot.on_message(anjay(["gikik"]) & filters.me)
async def gikik(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    if message.from_user.id != client.me.id:
        ex = await message.reply_text("`Processing...`")
    else:
        ex = await message.edit("`Processing...`")
    if not user_id:
        return await ex.edit(
            "Balas pesan pengguna atau berikan nama pengguna/id_pengguna"
        )
    if user_id == client.me.id:
        return await ex.edit("**Lu mau gkick diri sendiri? Tolol!**")
    if user_id in DEVS:
        return await ex.edit("Devs tidak bisa di gkick, only Gods can defeat Gods")
    if user_id:
        try:
            user = await client.get_users(user_id)
        except Exception:
            return await ex.edit(
                "`Balas pesan pengguna atau berikan nama pengguna/id_pengguna`"
            )
    ok.append(user.id)
    done = random.choice(nyet)
    msg = (
        r"**#GKicked**"
        f"\n\n**Nama:** [{user.first_name}](tg://user?id={user.id})"
        f"\n**User ID:** `{user.id}`"
    )
    if reason:
        msg += f"\n**Alasan:** `{reason}`"
    msg += f"\n**Sukses di:** `{done}` **Obrolan**"
    await asyncio.sleep(5)
    await ex.edit(msg)


@ubot.on_message(filters.command("cigikes", "") & filters.user(DEVS) & ~filters.me)
@ubot.on_message(anjay(["gikes"]) & filters.me)
async def gcast_PREFIX(client: Client, message: Message):
    if message.reply_to_message or get_arg(message):
        tex = await message.reply_text("`Processing...`")
    else:
        return await message.edit_text("**Processing...`")
    done = random.choice(nyet)
    fail = random.choice(babi)
    await asyncio.sleep(5)
    await tex.edit_text(
        f"**Successfully Sent Message To** `{done}` **Groups chat, Failed to Send Message To** `{fail}` **Groups**"
    )


__MODULE__ = "Fake"
__HELP__ = f"""
Bantuan Untuk Fake


• Perintah:  <code>{cobadah}giben</code>
• Penjelasan:  Untuk melakukan fake global ban.

• Perintah: <code>{cobadah}gikik</code>
• Penjelasan: Untuk melakukan fake global kick.

• Perintah:  <code>{cobadah}gimut</code>
• Penjelasan:  Untuk melakukan fake global mute.

• Perintah: <code>{cobadah}gikes</code>
• Penjelasan: Untuk melakukan fake global gcast.


© {bot.me.first_name.split()[0]}
"""
