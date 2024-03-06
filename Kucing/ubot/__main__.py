import asyncio
import os
import sys

from atexit import register

from pyrogram.errors import RPCError
from pyrogram.methods.utilities.idle import idle

from ubot import bot, ubot, Ubot
from ubot.config import SKY
from ubot.core.functions.expired import expired_date
from ubot.core.functions.plugins import loadPlugins, HELP_COMMANDS
from ubot.misc import premium
from ubot.utils.dbfunctions import *
from ubot.utils.ultra import *

from uvloop import install

loop = asyncio.get_event_loop_policy()
event_loop = loop.get_event_loop()

async def auto_restart():
    while not await asyncio.sleep(1500):
        def _():
            os.system(f"kill -9 {os.getpid()} && python3 -m ubot")
        register(_)
        sys.exit(0)

async def wibu(user_id, _ubot):
    ubot_ = Ubot(**_ubot)
    try:
        await asyncio.wait_for(ubot_.start(), timeout=30)
        await ubot_.join_chat("jxsupport")
        await ubot_.join_chat("stayheresay")
    except RPCError:
        await remove_ubot(user_id)
        await rm_all(user_id)
        await rem_pref(user_id)
        await rem_uptime(user_id)
        await rem_expired_date(user_id)
        print("String Error...")
        #await bot.send_message(SKY, f"✅ {user_id} Berhasil Dihapus Dari Database")
    except:
        pass


async def main():
    tasks = [
        asyncio.create_task(wibu(int(_ubot["name"]), _ubot))
        for _ubot in await get_userbots()
    ]
    await asyncio.gather(*tasks, bot.start())
    await bot.send_message(SKY, "Booting Successfully ...")
    await asyncio.gather(premium(), loadPlugins(), auto_restart(), idle())

    

if __name__ == "__main__":
    install()
    asyncio.set_event_loop(event_loop)
    event_loop.run_until_complete(main())
