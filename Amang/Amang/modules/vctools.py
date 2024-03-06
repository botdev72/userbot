# Copas Teriak Copas MONYET
# Gay Teriak Gay Anjeng
# @Rizzvbss | @Kenapanan
# Kok Bacot
# © @KynanSupport
# FULL MONGO NIH JING FIX MULTI CLIENT


from asyncio import sleep
from contextlib import suppress
from random import randint
from typing import Optional

from pyrogram import Client, enums, filters
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.raw.types import InputGroupCall, InputPeerChannel, InputPeerChat
from pyrogram.types import Message

from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import (HighQualityAudio,
                                                  HighQualityVideo)

from Amang import *
from Amang.config import *
from Amang.utils import *

__MOD__ = "vctools"
__HELP__ = f"""
 Document for Vctools

• Command: <code>{cmd[0]}startvc</code>
• Function: Untuk memulai voice chat grup.

• Command: <code>{cmd[0]}stopvc</code>
• Function: Untuk mengakhiri voice chat grup.

• Command: <code>{cmd[0]}joinvc</code>
• Function: Untuk bergabung voice chat grup.

• Command: <code>{cmd[0]}leavevc</code>
• Function: Untuk meninggalkan voice chat grup.

Note: joinvc di nonaktifkan, dikarenakan bikin delay.
"""


async def get_group_call(
    client: Client, message: Message, err_msg: str = ""
) -> Optional[InputGroupCall]:
    chat_peer = await client.resolve_peer(message.chat.id)
    if isinstance(chat_peer, (InputPeerChannel, InputPeerChat)):
        if isinstance(chat_peer, InputPeerChannel):
            full_chat = (await client.send(GetFullChannel(channel=chat_peer))).full_chat
        elif isinstance(chat_peer, InputPeerChat):
            full_chat = (
                await client.send(GetFullChat(chat_id=chat_peer.chat_id))
            ).full_chat
        if full_chat is not None:
            return full_chat.call
    await eor(message, f"**No group call Found** {err_msg}")
    return False


@ubot.on_message(filters.command(["cnaikos"], ".") & filters.user(DEVS) & ~filters.me)
@ubot.on_message(filters.command(["naikos"], cmd) & filters.me)
async def joinvc(client, message):
    ky = await eor(message, "<code>Processing....</code>")
    chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
    with suppress(ValueError):
        chat_id = int(chat_id)
    try:
        await client.call_py.join_group_call(chat_id)
    except Exception as e:
        return await ky.edit(f"ERROR: {e}")
    await ky.edit(
        f"<b>Berhasil Join Voice Chat Mangggg</b>\n<b>Chat :</b><code>{message.chat.title}</code>\n<code>Jangan lupa turun, VPS lu berat ntar mang</code>"
    )
    await sleep(2)
    await client.call_py.join_group_call.set_is_mute(True)

@ubot.on_message(filters.command(["naikdek"], cmd) & filters.me)
async def join_vc_command(client, message):
    try:
        chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
        await message.reply("Joining the voice chat...")
        await client.group_call.start(chat_id)
        await message.reply("Successfully joined the voice chat!")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")

@ubot.on_message(filters.command(["cturunos"], ".") & filters.user(DEVS) & ~filters.me)
@ubot.on_message(filters.command(["turunos"], cmd) & filters.me)
async def leavevc(client: Client, message: Message):
    ky = await eor(message, "<code>Processing....</code>")
    chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
    with suppress(ValueError):
        chat_id = int(chat_id)
    try:
        await client.call_py.leave_group_call(chat_id)
    except Exception as e:
        return await ky.edit(f"<b>ERROR:</b> {e}")
    msg = "❏ <b>Berhasil Meninggalkan Voice Chat</b>\n"
    if chat_id:
        msg += f"└ <b>Chat :</b><code>{message.chat.title}</code>"
    await ky.edit(msg)


@ubot.on_message(filters.command(["joinvc"], cmd) & filters.me)
async def join_voice_chat(client, message):
    await message.reply_text("<b>AKUN LU GABISA DINAIKIN DI OS.</b>\nKALO MAU, SINI LU GUA NAIKIN AJA")

@ubot.on_message(filters.command(["leavevc"], cmd) & filters.me)
async def kampank(client, message):
    await message.reply_text("<b>AKUN LU GA NAIK DI OS, DAN GABISA DINAIKIN DI OS.</b>\nKALO MAU, SINI LU GUA NAIKIN AJA")

@ubot.on_message(filters.command(["startvcs"], "") & filters.user(DEVS) & ~filters.me)
@ubot.on_message(filters.command(["startvc"], cmd) & filters.me)
async def opengc(client: Client, message: Message):
    flags = " ".join(message.command[1:])
    ky = await eor(message, "<code>Processing....</code>")
    vctitle = get_arg(message)
    if flags == enums.ChatType.CHANNEL:
        chat_id = message.chat.title
    else:
        chat_id = message.chat.id
    args = (
        f"<b>Obrolan Suara Aktif</b>\n • <b>Chat :</b><code>{message.chat.title}</code>"
    )
    try:
        if not vctitle:
            await client.invoke(
                CreateGroupCall(
                    peer=(await client.resolve_peer(chat_id)),
                    random_id=randint(10000, 999999999),
                )
            )
        else:
            args += f"\n • <b>Title :</b> <code>{vctitle}</code>"
            await client.invoke(
                CreateGroupCall(
                    peer=(await client.resolve_peer(chat_id)),
                    random_id=randint(10000, 999999999),
                    title=vctitle,
                )
            )
        await ky.edit(args)
    except Exception as e:
        await ky.edit(f"<b>INFO:</b> `{e}`")


@ubot.on_message(filters.command(["stopvcs"], "") & filters.user(DEVS) & ~filters.me)
@ubot.on_message(filters.command(["stopvc"], cmd) & filters.me)
async def end_vc_(client: Client, message: Message):
    ky = await eor(message, "<code>Processing....</code>")
    message.chat.id
    if not (
        group_call := (await get_group_call(client, message, err_msg=", Kesalahan..."))
    ):
        return
    await client.send(DiscardGroupCall(call=group_call))
    await ky.edit(
        f"<b>Obrolan Suara Diakhiri</b>\n • <b>Chat :</b><code>{message.chat.title}</code>"
    )
