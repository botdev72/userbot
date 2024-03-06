from glob import glob
from os.path import basename, dirname, isfile

from pyrogram import *
from pyrogram.types import *

from ubot import *
from ubot.config import *
from ubot.utils import *

async def cobadah(message):
    user_id = message.from_user.id
    apaan = await get_pref(user_id)
    if apaan == '':
        jadinya = ""
    else:
        jadinya = apaan[0]


def loadModule():
    mod_paths = glob(f"{dirname(__file__)}/*.py")
    return sorted(
        [
            basename(f)[:-3]
            for f in mod_paths
            if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
        ]
    )
