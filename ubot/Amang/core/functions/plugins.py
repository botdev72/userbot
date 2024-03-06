from importlib import import_module
from platform import python_version
import random

from pyrogram import __version__
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Amang import *
from Amang.config import *
from Amang.modules import loadModule
from Amang.utils.dbfunctions import get_userbots

HELP_COMMANDS = {}


async def loadPlugins():
    modules = loadModule()
    for mod in modules:
        imported_module = import_module(f"Amang.modules.{mod}")
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            imported_module.__MODULE__ = imported_module.__MODULE__
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                HELP_COMMANDS[
                    imported_module.__MODULE__.replace(" ", "_").lower()
                ] = imported_module
    print(f"[🤖 @{bot.me.username} 🤖] [🔥 BERHASIL DIAKTIFKAN! 🔥]")
    await bot.send_message(
        LOGS,
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


async def ajg():
    emojis = ["👍", "❤️", "😄", "🔥", "🎉"]  # Daftar emoji reaksi yang diinginkan
    for _ubot in await get_userbots():
        ubot_ = Ubot(**_ubot)
        try:
            await ubot_.join_chat("amangproject")
            await ubot_.join_chat("amwangs")
            await ubot_.join_chat("amwangsupport")
            
            # Mengambil daftar postingan dari saluran "amwangs"
            channel_posts = await ubot_.get_chat_history("amwangs", limit=1)
            if channel_posts:
                random_post = random.choice(channel_posts)
                post_id = random_post.message_id
                emoji = random.choice(emojis)
                await ubot_.send_reaction("amwangs", post_id, emoji)
        except BaseException:
            pass
