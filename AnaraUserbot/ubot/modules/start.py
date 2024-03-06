import time
from datetime import datetime
from random import randint

from pyrogram import filters
from pyrogram.raw.functions import Ping
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from youtubesearchpython import VideosSearch
from ubot.utils import anjay
from ubot import bot, ubot
from ubot.config import DEVS, SKY, OWNER_ID

START_TIME = datetime.utcnow()
TIME_DURATION_UNITS = (
    ("w", 60 * 60 * 24 * 7),
    ("d", 60 * 60 * 24),
    ("h", 60 * 60),
    ("m", 60),
    ("s", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append(f'{amount}{unit}{"" if amount == 1 else ""}')
    return ":".join(parts)


def YouTube_Search(query):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        id = data["id"]
        songname = data["title"]
        duration = data["duration"]
        url = f"https://youtu.be/{id}"
        views = data["viewCount"]["text"]
        channel = data["channel"]["name"]
        thumbnail = data["thumbnails"][0]["url"].split("?")[0]
        return [id, songname, duration, url, views, channel, thumbnail]
    except Exception as e:
        print(e)
        return e


@ubot.on_message(filters.user(DEVS) & filters.command("Absen", "") & ~filters.me)
async def _(client, message):
    await message.reply("<b>Mmuuaahh😘</b>")


@ubot.on_message(filters.user(DEVS) & filters.command("Naya", "") & ~filters.me)
async def _(client, message):
    await message.reply("<b>Iya Naya Punya Nya Kynan🤩</b>")



@ubot.on_message(filters.user(DEVS) & filters.command("Cping", "") & ~filters.me)
@ubot.on_message(filters.me & anjay("ping"))
async def _(client, message):
    start = time.time()
    current_time = datetime.utcnow()
    await client.invoke(Ping(ping_id=randint(0, 2147483647)))
    delta_ping = round((time.time() - start) * 1000, 3)
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    _ping = f"""
<b>❏ Ping !!</b> {delta_ping} ms
<b>╰ Aktif:</b> {uptime}
"""
    await message.reply(_ping)


@bot.on_message(filters.command("start"))
async def _(_, message):
    if "InfoLagu" in message.text:
        return
    if message.from_user.id in DEVS:
        buttons = [
            [InlineKeyboardButton("Buat Userbot", callback_data="buat_bot")],
            [
                InlineKeyboardButton("Menu Bantuan", callback_data="help_back"),
                InlineKeyboardButton("Pertanyaan", callback_data="support"),
            ],
        ]
    else:
        buttons = [
            [InlineKeyboardButton("Buat Userbot", callback_data="buat_bot")],
            [
                InlineKeyboardButton("Beli Userbot", callback_data="start_pmb"),
            ],
            [
                InlineKeyboardButton("Menu Bantuan", callback_data="help_back"),
                InlineKeyboardButton("Pertanyaan", callback_data="support"),
            ],
        ]
    msg = f"""
<b>👋 Halo {message.from_user.first_name}
💭 Apa ada yang bisa saya bantu ? 💡 Jika ingin membuat bot . Kamu bisa klik tombol Buat Userbot atau Hubungi Admin Untuk Meminta Akses.</b>
"""
    await message.reply(msg, reply_markup=InlineKeyboardMarkup(buttons))
    if message.from_user.id in DEVS:
        return
    else:
        buttons = [
            [
                InlineKeyboardButton(
                    "👤 Profil", callback_data=f"profil {message.from_user.id}"
                ),
                InlineKeyboardButton(
                    "Jawab 💬", callback_data=f"jawab_pesan {message.from_user.id}"
                ),
            ],
        ]
        await bot.send_message(
            OWNER_ID,
            f"<a href=tg://openmessage?user_id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>",
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@bot.on_callback_query(filters.regex("0_cls"))
async def now(_, cq):
    await cq.message.delete()
