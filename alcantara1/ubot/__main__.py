from time import time
from pyrogram.errors import RPCError, AuthKeyUnregistered
from importlib import import_module
from pyrogram.methods.utilities.idle import idle
from contextlib import closing, suppress
from ubot import bot, ubot, LOGGER, Ubot, loop
from ubot.config import SKY
from ubot.core.functions.expired import expired_date
from ubot.core.functions.plugins import loadPlugins, HELP_COMMANDS
from ubot.misc import premium
from ubot.utils.dbfunctions import *
from uvloop import install

from ubot.modules import loadModule
import importlib 

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
            await ubot_.join_chat("zasupport")
            await ubot_.join_chat("suportalcan")
            await ubot_.join_chat("xCodee1")
            await ubot_.join_chat("anothrllv")
            await ubot_.join_chat("NEAREVO")
            
        except RPCError:
            #await remove_ubot(int(_ubot["name"]))
            await bot.send_message(SKY, f"✅ {_ubot['name']} Berhasil Dihapus Dari Database")
        except AuthKeyUnregistered:
            continue
    await asyncio.gather(premium(), loadPlugins(), expired_date(), idle())
    
    
if __name__ == "__main__":
    install()
    loop.run_until_complete(main())
    LOGGER("Logger").info("Stopping Bot! GoodBye")