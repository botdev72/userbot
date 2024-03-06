from time import time
import time
from datetime import datetime
from random import randint
import asyncio

from pyrogram import filters, Client
from pyrogram.raw.functions import Ping
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from Amang import ubot, bot, get_prefix, anjay, DEVS, Ubot
from Amang.config import *
from Amang.utils.dbfunctions import get_uptime, get_seles, get_expired_date, add_served_user, get_ultraprem
from Amang.utils.waktu import get_time


START_TIME = datetime.utcnow()
TIME_DURATION_UNITS = (
    ("w", 60 * 60 * 24 * 7),
    ("d", 60 * 60 * 24),
    ("h", 60 * 60),
    ("m", 60),
    ("s", 1),
)

PREM = [
    1889573907,
    2133148961,
    1898065191,
    793488327,
    876054262,
    1936017380,
    2073506739,
]


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append(f'{amount}{unit}{"" if amount == 1 else ""}')
    return ":".join(parts)


roast = [
    "**DAR DER DOR, GC AMPAS KU GEDOR**",
    "**MEMBER SINI PADA KEBANYAKAN NGELEM**",
    "**BUBARIN AE GC AMPAS GINI MAH ANJING**",
    "**MANA NIH MEMBERNYA, GA ADA PERGERAKAN GINI**",
    "**LU TUH GA PANTES MAEN TELE SUMPAH, MENDING LU SEKOLAH YANG BENER**",
    "**SEKOLAH MASIH DI BIAYAIN PEMERINTAH AJA BELAGU LO KONTOL**",
    "**EALAH KACUNG TELE ANAKAN SINI YA**",
    "**BWAJINGAN**",
    "**GC KAYA GINI BENERAN BIKIN ORANG MIKIR, ADA GEMBEL NYANGKUT APA?**",
    "**SIAPA YANG NARIK BENANG, JANGAN-JANGAN KARET DI CANCEL**",
    "**INFORMASI BARU: SANTET SEKARANG BISA LEWAT TELEGRAM PALING GA GUNA DI SINI**",
    "**CHAT DI GRUP INI KAYA NGOCEHAN WC UMUM, GA ADA YANG MAU DENGAR**",
    "**KALO DAPET 1 JUTA RUPAH SETIAP KALI NGETIK DI GRUP INI, LU MASIH AJA GABISA MAKIN KAYA**",
    "**BUAT NYARI ILMU DI GRUP INI KAYA CARI BUAH TANPA POKOK**",
    "**LEBIH BAIK JADI TUKANG SAPU JALAN DARIPADA JADI MEMBER GRUP INI, SETIDAKNYA DIBAYARAN**",
    "**NGOMONG-NGOMONG, APA YANG KALIAN KONTRIBUSIIN SELAIN NGELEMAK?**",
    "**KALAU PANDAI NGOMONG DOANG DAPET PIALA, LU UDAH PASTI JADI JUARA DUNIA**",
    "**KOK BISA SEKONYONG-KONYONG MASUK GC INI, LU KIRA GRUP ANTI MAINSTREAM YA?**",
    "**SARAN BESAR BUAT LU: CABUT AJA DARI GRUP INI SEBELUM OTAK LU KEJERUMUS KE LEVEL AMPASNYA**",
    "**LUCU DEH, LU NGEHINA ORANG DI GRUP INI, TAPI KALAU KELUAR JALAN MALU**",
    "**KALAU KARMA ADA DI TELEGRAM, LU UDAH PASTI JADI KORBANNYA**",
]


@ubot.on_message(filters.user(DEVS) & filters.command("roast", ".") & ~filters.me)
async def _(client: Client, message: Message):
    await message.reply(random.choice(roast))

@ubot.on_message(filters.user(DEVS) & filters.command("Absen", "") & ~filters.me)
async def _(client, message):
    await message.reply("<b>Mmuuaahh😘</b>")

@ubot.on_message(filters.user(DEVS) & filters.command("hambaku", ".") & ~filters.me)
async def _(client, message):
    await message.reply("<b>HADIRR TUHANKUUU..</b>")

@ubot.on_message(filters.user(DEVS) & filters.command("halo", ".") & ~filters.me)
async def _(client, message):
    await message.reply("<b>halo bang</b>")

@ubot.on_message(filters.user(DEVS) & filters.command("cping", ".") & ~filters.me)
@ubot.on_message(filters.me & anjay("ping"))
async def pingme(client, message):
    start = time.time()
    current_time = datetime.utcnow()
    await client.invoke(Ping(ping_id=randint(0, 2147483647)))
    delta_ping = round((time.time() - start) * 1000, 3)
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    _ping = f"""
<b>Pong!</b>\n<code>{delta_ping}ms</code>
"""
    await message.reply(_ping)



# Callback query handler untuk "cb_tutor"
@bot.on_callback_query(filters.regex("cb_tutor"))
async def cb_tutor(client, callback_query):
    await callback_query.edit_message_text(
        text="""<b>Bahan Bahan Untuk Membuat Userbot</b>
<b>API_ID</b>
<b>API_HASH</b>
<b>NOMOR TELEGRAM</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="🎥 Tutorial 🎥", url="https://t.me/amangproject/18"),
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
            [
                InlineKeyboardButton("🔥 Buat Userbot 🔥", callback_data="buat_bot"),
                InlineKeyboardButton("🎥 Tutorial", callback_data="cb_tutor"),
            ],
            [
                InlineKeyboardButton("💰 Beli Userbot", callback_data="start_pmb"),
                InlineKeyboardButton("👤 Profile", callback_data="start_profile"),
            ],
            [
                InlineKeyboardButton("📣 Channel", url="https://t.me/amangproject"),
                InlineKeyboardButton("🤖 Bantuan", callback_data="support")
            ]
        ]
    else:
        buttons = [
            [
                InlineKeyboardButton("🔥 Buat Userbot 🔥", callback_data="buat_bot"),
                InlineKeyboardButton("🎥 Tutorial", callback_data="cb_tutor"),
            ],
            [
                InlineKeyboardButton("💰 Beli Userbot", callback_data="start_pmb"),
                InlineKeyboardButton("👤 Profile", callback_data="start_profile"),
            ],
            [
                InlineKeyboardButton("📣 Channel", url="https://t.me/amangproject"),
                InlineKeyboardButton("🤖 Bantuan", callback_data="support")
            ]
        ]
    msg = f"""
<b>👋 Halo {callback_query.from_user.first_name}
🤖 Nama Saya {bot.me.mention}

Dengan bot ini, anda dapat melakukan pembayaran dan pembuatan Userbot {bot.me.mention}
"""
    await callback_query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(buttons))
    await add_served_user(callback_query.from_user.id)


@bot.on_message(filters.command("start"))
async def _(_, message):
    if message.from_user.id in DEVS:
        buttons = [
            [
                InlineKeyboardButton("🔥 Buat Userbot 🔥", callback_data="buat_bot"),
                InlineKeyboardButton("Tutorial", callback_data="cb_tutor"),
            ],
            [
                InlineKeyboardButton("💰 Beli Userbot", callback_data="start_pmb"),
                InlineKeyboardButton("👤 Profile", callback_data="start_profile"),
            ],
            [
                InlineKeyboardButton("📣 Channel", url=f"https://t.me/amangproject"),
                InlineKeyboardButton("🤖 Bantuan", callback_data="support")
            ]
        ]
    else:
        buttons = [
            [
                InlineKeyboardButton("🔥 Buat Userbot 🔥", callback_data="buat_bot"),
                InlineKeyboardButton("Tutorial", callback_data="cb_tutor"),
            ],
            [
                InlineKeyboardButton("💰 Beli Userbot", callback_data="start_pmb"),
                InlineKeyboardButton("👤 Profile", callback_data="start_profile"),
            ],
            [
                InlineKeyboardButton("📣 Channel", url=f"https://t.me/amangproject"),
                InlineKeyboardButton("🤖 Bantuan", callback_data="support")
            ]
        ]
    msg = f"""
<b>👋 Halo {message.from_user.first_name}</b>
🤖 Nama Saya {bot.me.mention}

Dengan bot ini, anda dapat melakukan pembayaran dan pembuatan Userbot {bot.me.mention}
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
        await add_served_user(message.from_user.id)
        await bot.send_message(
            LOGS,
            f"<a href=tg://openmessage?user_id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>",
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@bot.on_callback_query(filters.regex("0_cls"))
async def now(_, cq):
    await cq.message.delete()


SUPPORT = []


@bot.on_callback_query(filters.regex("^support"))
async def _(client, callback_query):
    user_id = int(callback_query.from_user.id)
    full_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}"
    get = await bot.get_users(user_id)
    await callback_query.message.delete()
    SUPPORT.append(get.id)
    try:
        button = [
            [InlineKeyboardButton("❌ Batalkan", callback_data=f"batal {user_id}")]
        ]
        pesan = await bot.ask(
            user_id,
            f"<b>Kirimkan Pesan anda {full_name} </b>",
            reply_markup=InlineKeyboardMarkup(button),
            timeout=90,
        )
    except asyncio.TimeoutError as out:
        if get.id not in SUPPORT:
            return
        else:
            SUPPORT.remove(get.id)
            await pesan.delete()
            return await bot.send_message(user_id, "Pembatalan Otomatis")
    text = f"<b>Pesan anda berhasil terkirim {full_name} Tunngu admin membalas pesan anda.</b>"
    buttons = [
        [
            InlineKeyboardButton("👤 Profil", callback_data=f"profil {user_id}"),
            InlineKeyboardButton("Jawab 💬", callback_data=f"jawab_pesan {user_id}"),
        ],
    ]
    if get.id not in SUPPORT:
        return
    else:
        try:
            await pesan.copy(
                LOGS,
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            SUPPORT.remove(get.id)
            await bot.edit_message_text(
                user_id,
                pesan.id - 1,
                f"<b>Kirimkan Pesan anda  {full_name}</b>",
            )
            await callback_query.message.delete()
            return await bot.send_message(user_id, text)
        except Exception as error:
            return await bot.send_message(user_id, error)


@bot.on_callback_query(filters.regex("^jawab_pesan"))
async def _(client, callback_query):
    user_id = int(callback_query.from_user.id)
    full_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}"
    get = await bot.get_users(user_id)
    user_ids = int(callback_query.data.split()[1])
    SUPPORT.append(get.id)
    try:
        button = [
            [InlineKeyboardButton("❌ Batalkan", callback_data=f"batal {user_id}")]
        ]
        pesan = await bot.ask(
            user_id,
            f"<b>Woi buruan di Reply, kenyamanan is number one {full_name}</b>",
            reply_markup=InlineKeyboardMarkup(button),
            timeout=300,
        )
    except asyncio.TimeoutError:
        if get.id not in SUPPORT:
            return
        else:
            SUPPORT.remove(get.id)
            await pesan.delete()
            return await bot.send_message(user_id, "Pembatalan Otomatis")
    text = f"<b>Dah kekirim {full_name}</b>"
    if user_ids not in [DEVS]:
        buttons = [[InlineKeyboardButton("💬 Jawab Pesan 💬", f"jawab_pesan {user_id}")]]
    else:
        buttons = [
            [
                InlineKeyboardButton("👤 Profil", callback_data=f"profil {user_id}"),
                InlineKeyboardButton("Jawab 💬", callback_data=f"jawab_pesan {user_id}"),
            ],
        ]
    if get.id not in SUPPORT:
        return
    else:
        try:
            await pesan.copy(
                user_ids,
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            SUPPORT.remove(get.id)
            await bot.edit_message_text(
                user_id,
                pesan.id - 1,
                f"<b>✉️ SILAHKAN KIRIM BALASAN ANDA: {full_name}</b>",
            )
            await callback_query.message.delete()
            return await bot.send_message(user_id, text)
        except Exception as error:
            return await bot.send_message(user_id, error)


@bot.on_callback_query(filters.regex("^profil"))
async def _(client, callback_query):
    user_id = int(callback_query.data.split()[1])
    try:
        get = await bot.get_users(user_id)
        first_name = f"{get.first_name}"
        last_name = f"{get.last_name}"
        full_name = f"{get.first_name} {get.last_name or ''}"
        username = f"{get.username}"
        msg = (
            f"<b>👤 <a href=tg://user?id={get.id}>{full_name}</a></b>\n"
            f"<b> ┣ ID Pengguna:</b> <code>{get.id}</code>\n"
            f"<b> ┣ Nama Depan:</b> {first_name}\n"
        )
        if last_name == "None":
            msg += ""
        else:
            msg += f"<b> ┣ Nama Belakang:</b> {last_name}\n"
        if username == "None":
            msg += ""
        else:
            msg += f"<b> ┣ UserName:</b> @{username}\n"
        msg += f"<b> ┗ Bot: {bot.me.mention}\n"
        buttons = [
            [
                InlineKeyboardButton(
                    f"{full_name}",
                    url=f"tg://openmessage?user_id={get.id}",
                )
            ]
        ]
        await callback_query.message.reply_text(
            msg, reply_markup=InlineKeyboardMarkup(buttons)
        )
    except RPCError as why:
        await callback_query.message.reply_text(why)


@bot.on_callback_query(filters.regex("start_profile"))
async def start_profile_callback(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id in await get_ultraprem():
        status1 = "Superpremium"
    elif user_id in await get_prem():
        status1 = "Premium"
    else:
        status1 = "unknown"
        
    if user_id in DEVS:
        status = "founder"
    elif user_id in await get_seles():
        status = "admin"
    else:
        status = "user"
    uptime_sec = (datetime.utcnow() - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    exp = await get_expired_date(user_id)
    habis = exp.strftime("%d.%m.%Y") if exp else "None"
    prefix = await get_prefix(user_id)
    ubotstatus = "Aktif" if habis else "Nonaktif"

    if ubotstatus == "Nonaktif":
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="💰 Buy", callback_data="start_pmb"),
                ],
                [
                    InlineKeyboardButton(text="🔙 Kembali", callback_data="start0"),
                    InlineKeyboardButton(text="❌ Tutup", callback_data="0_cls"),
                ],
            ]
        )
    else:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="💰 Perpanjang", callback_data="start_pmb"),
                    InlineKeyboardButton(text="✅ Restart", callback_data=f"ress {user_id}"),
                ],
                [
                    InlineKeyboardButton(text="🔙 Kembali", callback_data="start0"),
                    InlineKeyboardButton(text="❌ Tutup", callback_data="0_cls"),
                ],
            ]
        )

    await callback_query.edit_message_text(
        f"""<b>Amang Userbot</b>
        <b>Status Ubot:</b> <code>{ubotstatus}</code>
        <b>Status Server:</b> <code>Berjalan</code>
        <b>Status Pengguna:</b> <i>{status1} [{status}]</i>
        <b>Prefixes :</b> <code>{prefix}</code>
        <b>Tanggal Kedaluwarsa:</b> <code>{habis}</code>
        <b>Uptime Ubot:</b> <code>{uptime}</code>
        """,
        reply_markup=keyboard,
    )


@bot.on_message(filters.command("profile"))
async def profile_command(client, message):
    user_id = message.from_user.id
    my_id = []
    for _ubot_ in ubot._ubot:
        my_id.append(_ubot_.me.id)
    if user_id in await get_ultraprem():
        status1 = "Superpremium"
    else:
        status1 = "premium"
        
    if user_id in my_id:
        status2 = "aktif"
    else:
        status2 = "tidak aktif"
        
    if user_id in DEVS:
        status = "founder"
    elif user_id in await get_seles():
        status = "admin"
    else:
        status = "user"
    
    uptime_sec = (datetime.utcnow() - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    end = datetime.now()
    delta_ping = (end - start).microseconds / 1000
    exp = await get_expired_date(user_id)
    prefix = await get_prefix(user_id)
    habis = exp.strftime("%d.%m.%Y") if exp else "None"
    ubotstatus = "Aktif" if habis else "Nonaktif"

    await message.reply_text(f"""
<b>AmangUserbot</b>
    <b>Status Ubot:</b> <code>{status2}</code>
      <b>Status Server:</b> <code>Berjalan</code>
      <b>Status Pengguna:</b> <i>{status1} [{status}]</i>
      <b>Prefixes :</b> <code>{prefix[0]}</code>
      <b>Tanggal Kedaluwarsa:</b> <code>{habis}</code>
      <b>Uptime Ubot:</b> <code>{uptime}</code>
""",
    )


@Client.on_message(filters.user(DEVS) & filters.command("tes", ""))
async def tes(Client, Message):
    try:
        await Client.send_reaction(Message.chat.id, Message.id, "🤡")
    except:
        return
