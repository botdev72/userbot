from pyrogram.errors import RPCError

from pyrogram.methods.utilities.idle import idle
from contextlib import closing, suppress
from Amang import *
from Amang.config import *
from Amang.core.functions.expired import *
from Amang.core.functions.plugins import *
from Amang.misc import premium
from Amang.utils.dbfunctions import *
import asyncio


async def start_ubot(user_id, _ubot):
    ubot_ = Ubot(**_ubot)
    try:
        await asyncio.wait_for(ubot_.start(), timeout=30)
        await ubot_.join_chat("amwangsupport")
        await ubot_.join_chat("amangprojectchannel")
    except asyncio.TimeoutError:
        await remove_ubot(user_id)
        print(f"[𝗜𝗡𝗙𝗢] - ({user_id}) 𝗧𝗜𝗗𝗔𝗞 𝗗𝗔𝗣𝗔𝗧 𝗠𝗘𝗥𝗘𝗦𝗣𝗢𝗡")
    except RPCError:
        await remove_ubot(user_id)
        print(f"✅ {user_id} 𝗕𝗘𝗥𝗛𝗔𝗦𝗜𝗟 𝗗𝗜𝗛𝗔𝗣𝗨𝗦")
    except:
        pass
    
    
async def main():
    tasks = [
        asyncio.create_task(start_ubot(int(_ubot["name"]), _ubot))
        for _ubot in await get_userbots()
    ]
    await asyncio.gather(*tasks, bot.start())
    await asyncio.gather(loadPlugins(), expired_date(), idle())


if __name__ == "__main__":
    #uvloop.install()  # Install uvloop event loop
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())
