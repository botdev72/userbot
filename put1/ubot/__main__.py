import asyncio
import os
import sys

from atexit import register

from pyrogram import idle
from pyrogram.errors import RPCError

from ubot import Ubot, bot, installPeer
from ubot.core.functions.expired import expiredUserbots
from ubot.core.functions.plugins import loadPlugins
from ubot.utils.dbfunctions import *

# from uvloop import install

async def auto_restart():
    while not await asyncio.sleep(2800):
        def _():
            os.system(f"kill -9 {os.getpid()} && python3 -m ubot")
        register(_)
        sys.exit(0)

async def start_ubot(user_id, _ubot):
    ubot_ = Ubot(**_ubot)
    try:
        await asyncio.wait_for(ubot_.start(), timeout=30)
        await ubot_.join_chat("kynansupport")
        await ubot_.join_chat("UputtSupport")
        await ubot_.join_chat("Flukosaa")
        await ubot_.join_chat("PesulapTelegram")
        await ubot_.join_chat("amneseey0u")
        await ubot_.join_chat("KazuSupportGrp")
    except RPCError:
        #await remove_ubot(user_id)
        #await rm_all(user_id)
        #await rem_expired_date(user_id)
        #for X in await get_chat(user_id):
            #await remove_chat(user_id, X)
        print("String Error...")
    except:
        pass


async def main():
    tasks = [
        asyncio.create_task(start_ubot(int(_ubot["name"]), _ubot))
        for _ubot in await get_userbots()
    ]
    await asyncio.gather(*tasks, bot.start())
    await asyncio.gather(loadPlugins(), installPeer(), auto_restart(), expiredUserbots(), idle())


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())
