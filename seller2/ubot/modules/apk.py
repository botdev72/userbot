# Copas Teriak Copas MONYET
# Gay Teriak Gay Anjeng
# @Rizzvbss | @Kenapanan
# Kok Bacot
# © @KynanSupport
# FULL MONGO NIH JING FIX MULTI CLIENT

from datetime import datetime
from asyncio import sleep
from pyrogram import *
from pyrogram.types import *

from ubot import *
from ubot.utils import *

__MODULE__ = "Afk"
__HELP__ = """
Bantuan Untuk Afk

• Perintah: <code>{0}afk</code> [alasan]
• Penjelasan: Untuk mengaktifkan mode afk.
"""

afk_sanity_check: dict = {}
afkstr = """
• AFK Aktif\n\n Alasan {}
"""
onlinestr = """
• AFK Tidak Aktif\n\nAlasan {}
"""


async def is_afk_(f, client, message):
    user_id = client.me.id
    af_k_c = await check_afk(user_id)
    if af_k_c:
        return bool(True)
    else:
        return bool(False)


is_afk = filters.create(func=is_afk_, name="is_afk_")


@KY.UBOT("afk")
async def set_afk(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    if len(message.command) == 1:
        return await eor(
            message,
            f"<b>Gunakan format dengan berikan alasan</b>\n\n<b>Contoh</b> : <code>afk berak</code>",
        )
    user_id = client.me.id
    botlog = "me"
    pablo = await eor(message, "<code>Processing...</code>")
    msge = None
    msge = get_text(message)
    start_1 = datetime.now()
    afk_start = start_1.replace(microsecond=0)
    if msge:
        msg = f"{emo.sukses}<b>• Sedang AFK</b>.\n{emo.anu}<b>• Alasan</b> : <code>{msge}</code>"
        await client.send_message(botlog, afkstr.format(msge))
        await go_afk(user_id, afk_start, msge)
    else:
        msg = f"{emo.sukses}<b>• Sedang AFK</b>."
        await client.send_message(botlog, afkstr.format(msge))
        await go_afk(user_id, afk_start)
    await pablo.edit(msg)


@ubot.on_message(
    is_afk
    & (filters.mentioned | filters.private)
    & ~filters.me
    & ~filters.bot
    & filters.incoming
)
async def afk_er(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    user_id = client.me.id
    if not message:
        return
    if not message.from_user:
        return
    if message.from_user.id == user_id:
        return
    use_r = int(user_id)
    if use_r not in afk_sanity_check.keys():
        afk_sanity_check[use_r] = 1
    else:
        afk_sanity_check[use_r] += 1
    if afk_sanity_check[use_r] == 5:
        await message.reply_text(f"{emo.sukses} <b>• Sedang AFK</b>.")
        afk_sanity_check[use_r] += 1
        return
    if afk_sanity_check[use_r] > 5:
        return
    lol = await check_afk(user_id)
    reason = lol["reason"]
    if reason == "":
        reason = None
    back_alivee = datetime.now()
    afk_start = lol["time"]
    afk_end = back_alivee.replace(microsecond=0)
    total_afk_time = str((afk_end - afk_start))
    message_to_reply = (
        f"{emo.sukses}<b>• Sedang AFK</b>\n{emo.profil}<b>• Waktu</b> :<code>{total_afk_time}</code>\n{emo.anu}<b>• Alasan</b> : <code>{reason}</code>"
        if reason
        else f"{emo.sukses}<b>• Sedang AFK</b>\n{emo.profil}<b>• Waktu</b> :<code>{total_afk_time}</code>"
    )
    await message.reply(message_to_reply)


@ubot.on_message(filters.outgoing & filters.me & is_afk)
async def no_afke(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    user_id = client.me.id
    botlog = "me"
    lol = await check_afk(user_id)
    back_alivee = datetime.now()
    afk_start = lol["time"]
    afk_end = back_alivee.replace(microsecond=0)
    total_afk_time = str((afk_end - afk_start))
    kk = await message.reply(
        f"{emo.profil}<b>• Saya Kembali.</b>\n{emo.anu}<b>• AFK Selama</b> : <code>{total_afk_time}</code>"
    )
    await sleep(3)
    await kk.delete()
    await no_afk(user_id)
    await client.send_message(botlog, onlinestr.format(total_afk_time))
