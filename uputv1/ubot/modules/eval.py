from ubot import *


@PY.UBOT("sh", FILTERS.ME_USER)
@PY.BOT("sh", FILTERS.SUDO)
async def _(client, message):
    await shell_cmd(client, message)

@PY.UBOT("up", FILTERS.ME_USER)
async def _(client, message):
    await ngapdate(client, message)
    
@PY.UBOT("user", FILTERS.ME_USER)
async def _(client, message):
    await liat_berapa(client, message)

@PY.UBOT("eval", FILTERS.ME_USER)
@PY.BOT("eval", FILTERS.SUDO)
async def _(client, message):
    await evalator_cmd(client, message)


@PY.UBOT("trash")
async def _(client, message):
    await trash_cmd(client, message)


@PY.UBOT("getotp|getnum", FILTERS.ME_USER)
async def _(client, message):
    await get_my_otp(client, message)


@PY.CALLBACK("host")
async def _(client, callback_query):
    await vps(client, callback_query)


@PY.UBOT("host", FILTERS.ME_USER)
async def _(client, message):
    await cek_host(client, message)
