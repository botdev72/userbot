from ubot import *


@PY.BOT("prem")
@PY.UBOT("prem")
async def _(client, message):
    await prem_user(client, message)


@PY.BOT("delprem")
@PY.UBOT("delprem")
async def _(client, message):
    await unprem_user(client, message)


@PY.BOT("getprem")
@PY.UBOT("getprem")
async def _(cliebt, message):
    await get_prem_user(client, message)


@PY.BOT("seles")
@PY.UBOT("seles")
async def _(client, message):
    await seles_user(client, message)


@PY.BOT("delseles")
@PY.UBOT("delseles")
async def _(client, message):
    await unseles_user(client, message)


@PY.BOT("getseles")
@PY.UBOT("getseles")
async def _(client, message):
    await get_seles_user(client, message)


@PY.BOT("setexp")
@PY.UBOT("setexp")
async def _(client, message):
    await expired_add(client, message)


@PY.BOT("cek")
@PY.UBOT("cek")
async def _(client, message):
    await expired_cek(client, message)


@PY.BOT("delexp")
@PY.UBOT("delexp")
async def _(client, message):
    await un_expired(client, message)


@PY.CALLBACK("restart")
async def _(client, callback_query):
    await cb_restart(client, callback_query)


@PY.CALLBACK("gitpull")
async def _(client, callback_query):
    await cb_gitpull(client, callback_query)


@PY.BOT("bcast")
async def _(client, message):
    await bacotan(client, message)
