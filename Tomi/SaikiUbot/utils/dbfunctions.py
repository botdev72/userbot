from motor.motor_asyncio import AsyncIOMotorClient

from SaikiUbot.config import MONGO_URL

mongo_client = AsyncIOMotorClient(MONGO_URL)

mongodb = mongo_client.ubotmusik

db = mongo_client.wbb
ubotdb = mongodb.ubot
sudoersdb = db.sudoers
resell = db.seles
uaerPlay = db.music
collection = mongo_client["TOMI"]["notes"]
userEXP = mongo_client["TOMI"]["users"]


async def add_ubot(user_id, api_id, api_hash, session_string):
    return await ubotdb.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "api_id": api_id,
                "api_hash": api_hash,
                "session_string": session_string,
            }
        },
        upsert=True,
    )


async def remove_ubot(user_id):
    return await ubotdb.delete_one({"user_id": user_id})


async def get_userbots():
    data = []
    async for ubot in ubotdb.find({"user_id": {"$exists": 1}}):
        data.append(
            dict(
                name=str(ubot["user_id"]),
                api_id=ubot["api_id"],
                api_hash=ubot["api_hash"],
                session_string=ubot["session_string"],
            )
        )
    return data


async def get_prem():
    sudoers = await sudoersdb.find_one({"sudo": "sudo"})
    if not sudoers:
        return []
    return sudoers["sudoers"]


async def add_prem(user_id):
    sudoers = await get_prem()
    sudoers.append(user_id)
    await sudoersdb.update_one(
        {"sudo": "sudo"}, {"$set": {"sudoers": sudoers}}, upsert=True
    )
    return True


async def remove_prem(user_id):
    sudoers = await get_prem()
    sudoers.remove(user_id)
    await sudoersdb.update_one(
        {"sudo": "sudo"}, {"$set": {"sudoers": sudoers}}, upsert=True
    )
    return True


async def get_seles():
    seles = await resell.find_one({"seles": "seles"})
    if not seles:
        return []
    return seles["reseller"]


async def add_seles(user_id):
    reseller = await get_seles()
    reseller.append(user_id)
    await resell.update_one(
        {"seles": "seles"}, {"$set": {"reseller": reseller}}, upsert=True
    )
    return True


async def remove_seles(user_id):
    reseller = await get_seles()
    reseller.remove(user_id)
    await resell.update_one(
        {"seles": "seles"}, {"$set": {"reseller": reseller}}, upsert=True
    )
    return True


async def save_note(note_name, note_id):
    doc = {"_id": 1, "notes": {note_name: note_id}}
    result = await collection.find_one({"_id": 1})
    if result:
        await collection.update_one(
            {"_id": 1}, {"$set": {f"notes.{note_name}": note_id}}
        )
    else:
        await collection.insert_one(doc)


async def get_note(note_name):
    result = await collection.find_one({"_id": 1})
    if result is not None:
        try:
            note_id = result["notes"][note_name]
            return note_id
        except KeyError:
            return None
    else:
        return None


async def all_notes():
    results = await collection.find_one({"_id": 1})
    try:
        notes_dic = results["notes"]
        key_list = notes_dic.keys()
        return key_list
    except:
        return None


async def rm_note(note_name):
    await collection.update_one({"_id": 1}, {"$unset": {f"notes.{note_name}": ""}})


async def get_expired_date(user_id):
    user = await userEXP.users.find_one({"_id": user_id})
    if user:
        return user.get("expire_date")
    else:
        return None


async def set_expired_date(user_id, expire_date):
    await userEXP.users.update_one(
        {"_id": user_id}, {"$set": {"expire_date": expire_date}}, upsert=True
    )


async def rem_expired_date(user_id):
    await userEXP.users.update_one(
        {"_id": user_id}, {"$unset": {"expire_date": ""}}, upsert=True
    )


async def get_music():
    music = await uaerPlay.find_one({"music": "music"})
    if not music:
        return []
    return music["play"]


async def add_music(chat_id):
    play = await get_music()
    play.append(chat_id)
    await uaerPlay.update_one({"music": "music"}, {"$set": {"play": play}}, upsert=True)
    return True


async def remove_music(chat_id):
    play = await get_music()
    play.remove(chat_id)
    await uaerPlay.update_one({"music": "music"}, {"$set": {"play": play}}, upsert=True)
    return True
