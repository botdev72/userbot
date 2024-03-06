from ubot import ubot, anjay
from pyrogram import *
from pyrogram.types import *
from ubot.utils import get_arg
from ubot.utils.dbfunctions import set_var, del_var, get_var

__MODULE__ = "Settings"
__HELP__ = """
Bantuan Untuk Settings

• Perintah: <code>{0}prefix</code> [trigger]
• Penjelasan: Untuk mengatur handler userbot anda.

• Perintah: <code>{0}setemo</code>
• Penjelasan: Untuk mengubah tampilan emoji Ping.

• Perintah: <code>{0}setemo2</code>
• Penjelasan: Untuk mengubah tampilan emoji Uptime.
"""
