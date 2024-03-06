from Amang.config import OWNER
from Amang.utils.dbfunctions import *


async def premium():
    if OWNER not in await get_seles():
        await add_seles(OWNER)
    if OWNER not in await get_prem():
        await add_prem(OWNER)
    if OWNER not in await get_ultraprem():
        await add_ultraprem(OWNER)
