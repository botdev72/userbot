import importlib
import random
from datetime import datetime, timedelta

from pyrogram.enums import ChatType
from pytz import timezone

from .. import *
from ..misc import ONLY_UBOT
from ..modules import loadModule


@PY.BOT("login", FILTERS.OWNER)
@PY.UBOT("login", PREFIX, FILTERS.ME_OWNER)
async def _(client, message):
    if len(message.command) < 2:
        return await message.reply(
            f"<code>{message.text}</code> <b>String Pyrogram</b>"
        )
    try:
        ub = Ubot(
            name=f"ubot{random.randrange(9999)}",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=message.command[1],
        )
        await ub.start()
        now = datetime.now(timezone("Asia/Jakarta"))
        expire_date = now + timedelta(days=30)
        await set_expired_date(ub.me.id, expire_date)
        get_my_id.append(ub.me.id)
        users = 0
        group = 0
        async for dialog in ub.get_dialogs():
            if dialog.chat.type == ChatType.PRIVATE:
                users += 1
            elif dialog.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
                group += 1
        get_my_peer[ub.me.id] = {"group": group, "users": users}
        await add_ubot(
            user_id=int(ub.me.id),
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=message.command[1],
        )
        for mod in loadModule():
            importlib.reload(importlib.import_module(f"userbot.modules.{mod}"))
        return await message.reply(
            f"<b>✅ Berhasil Login Di Akun: <a href='tg://user?id={ub.me.id}'>{ub.me.first_name} {ub.me.last_name or ''}</a></b>"
        )
    except Exception as error:
        return await message.reply(f"<code>{error}</code>")


@PY.BOT("self", FILTERS.OWNER)
async def _(client, message):
    msg = await message.reply("<b>Tunggu sebentar</b>")
    try:
        ubot._ubot.remove(ubot)
        SELF = Ubot(
            name="ubot",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=SESSION_STRING,
        )
        await SELF.start()
        for mod in loadModule():
            importlib.reload(importlib.import_module(f"userbot.modules.{mod}"))
        return await msg.edit(
            f"<b>✅ Restart Berhasil Dilakukan {SELF.me.first_name} {SELF.me.last_name or ''} | {SELF.me.id}</b>"
        )
    except Exception as error:
        return await msg.edit(f"<code>{error}</code>")


@PY.BOT("restart", ONLY_UBOT)
async def _(client, message):
    msg = await message.reply("<b>Tunggu sebentar</b>")
    for X in ubot._ubot:
        if message.from_user.id == X.me.id:
            for _ubot_ in await get_userbots():
                if X.me.id == int(_ubot_["name"]):
                    try:
                        ubot._ubot.remove(X)
                        UB = Ubot(**_ubot_)
                        await UB.start()
                        for mod in loadModule():
                            importlib.reload(
                                importlib.import_module(f"userbot.modules.{mod}")
                            )
                        return await msg.edit(
                            f"<b>✅ Restart Berhasil Dilakukan {UB.me.first_name} {UB.me.last_name or ''} | {UB.me.id}</b>"
                        )
                    except Exception as error:
                        return await msg.edit(f"<b>{error}</b>")
