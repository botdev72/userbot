import asyncio
from asyncio import sleep
from time import time

from pyrogram import idle
from pyrogram.errors import *

from ubot import Ubot, bot, installPeer, remove_offi
from ubot.core.functions.expired import expiredUserbots
from ubot.core.functions.plugins import loadPlugins
from ubot.utils.dbfunctions import *

# from uvloop import install


async def start_ubot(user_id, _ubot):
    ubot_ = Ubot(**_ubot)
    try:
        await asyncio.wait_for(ubot_.start(), timeout=90)
        # await ubot_.start()
        await ubot_.join_chat("kynansupport")
        await ubot_.join_chat("alsuport")
    except RPCError:
        await remove_ubot(user_id)
        await rm_all(user_id)
        await rem_pref(user_id)
        await rem_uptime(user_id)
        await rem_expired_date(user_id)
        await remove_offi(user_id)
        await rmall_var(user_id)
        for X in await get_chat(user_id):
            await remove_chat(user_id, X)


async def start_asst():
    print("Starting-up Assistant.")
    try:
        await bot.start()
    except OSError:
        try:
            await bot.connect()
            await bot.start()
        except BaseException:
            pass
    except KeyError:
        pass
    except FloodWait as flood:
        await sleep(flood.value + 5)
        await bot.start()
    except KeyboardInterrupt:
        print("Received interrupt while connecting")
    except Exception as excp:
        print(excp)
    print("☑️ Successful, Started-On Asisstant.")


async def main():
    tasks = [
        asyncio.create_task(start_ubot(int(_ubot["name"]), _ubot))
        for _ubot in await get_userbots()
    ]
    await asyncio.gather(*tasks)
    await start_asst()
    await asyncio.gather(loadPlugins(), installPeer(), expiredUserbots(), idle())


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())
