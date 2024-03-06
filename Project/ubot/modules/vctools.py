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

from pyrogram import Client, enums
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.raw.types import InputGroupCall, InputPeerChannel, InputPeerChat
from pyrogram.types import Message

from ubot import *
from ubot.utils import *

daftar_join = []

turun_dewek = False


__MODULE__ = "VoiceChat"
__HELP__ = """
Bantuan Untuk Voice Chat

• Perintah: <code>{0}startvc</code>
• Penjelasan: Untuk memulai voice chat grup.

• Perintah: <code>{0}stopvc</code>
• Penjelasan: Untuk mengakhiri voice chat grup.

• Perintah: <code>{0}leavevc</code>
• Penjelasan: Untuk meninggalkan voice chat grup.

• Perintah: <code>{0}joinvc</code>
• Penjelasan: Untuk bergabung voice chat grup.
"""


async def get_group_call(
    client: Client, message: Message, err_msg: str = ""
) -> Optional[InputGroupCall]:
    emo = Emo(client.me.id)
    await emo.initialize()
    chat_peer = await client.resolve_peer(message.chat.id)
    if isinstance(chat_peer, (InputPeerChannel, InputPeerChat)):
        if isinstance(chat_peer, InputPeerChannel):
            full_chat = (
                await client.invoke(GetFullChannel(channel=chat_peer))
            ).full_chat
        elif isinstance(chat_peer, InputPeerChat):
            full_chat = (
                await client.invoke(GetFullChat(chat_id=chat_peer.chat_id))
            ).full_chat
        if full_chat is not None:
            return full_chat.call
    await message.reply(f"{emo.gagal} **No group call Found** {err_msg}")
    return False


@KY.UBOT("startvc", sudo=True)
async def opengc(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    flags = " ".join(message.command[1:])
    ky = await message.reply(f"{emo.proses} <b>Processing....</b>")
    await sleep(2)
    vctitle = get_arg(message)
    if flags == enums.ChatType.CHANNEL:
        chat_id = message.chat.title
    else:
        chat_id = message.chat.id
    args = f"{emo.sukses} <b>Obrolan Suara Aktif</b>\n <b>• Chat :</b> <code>{message.chat.title}</code>"
    try:
        if not vctitle:
            await client.invoke(
                CreateGroupCall(
                    peer=(await client.resolve_peer(chat_id)),
                    random_id=randint(10000, 999999999),
                )
            )
        else:
            args += f"\n<b>• Title :</b> <code>{vctitle}</code>"
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


@KY.UBOT("stopvc", sudo=True)
async def end_vc_(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    ky = await message.reply(f"{emo.proses} <b>Processing....</b>")
    message.chat.id
    if not (
        group_call := (await get_group_call(client, message, err_msg=", Kesalahan..."))
    ):
        return
    await client.invoke(DiscardGroupCall(call=group_call))
    await ky.edit(
        f"{emo.sukses} <b>Obrolan Suara Diakhiri</b>\n<b>• Chat :</b> <code>{message.chat.title}</code>"
    )


@KY.UBOT("joinvc", sudo=True)
@cek_offi
async def joinvc(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    for x in ubot._ubot:
        x.me.id
    ky = await message.reply(f"{emo.proses} <b>Processing....</b>")
    chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
    with suppress(ValueError):
        chat_id = int(chat_id)
    naek = await client.kntl.start(chat_id)
    if naek:
        await ky.edit("**Akun anda sudah berada diatas !!**")
    else:
        try:
            await client.kntl.start(chat_id)
        except Exception as e:
            return await ky.edit(f"ERROR: {e}")
        await ky.edit(
            f"{emo.sukses} <b>Berhasil Join Voice Chat</b>\n<b>• Chat :</b> <code>{message.chat.title}</code>"
        )
        await sleep(1)
        await client.kntl.set_is_mute(True)


@KY.UBOT("leavevc", sudo=True)
@cek_offi
async def leavevc(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    for x in ubot._ubot:
        x.me.id
    ky = await message.reply(f"{emo.proses} <b>Processing....</b>")
    chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
    with suppress(ValueError):
        chat_id = int(chat_id)
    turun = await client.kntl.stop()
    if turun:
        await ky.edit("**Anda sedang tidak berada di dalam obrolan suara manapun.**")
    else:
        try:
            await client.kntl.stop()
        except Exception as e:
            return await ky.edit(f"<b>ERROR:</b> {e}")
        msg = f"{emo.sukses} <b>Berhasil Meninggalkan Voice Chat</b>\n"
        if chat_id:
            msg += f"• <b>Chat : </b><code>{message.chat.title}</code>"
        await ky.edit(msg)


@KY.UBOT("listos", sudo=True)
async def liat_os(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    ky = await message.reply(f"{emo.proses} **Processing...**")
    for y in ubot._ubot:
        msg = f"{emo.sukses} <b>Total Naik Os {len(await get_osnya(y.me.id))}</b>\n\n"
    for x in await get_osnya(y.me.id):
        try:
            get = await y.get_chat(x)
            msg += f"<b>• {y.me.id} Os Di {get.title} | <code>{get.id}</code></b>\n"
        except:
            msg += f"<b>• <code>{x}</code></b>\n"
    await ky.delete()
    await message.reply(msg)
