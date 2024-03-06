from asyncio import get_event_loop, sleep
from functools import partial, wraps
from io import BytesIO
from re import findall
from time import time

from pyrogram import Client, enums
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.errors import PeerIdInvalid, UserNotParticipant
from pyrogram.types import Message

from Amang import aiosession, ubot
from Amang.config import *


async def make_carbon(code):
    url = "https://carbonara.solopov.dev/api/cook"
    async with aiosession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image


def run_sync(func, *args, **kwargs):
    return get_event_loop().run_in_executor(None, partial(func, *args, **kwargs))


def get_urls_from_text(text: str) -> bool:
    regex = r"""(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]
                [.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(
                \([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\
                ()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))""".strip()
    return [x[0] for x in findall(regex, str(text))]


def extract_text_and_keyb(ikb, text: str, row_width: int = 2):
    keyboard = {}
    try:
        text = text.strip()
        if text.startswith("`"):
            text = text[1:]
        if text.endswith("`"):
            text = text[:-1]

        text, keyb = text.split("~")

        keyb = findall(r"\[.+\,.+\]", keyb)
        for btn_str in keyb:
            btn_str = re_sub(r"[\[\]]", "", btn_str)
            btn_str = btn_str.split(",")
            btn_txt, btn_url = btn_str[0], btn_str[1].strip()

            if not get_urls_from_text(btn_url):
                continue
            keyboard[btn_txt] = btn_url
        keyboard = ikb(keyboard, row_width)
    except Exception:
        return
    return text, keyboard


async def check_perms(message, permissions, text_permissions):
    try:
        user = await message.chat.get_member(message.from_user.id)
    except (UserNotParticipant, PeerIdInvalid, AttributeError):
        return False
    if user.status == ChatMemberStatus.OWNER:
        return True
    if user.user.id in [OWNER_ID]:
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


flood = {}


async def extract_userid(message, text):
    def is_int(text):
        try:
            int(text)
        except ValueError:
            return False
        return True

    text = text.strip()

    if is_int(text):
        return int(text)

    entities = message.entities
    app = message._client
    entity = entities[1 if message.text.startswith("/") else 0]
    if entity.type == enums.MessageEntityType.MENTION:
        return (await app.get_users(text)).id
    if entity.type == enums.MessageEntityType.TEXT_MENTION:
        return entity.user.id
    return None


async def extract_user_and_reason(message, sender_chat=False):
    args = message.text.strip().split()
    text = message.text
    user = None
    reason = None
    if message.reply_to_message:
        reply = message.reply_to_message
        if not reply.from_user:
            if (
                reply.sender_chat
                and reply.sender_chat != message.chat.id
                and sender_chat
            ):
                id_ = reply.sender_chat.id
            else:
                return None, None
        else:
            id_ = reply.from_user.id

        if len(args) < 2:
            reason = None
        else:
            reason = text.split(None, 1)[1]
        return id_, reason

    if len(args) == 2:
        user = text.split(None, 1)[1]
        return await extract_userid(message, user), None

    if len(args) > 2:
        user, reason = text.split(None, 2)[1:]
        return await extract_userid(message, user), reason

    return user, reason


async def extract_user(message):
    return (await extract_user_and_reason(message))[0]


admins_in_chat = {}


async def list_admins(client: Client, chat_id: int):
    global admins_in_chat
    if chat_id in admins_in_chat:
        interval = time() - admins_in_chat[chat_id]["last_updated_at"]
        if interval < 3600:
            return admins_in_chat[chat_id]["data"]

    admins_in_chat[chat_id] = {
        "last_updated_at": time(),
        "data": [
            member.user.id
            async for member in client.get_chat_members(
                chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS
            )
        ],
    }
    return admins_in_chat[chat_id]["data"]


async def edit_or_reply(message: Message, *args, **kwargs) -> Message:
    apa = (
        message.reply_text
        if bool(message.from_user and message.from_user.is_self or message.outgoing)
        else (message.reply_to_message or message).reply_text
    )
    return await apa(*args, **kwargs)


eor = edit_or_reply
