import asyncio
import requests
from pyrogram import *
from pyrogram.errors.exceptions.flood_420 import FloodWait
from pyrogram.types import *
from ubot.utils.http import *
from ubot import *
from ubot.utils import MEMES, eor, get_text

__MODULE__ = "Salam"
__HELP__ = """
Bantuan Untuk Salam


• Perintah: <code>{0}p</code>
• Penjelasan: Coba aja sendiri.

• Perintah: <code>{0}pe</code>
• Penjelasan: Coba aja sendiri.

• Perintah: <code>{0}l</code>
• Penjelasan: Coba aja sendiri.

• Perintah: <code>{0}el</code>
• Penjelasan: Coba aja sendiri.

• Perintah: <code>{0}as</code>
• Penjelasan: Coba aja sendiri.

"""


@KY.UBOT("p")
async def salamone(client: Client, message: Message):
    await message.edit(
            "Assalamualaikum Sayang.",
    )


@KY.UBOT("pe")
async def salamdua(client: Client, message: Message):
    await message.edit(
            "Assalamualaikum Warahmatullahi Wabarakatuh",
    )


@KY.UBOT("l")
async def jwbsalam(client: Client, message: Message):
    await message.edit(
            "Wa'alaikumsalam Kaum Dajjal...",
    )


@KY.UBOT("el")
async def jwbsalamlngkp(client: Client, message: Message):
    await message.edit(
            "Wa'alaikumsalam Warahmatullahi Wabarakatuh",
    )



@KY.UBOT("as")
async def salamarab(client: Client, message: Message):
    xx = await message.edit("Salam Dulu Gua..")
    await asyncio.sleep(2)
    await xx.edit("السَّلاَمُ عَلَيْكُمْ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ")
