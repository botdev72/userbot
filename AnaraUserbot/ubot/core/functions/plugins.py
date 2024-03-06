from importlib import import_module
from platform import python_version

from pyrogram import __version__
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ubot import bot, ubot
from ubot.config import SKY
from ubot.modules import loadModule

HELP_COMMANDS = {}


async def loadPlugins():
    modules = loadModule()
    for mod in modules:
        imported_module = import_module(f"sky.modules.{mod}")
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            imported_module.__MODULE__ = imported_module.__MODULE__
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                HELP_COMMANDS[
                    imported_module.__MODULE__.replace(" ", "_").lower()
                ] = imported_module
    print(f"[🤖 @{bot.me.username} 🤖] [🔥 BERHASIL DIAKTIFKAN! 🔥]")
    await bot.send_message(
        SKY,
        f"""
<b>🔥 {bot.me.mention} Berhasil Diaktifkan</b>
<b>📘 Python: {python_version()}</b>
<b>📙 Pyrogram: {__version__}</b>
<b>👮‍♂ User: {len(ubot._ubot)}</b>
""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🗑 TUTUP 🗑", callback_data="0_cls")]],
        ),
    )
