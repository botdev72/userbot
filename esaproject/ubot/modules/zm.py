from pyrogram import filters

from . import bot, ubot, anjay, cobadah, eor
from ubot.utils import *

__MODULE__ = "Zombies"
__HELP__ = """
Bantuan Untuk Zombies

• Perintah: <code>{0}zombie</code>
• Penjelasan: Untuk mengeluarkan akun depresi digrup anda.
"""


@ubot.on_message(anjay("zombie") & filters.me)
async def _(client, message):
    chat_id = message.chat.id
    deleted_users = []
    banned_users = 0
    m = await message.edit(
        "<code>Sedang mencari akun-akun depresi ditinggal kawin...</code>"
    )

    async for i in client.get_chat_members(chat_id):
        if i.user.is_deleted:
            deleted_users.append(i.user.id)
    if len(deleted_users) > 0:
        for deleted_user in deleted_users:
            try:
                await message.chat.ban_member(deleted_user)
            except Exception:
                pass
            banned_users += 1
        await m.edit(
            f"<b>Berhasil mengkawinkan {banned_users} Akun Depresi Ditinggal Kawin.</b>"
        )
    else:
        await m.edit("<b>Saya tidak menemukan akun depresi di tinggal kawin.</b>")
