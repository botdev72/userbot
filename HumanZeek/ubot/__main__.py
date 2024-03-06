import asyncio
import os
import sys

from atexit import register
from pyrogram import idle

from pyrogram.errors import RPCError
from pyrogram import idle

from ubot import bot, ubot, Ubot
from ubot.config import SKY
from ubot.core.functions.expired import expired_date
from ubot.core.functions.plugins import loadPlugins
from ubot.misc import premium
from ubot.utils.dbfunctions import *
from ubot.utils.ultra import *

async def auto_restart():
    while not await asyncio.sleep(3600):
        def _():
            os.system(f"kill -9 {os.getpid()} && python3 -m ubot")
        register(_)
        sys.exit(0)

async def wibu(user_id, _ubot):
    ubot_ = Ubot(**_ubot)
    try:
        await asyncio.wait_for(ubot_.start(), timeout=30)
        await ubot_.join_chat("hzkcutez")
        await ubot_.join_chat("hzzzkki")
        await ubot_.join_chat("hzstores")
    except asyncio.TimeoutError:
        await remove_ubot(user_id)
        await rem_uptime(user_id)
        await rem_pref(user_id)
        await rm_all(user_id)
        await remove_ultraprem(user_id)
        print("TImeout Error Bangsat ...")
    except RPCError:
        await remove_ubot(user_id)
        await rm_all(user_id)
        await rem_pref(user_id)
        await rem_uptime(user_id)
        await rem_expired_date(user_id)
        print("String Error...")


async def main():
    tasks = [
        asyncio.create_task(wibu(int(_ubot["name"]), _ubot))
        for _ubot in await get_userbots()
    ]
    await asyncio.gather(*tasks, bot.start())
    await bot.send_message(SKY, "Booting Successfully ...")
    await asyncio.gather(premium(), loadPlugins(), idle())

    

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
