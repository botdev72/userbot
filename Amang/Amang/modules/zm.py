from pyrogram import filters

from Amang import *
from Amang.utils import *

__MOD__ = "zombie"
__HELP__ = f"""
 Document for Zombie

• Command: <code>{cmd[0]}zombies</code>
• Function: Ban Deleted Accounts.
"""


@ubot.on_message(filters.command("zombies", cmd) & filters.me)
async def _(client, message):
    chat_id = message.chat.id
    deleted_users = []
    banned_users = 0
    m = await eor(
        message, "<code>Finding ghosts...</code>"
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
            f"<b>Banned {banned_users} Deleted Accounts</b>"
        )
    else:
        await m.edit("<b>There are no deleted accounts in this chat.</b>")
