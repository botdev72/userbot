from asyncio import get_event_loop, sleep
from functools import partial, wraps

from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.errors import PeerIdInvalid, UserNotParticipant
from pyrogram.types import Message

from SaikiUbot import ubot
from SaikiUbot.config import *


def run_sync(func, *args, **kwargs):
    return get_event_loop().run_in_executor(None, partial(func, *args, **kwargs))


async def check_perms(message, permissions, text_permissions):
    try:
        user = await message.chat.get_member(message.from_user.id)
    except (UserNotParticipant, PeerIdInvalid, AttributeError):
        return False
    if user.status == ChatMemberStatus.OWNER:
        return True
    if user.user.id == OWNER_ID:
        return True
    for ub in ubot._ubot:
        if user.user.id == ub.me.id:
            return True
    if not permissions and user.status == ChatMemberStatus.ADMINISTRATOR:
        return True
    if user.status != ChatMemberStatus.ADMINISTRATOR:
        Tm = await message.reply_text(
            """
<b>🙏🏻 Mohon maaf {mention} anda bukan admin dari group {chat}

✅ Untuk menggunakan perintah <code>{cmd}</code> harus menjadi admin terlebih dahulu</b>
""".format(
                mention=message.from_user.mention,
                chat=message.chat.title,
                cmd=message.text.split()[0],
            )
        )
        await sleep(5)
        await Tm.delete()
        return False

    missing_perms = [
        permission
        for permission in (
            [permissions] if isinstance(permissions, str) else permissions
        )
        if not getattr(user.privileges, permission)
    ]

    if not missing_perms:
        return True
    Tm = await message.reply_text(
        """
<b>🙏🏻 Mohon maaf {mention} anda bukan admin dari group {chat}

✅ Untuk menggunakan perintah <code>{cmd}</code> harus menjadi admin terlebih dahulu 

🔐 {text}</b>
""".format(
            mention=message.from_user.mention,
            chat=message.chat.title,
            cmd=message.text.split()[0],
            text=text_permissions,
        )
    )
    await sleep(5)
    await Tm.delete()
    return False


def require_admin(permissions, text_permissions):
    def decorator(func):
        @wraps(func)
        async def wrapper(client, message: Message, *args, **kwargs):
            if message.chat.type == ChatType.CHANNEL:
                return await func(client, message, *args, *kwargs)
            if (
                not message.from_user
                and message.sender_chat
                and message.sender_chat.id == message.chat.id
            ):
                return await func(client, message, *args, *kwargs)
            has_perms = await check_perms(message, permissions, text_permissions)
            if has_perms:
                return await func(client, message, *args, *kwargs)

        return wrapper

    return decorator
