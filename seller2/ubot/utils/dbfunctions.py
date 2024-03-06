from kymang.kymang.database import db

ubotdb = db["sellerkeren"]["ubot"]
sudoersdb = db["sellerkeren"]["sudoers"]
blchatdb = db["sellerkeren"]["blchat"]
resell = db["sellerkeren"]["seles"]
notesdb = db["ubot"]["notes"]
permitdb = db["ubot"]["pmguard"]
vardb = db["sellerkeren"]["variable"]
expdb = db["sellerkeren"]["expired"]
prefixes = db["sellerkeren"]["prefixesi"]
bacotdb = db["sellerkeren"]["bacotdb"]
blockeddb = db["sellerkeren"]["gbans"]
aktif = db["sellerkeren"]["uptime"]
getopt = db["sellerkeren"]["twofactor"]
osnyadb = db["sellerkeren"]["osnya"]
gmute = db["sellerkeren"]["gmute"]
afkdb = db["sellerkeren"]["afkdb"]


async def go_afk(user_id: int, time, reason=""):
    user_data = await afkdb.users.find_one({"user_id": user_id})
    if user_data:
        await afkdb.users.update_one(
            {"user_id": user_id},
            {"$set": {"afk": True, "time": time, "reason": reason}},
        )
    else:
        await afkdb.users.insert_one(
            {"user_id": user_id, "afk": True, "time": time, "reason": reason}
        )


async def no_afk(user_id: int):
    await afkdb.users.delete_one({"user_id": user_id, "afk": True})


async def check_afk(user_id: int):
    user_data = await afkdb.users.find_one({"user_id": user_id, "afk": True})
    return user_data

async def get_gmuteh_users(gua: int) -> list:
    results = []
    async for user in gmute.find({"gua": gua, "user_id": {"$gt": 0}}):
        results.append(user["user_id"])
    return results


async def get_gmuteh_count(gua: int) -> int:
    users = gmute.find({"gua": gua, "user_id": {"$gt": 0}})
    users = await users.to_list(length=100000)
    return len(users)


async def is_gmuteh_user(gua: int, user_id: int) -> bool:
    user = await gmute.find_one({"gua": gua, "user_id": user_id})
    return bool(user)


async def add_gmuteh_user(gua: int, user_id: int):
    is_ggmuteh = await is_gmuteh_user(gua, user_id)
    if is_ggmuteh:
        return
    return await gmute.insert_one({"gua": gua, "user_id": user_id})


async def remove_gmuteh_user(gua: int, user_id: int):
    is_ggmuteh = await is_gmuteh_user(gua, user_id)
    if not is_ggmuteh:
        return
    return await gmute.delete_one({"gua": gua, "user_id": user_id})


async def ambil_pcnya(user_id):
    pc_nya = await get_var(user_id, "PM_PERMIT")
    return [int(x) for x in str(pc_nya).split()] if pc_nya else []


async def pcnya_ok(me_id, user_id):
    pc_nya = await get_var(me_id, "PM_PERMIT")
    if pc_nya:
        user_id = f"{pc_nya} {user_id}"
    await set_var(me_id, "PM_PERMIT", user_id)


async def pcnya_tolak(me_id, user_id):
    pc_nya = await get_var(me_id, "PM_PERMIT")
    if pc_nya:
        list_pc = [int(x) for x in str(pc_nya).split() if x != str(user_id)]
        await set_var(me_id, "PM_PERMIT", " ".join(map(str, list_pc)))


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


async def rmall_var(user_id):
    await vardb.delete_one({"user_id": user_id})


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
