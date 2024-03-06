
from ubot.core.database import db

user = db.supro


async def get_supro():
    supro = await user.find_one({"supro": "supro"})
    if not supro:
        return []
    return supro["list"]


async def add_supro(user_id):
    list = await get_supro()
    list.append(user_id)
    await user.update_one({"supro": "supro"}, {"$set": {"list": list}}, upsert=True)
    return True


async def remove_supro(user_id):
    list = await get_supro()
    list.remove(user_id)
    await user.update_one({"supro": "supro"}, {"$set": {"list": list}}, upsert=True)
    return True
