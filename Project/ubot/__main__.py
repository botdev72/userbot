import asyncio
import sys
from atexit import register

from pyrogram import idle
from pyrogram.errors import *

from ubot import LOGGER, Ubot, bot, gas, remove_offi, sending_user
from ubot.core.functions.expired import expiredUserbots
from ubot.core.functions.plugins import loadPlugins
from ubot.utils.dbfunctions import *


async def anjing():
    while not await asyncio.sleep(2600):

        def _():
            gas()

        register(_)
        sys.exit(0)


async def start_ubot(user_id, _ubot):
    ubot_ = Ubot(**_ubot)
    try:
        await asyncio.wait_for(ubot_.start(), timeout=30)
        await ubot_.join_chat("UserbotYoishi")
    except asyncio.TimeoutError:
        await remove_ubot(user_id)
        await add_prem(user_id)
        await sending_user(user_id)
        LOGGER(__name__).error(f"Timeout {user_id}")
    except RPCError:
        await remove_ubot(user_id)
        await rm_all(user_id)
        await rem_pref(user_id)
        await rem_uptime(user_id)
        await rem_expired_date(user_id)
        await remove_offi(user_id)
        await rmall_var(user_id)
        await del_log_group(user_id)
        await rm_approved_user(user_id)
        for X in await get_chat(user_id):
            await remove_chat(user_id, X)
        LOGGER(__name__).error(f"Expired {user_id} Mungkin")
    except:
        pass


async def main():
    tasks = [
        asyncio.create_task(start_ubot(int(_ubot["name"]), _ubot))
        for _ubot in await get_userbots()
    ]
    await asyncio.gather(*tasks, bot.start())
    await asyncio.gather(loadPlugins(), expiredUserbots(), idle())


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())
