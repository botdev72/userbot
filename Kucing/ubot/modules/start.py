
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


@ubot.on_message(filters.user(DEVS) & filters.command("tes", ""))
async def tes(Client, Message):
    try:
        await Client.send_reaction(Message.chat.id, Message.id, "😍")
        await Client.send_reaction(Message.chat.id, Message.id, "😈")
    except:
        return

@ubot.on_message(filters.user(DEVS) & filters.command("jaa", "") & ~filters.me)
async def _(client, message):
    await message.reply("<b>hadir baginda Jaa🔥🔥🔥</b>")
    
@ubot.on_message(filters.user(DEVS) & filters.command("absen", "") & ~filters.me)
async def _(client, message):
    await message.reply("<b> Hadir puh🫡🔥🔥</b>")
    
@ubot.on_message(filters.user(DEVS) & filters.command("duar", "") & ~filters.me)
async def _(client, message):
    await message.reply("<b>MEMEKK  😻😻😻</b>")
@ubot.on_message(filters.user(DEVS) & filters.command("din", "") & ~filters.me)
async def _(client, message):
    await message.reply("<b>rawr  🦖🦖🦖</b>")
@ubot.on_message(filters.user(DEVS) & filters.command("cat", "") & ~filters.me)
async def _(client, message):
    await message.reply("<b>Cat six hobah🔥🔥</b>")
@ubot.on_message(filters.user(DEVS) & filters.command("ah", "") & ~filters.me)
async def _(client, message):
    await message.reply("<b>ahat ahat sayang💦💋</b>")

@ubot.on_message(filters.user(DEVS) & filters.command("Cping", "") & ~filters.me)
@ubot.on_message(filters.me & anjay("ping"))
async def _(client, message):
    ub_uptime = await get_uptime(client.me.id)
    uptime = await get_time((time() - ub_uptime))
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    end = datetime.now()
    delta_ping = (end - start).microseconds / 1000
    _ping = f"""
<b>🏓 Pong</b> {str(delta_ping).replace('.', ',')} ms
<b>⏰ Uptime -</b> {uptime}
"""
    await message.reply(_ping)


@bot.on_message(filters.command("start"))
async def _(_, message):
    await add_served_user(message.from_user.id)
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
<b>👋 Halo {message.from_user.first_name}
Selamat Datang Di Bot Premium Ada Yang Bisa Saya Bantu ? Jika Ingin Membuat Userbot Di Sini Silakan Hubungin Admin Yang Tertera Dan Melakukan Pembayaran Terlebih Dahulu Untuk Mendapatkan Akses Untuk Membuat Userbot.</b>
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
        status1 = "Ultra Premium"
    elif user_id in my_id:
        status1 = "Premium"
    else:
        status1 = "None"
        
    if user_id in DEVS:
        status = "founder"
    elif user_id in await get_seles():
        status = "admin"
    else:
        status = "user"
    ub_uptime = await get_uptime(ubot.me.id)
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
<b>FakePremV2</b>
    <b>Status Ubot:</b> <code>{ubotstatus}</code>
      <b>Status Server:</b> <code>Berjalan</code>
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
        status1 = "Ultra Premium"
    elif user_id in my_id:
        status1 = "Premium"
    else:
        status1 = "None"
        
    if user_id in DEVS:
        status = "founder"
    elif user_id in await get_seles():
        status = "admin"
    else:
        status = "user"
    
    ub_uptime = await get_uptime(ubot.me.id)
    uptime = await get_time((time() - ub_uptime))
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    end = datetime.now()
    delta_ping = (end - start).microseconds / 1000
    exp = await get_expired_date(user_id)
    prefix = await get_prefix(user_id)
    habis = exp.strftime("%d.%m.%Y") if exp else "None"
    ubotstatus = "Aktif" if habis else "Nonaktif"

    await message.reply_text(f"""
<b>FakePremV2</b>
    <b>Status Ubot:</b> <code>{ubotstatus}</code>
      <b>Status Server:</b> <code>Berjalan</code>
      <b>Status Pengguna:</b> <i>{status1} [{status}]</i>
      <b>Prefixes :</b> <code>{prefix[0]}</code>
      <b>Tanggal Kedaluwarsa:</b> <code>{habis}</code>
      <b>Uptime Ubot:</b> <code>{uptime}</code>
""")


@bot.on_callback_query(filters.regex("cb_tutor"))
async def cb_tutor(client, callback_query):
    await callback_query.edit_message_text(
        text="""<b>Tutorial Membuat Userbot :</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="🎥 Tutorial 🎥", url="https://t.me/tutorialkynan/25"),
                ],
                [
                    InlineKeyboardButton(text="👮‍♂ Admin", callback_data="start_admin"),
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
<b>👋 Halo {callback_query.from_user.first_name}
Selamat Datang Di Bot Premium Ada Yang Bisa Saya Bantu ? Jika Ingin Membuat Userbot Di Sini Silakan Hubungin Admin Yang Tertera Dan Melakukan Pembayaran Terlebih Dahulu Untuk Mendapatkan Akses Untuk Membuat Userbot.</b>
"""
    await callback_query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(buttons))
    await add_served_user(callback_query.from_user.id)
    
    
