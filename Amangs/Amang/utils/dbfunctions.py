import codecs
import pickle
from typing import Dict, List, Union
import random

from motor.motor_asyncio import AsyncIOMotorClient as MongoClient

from Amang import *
from Amang.config import MONGO_URL


pilih_acak = random.choice(MONGO_URL)
mongo = MongoClient(pilih_acak)

db = mongo.ubot
ubotdb = db.ubot
vardb = db["var"]
sudoersdb = db.sudoers
chatsdb = db.chats
logdb = db.gruplog
userdb = db.users
blchatdb = db.blchat
chatdb = db.chatdb
resell = db.seles
notesdb = db.notes
pmdb = db["antipms"]
bacotdb = db.bacotdb
userEXP = mongo["ubot"]["users"]
prefdb = db["jembi"]
ultrapremdb = db["KynanWibu"]["ultraprem"]
akseserdb = db["akseser"]
aktif = db["plernya"]["uptime"]

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


async def get_pref(user_id):
    user = await prefdb.users.find_one({"_id": user_id})
    if user:
        return user.get("prefix")
    else:
        return None


async def set_pref(user_id, prefix):
    await prefdb.users.update_one(
        {"_id": user_id}, {"$set": {"prefix": prefix}}, upsert=True
    )


async def rem_pref(user_id):
    await prefdb.users.update_one(
        {"_id": user_id}, {"$unset": {"prefix": ""}}, upsert=True
    )


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


async def buat_log():
    botlog_chat_id = None
    for _ubot in await get_userbots():
        ubot_ = Ubot(**_ubot)
    try:
        if ubot_.is_connected:
            await ubot_.disconnect()
        else:
            ubot_.in_memory = False
            await ubot_.start()
        try:
            user = await ubot_.get_me()
            user_id = user.id
            user_data = await userdb.users.find_one({"user_id": user_id})
            botlog_chat_id = None

            if user_data:
                botlog_chat_id = user_data.get("bot_log_group_id")

            if not user_data or not botlog_chat_id:
                group_name = "Amang Premium Logs"
                group_description = "Jangan Hapus Atau Keluar Dari Grup Ini\n\nCreated By @amwangsupport .\nJika menemukan kendala atau ingin menanyakan sesuatu\nHubungi : @amwang atau bisa ke @amwangsupport."
                group = await ubot_.create_supergroup(group_name, group_description)
                botlog_chat_id = group.id
                photo = "Amang/resources/logo.jpg"
                await ubot_.set_chat_photo(botlog_chat_id, photo=photo)
                message_text = f"Grup Log Berhasil Dibuat,\nKetik `{cmd[0]}setlog` untuk menentapkan grup log ini sebagai tempat log bot\n"
                await set_botlog(user_id, botlog_chat_id)
                await asyncio.sleep(2)
                await ubot_.send_message(botlog_chat_id, message_text)
                await asyncio.sleep(1)

                await userdb.users.update_one(
                    {"user_id": user_id},
                    {"$set": {"bot_log_group_id": botlog_chat_id}},
                    upsert=True,
                )
        except Exception as a:
            LOGGER("Info").info(f"{a}")

    except Exception as e:
        LOGGER("X").info(f"{e}")

    if botlog_chat_id is None:
        return None

    return int(botlog_chat_id)


async def get_botlog(user_id: int):
    user_data = await logdb.users.find_one({"user_id": user_id})
    botlog_chat_id = user_data.get("bot_log_group_id") if user_data else None
    return botlog_chat_id


async def set_botlog(user_id: int, botlog_chat_id: int):
    await logdb.users.update_one(
        {"user_id": user_id},
        {"$set": {"bot_log_group_id": botlog_chat_id}},
        upsert=True,
    )


async def get_log_groups(user_id: int):
    user_data = await logdb.users.find_one({"user_id": user_id})
    botlog_chat_id = user_data.get("bot_log_group_id") if user_data else []
    return botlog_chat_id


def obj_to_str(obj):
    if not obj:
        return False
    string = codecs.encode(pickle.dumps(obj), "base64").decode()
    return string


def str_to_obj(string: str):
    obj = pickle.loads(codecs.decode(string.encode(), "base64"))
    return obj


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

async def bacotan(user_id: int) -> list:
    cot = []
    async for chat in chatdb.users.find({"user_id": user_id, "chat_id": {"$lt": 0}}):
        cot.append(chat["chat_id"])
    return cot


async def add_bacot(user_id: int, chat_id: int) -> bool:
    if not await chatdb.users.find_one({"user_id": user_id, "chat_id": chat_id}):
        await chatdb.users.insert_one({"user_id": user_id, "chat_id": chat_id})
        return True
    return False


async def del_bacot(user_id: int, chat_id: int) -> bool:
    if await chatdb.users.find_one({"user_id": user_id, "chat_id": chat_id}):
        await chatdb.users.delete_one({"user_id": user_id, "chat_id": chat_id})
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
            await message.reply_text("Maaf, fitur ini hanya tersedia pada versi Super Premium.")
            return
        await func(client, message)
    return wrapper


async def get_akses():
    akseser = await akseserdb.find_one({"akses": "akses"})
    if not akseser:
        return []
    return akseser["akseser"]


async def add_akses(user_id):
    akseser = await get_akses()
    akseser.append(user_id)
    await akseserdb.update_one(
        {"akses": "akses"}, {"$set": {"akseser": akseser}}, upsert=True
    )
    return True


async def remove_akses(user_id):
    akseser = await get_akses()
    akseser.remove(user_id)
    await akseserdb.update_one(
        {"akses": "akses"}, {"$set": {"akseser": akseser}}, upsert=True
    )
    return True
