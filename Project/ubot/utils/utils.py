import logging
from asyncio import get_event_loop
from functools import partial
from io import BytesIO
from time import time

from pyrogram import Client, enums
from pyrogram.errors import *
from pyrogram.types import *

from ubot import aiosession

LOGS = logging.getLogger(__name__)


async def make_carbon(code):
    url = "https://carbonara.solopov.dev/api/cook"
    async with aiosession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image


def run_sync(func, *args, **kwargs):
    return get_event_loop().run_in_executor(None, partial(func, *args, **kwargs))


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


async def eor(msg, text):
    msg = (
        message.reply_text
        if bool(message.from_user and message.from_user.is_self or message.outgoing)
        else (message.reply_to_message or message).reply_text
    )
    return await msg(text)


"""
# eor = edit_or_reply

from inspect import getfullargspec


async def eor(msg, text, **kwargs):
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    try:
        return await func(text, **{k: v for k, v in kwargs.items() if k in spec})
    except MessageNotModified as e:
        LOGS.exception(f"{e}")





async def eor(message, text=None, **args):
    try:
        try:
            time = args.get("time", None)
            edit_time = args.get("edit_time", None)
            if "edit_time" in args:
                del args["edit_time"]
            if "time" in args:
                del args["time"]
            if "link_preview" not in args:
                args["disable_web_page_preview"] = False
            args["reply_to_message_id"] = message.reply_to_message or message
            if message.outgoing:
                if edit_time:
                    await sleep(edit_time)
                if "file" in args and args["file"] and not message.media:
                    await message.delete()
                    ok = await message.reply_text(text, **args)
                else:
                    try:
                        try:
                            del args["reply_to_message_id"]
                        except KeyError:
                            pass
                        ok = await message.edit(text, **args)
                    except MessageNotModified:
                        ok = message

            else:
                try:
                    ok = await message.reply_text(text, **args)
                except AttributeError:
                    # ok = message
                    pass
            if time:
                await sleep(time)
                return await ok.delete()
            return ok
        except AttributeError:
            pass
    except UnboundLocalError:
        pass


async def eod(message, text=None, **kwargs):
    kwargs["time"] = kwargs.get("time", 8)
    return await message.reply(text, **kwargs)


async def _try_delete(message):
    try:
        return await message.delete()
    except MessageDeleteForbidden:
        pass
    except BaseException as er:
        LOGS.error("Error while Deleting Message..")
        LOGS.exception(er)


setattr(Message, "eor", eor)
setattr(Message, "try_delete", _try_delete)
"""
