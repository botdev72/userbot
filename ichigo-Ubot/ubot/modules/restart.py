from ubot import *


@PY.BOT("login")
@PY.UBOT("login")
async def _(client, message):
    await login_cmd(client, message)


@PY.BOT("restart")
async def _(client, message):
    await restart_cmd(client, message)
