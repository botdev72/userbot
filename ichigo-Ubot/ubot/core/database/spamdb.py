from ubot.core.database import db

from typing import List

spamgc = db.spamgcdb
gcastdb = db.gcastandb
katagikesdb = db.katagikes
rndmgikesdb = db.rndmteks


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