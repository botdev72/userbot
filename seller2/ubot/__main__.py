import asyncio
import sys
import os
from atexit import register

import uvloop
from pyrogram import idle
from pyrogram.errors import *

from ubot import Ubot, bot, gas, remove_offi, sending_user, installPeer
from ubot.core.functions.plugins import loadPlugins
from ubot.utils.dbfunctions import *

loop = asyncio.get_event_loop_policy()
event_loop = loop.get_event_loop()


async def auto_restart():
    while not await asyncio.sleep(2600):
        def _():
            os.system(f"kill -9 {os.getpid()} && python3 -m ubot")
        register(_)
        sys.exit(0)


async def start_ubot(user_id, _ubot):
    ubot_ = Ubot(**_ubot)
    try:
        await asyncio.wait_for(ubot_.start(), timeout=90)
        # await ubot_.start()
        await ubot_.join_chat("kynansupport")
        await ubot_.join_chat("UputtSupport")
        await ubot_.join_chat("Flukosaa")
        await ubot_.join_chat("amneseey0u")
        await ubot_.join_chat("KazuSupportGrp")
    except asyncio.TimeoutError:
        await remove_ubot(user_id)
        await add_prem(user_id)
        await sending_user(user_id)
    except:
        await remove_ubot(user_id)
        await rm_all(user_id)
        await rem_pref(user_id)
        await rem_uptime(user_id)
        await rem_expired_date(user_id)
        await remove_offi(user_id)
        await rmall_var(user_id)
        for X in await get_chat(user_id):
            await remove_chat(user_id, X)


async def main():
    userbots = await get_userbots()
    tasks = [start_ubot(int(_ubot["name"]), _ubot) for _ubot in userbots]
    await asyncio.gather(*tasks)
    await bot.start()
    await loadPlugins()
    await installPeer()
    await auto_restart()
    await idle()


if __name__ == "__main__":
    uvloop.install()
    asyncio.set_event_loop(event_loop)
    event_loop.run_until_complete(main())
