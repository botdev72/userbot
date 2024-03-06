
from pyrogram.errors import RPCError

from pyrogram.methods.utilities.idle import idle
from contextlib import closing, suppress
from ubot import bot, ubot, LOGGER, Ubot
from ubot.config import SKY
from ubot.core.functions.expired import expired_date
from ubot.core.functions.plugins import loadPlugins
from ubot.misc import premium
from ubot.utils.dbfunctions import get_userbots, remove_ubot
from uvloop import install
import asyncio

async def start_bot():
    await bot.start()
    LOGGER("Started Bot").info("Successfully Start ")
    await ubot.start()
    LOGGER("Started Ubot").info("Successfully Start ")
    for _ubot in await get_userbots():
        ubot_ = Ubot(**_ubot)
        try:
            await ubot_.start()
            LOGGER("Started Client").info("Successfully Start ")
            await ubot_.join_chat("kynansupport")
            await ubot_.join_chat("veaperas1k")
            await ubot_.join_chat("kontenfilm")
            await ubot_.join_chat("kazusupportgrp")
            LOGGER("Join Client").info("Join Successfully ")
        except RPCError:
            await remove_ubot(int(_ubot["name"]))
            await bot.send_message(SKY, f"✅ {_ubot['name']} Berhasil Dihapus Dari Database")
    install()
    await asyncio.gather(premium(), loadPlugins(), expired_date(), idle())
    
    
loop = asyncio.get_event_loop_policy()
event_loop = loop.get_event_loop()
asyncio.set_event_loop(event_loop)
event_loop.run_until_complete(start_bot())
LOGGER("Logger").info("Stopping Bot! GoodBye")
    
