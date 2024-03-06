from asyncio import get_event_loop_policy

from pyrogram.errors import RPCError
from pyrogram.methods.utilities.idle import idle
from uvloop import install

from Amang import *
from Amang.config import LOGS
from Amang.core.functions.expired import expired_date, reboots
from Amang.core.functions.plugins import ajg, loadPlugins
from Amang.misc import premium
from Amang.utils.dbfunctions import get_userbots, remove_ubot


async def main():
    await bot.start()
    LOGGER("Started Bot").info("Successfully Starting Bot ")
    await ubot.start()
    LOGGER("Started Bot").info("Successfully Starting Ubot ")
    for _ubot in await get_userbots():
        ubot_ = Ubot(**_ubot)
        try:
            await ubot_.start()
            LOGGER("Started Bot").info("Successfully Starting Ubot ")
            await ajg()
        except RPCError:
            await remove_ubot(int(_ubot["name"]))
            print(f"✅ {_ubot['name']} Berhasil Dihapus Dari Database")
#    install()
    await premium()
    await loadPlugins()
    LOGGER("Started LoadPlugins").info("Successfully LoadPlugin ")
    await expired_date()
#    await rebot()
    await idle()

if __name__ == "__main__":
    get_event_loop_policy().get_event_loop().run_until_complete(main())
    LOGGER("Logger").info("Stopping Bot! GoodBye")
