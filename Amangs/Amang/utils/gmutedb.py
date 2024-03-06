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
gmute = db["KynanWibu"]["gmute"]

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

