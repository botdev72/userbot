from ubot.core.database import db

vardb = db.variable


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
