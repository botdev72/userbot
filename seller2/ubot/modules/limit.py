from asyncio import sleep

from pyrogram.raw.functions.messages import DeleteHistory, StartBot

from ubot import *
from ubot.utils import *


@KY.UBOT("limit")
async def _(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    x = await client.get_me()
    await client.unblock_user("SpamBot")
    bot_info = await client.resolve_peer("SpamBot")
    msg = await message.reply(f"{emo.proses} <b>Processing...</b>")
    response = await client.invoke(
        StartBot(
            bot=bot_info,
            peer=bot_info,
            random_id=client.rnd_id(),
            start_param="start",
        )
    )
    await sleep(1)
    status = await client.get_messages("SpamBot", response.updates[1].message.id + 1)
    result = status.text
    emoji = None
    if "Good news" in result or "Kabar baik" in result:
        emoji = f"{emo.sukses}"
    if "I'm afraid" in result or "Saya khawatir" in result:
        emoji = f"{emo.gagal}"
    await msg.edit(f"{emoji} **{status.text}**\n\n ~ {emo.anu} **{x.first_name}**")

    return await client.invoke(DeleteHistory(peer=bot_info, max_id=0, revoke=True))


__MODULE__ = "Limit"
__HELP__ = """
Bantuan Untuk Limit

• Perintah: <code>{0}limit</code>
• Penjelasan: Untuk mengecek akun anda terbatas atau tidak.
"""
