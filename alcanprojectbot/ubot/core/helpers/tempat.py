from pyrogram import *
from pyrogram.types import *
from ubot.core.database import get_supro, get_violet



def cek_pro(func):
    async def wrapper(client, message):
        user_id = message.from_user.id
        if user_id not in await get_supro():
            return await message.reply_text("Maaf, anda bukan pegguna Super Pro.")
        #elif user_id not in await get_violet():
            #return await message.reply_text("Maaf, anda bukan pegguna Super Violet.")
        await func(client, message)
    return wrapper
  
def cek_violet(func):
    async def wrapper(client, message):
        user_id = message.from_user.id
        cekpro = await get_supro()
        cekvio = await get_violet()
        if user_id not in cekvio:
            return await message.reply_text("Maaf, anda bukan pegguna Super Violet.")
        #elif user_id not in await get_violet():
            #return await message.reply_text("Maaf, anda bukan pegguna Super Violet.")
        await func(client, message)
    return wrapper
