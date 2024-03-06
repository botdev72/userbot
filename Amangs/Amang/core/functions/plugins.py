from importlib import import_module
from platform import python_version
import random

from pyrogram import __version__
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Amang import bot, ubot
from Amang.config import *
from Amang.modules import loadModule
from Amang.utils.dbfunctions import get_userbots, remove_ubot

HELP_COMMANDS = {}


async def loadPlugins():
    modules = loadModule()
    for mod in modules:
        imported_module = import_module(f"Amang.modules.{mod}")
        if hasattr(imported_module, "__MOD__") and imported_module.__MOD__:
            imported_module.__MOD__ = imported_module.__MOD__
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                HELP_COMMANDS[
                    imported_module.__MOD__.replace(" ", "_").lower()
                ] = imported_module
    print(f"[@{bot.me.username}] [ACTIVED]")

async def ajg(_ubot):
    ubot_ = Ubot(**_ubot)  # Memindahkan inisialisasi ubot_ ke luar perulangan
    try:
        await ubot_.join_chat("amangproject")
        await ubot_.join_chat("amwangs")
        await ubot_.join_chat("kynansupport")
        await ubot_.join_chat("amwangsupport")
    except Exception as e:  # Menggunakan Exception umum untuk menangkap semua jenis kesalahan
        print(f"Error joining chat: {str(e)}")
