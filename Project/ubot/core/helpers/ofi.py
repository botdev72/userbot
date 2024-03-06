from ubot.utils.dbfunctions import db

user = db.official


async def get_offi():
    official = await user.find_one({"official": "official"})
    if not official:
        return []
    return official["list"]


async def add_offi(user_id):
    list = await get_offi()
    list.append(user_id)
    await user.update_one(
        {"official": "official"}, {"$set": {"list": list}}, upsert=True
    )
    return True


async def remove_offi(user_id):
    list = await get_offi()
    if user_id in list:
        list.remove(user_id)
        await user.update_one(
            {"official": "official"}, {"$set": {"list": list}}, upsert=True
        )
        return True


def cek_offi(func):
    async def wrapper(client, message):
        user_id = message.from_user.id
        if user_id not in await get_offi():
            return await message.reply_text("Tidak ada akses.")
        await func(client, message)

    return wrapper
