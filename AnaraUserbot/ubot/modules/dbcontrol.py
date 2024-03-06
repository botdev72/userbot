from datetime import datetime, timedelta

from pyrogram import filters
from pyrogram.errors import *
from pyrogram.types import *
from pytz import timezone

from . import bot, ubot, anjay, cobadah
from ubot.config import *
from ubot.utils.dbfunctions import *



@bot.on_message(filters.command("prem", ["!", "/"]))
@ubot.on_message(anjay("prem") & filters.me)
async def _(client, message):
    if message.from_user.id not in await get_seles():
        return
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
    if user.id in sudoers:
        return await message.reply_text("Sudah Menjadi Pengguna Premium.")
    added = await add_prem(user.id)
    if added:
        await message.reply_text(f"{user.mention} Sebagai Pengguna Premium")
        await bot.send_message(
            OWNER_ID,
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


@bot.on_message(anjay("delprem", ["!", "/"]) & filters.user(DEVS))
@ubot.on_message(
    anjay("delprem") & filters.me & filters.user(DEVS)
)
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
@ubot.on_message(
    anjay("getprem") & filters.me & filters.user(DEVS)
)
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


@bot.on_message(filters.command("seles", ["!", "/"]) & filters.user(1054295664))
@ubot.on_message(anjay("seles") & filters.me & filters.user(1054295664))
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
        return await message.reply_text("Sudah menjadi reseller.")
    added = await add_seles(user.id)
    if added:
        await add_prem(user.id)
        await message.reply_text(f"{user.mention} Silahkan Buka @{bot.me.username}")
        await bot.send_message(
            OWNER_ID,
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


@bot.on_message(filters.command("delseles", ["!", "/"]) & filters.user(1054295664))
@ubot.on_message(
    anjay("delseles") & filters.me & filters.user(1054295664)
)
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


@bot.on_message(filters.command("getseles", ["!", "/"]) & filters.user(1054295664))
@ubot.on_message(
    anjay("getseles") & filters.me & filters.user(1054295664)
)
async def _(cliebt, message):
    sudoers = await get_seles()
    text = "<b>📝 LIST RESELLER\n"
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



@bot.on_message(filters.command("setexp") & filters.user(1054295664))
@ubot.on_message(
    anjay("setexp") & filters.me & filters.user(1054295664)
)
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


@bot.on_message(filters.command("delexp") & filters.user(1054295664))
@ubot.on_message(
    anjay("delexp") & filters.me & filters.user(1054295664)
)
async def _(client, message):
    user_id = int(message.text.split()[1])
    await rem_expired_date(user_id)
    await message.reply(f"User {user_id} telah dihapus expired.")
