import codecs
import pickle
from typing import List

from motor.motor_asyncio import AsyncIOMotorClient as MongoClient

from ubot import MONGO_URL

mongo = MongoClient(MONGO_URL)

db = mongo.UbotGcast

ubotdb = db.ubot
sudoersdb = db.sudoers
blchatdb = db.blchat
resell = db.seles
notesdb = db.notes
permitdb = db.pmguard
vardb = db.variable
expdb = db.expired
prefixes = db.prefix
bacotdb = db.bacotdb
blockeddb = db.gbans
aktif = db.uptime
getopt = db.twofactor
osnyadb = db.osnya
logrupdb = db.logger
spamgc = db.spamgcdb
gcastdb = db.gcastandb
katagikesdb = db.katagikes
rndmgikesdb = db.rndmteks


def obj_to_str(obj):
    return codecs.encode(pickle.dumps(obj), "base64").decode() if obj else False


def str_to_obj(string: str):
    return pickle.loads(codecs.decode(string.encode(), "base64"))


async def ambil_jumlah_rndm() -> dict:
    orang_nya = 0
    rndm_nya = 0
    async for org in rndmgikesdb.find({"orang": {"$lt": 0}}):
        rndmm = await daftar_rndm(org["orang"])
        rndm_nya += len(rndmm)
        orang_nya += 1
    return {
        "orang_nya": orang_nya,
        "rndm_nya": rndm_nya,
    }


async def daftar_rndm(orang: int) -> List[str]:
    _rndmm = await rndmgikesdb.find_one({"orang": orang})
    return [] if not _rndmm else _rndmm["rndmm"]


async def tambah_rndm(orang: int, rndm: str):
    rndm = rndm.lower().strip()
    _rndmm = await daftar_rndm(orang)
    _rndmm.append(rndm)
    await rndmgikesdb.update_one(
        {"orang": orang},
        {"$set": {"rndmm": _rndmm}},
        upsert=True,
    )


async def kureng_rndm(orang: int, rndm: str) -> bool:
    rndmmd = await daftar_rndm(orang)
    rndm = rndm.lower().strip()
    if rndm in rndmmd:
        rndmmd.remove(rndm)
        await rndmgikesdb.update_one(
            {"orang": orang},
            {"$set": {"rndmm": rndmmd}},
            upsert=True,
        )
        return True
    return False


async def ambil_jumlah_kata() -> dict:
    orang_nya = 0
    kata_nya = 0
    async for org in katagikesdb.find({"orang": {"$lt": 0}}):
        katax = await ambil_daftar(org["orang"])
        kata_nya += len(katax)
        orang_nya += 1
    return {
        "orang_nya": orang_nya,
        "kata_nya": kata_nya,
    }


async def ambil_daftar(orang: int) -> List[str]:
    _katax = await katagikesdb.find_one({"orang": orang})
    return [] if not _katax else _katax["katax"]


async def tambah_kata(orang: int, kata: str):
    kata = kata.lower().strip()
    _katax = await ambil_daftar(orang)
    _katax.append(kata)
    await katagikesdb.update_one(
        {"orang": orang},
        {"$set": {"katax": _katax}},
        upsert=True,
    )


async def kureng_kata(orang: int, kata: str) -> bool:
    kataxd = await ambil_daftar(orang)
    kata = kata.lower().strip()
    if kata in kataxd:
        kataxd.remove(kata)
        await katagikesdb.update_one(
            {"orang": orang},
            {"$set": {"katax": kataxd}},
            upsert=True,
        )
        return True
    return False


async def ambil_gcs(user_id):
    sch = await gcastdb.find_one({"chat_id": user_id})
    if not sch:
        return []
    return sch["list"]


async def tambah_gcs(user_id, chat_id):
    list = await ambil_gcs(user_id)
    list.append(chat_id)
    await gcastdb.update_one(
        {"chat_id": user_id}, {"$set": {"list": list}}, upsert=True
    )
    return True


async def kureng_gcs(user_id, chat_id):
    list = await ambil_gcs(user_id)
    list.remove(chat_id)
    await gcastdb.update_one(
        {"chat_id": user_id}, {"$set": {"list": list}}, upsert=True
    )
    return True


async def ambil_spgc(user_id):
    sch = await spamgc.find_one({"chat_id": user_id})
    if not sch:
        return []
    return sch["list"]


async def tambah_spgc(user_id, chat_id):
    list = await ambil_spgc(user_id)
    list.append(chat_id)
    await spamgc.update_one({"chat_id": user_id}, {"$set": {"list": list}}, upsert=True)
    return True


async def kureng_spgc(user_id, chat_id):
    list = await ambil_spgc(user_id)
    list.remove(chat_id)
    await spamgc.update_one({"chat_id": user_id}, {"$set": {"list": list}}, upsert=True)
    return True


async def get_log_group(user_id: int) -> bool:
    cek = await logrupdb.find_one({"user_id": user_id})
    if not cek:
        return None
    return cek["logger"]


async def set_log_group(user_id: int, logger):
    cek = await get_log_group(user_id)
    if cek:
        await logrupdb.update_one({"user_id": user_id}, {"$set": {"logger": logger}})
    else:
        await logrupdb.insert_one({"user_id": user_id, "logger": logger})


async def del_log_group(user_id: int):
    await logrupdb.delete_one({"user_id": user_id})


async def get_osnya(user_id):
    osnya = await osnyadb.find_one({"osnya": user_id})
    if not osnya:
        return []
    return osnya["list"]


async def add_osnya(user_id):
    list = await get_osnya(user_id)
    list.append(user_id)
    await osnyadb.update_one({"osnya": user_id}, {"$set": {"list": list}}, upsert=True)
    return True


async def remove_osnya(user_id):
    list = await get_osnya(user_id)
    list.remove(user_id)
    await osnyadb.update_one({"osnya": user_id}, {"$set": {"list": list}}, upsert=True)
    return True


async def get_two_factor(user_id):
    user = await getopt.users.find_one({"_id": user_id})
    if user:
        return user.get("twofactor")
    else:
        return None


async def set_two_factor(user_id, twofactor):
    await getopt.users.update_one(
        {"_id": user_id}, {"$set": {"twofactor": twofactor}}, upsert=True
    )


async def rem_two_factor(user_id):
    await getopt.users.update_one(
        {"_id": user_id}, {"$unset": {"twofactor": ""}}, upsert=True
    )


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
    does_they_exists = await permitdb.users.find_one({"user_id": "setujui"})
    if does_they_exists:
        await permitdb.users.update_one(
            {"user_id": "setujui"}, {"$push": {"good_id": good_usr}}
        )
    else:
        await permitdb.users.insert_one({"user_id": "setujui", "good_id": [good_usr]})


async def rm_approved_user(user_id):
    bad_usr = int(user_id)
    does_good_ones_exists = await permitdb.users.find_one({"user_id": "setujui"})
    if does_good_ones_exists:
        await permitdb.users.update_one(
            {"user_id": "setujui"}, {"$pull": {"good_id": bad_usr}}
        )
    else:
        return None


async def check_user_approved(user_id):
    random_usr = int(user_id)
    does_good_users_exists = await permitdb.users.find_one({"user_id": "setujui"})
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


async def set_var(orang, nama_var, value, query="datanya"):
    update_data = {"$set": {f"{query}.{nama_var}": value}}
    await vardb.update_one({"_id": orang}, update_data, upsert=True)


async def get_var(orang, nama_var, query="datanya"):
    result = await vardb.find_one({"_id": orang})
    return result.get(query, {}).get(nama_var, None) if result else None


async def remove_var(orang, nama_var, query="datanya"):
    hapus_data = {"$unset": {f"{query}.{nama_var}": ""}}
    await vardb.update_one({"_id": orang}, hapus_data)


async def all_var(user_id, query="datanya"):
    result = await vardb.find_one({"_id": user_id})
    return result.get(query) if result else None


async def rmall_var(orang):
    await vardb.delete_one({"_id": orang})


async def ambil_list_var(user_id, nama_var, query="datanya"):
    data_ = await get_var(user_id, nama_var, query)
    return [int(x) for x in str(data_).split()] if data_ else []


async def add_var(user_id, nama_var, value, query="datanya"):
    list_data = await ambil_list_var(user_id, nama_var, query)
    list_data.append(value)
    await set_var(user_id, nama_var, " ".join(map(str, list_data)), query)


async def rem_var(user_id, nama_var, value, query="datanya"):
    list_data = await ambil_list_var(user_id, nama_var, query)
    if value in list_data:
        list_data.remove(value)
        await set_var(user_id, nama_var, " ".join(map(str, list_data)), query)


async def get_chat(user_id):
    chat = await blchatdb.find_one({"chat": user_id})
    if not chat:
        return []
    return chat["list"]


async def add_chat(user_id, chat_id):
    list = await get_chat(user_id)
    list.append(chat_id)
    await blchatdb.update_one({"chat": user_id}, {"$set": {"list": list}}, upsert=True)
    return True


async def remove_chat(user_id, chat_id):
    list = await get_chat(user_id)
    list.remove(chat_id)
    await blchatdb.update_one({"chat": user_id}, {"$set": {"list": list}}, upsert=True)
    return True


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
