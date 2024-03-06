import codecs
import pickle
import asyncio
from typing import Dict, List, Union
from pyrogram import *
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient

#import pymongo

from ubot.config import MONGO_URL

mongo = MongoClient(MONGO_URL)

db = mongo
ubotdb = db["KynanWibu"]["ubot"]
sudoersdb = db["KynanWibu"]["sudoers"]
blchatdb = db["KynanWibu"]["blchat"]
resell = db["KynanWibu"]["seles"]
notesdb = db["KynanWibu"]["notes"]
permitdb = db["KynanWibu"]["pmguard"]
vardb = db["KynanWibu"]["variable"]
expdb = db["KynanWibu"]["expired"]
prefixes = db["KynanWibu"]["prefixesi"]
bacotdb = db["KynanWibu"]["bacotdb"]
blockeddb = db["KynanWibu"]["gbans"]
aktif = db["KynanWibu"]["uptime"]


async def get_uptime(user_id):
    user = await aktif.users.find_one({"_id": user_id})
    if user:
        return user.get("uptime")
    else:
        return None


async def set_uptime(user_id, expire_date):
    await aktif.users.update_one(
        {"_id": user_id}, {"$set": {"uptime": expire_date}}, upsert=True
    )


async def rem_uptime(user_id):
    await aktif.users.update_one(
        {"_id": user_id}, {"$unset": {"uptime": ""}}, upsert=True
    )

async def get_banned_users(gua: int) -> list:
    results = []
    async for user in blockeddb.find({"gua": gua, "user_id": {"$gt": 0}}):
        results.append(user["user_id"])
    return results


async def get_banned_count(gua: int) -> int:
    users = blockeddb.find({"gua": gua, "user_id": {"$gt": 0}})
    users = await users.to_list(length=100000)
    return len(users)


async def is_banned_user(gua: int, user_id: int) -> bool:
    user = await blockeddb.find_one({"gua": gua, "user_id": user_id})
    return bool(user)


async def add_banned_user(gua: int, user_id: int):
    is_gbanned = await is_banned_user(gua, user_id)
    if is_gbanned:
        return
    return await blockeddb.insert_one({"gua": gua, "user_id": user_id})


async def remove_banned_user(gua: int, user_id: int):
    is_gbanned = await is_banned_user(gua, user_id)
    if not is_gbanned:
        return
    return await blockeddb.delete_one({"gua": gua, "user_id": user_id})

async def is_served_user(user_id: int) -> bool:
    user = await bacotdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True

async def get_served_users() -> list:
    users_list = []
    async for user in bacotdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list

async def add_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if is_served:
        return
    return await bacotdb.insert_one({"user_id": user_id})
    
#async def get_pref(user_id):
    #user = await prefixes.users.find_one({"_id": user_id})
    #if not user:
        #return None
    #else:
        #get_ah = user["prefixesi"]
        #if len(get_ah) == 1 and get_ah[0] == "":
            #return "."
        #return get_ah
        
async def get_pref(user_id):
    user = await prefixes.users.find_one({"_id": user_id})
    if user:
        return user.get("prefixesi")
    else:
        return "."

async def set_pref(user_id, prefix):
    await prefixes.users.update_one(
        {"_id": user_id}, {"$set": {"prefixesi": prefix}}, upsert=True
    )


async def rem_pref(user_id):
    await prefixes.users.update_one(
        {"_id": user_id}, {"$unset": {"prefixesi": ""}}, upsert=True
    )

async def add_approved_user(user_id):
    good_usr = int(user_id)
    does_they_exists = await permitdb.find_one({"user_id": "APPROVED_USERS"})
    if does_they_exists:
        await permitdb.update_one(
            {"user_id": "APPROVED_USERS"}, {"$push": {"good_id": good_usr}}
        )
    else:
        await permitdb.insert_one({"user_id": "APPROVED_USERS", "good_id": [good_usr]})


async def rm_approved_user(user_id):
    bad_usr = int(user_id)
    does_good_ones_exists = await permitdb.find_one({"user_id": "APPROVED_USERS"})
    if does_good_ones_exists:
        await permitdb.update_one(
            {"user_id": "APPROVED_USERS"}, {"$pull": {"good_id": bad_usr}}
        )
    else:
        return None


async def check_user_approved(user_id):
    random_usr = int(user_id)
    does_good_users_exists = await permitdb.find_one({"user_id": "APPROVED_USERS"})
    if does_good_users_exists:
        good_users_list = [
            cool_user for cool_user in does_good_users_exists.get("good_id")
        ]
        if random_usr in good_users_list:
            return True
        else:
            return False
    else:
        return False


async def set_var(user_id, var, value):
    vari = await vardb.find_one({"user_id": user_id, "var": var})
    if vari:
        await vardb.update_one(
            {"user_id": user_id, "var": var}, {"$set": {"vardb": value}}
        )
    else:
        await vardb.insert_one({"user_id": user_id, "var": var, "vardb": value})


async def get_var(user_id, var):
    cosvar = await vardb.find_one({"user_id": user_id, "var": var})
    if not cosvar:
        return None
    else:
        get_cosvar = cosvar["vardb"]
        return get_cosvar


async def del_var(user_id, var):
    cosvar = await vardb.find_one({"user_id": user_id, "var": var})
    if cosvar:
        await vardb.delete_one({"user_id": user_id, "var": var})
        return True
    else:
        return False


async def blacklisted_chats(user_id: int) -> list:
    chats_list = []
    async for chat in blchatdb.users.find({"user_id": user_id, "chat_id": {"$lt": 0}}):
        chats_list.append(chat["chat_id"])
    return chats_list


async def blacklist_chat(user_id: int, chat_id: int) -> bool:
    if not await blchatdb.users.find_one({"user_id": user_id, "chat_id": chat_id}):
        await blchatdb.users.insert_one({"user_id": user_id, "chat_id": chat_id})
        return True
    return False


async def whitelist_chat(user_id: int, chat_id: int) -> bool:
    if await blchatdb.users.find_one({"user_id": user_id, "chat_id": chat_id}):
        await blchatdb.users.delete_one({"user_id": user_id, "chat_id": chat_id})
        return True
    return False


async def save_note(user_id, note_name, message):
    doc = {"_id": user_id, "notes": {note_name: message}}
    result = await notesdb.find_one({"_id": user_id})
    if result:
        await notesdb.update_one(
            {"_id": user_id}, {"$set": {f"notes.{note_name}": message}}
        )
    else:
        await notesdb.insert_one(doc)


async def get_note(user_id, note_name):
    result = await notesdb.find_one({"_id": user_id})
    if result is not None:
        try:
            note_id = result["notes"][note_name]
            return note_id
        except KeyError:
            return None
    else:
        return None


async def rm_note(user_id, note_name):
    await notesdb.update_one({"_id": user_id}, {"$unset": {f"notes.{note_name}": ""}})


async def all_notes(user_id):
    results = await notesdb.find_one({"_id": user_id})
    try:
        notes_dic = results["notes"]
        key_list = notes_dic.keys()
        return key_list
    except:
        return None


async def rm_all(user_id):
    await notesdb.update_one({"_id": user_id}, {"$unset": {"notes": ""}})


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


async def get_expired_date(user_id):
    user = await expdb.users.find_one({"_id": user_id})
    if user:
        return user.get("expire_date")
    else:
        return None


async def set_expired_date(user_id, expire_date):
    await expdb.users.update_one(
        {"_id": user_id}, {"$set": {"expire_date": expire_date}}, upsert=True
    )


async def rem_expired_date(user_id):
    await expdb.users.update_one(
        {"_id": user_id}, {"$unset": {"expire_date": ""}}, upsert=True
    )
