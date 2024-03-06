import asyncio

from pyrogram import idle
from pyrogram.errors import RPCError
from uvloop import install

from ubot import *

loop = asyncio.get_event_loop_policy()
event_loop = loop.get_event_loop()


async def loader_user(user_id, _ubot):
    ubot_ = Ubot(**_ubot)
    try:
        await asyncio.wait_for(ubot_.start(), timeout=90)
        await ubot_.join_chat("kynansupport")
        await asyncio.join_chat("friendshipsuport")
        await asyncio.join_chat ("friendshipstoree")
        # await del_log_group(ubot_.me.id)
        # ajg = await get_log(ubot_)
        # await ubot_.delete_supergroup(int(ajg.id))
    except RPCError:
        await remove_ubot(user_id)
        await rm_all(user_id)
        await rem_expired_date(user_id)
        await rem_pref(user_id)
        await rmall_var(user_id)
        for X in await get_chat(user_id):
            await remove_chat(user_id, X)
        print(f"✅ {user_id} 𝗕𝗘𝗥𝗛𝗔𝗦𝗜𝗟 𝗗𝗜𝗛𝗔𝗣𝗨𝗦")
    except:
        pass


async def main():
    userbots = await get_userbots()
    tasks = [loader_user(int(_ubot["name"]), _ubot) for _ubot in userbots]
    await asyncio.gather(*tasks, bot.start())
    await asyncio.gather(loadPlugins(), installPeer(), expiredUserbots(), idle())


if __name__ == "__main__":
    install()
    asyncio.set_event_loop(event_loop)
    event_loop.run_until_complete(main())
