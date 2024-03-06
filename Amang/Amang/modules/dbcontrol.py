from datetime import datetime, timedelta

from pyrogram import filters
from pyrogram.errors import *
from pyrogram.types import *
from pytz import timezone

from Amang import *
from Amang.config import *
from Amang.utils.dbfunctions import *

@ubot.on_message(filters.command("prem", cmd) & filters.me)
@bot.on_message(filters.command("prem") & ~filters.via_bot)
async def handle_premium_command(client, message):
    MAX_UBOT = 23  # Batas maksimum pengguna ubot

    if len(ubot._ubot) == MAX_UBOT:
        await message.reply_text("AmangPyrobot sudah mencapai batas maksimum pengguna.\nSilahkan gunakan bot kedua dengan cara \n\n<code> /prem@amwang2_bot user_id </code>")
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

    added = await add_prem(user.id)
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


@bot.on_message(filters.command("delprem", ["!", "/"]) & filters.user(DEVS))
@ubot.on_message(filters.command("delprem", cmd) & filters.me & filters.user(DEVS))
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


@bot.on_message(filters.command("getprem", ["!", "/"]) & filters.user(DEVS))
@ubot.on_message(filters.command("getprem", cmd) & filters.me & filters.user(DEVS))
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


@bot.on_message(filters.command("addseller", ["!", "/"]) & filters.user(DEVS))
@ubot.on_message(filters.command("addseller", cmd) & filters.me & filters.user(DEVS))
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
        await add_prem(user.id)
        await message.reply_text(f"{user.mention} Silahkan Buka @{bot.me.username}")
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


@bot.on_message(filters.command("delseller", ["!", "/"]) & filters.user(DEVS))
@ubot.on_message(filters.command("delseller", cmd) & filters.me & filters.user(DEVS))
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


@bot.on_message(filters.command("seller", ["!", "/"]) & filters.user(DEVS))
@ubot.on_message(filters.command("seller", cmd) & filters.me & filters.user(DEVS))
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


@bot.on_message(filters.command("setexp") & filters.user(DEVS))
@ubot.on_message(filters.command("setexp", cmd) & filters.me & filters.user(DEVS))
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


@bot.on_message(filters.command("exph") & filters.user(DEVS))
@ubot.on_message(filters.command("exph", cmd) & filters.me & filters.user(DEVS))
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


@bot.on_message(filters.command("delexp") & filters.user(DEVS))
@ubot.on_message(filters.command("delexp", cmd) & filters.me & filters.user(DEVS))
async def _(client, message):
    user_id = int(message.text.split()[1])
    await rem_expired_date(user_id)
    await message.reply(f"User {user_id} telah dihapus expired.")


@bot.on_message(filters.command("bacot"))
async def gcast_handler(_, message):
    if len(message.command) > 1:
        text = " ".join(message.command[1:])
    elif message.reply_to_message is not None:
        text = message.reply_to_message.text
    else:
        await message.reply("<code>Silakan sertakan pesan atau balas pesan yang ingin disiarkan.</code>")
        return

    if message.from_user.id not in DEVS:  # Ganti DEVS dengan daftar ID pengguna yang diizinkan
        await message.reply_text("<code>Maaf, hanya ADMINS yang diizinkan menggunakan perintah ini.</code>")
        return

    ubot = await get_userbots()  # Ganti ini dengan fungsi atau metode untuk mendapatkan daftar userbot yang ingin Anda kirimkan pesan
    total_users = len(ubot)
    sent_count = 0
    for x in ubot:
        try:
            await bot.send_message(chat_id=x["id"], text=text)
            sent_count += 1
        except Exception as e:
            await message.reply(f"Error saat mengirim pesan ke {x['id']}: {str(e)}")

    return await message.reply_text(f"<b>Pesan siaran berhasil dikirim kepada {sent_count} dari {total_users} pengguna.</b>")
