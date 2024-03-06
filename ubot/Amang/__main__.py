from pyrogram import idle
import asyncio
from pyrogram.errors import RPCError
from uvloop import install

from Amang import bot, Ubot, ubot, LOGGER
from Amang.config import LOGS
from Amang.core.functions.expired import expired_date, rebot
from Amang.core.functions.plugins import ajg, loadPlugins
from Amang.misc import premium
from Amang.utils.dbfunctions import get_userbots, remove_ubot

from asyncio import get_event_loop_policy

async def main():
    await bot.start()
    LOGGER("Started Bot").info("Successfully Start ")
    await ubot.start()
    LOGGER("Started Ubot").info("Successfully Start ")
    for _ubot in await get_userbots():
        ubot_ = Ubot(**_ubot)
        try:
            await ubot_.start()
            LOGGER("Started Client").info("Successfully Start ")
            await ajg()
        except RPCError:
            await remove_ubot(int(_ubot["name"]))
            await bot.send_message(LOGS, f"✅ {_ubot['name']} Berhasil Dihapus Dari Database")
    await premium()
    await loadPlugins()
    await rebot()
    await expired_date()
    install()
    await idle()


if __name__ == "__main__":
    try:
        get_event_loop_policy().get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        LOGGER("Logger").info("Stopping Bot! GoodBye")
