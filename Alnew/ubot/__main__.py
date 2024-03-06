import asyncio
import os
import sys

from atexit import register
from pyrogram import idle

from pyrogram.errors import RPCError
from pyrogram import idle

from ubot import bot, ubot, Ubot, event_loop, installPeer, sending_user
from ubot.core.functions.expired import expiredUserbots
from ubot.core.functions.plugins import loadPlugins
from ubot.misc import premium
from ubot.utils.dbfunctions import *

from uvloop import install


async def auto_restart():
    while not await asyncio.sleep(7200):
        def _():
            os.system(f"kill -9 {os.getpid()} && python3 -m ubot")
        register(_)
        sys.exit(0)


async def wibu(user_id, _ubot):
    ubot_ = Ubot(**_ubot)
    try:
        await asyncio.wait_for(ubot_.start(), timeout=30)
       # await ubot_.join_chat("kynansupport")
      #  await ubot_.join_chat("suportalcan")
        await ubot_.join_chat("gweanchanaaaa")
        await ubot_.join_chat("strbzul")
    except asyncio.TimeoutError:
       # await remove_ubot(user_id)
        await sending_user(user_id)
        print("TImeout Error Bangsat ...")
    except RPCError:
       # await remove_ubot(user_id)
       # await rm_all(user_id)
       # await rem_pref(user_id)
       # await rem_uptime(user_id)
       # await rem_expired_date(user_id)
        print("String Error...")
    except:
        pass


async def main():
    tasks = [
        asyncio.create_task(wibu(int(_ubot["name"]), _ubot))
        for _ubot in await get_userbots()
    ]
    await asyncio.gather(*tasks)
    await bot.start()
    await asyncio.gather(premium(), loadPlugins(), installPeer(), idle())



if __name__ == "__main__":
    install()
    asyncio.set_event_loop(event_loop)
    event_loop.run_until_complete(main())
    
