from pyrogram import *
from pyrogram.types import *
from .dbfunctions import db

ultrapremdb = db["Kazu"]["ultraprem"]

async def get_ultraprem():
    ultraprem = await ultrapremdb.find_one({"ultra": "ultra"})
    if not ultraprem:
        return []
    return ultraprem["ultraprem"]


async def add_ultraprem(user_id):
    ultraprem = await get_ultraprem()
    ultraprem.append(user_id)
    await ultrapremdb.update_one(
        {"ultra": "ultra"}, {"$set": {"ultraprem": ultraprem}}, upsert=True
    )
    return True


async def remove_ultraprem(user_id):
    ultraprem = await get_ultraprem()
    ultraprem.remove(user_id)
    await ultrapremdb.update_one(
        {"ultra": "ultra"}, {"$set": {"ultraprem": ultraprem}}, upsert=True
    )
    return True


def check_access(func):
    async def wrapper(client, message):
        user_id = message.from_user.id
        if user_id not in await get_ultraprem():
            await message.reply_text("Maaf, fitur ini hanya tersedia pada versi Ultra Premium.\nJika ingin menggunakan fitur ini, Silakan Upgrade ke Versi Ultra Premium.")
            return
        await func(client, message)
    return wrapper
