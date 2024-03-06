import asyncio
import random

from .. import *

__MODULE__ = "SANGMATA"
__HELP__ = f"""
Perintah:
         <code>{PREFIX[0]}sg</code> [user_id/reply user]
Penjelasan:
           Untuk memeriksa histori nama/username
"""


@PY.UBOT("sg", PREFIX)
async def _(client, message):
    user_id = await extract_user(message)
    lol = await message.reply("</b>Memproses. . .</b>")
    if not user_id:
        return await lol.edit("<b>user tidak ditemukan</b>")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await lol.edit(error)
    bot = ["@Sangmata_bot", "@SangMata_beta_bot"]
    try:
        await client.join_chat("https://t.me/+QvgWBX23s3RkOWVl")
    except:
        pass
    getbot = random.choice(bot)
    txt = await client.send_message(-1001835552147, f"{getbot} allhistory {user.id}")
    await asyncio.sleep(4)
    await lol.delete()
    try:
        sg = await client.get_messages(-1001835552147, txt.id + 1)
        await message.reply(sg.text)
    except:
        await message.reply("❌ api sedang error silahkan coba lagi nanti")
    await client.leave_chat(-1001835552147)
