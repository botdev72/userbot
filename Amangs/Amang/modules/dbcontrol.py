from datetime import datetime, timedelta

from pyrogram import filters
from pyrogram.errors import *
from pyrogram.types import *
from pytz import timezone


from Amang import *
from Amang.config import *
from Amang.utils.dbfunctions import *

"""
@bot.on_message(filters.command("prem") & ~filters.via_bot)
async def handle_premium_command(client, message):

    if len(ubot._ubot) == MAX_UBOT:
        await message.reply_text("AmangPyrobot sudah mencapai batas maksimum pengguna.\nSilahkan gunakan bot selanjutnya")
        return

    if message.chat.id != SELLER_GROUP:
        await message.reply_text("Perintah ini hanya dapat digunakan di grup resmi seller [ubot].")
        return

    if message.from_user.id not in await get_seles():
        return

    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        if len(message.command) < 2:
            return await message.reply_text("Balas pesan pengguna atau berikan user_id/username.")
        else:
            try:
                user = await client.get_users(message.text.split()[1])
            except Exception as error:
                await message.reply(error)

    sudoers = await get_prem()
    if user.id in sudoers:
        return await message.reply_text("Pengguna sudah menjadi Pengguna Premium.")

    added = await add_prem(user.id), await add_akses(user.id)
    if added:
        await message.reply_text(f"{user.mention} telah menjadi Pengguna Premium.")
        await bot.send_message(
            user.id,
            "Terima kasih telah berlangganan Amang Userbot premium."
        )
        await bot.send_message(
            LOGS,
            f"{message.from_user.id} > {user.id}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "👤 Profil", callback_data=f"profil {message.from_user.id}"
                        ),
                        InlineKeyboardButton(
                            "Profil 👤", callback_data=f"profil {user.id}"
                        ),
                    ],
                ]
            ),
        )
    else:
        await message.reply_text("Terjadi kesalahan, periksa log.")
"""

@bot.on_message(filters.command("delprem", ["!", "/"]) & filters.user(AMANG))
@ubot.on_message(filters.me & anjay("delprem") & filters.me & filters.user(AMANG))
async def _(client, message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        if len(message.command) < 2:
            return await message.reply_text(
                "Balas pesan pengguna atau berikan user_id/username."
            )
        else:
            try:
                user = await client.get_users(message.text.split()[1])
            except Exception as error:
                await message.reply(error)
    sudoers = await get_prem()
    if user.id not in sudoers:
        return await message.reply_text("Tidak Ditemukan Pengguna Premium Tersebut.")
    removed = await remove_prem(user.id)
    if removed:
        await message.reply_text(
            f"{user.mention} Berhasil Dihapus Dari Pengguna Premium"
        )
    else:
        await message.reply_text("Terjadi kesalahan, periksa log.")


@bot.on_message(filters.command("getprem", ["!", "/"]) & filters.user(AMANG))
@ubot.on_message(filters.me & anjay("getprem") & filters.me & filters.user(AMANG))
async def _(cliebt, message):
    sudoers = await get_prem()
    text = "<b>📝 LIST MAKER USERBOT\n"
    for count, user_id in enumerate(sudoers, 1):
        try:
            user = await bot.get_users(user_id)
            user = f"<a href=tg://user?id={user.id}>{user.first_name} {user.last_name or ''}</a> > <code>{user.id}</code>"
        except Exception:
            continue
        text += f" ┣ {user}\n"
    if not text:
        await message.reply_text("Tidak Ada Pengguna Yang Ditemukan")
    else:
        await message.reply_text(text)


@bot.on_message(filters.command("addseller", ["!", "/"]) & filters.user(AMANG))
@ubot.on_message(filters.me & anjay("addseller") & filters.me & filters.user(AMANG))
async def _(client, message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        if len(message.command) < 2:
            return await message.reply_text(
                "Balas pesan pengguna atau berikan user_id/username."
            )
        else:
            try:
                user = await client.get_users(message.text.split()[1])
            except Exception as error:
                await message.reply(error)
    sudoers = await get_seles()
    if user.id in sudoers:
        return await message.reply_text("Sudah menjadi seller.")
    added = await add_seles(user.id)
    if added:
        await message.reply_text(f"{user.mention} Berhasil Ditambahkan ke seller @{bot.me.username}")
        await bot.send_message(
            LOGS,
            f"{message.from_user.id} > {user.id}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "👤 Profil", callback_data=f"profil {message.from_user.id}"
                        ),
                        InlineKeyboardButton(
                            "Profil 👤", callback_data=f"profil {user.id}"
                        ),
                    ],
                ]
            ),
        )
    else:
        await message.reply_text("Terjadi kesalahan, periksa log.")


@bot.on_message(filters.command("delseller", ["!", "/"]) & filters.user(AMANG))
@ubot.on_message(filters.me & anjay("delseller") & filters.me & filters.user(AMANG))
async def _(client, message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        if len(message.command) < 2:
            return await message.reply_text(
                "Balas pesan pengguna atau berikan user_id/username."
            )
        else:
            try:
                user = await client.get_users(message.text.split()[1])
            except Exception as error:
                await message.reply(error)
    sudoers = await get_seles()
    if user.id not in sudoers:
        return await message.reply_text("Tidak Ditemukan.")
    removed = await remove_seles(user.id)
    if removed:
        await remove_prem(user.id)
        await message.reply_text(f"{user.mention} Berhasil Dihapus Reseller")
    else:
        await message.reply_text("Terjadi kesalahan, periksa log.")


@bot.on_message(filters.command("seller", ["!", "/"]) & filters.user(AMANG))
@ubot.on_message(filters.me & anjay("seller") & filters.me & filters.user(AMANG))
async def _(cliebt, message):
    sudoers = await get_seles()
    text = "<b>RESELLER AMANG UBOT\n"
    for count, user_id in enumerate(sudoers, 1):
        try:
            user = await bot.get_users(user_id)
            user = f"<a href=tg://user?id={user.id}>{user.first_name} {user.last_name or ''}</a> > <code>{user.id}</code>"
        except Exception:
            continue
        text += f" » {user}\n"
    if not text:
        await message.reply_text("Tidak Ada Pengguna Yang Ditemukan")
    else:
        await message.reply_text(text)


@bot.on_message(filters.command("setexp") & filters.user(AMANG))
@ubot.on_message(filters.me & anjay("setexp") & filters.me & filters.user(AMANG))
async def _(client, message):
    try:
        user_id = int(message.text.split()[1])
        duration = int(message.text.split()[2])
    except (IndexError, ValueError) as error:
        return await message.reply(error)
    now = datetime.now(timezone("Asia/Jakarta"))
    expire_date = now + timedelta(days=duration)
    await set_expired_date(user_id, expire_date)
    await message.reply(f"User {user_id} telah diaktifkan selama {duration} hari.")


@bot.on_message(filters.command("exph") & filters.user(AMANG))
@ubot.on_message(filters.me & anjay("exph") & filters.me & filters.user(AMANG))
async def _(client, message):
    try:
        user_id = int(message.text.split()[1])
        duration = int(message.text.split()[2])
    except (IndexError, ValueError) as error:
        return await message.reply(error)
    now = datetime.now(timezone("Asia/Jakarta"))
    expire_date = now + timedelta(hours=duration)
    await set_expired_date(user_id, expire_date)
    await message.reply(f"User {user_id} telah diaktifkan selama {duration} jam.")


@bot.on_message(filters.command("delexp") & filters.user(AMANG))
@ubot.on_message(filters.me & anjay("delexp") & filters.me & filters.user(AMANG))
async def _(client, message):
    user_id = int(message.text.split()[1])
    await rem_expired_date(user_id)
    await message.reply(f"User {user_id} telah dihapus expired.")


@bot.on_message(filters.command("bacotan"))
async def bacotan(_, message: Message):
    if message.reply_to_message:
        x = message.reply_to_message.message_id
        y = message.chat.id
    else:
        if len(message.command) < 2:
            return await message.reply_text(
                "**Usage**:\n/broadcast [MESSAGE] or [Reply to a Message]"
            )
        query = message.text.split(None, 1)[1]

    susr = 0
    served_users = []
    susers = await get_served_users()
    for user in susers:
        served_users.append(int(user["user_id"]))
    for i in served_users:
        try:
            await bot.forward_messages(
                i, y, x
            ) if message.reply_to_message else await bot.send_message(
                i, text=query
            )
            susr += 1
        except FloodWait as e:
            flood_time = int(e.x)
            if flood_time > 200:
                continue
            await asyncio.sleep(flood_time)
        except Exception:
            pass
    try:
        await message.reply_text(
            f"**Broadcasted Message to {susr} Users.**"
        )
    except:
        pass


@bot.on_message(filters.command("delsuprem", ["!", "/"]) & filters.user(OWNER))
async def _(client, message):
    if message.reply_to_message:
        chat_id = message.reply_to_message.sender.chat.id
    else:
        if len(message.command) < 2:
            return await message.reply_text("berikan chat_id.")
        else:
            chat_id = int(message.text.split()[1])
    uprem = await get_ultraprem()
    if chat_id not in uprem:
        return await message.reply_text("Pengguna Tidak Ditemukan.")
    removed = await remove_ultraprem(chat_id)
    if removed:
        await message.reply_text(f"{chat_id} Berhasil Dihapus Dari superpremium")
    else:
        await message.reply_text("Terjadi kesalahan.")


@bot.on_message(filters.command("getsuprem", ["!", "/"]) & filters.user(OWNER))
async def _(cliebt, message):
    uprem = await get_ultraprem()
    text = "<b>📝 LIST SUPER PREMIUM\n"
    for count, chat_id in enumerate(uprem, 1):
        try:
            chat = f"<code>{chat_id}</code>"
        except Exception:
            continue
        text += f" ┣ {chat}\n"
    if not text:
        await message.reply_text("Tidak Ada Pengguna Yang Ditemukan")
    else:
        await message.reply_text(text)

"""
@bot.on_message(filters.command("suprem") & ~filters.via_bot)
async def handle_premium_command(client, message):
    MAX_UBOT = 20  # Batas maksimum pengguna ubot

    if len(ubot._ubot) == MAX_UBOT:
        await message.reply_text("AmangPyrobot sudah mencapai batas maksimum pengguna.\nSilahkan gunakan bot selanjutnya")
        return

    if message.chat.id != SELLER_GROUP:
        await message.reply_text("Perintah ini hanya dapat digunakan di grup resmi seller [ubot].")
        return

    if message.from_user.id not in await get_seles():
        return

    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        if len(message.command) < 2:
            return await message.reply_text("Balas pesan pengguna atau berikan user_id/username.")
        else:
            try:
                user = await client.get_users(message.text.split()[1])
            except Exception as error:
                await message.reply(error)

    sudoers = await get_ultraprem()
    if user.id in sudoers:
        return await message.reply_text("Pengguna sudah menjadi Pengguna Super premium.")

    added = await add_ultraprem(user.id), await add_prem(user.id), await add_akses(user.id)
    if added:
        await message.reply_text(f"{user.mention} telah menjadi Pengguna Premium.")
        await bot.send_message(
            user.id,
            "Terima kasih telah berlangganan Amang Userbot Superpremium."
        )
        await bot.send_message(
            LOGS,
            f"{message.from_user.id} > {user.id}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "👤 Admin", callback_data=f"profil {message.from_user.id}"
                        ),
                        InlineKeyboardButton(
                            "Buyer 👤", callback_data=f"profil {user.id}"
                        ),
                    ],
                ]
            ),
        )
    else:
        await message.reply_text("Terjadi kesalahan, periksa log.")
"""

@bot.on_message(filters.command("suprem"))
async def handle_premium_command(client, message):
    MAX_UBOT = 20  # Batas maksimum pengguna ubot

    if len(ubot._ubot) == MAX_UBOT:
        await message.reply_text("AmangPyrobot sudah mencapai batas maksimum pengguna.\nSilahkan gunakan bot selanjutnya")
        return

    if message.chat.id != SELLER_GROUP:
        await message.reply_text("Perintah ini hanya dapat digunakan di grup resmi seller [ubot].")
        return

    if message.from_user.id not in await get_seles():
        return

    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        if len(message.command) < 2:
            return await message.reply_text("Balas pesan pengguna atau berikan user_id/username.")
        else:
            try:
                user = await client.get_users(message.command[1])
            except Exception as error:
                await message.reply(str(error))
                return

    sudoers = await get_ultraprem()
    if user.id in sudoers:
        return await message.reply_text("Pengguna sudah menjadi Pengguna Super premium.")

    # Mengirimkan tombol persetujuan kepada pengguna
    approve_button = InlineKeyboardButton("Setuju", callback_data=f"approve_supremium {user.id}")
    markup = InlineKeyboardMarkup([[approve_button]])
    await bot.send_message(SELLER_GROUP, f"Klik tombol 'Setuju' untuk memberikan status premium kepada pengguna dengan ID: {user.id}", reply_markup=markup)
    
    # Menyimpan User ID yang akan diberikan status premium
    global pending_user_id
    pending_user_id = user.id

@bot.on_callback_query(filters.regex("^approve_supremium"))
async def handle_approve_supremium_callback(client, callback_query):
    global pending_user_id
    if pending_user_id:
        user_id = pending_user_id
        pending_user_id = None
        # Memproses status premium untuk pengguna dengan ID user_id
        added = await add_ultraprem(user_id), await add_prem(user_id), await add_akses(user_id)
        if added:
            await bot.send_message(SELLER_GROUP, f"Berhasil memberikan status Superpremium kepada pengguna dengan ID: {user_id}")
            await bot.send_message(
                user_id,
                "Terima kasih telah berlangganan Amang Userbot Superpremium."
            )
            await bot.send_message(
                LOGS,
                f"{callback_query.from_user.id} > {user_id}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "👤 Admin", callback_data=f"profil {callback_query.from_user.id}"
                            ),
                            InlineKeyboardButton(
                                "Buyer 👤", callback_data=f"profil {user_id}"
                            ),
                        ],
                    ]
                ),
            )
        else:
            await bot.send_message(callback_query.from_user.id, "Terjadi kesalahan, periksa log.")


@bot.on_message(filters.command("prem"))
async def handle_prem_command(client, message):

    if len(ubot._ubot) == MAX_UBOT:
        await message.reply_text("AmangPyrobot sudah mencapai batas maksimum pengguna.\nSilahkan gunakan bot selanjutnya")
        return

    if message.chat.id != SELLER_GROUP:
        await message.reply_text("Perintah ini hanya dapat digunakan di grup resmi seller [ubot].")
        return

    if message.from_user.id not in await get_seles():
        return

    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        if len(message.command) < 2:
            return await message.reply_text("Balas pesan pengguna atau berikan user_id/username.")
        else:
            try:
                user = await client.get_users(message.command[1])
            except Exception as error:
                await message.reply(str(error))
                return

    sudoers = await get_prem()
    if user.id in sudoers:
        return await message.reply_text("Pengguna sudah menjadi Pengguna premium.")

    # Mengirimkan tombol persetujuan kepada pengguna
    approve_button = InlineKeyboardButton("Setuju", callback_data=f"approve_premium {user.id}")
    markup = InlineKeyboardMarkup([[approve_button]])
    await bot.send_message(SELLER_GROUP, f"Klik tombol 'Setuju' untuk memberikan status premium kepada pengguna dengan ID: {user.id}", reply_markup=markup)
    
    # Menyimpan User ID yang akan diberikan status premium
    global pending_user_id
    pending_user_id = user.id

@bot.on_callback_query(filters.regex("^approve_premium"))
async def handle_approve_supremium_callback(client, callback_query):
    global pending_user_id
    if pending_user_id:
        user_id = pending_user_id
        pending_user_id = None
        # Memproses status premium untuk pengguna dengan ID user_id
        added = await add_prem(user_id), await add_akses(user_id)
        if added:
            await bot.send_message(SELLER_GROUP, f"Berhasil memberikan status premium kepada pengguna dengan ID: {user_id}")
            await bot.send_message(
                user_id,
                "Terima kasih telah berlangganan Amang Userbot premium."
            )
            await bot.send_message(
                LOGS,
                f"ADMIN {callback_query.from_user.id} BERHASIL MEMBERIKAN AKSES KE {user_id}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "👤 Admin", callback_data=f"profil {callback_query.from_user.id}"
                            ),
                            InlineKeyboardButton(
                                "Buyer 👤", callback_data=f"profil {user_id}"
                            ),
                        ],
                    ]
                ),
            )
        else:
            await bot.send_message(callback_query.from_user.id, "Terjadi kesalahan, periksa log.")