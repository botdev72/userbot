from asyncio import gather
from os import remove

from pyrogram import filters
from pyrogram.enums import ChatType

from Amang import *
from Amang.config import *
from Amang.utils import *

__MOD__ = "UserInfo"
__HELP__ = f"""
Document for Info

• Command: <code>{cmd[0]}info</code> [user_id/username/reply to users]
• Function: To get detailed information about a Telegram user.

• Command: <code>{cmd[0]}cinfo</code> [chat_id/username/reply to chat]
• Function: To get detailed information about a group/channel.

• Command: <code>{cmd[0]}id</code>
• Function: To get the ID of a user/group/channel.

• Command: <code>{cmd[0]}id</code> [reply to user/media]
• Function: To get the ID of a user/media.
"""


@ubot.on_message(filters.me & anjay("info"))
async def _(client, message):
    user_id = await extract_user(message)
    Tm = await message.reply_text("</b>Processing . . .</b>")
    if not user_id:
        return await Tm.edit(
            "<b>Provide a user id/username/reply to get the user's info.</b>"
        )
    try:
        user = await client.get_users(user_id)
        username = f"@{user.username}" if user.username else "-"
        first_name = f"{user.first_name}" if user.first_name else "-"
        last_name = f"{user.last_name}" if user.last_name else "-"
        fullname = (
            f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
        )
        user_details = (await client.get_chat(user.id)).bio
        bio = f"{user_details}" if user_details else "-"
        h = f"{user.status}"
        if h.startswith("UserStatus"):
            y = h.replace("UserStatus.", "")
            status = y.capitalize()
        else:
            status = "-"
        dc_id = f"{user.dc_id}" if user.dc_id else "-"
        common = await client.get_common_chats(user.id)
        out_str = f"""<b>USER INFORMATION:</b>

🆔 <b>User ID:</b> <code>{user.id}</code>
👤 <b>First Name:</b> {first_name}
🗣️ <b>Last Name:</b> {last_name}
🌐 <b>Username:</b> {username}
🏛️ <b>DC ID:</b> <code>{dc_id}</code>
🤖 <b>Is Bot:</b> <code>{user.is_bot}</code>
🚷 <b>Is Scam:</b> <code>{user.is_scam}</code>
🚫 <b>Restricted:</b> <code>{user.is_restricted}</code>
✅ <b>Verified:</b> <code>{user.is_verified}</code>
⭐ <b>Premium:</b> <code>{user.is_premium}</code>
📝 <b>User Bio:</b> {bio}

👀 <b>Same groups seen:</b> {len(common)}
👁️ <b>Last Seen:</b> <code>{status}</code>
🔗 <b>User permanent link:</b> <a href=tg://user?id={user.id}>{fullname}</a>
"""
        photo_id = user.photo.big_file_id if user.photo else None
        if photo_id:
            photo = await client.download_media(photo_id)
            await gather(
                Tm.delete(),
                client.send_photo(
                    message.chat.id,
                    photo,
                    caption=out_str,
                    reply_to_message_id=message.id,
                ),
            )
            remove(photo)
        else:
            await Tm.edit(out_str, disable_web_page_preview=True)
    except Exception as e:
        return await Tm.edit(f"INFO: {e}")


@ubot.on_message(filters.me & anjay("cinfo"))
async def _(client, message):
    Tm = await message.reply_text("</b>Processing . . .</b>")
    try:
        if len(message.text.split()) > 1:
            chat_u = message.text.split()[1]
            chat = await client.get_chat(chat_u)
        else:
            if message.chat.type == ChatType.PRIVATE:
                return await Tm.edit(
                    f"Use this command within a group or use !info [group username or id]`"
                )
            else:
                chatid = message.chat.id
                chat = await client.get_chat(chatid)
        h = f"{chat.type}"
        if h.startswith("ChatType"):
            y = h.replace("ChatType.", "")
            type = y.capitalize()
        else:
            type = "Private"
        username = f"@{chat.username}" if chat.username else "-"
        description = f"{chat.description}" if chat.description else "-"
        dc_id = f"{chat.dc_id}" if chat.dc_id else "-"
        out_str = f"""<b>CHAT INFORMATION:</b>

🆔 <b>Chat ID:</b> <code>{chat.id}</code>
👥 <b>Title:</b> {chat.title}
👥 <b>Username:</b> {username}
📩 <b>Type:</b> <code>{type}</code>
🏛️ <b>DC ID:</b> <code>{dc_id}</code>
🗣️ <b>Is Scam:</b> <code>{chat.is_scam}</code>
🎭 <b>Is Fake:</b> <code>{chat.is_fake}</code>
✅ <b>Verified:</b> <code>{chat.is_verified}</code>
🚫 <b>Restricted:</b> <code>{chat.is_restricted}</code>
🔰 <b>Protected:</b> <code>{chat.has_protected_content}</code>

🚻 <b>Total members:</b> <code>{chat.members_count}</code>
📝 <b>Description:</b>
<code>{description}</code>
"""
        photo_id = chat.photo.big_file_id if chat.photo else None
        if photo_id:
            photo = await client.download_media(photo_id)
            await gather(
                Tm.delete(),
                client.send_photo(
                    message.chat.id,
                    photo,
                    caption=out_str,
                    reply_to_message_id=message.id,
                ),
            )
            remove(photo)
        else:
            await Tm.edit(out_str, disable_web_page_preview=True)
    except Exception as e:
        return await Tm.edit(f"INFO: `{e}`")
