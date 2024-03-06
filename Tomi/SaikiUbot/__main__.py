from asyncio import get_event_loop_policy

from pyrogram.enums import ChatType
from pyrogram.errors import RPCError
from pyrogram.methods.utilities.idle import idle

from SaikiUbot import (OWNER_ID, Ubot, bot, get_my_id, get_my_peer,
                       get_userbots, lang_code, loadPlugins, premium,
                       rem_expired_date, remove_ubot, ubot)

from .misc import pybot


async def main():
    await bot.start()
    print(f"INFO: Started Bot {bot.me.first_name} | {bot.me.id}")
    await ubot.start()
    get_my_id.append(ubot.me.id)
    lang_code[ubot.me.id] = {"negara": "id"}
    users = 0
    group = 0
    async for dialog in ubot.get_dialogs():
        if dialog.chat.type == ChatType.PRIVATE:
            users += 1
        elif dialog.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
            group += 1
    get_my_peer[ubot.me.id] = {"group": group, "users": users}
    print(
        f"INFO: Started Selt {ubot.me.first_name} {ubot.me.last_name or ''} | {ubot.me.id}"
    )
    for _ubot in await get_userbots():
        ubot_ = Ubot(**_ubot)
        try:
            await ubot_.start()
            get_my_id.append(ubot_.me.id)
            lang_code[ubot_.me.id] = {"negara": "id"}
            users = 0
            group = 0
            async for dialog in ubot_.get_dialogs():
                if dialog.chat.type == ChatType.PRIVATE:
                    users += 1
                elif dialog.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
                    group += 1
            get_my_peer[ubot_.me.id] = {"group": group, "users": users}
            print(
                f"INFO: Started Ubot {ubot_.me.first_name} {ubot_.me.last_name or ''} | {ubot_.me.id}"
            )
        except RPCError:
            await remove_ubot(int(_ubot["name"]))
            await bot.send_message(OWNER_ID, f"✅ {_ubot['name']} Dihapus Dari Database")
            await rem_expired_date(int(_ubot["name"]))
            print(f"✅ {_ubot['name']} Dihapus Dari Database")
    await loadPlugins()
    await pybot()
    await premium()
    await idle()


if __name__ == "__main__":
    get_event_loop_policy().get_event_loop().run_until_complete(main())
