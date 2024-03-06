import asyncio
import os
import sys

from asyncio import get_event_loop_policy

from atexit import register
from pyrogram import idle
from pyrogram.errors import *

from ubot import *


async def auto_restart():
    while not await asyncio.sleep(2600):
        def _():
            gas()
        register(_)
        sys.exit(0)
        

async def loader_user(user_id, _ubot):
    ubot_ = Ubot(**_ubot)
    try:
        await asyncio.wait_for(ubot_.start(), timeout=90)
        await ubot_.join_chat("kynansupport")
        await ubot_.join_chat("alsuport")
    except RPCError:
        await remove_ubot(user_id)
        await rm_all(user_id)
        await rem_expired_date(user_id)
        for X in await get_chat(user_id):
            await remove_chat(user_id, X)
        print(f"✅ {user_id} 𝗕𝗘𝗥𝗛𝗔𝗦𝗜𝗟 𝗗𝗜𝗛𝗔𝗣𝗨𝗦")
    except Exception:
        pass


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
    #tasks = [loader_user(int(_ubot["name"]), _ubot) for _ubot in await get_userbots()]
    tasks = []
    for _ubot in await get_userbots():
        tasks.append(asyncio.create_task(loader_user(int(_ubot["name"]), _ubot)))
    await asyncio.gather(*tasks)
    await start_asst()
    await asyncio.gather(loadPlugins(), installPeer(), idle())


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())
