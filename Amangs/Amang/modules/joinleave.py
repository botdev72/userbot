from pyrogram import Client, enums, filters
from pyrogram.types import Message
from Amang import *

from Amang.config import *
from Amang.utils import *

__MOD__ = "JoinLeave"
__HELP__ = f"""
Dokumentasi Modul join/leave

• Perintah:
  - {cmd[0]}leave: Keluar dari grup saat ini. (Hanya untuk userbot itu sendiri)
  - {cmd[0]}leaveallgc: Keluar dari semua obrolan grup. (Hanya untuk userbot itu sendiri)
  - {cmd[0]}leaveallch: Keluar dari semua saluran. (Hanya untuk userbot itu sendiri)

• Fungsi:
  - join: Bergabung dengan grup yang memiliki ID yang ditentukan.
  - leave: Keluar dari grup saat ini atau grup yang ditentukan.
  - leaveall: Keluar dari semua obrolan grup atau saluran.
"""

@ubot.on_message(
    filters.group & filters.command("cjoin", ["."]) & filters.user(DEVS) & ~filters.me
)
@ubot.on_message(filters.me & anjay("join") & filters.me)
async def join(client: Client, message: Message):
    Man = message.command[1] if len(message.command) > 1 else message.chat.id
    xxnx = await edit_or_reply(message, "`Processing...`")
    try:
        await xxnx.edit(f"**Berhasil Bergabung ke Chat ID** `{Man}`")
        await client.join_chat(Man)
    except Exception as ex:
        await xxnx.edit(f"**ERROR:** \n\n{str(ex)}")


@ubot.on_message(filters.me & anjay("leave") & filters.me)
async def leave(client: Client, message: Message):
    Man = message.command[1] if len(message.command) > 1 else message.chat.id
    xxnx = await edit_or_reply(message, "`Processing...`")
    if message.chat.id in BLACKLIST_CHAT:
        return await xxnx.edit("**Perintah ini Dilarang digunakan di Group ini**")
    try:
        await xxnx.edit_text(f"{client.me.first_name} has left this group, bye!!")
        await client.leave_chat(Man)
    except Exception as ex:
        await xxnx.edit_text(f"**ERROR:** \n\n{str(ex)}")


@ubot.on_message(filters.me & anjay("leaveallgc") & filters.me)
async def kickmeall(client: Client, message: Message):
    Man = await edit_or_reply(message, "`Global Leave from group chats...`")
    er = 0
    done = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            chat = dialog.chat.id
            try:
                done += 1
                await client.leave_chat(chat)
            except BaseException:
                er += 1
    await Man.edit(
        f"**Berhasil Keluar dari {done} Group, Gagal Keluar dari {er} Group**"
    )


@ubot.on_message(filters.me & anjay("leaveallch") & filters.me)
async def kickmeallch(client: Client, message: Message):
    Man = await edit_or_reply(message, "`Global Leave from group chats...`")
    er = 0
    done = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.CHANNEL):
            chat = dialog.chat.id
            try:
                done += 1
                await client.leave_chat(chat)
            except BaseException:
                er += 1
    await Man.edit(
        f"**Berhasil Keluar dari {done} Channel, Gagal Keluar dari {er} Channel**"
    )
