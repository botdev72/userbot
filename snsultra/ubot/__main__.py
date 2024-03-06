from time import time
from pyrogram.errors import RPCError
from importlib import import_module
from pyrogram.methods.utilities.idle import idle
from contextlib import closing, suppress
from ubot import bot, ubot, LOGGER, Ubot, event_loop
from ubot.config import SKY
from ubot.core.functions.expired import expired_date
from ubot.core.functions.plugins import loadPlugins, HELP_COMMANDS
from ubot.misc import premium
from ubot.utils.dbfunctions import *
from uvloop import install

from ubot.modules import loadModule
import importlib 
import asyncio


async def start_bot():
    await bot.start()
    await ubot.start()
    await set_uptime(ubot.me.id, time())
    for _ubot in await get_userbots():
        ubot_ = Ubot(**_ubot)
        try:
            try:
                await ubot_.start()
                await ubot_.join_chat("suportkage")
                await ubot_.join_chat("kagestore69")
                await ubot_.join_chat("nakmelawak")
            except:
                pass
        except RPCError:
            await remove_ubot(int(_ubot["name"]))
            await bot.send_message(SKY, f"✅ {_ubot['name']} Berhasil Dihapus Dari Database")
    await asyncio.gather(premium(), expired_date(), loadPlugins(), idle())
    
if __name__ == "__main__":
    install()
    asyncio.set_event_loop(event_loop)
    event_loop.run_until_complete(start_bot())
    LOGGER("Logger").info("Stopping Bot! GoodBye")

    
