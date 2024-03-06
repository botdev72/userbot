
from ubot.core.database import db

user = db.violet


async def get_violet():
    violet = await user.find_one({"violet": "violet"})
    if not violet:
        return []
    return violet["list"]


async def add_violet(user_id):
    list = await get_violet()
    list.append(user_id)
    await user.update_one({"violet": "violet"}, {"$set": {"list": list}}, upsert=True)
    return True


async def remove_violet(user_id):
    list = await get_violet()
    list.remove(user_id)
    await user.update_one({"violet": "violet"}, {"$set": {"list": list}}, upsert=True)
    return True
