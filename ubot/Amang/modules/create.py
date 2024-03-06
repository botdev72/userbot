# Copas Teriak Copas MONYET
# Gay Teriak Gay Anjeng
# @Rizzvbss | @Kenapanan
# Kok Bacot
# © @KynanSupport
# FULL MONGO NIH JING FIX MULTI CLIENT

from pyrogram import Client, filters
from pyrogram.types import Message

from Amang import *
from Amang.utils import *

__MODULE__ = "create"
__HELP__ = f"""
 Document for Create

• Command: <code>{cmd[0]}buat</code> [gc atau ch]
• Function: Untuk membuat grup atau channel telegram.
"""


@ubot.on_message(filters.command(["buat"], cmd) & filters.me)
async def create(client: Client, message: Message):
    if len(message.command) < 3:
        return await eor(
            message,
            f"<code>buat gc</code> => Untuk Membuat Grup, <code>buat gc</code> => Untuk Mebuat Channel**",
        )
    group_type = message.command[1]
    split = message.command[2:]
    group_name = " ".join(split)
    xd = await eor(message, "<code>Processing...</code>")
    desc = "Welcome To My " + ("Group" if group_type == "gc" else "Channel")
    if group_type == "gc":  # for supergroup
        _id = await client.create_supergroup(group_name, desc)
        link = await client.get_chat(_id.id)
        await xd.edit(
            f"<b>Successfully Created Telegram Group: [{group_name}]({link.invite_link})</b>",
            disable_web_page_preview=True,
        )
    elif group_type == "ch":  # for channel
        _id = await client.create_channel(group_name, desc)
        link = await client.get_chat(_id.id)
        await xd.edit(
            f"<b>Successfully Created Telegram Channel: [{group_name}]({link.invite_link})</b>",
            disable_web_page_preview=True,
        )
