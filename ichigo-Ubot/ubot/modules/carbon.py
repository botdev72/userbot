from ubot import *


@PY.UBOT("carbon", sudo=True)
async def _(client, message):
    await carbon_func(client, message)
