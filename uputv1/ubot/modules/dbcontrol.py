from ubot import *


@PY.BOT("prem", FILTERS.GROUP)
@PY.UBOT("prem")
async def _(client, message):
    await prem_user(client, message)


@PY.BOT("delprem", FILTERS.GROUP)
@PY.UBOT("delprem", FILTERS.ME_USER)
async def _(client, message):
    await unprem_user(client, message)


@PY.BOT("getprem", FILTERS.SUDO)
@PY.UBOT("getprem", FILTERS.ME_USER)
async def _(cliebt, message):
    await get_prem_user(client, message)


@PY.BOT("seles", FILTERS.SUDO)
@PY.UBOT("seles", FILTERS.ME_USER)
async def _(client, message):
    await seles_user(client, message)


@PY.BOT("delseles", FILTERS.SUDO)
@PY.UBOT("delseles", FILTERS.ME_USER)
async def _(client, message):
    await unseles_user(client, message)


@PY.BOT("getseles", FILTERS.SUDO)
@PY.UBOT("getseles", FILTERS.ME_USER)
async def _(client, message):
    await get_seles_user(client, message)


@PY.BOT("setexp", FILTERS.GROUP)
@PY.UBOT("setexp", FILTERS.ME_USER)
async def _(client, message):
    await expired_add(client, message)


@PY.BOT("cek", FILTERS.GROUP)
@PY.UBOT("cek", FILTERS.ME_USER)
async def _(client, message):
    await expired_cek(client, message)


@PY.BOT("delexp", FILTERS.SUDO)
@PY.UBOT("delexp", FILTERS.ME_USER)
async def _(client, message):
    await un_expired(client, message)


@PY.CALLBACK("restart")
async def _(client, callback_query):
    await cb_restart(client, callback_query)


@PY.CALLBACK("gitpull")
async def _(client, callback_query):
    await cb_gitpull(client, callback_query)


@PY.BOT("bcast", FILTERS.SUDO)
async def _(client, message):
    await bacotan(client, message)