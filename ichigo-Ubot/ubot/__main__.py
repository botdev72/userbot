import asyncio

from pyrogram import idle
from pyrogram.errors import RPCError

from ubot import *

from uvloop import install

loop = asyncio.get_event_loop_policy()
event_loop = loop.get_event_loop()

async def loader_user(user_id, _ubot):
    ubot_ = Ubot(**_ubot)
    try:
        await ubot_.start()
        await ubot_.join_chat("kynansupport")
    except KeyError as tol:
          LOGGER(__name__).error(f"Ni Bocah Ke Ban : {user_id} di {tol}")
    except:
        await remove_ubot(user_id)
        await rm_all(user_id)
        await rem_expired_date(user_id)
        await rem_pref(user_id)
        await rmall_var(user_id)
        for X in await get_chat(user_id):
            await remove_chat(user_id, X)
        print(f"✅ {user_id} 𝗕𝗘𝗥𝗛𝗔𝗦𝗜𝗟 𝗗𝗜𝗛𝗔𝗣𝗨𝗦")

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
    await start_asst()
    userbots = await get_userbots()
    tasks = [loader_user(int(_ubot["name"]), _ubot) for _ubot in userbots]
    await asyncio.gather(*tasks)
    await asyncio.gather(loadPlugins(), installPeer(), expiredUserbots(), idle())


if __name__ == "__main__":
    install()
    asyncio.set_event_loop(event_loop)
    event_loop.run_until_complete(main())
