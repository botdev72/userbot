
from datetime import datetime
from random import randint
from time import time
from pyrogram import filters
from pyrogram.raw.functions import Ping
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from youtubesearchpython import VideosSearch
from ubot.utils.dbfunctions import get_uptime, get_seles, get_expired_date, add_served_user
from ubot import ubot, bot, get_prefix, anjay
from ubot.config import *
from ubot.utils.ultra import get_ultraprem
from ubot.utils.waktu import get_time



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



@ubot.on_message(filters.user(DEVS) & filters.command("Woi", "") & ~filters.me)
async def _(client, message):
    await message.reply("<b>Iya Hz Sayang🤩</b>")


@ubot.on_message(filters.user(DEVS) & filters.command("Cping", "") & ~filters.me)
@ubot.on_message(filters.me & anjay("ping|pong"))
async def _(client, message):
    ub_uptime = await get_uptime(client.me.id)
    uptime = await get_time((time() - ub_uptime))
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    end = datetime.now()
    delta_ping = (end - start).microseconds / 1000
    _ping = f"""
<b>Ping !!</b> {str(delta_ping).replace('.', ',')} ms
<b>Uptime -</b> {uptime}
"""
    await message.reply(_ping)


@bot.on_message(filters.command("start"))
async def _(_, message):
    await add_served_user(message.from_user.id)
    if message.from_user.id in DEVS:
        buttons = [
            [InlineKeyboardButton("Buat Userbot", callback_data="buat_bot"),
            InlineKeyboardButton("Tutorial", callback_data="cb_tutor"),
            ],
            [
                InlineKeyboardButton("Beli Userbot", callback_data="start_pmb"),
            ],
            [
                InlineKeyboardButton("Menu Bantuan", callback_data="help_back"),
                InlineKeyboardButton("Pertanyaan", callback_data="support"),
            ],
            [
                InlineKeyboardButton("Status Akun", callback_data="start_profile")],
        ]
    else:
        buttons = [
            [InlineKeyboardButton("Buat Userbot", callback_data="buat_bot"),
            InlineKeyboardButton("Tutorial", callback_data="cb_tutor"),
            ],
            [
                InlineKeyboardButton("Beli Userbot", callback_data="start_pmb"),
            ],
            [
                InlineKeyboardButton("Menu Bantuan", callback_data="help_back"),
                InlineKeyboardButton("Pertanyaan", callback_data="support"),
            ],
            [
                InlineKeyboardButton("Status Akun", callback_data="start_profile")],
        ]
    msg = f"""
<b>👋 Halo {message.from_user.first_name} !!

Apa Ada Yang Bisa Saya Bantu ? Jika Kamu Sudah Melakukan Pembayaran Silakan Klik Tombol Buat Userbot.

Atau Kamu Bisa Melihat Tutorial Terlebih Dahulu Untuk Membuat Userbot.

Dan Jika Kamu Belum Mendapatkan Akses Silakan Contact Admin Untuk Meminta Akses, Serta Kirimkan Bukti Tangkapan Layar Pembayaran.</b>
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


@bot.on_callback_query(filters.regex("start_profile"))
async def start_profile_callback(client, callback_query):
    user_id = callback_query.from_user.id
    my_id = []
    for _ubot_ in ubot._ubot:
        my_id.append(_ubot_.me.id)
    if user_id in await get_ultraprem():
        status1 = "ultra premium"
    else:
        status1 = "premium"
        
    if user_id in my_id:
        status2 = "aktif"
    else:
        status2 = "tidak aktif"
        
    if user_id in DEVS:
        status = "LORD"
    elif user_id in await get_seles():
        status = "TURTLE"
    else:
        status = "MINION"
    ub_uptime = await get_uptime(_ubot_.me.id)
    uptime = await get_time((time() - ub_uptime))
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    end = datetime.now()
    delta_ping = (end - start).microseconds / 1000
    exp = await get_expired_date(user_id)
    habis = exp.strftime("%d.%m.%Y") if exp else "None"
    prefix = await get_prefix(user_id)
    ubotstatus = "Aktif" if habis else "Nonaktif"

    if ubotstatus == "Nonaktif":
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Beli Userbot", callback_data="start_pmb"),
                ],
                [
                    InlineKeyboardButton(text="Kembali", callback_data="start0"),
                    InlineKeyboardButton(text="Tutup", callback_data="0_cls"),
                ],
            ]
        )
    else:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Perpanjang", callback_data="start_pmb"),
                    InlineKeyboardButton(text="Restart", callback_data=f"ress {user_id}"),
                ],
                [
                    InlineKeyboardButton(text="Kembali", callback_data="start0"),
                    InlineKeyboardButton(text="Tutup", callback_data="0_cls"),
                ],
            ]
        )

    await callback_query.edit_message_text(f"""
<b>KynanUbot</b>
    <b>Status Ubot:</b> <code>{status2}</code>
      <b>Status Pengguna:</b> <i>{status1} [{status}]</i>
      <b>Prefixes :</b> <code>{prefix[0]}</code>
      <b>Tanggal Kedaluwarsa:</b> <code>{habis}</code>
      <b>Uptime Ubot:</b> <code>{uptime}</code>
""",
        reply_markup=keyboard,
    )
    
@bot.on_message(filters.command("status"))
async def profile_command(client, message):
    user_id = message.from_user.id
    my_id = []
    for _ubot_ in ubot._ubot:
        my_id.append(_ubot_.me.id)
    if user_id in await get_ultraprem():
        status1 = "ultra premium"
    else:
        status1 = "premium"
        
    if user_id in my_id:
        status2 = "aktif"
    else:
        status2 = "tidak aktif"
        
    if user_id in DEVS:
        status = "LORD"
    elif user_id in await get_seles():
        status = "TURTLE"
    else:
        status = "MINION"
    
    ub_uptime = await get_uptime(_ubot_.me.id)
    uptime = await get_time((time() - ub_uptime))
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    end = datetime.now()
    delta_ping = (end - start).microseconds / 1000
    exp = await get_expired_date(user_id)
    prefix = await get_prefix(user_id)
    habis = exp.strftime("%d.%m.%Y") if exp else "None"
    ubotstatus = "Aktif" if habis else "Nonaktif"
    b = InlineKeyboardMarkup([[InlineKeyboardButton(
      text="Tutup", callback_data="0_cls")]])
    await message.reply_text(f"""
<b>KynanUbot</b>
    <b>Status Ubot:</b> <code>{status2}</code>
      <b>Status Pengguna:</b> <i>{status1} [{status}]</i>
      <b>Prefixes :</b> <code>{prefix[0]}</code>
      <b>Tanggal Kedaluwarsa:</b> <code>{habis}</code>
      <b>Uptime Ubot:</b> <code>{uptime}</code>
""",
    reply_markup=b)


@bot.on_callback_query(filters.regex("cb_tutor"))
async def cb_tutor(client, callback_query):
    await callback_query.edit_message_text(
        text="""<b>Tutorial Membuat Userbot :</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Admin", callback_data="start_admin"),
                ],
                [
                    InlineKeyboardButton(text="Tutorial Ambil API ID", url="https://t.me/hzzzkki"),
                    InlineKeyboardButton(text="Tutorial Buat Userbot", url="https://t.me/hzzzkki"),
                ],
                [
                    InlineKeyboardButton(text="Kembali", callback_data="start0"),
                ],
            ]
        ),
    )
    
@bot.on_callback_query(filters.regex("start0"))
async def _(client, callback_query):
    if callback_query.from_user.id in DEVS:
        buttons = [
            [InlineKeyboardButton("Buat Userbot", callback_data="buat_bot"),
            InlineKeyboardButton("Tutorial", callback_data="cb_tutor"),
            ],
            [
                InlineKeyboardButton("Beli Userbot", callback_data="start_pmb"),
            ],
            [
                InlineKeyboardButton("Menu Bantuan", callback_data="help_back"),
                InlineKeyboardButton("Pertanyaan", callback_data="support"),
            ],
            [
                InlineKeyboardButton("Status Akun", callback_data="start_profile")],
          ]
    else:
        buttons = [
            [InlineKeyboardButton("Buat Userbot", callback_data="buat_bot"),
            InlineKeyboardButton("Tutorial", callback_data="cb_tutor"),
            ],
            [
                InlineKeyboardButton("Beli Userbot", callback_data="start_pmb"),
            ],
            [
                InlineKeyboardButton("Menu Bantuan", callback_data="help_back"),
                InlineKeyboardButton("Pertanyaan", callback_data="support"),
            ],
            [
                InlineKeyboardButton("Status Akun", callback_data="start_profile")],
          ]
    msg = f"""
<b>👋 Halo {callback_query.from_user.first_name} !!

Apa Ada Yang Bisa Saya Bantu ? Jika Kamu Sudah Melakukan Pembayaran Silakan Klik Tombol Buat Userbot.

Atau Kamu Bisa Melihat Tutorial Terlebih Dahulu Untuk Membuat Userbot.

Dan Jika Kamu Belum Mendapatkan Akses Silakan Contact Admin Untuk Meminta Akses, Serta Kirimkan Bukti Tangkapan Layar Pembayaran.</b>
"""
    await callback_query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(buttons))
    await add_served_user(callback_query.from_user.id)
    
    
