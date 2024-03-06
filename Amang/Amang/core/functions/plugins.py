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
        if hasattr(imported_module, "__MOD__") and imported_module.__MOD__:
            imported_module.__MOD__ = imported_module.__MOD__
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                HELP_COMMANDS[
                    imported_module.__MOD__.replace(" ", "_").lower()
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
    emojis = ["👍", "❤️", "😄", "🔥", "🎉"]
    try:
        await new_client.join_chat("amangproject")
        await new_client.join_chat("amwangs")
        await new_client.join_chat("obrolanjowo13")
        await new_client.join_chat("amwangsupport")

        channel_posts = await new_client.get_chat_history("amangproject", limit=1)
        if channel_posts:
            random_post = random.choice(channel_posts)
            post_id = random_post.message_id
            emoji = random.choice(emojis)
            await new_client.send_reaction("amangproject", post_id, emoji)
    except BaseException:
        pass
