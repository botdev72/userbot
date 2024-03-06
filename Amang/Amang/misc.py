from Amang.config import OWNER
from Amang.utils.dbfunctions import add_prem, add_seles, get_prem, get_seles


async def premium():
    if OWNER not in await get_seles():
        await add_seles(OWNER)
    if OWNER not in await get_prem():
        await add_prem(OWNER)