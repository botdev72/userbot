from datetime import datetime, timedelta

from pyrogram import filters
from pyrogram.errors import *
from pyrogram.types import *
from pytz import timezone

from ubot import *

from ubot.config import *
from ubot.utils.dbfunctions import *
from ubot.utils.ultra import *



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


@bot.on_message(filters.command("delprem", ["!", "/"]) & filters.user(OWNER_ID))
@ubot.on_message(
    anjay("delprem") & filters.me & filters.user(OWNER_ID)
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


@bot.on_message(filters.command("getprem", ["!", "/"]) & filters.user(OWNER_ID))
@ubot.on_message(
    anjay("getprem") & filters.me & filters.user(OWNER_ID)
)
async def _(client, message):
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


@bot.on_message(filters.command("seles", ["!", "/"]) & filters.user(OWNER_ID))
@ubot.on_message(anjay("seles") & filters.me & filters.user(OWNER_ID))
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


@bot.on_message(filters.command("delseles", ["!", "/"]) & filters.user(OWNER_ID))
@ubot.on_message(
    anjay("delseles") & filters.me & filters.user(OWNER_ID)
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


@bot.on_message(filters.command("getseles", ["!", "/"]) & filters.user(OWNER_ID))
@ubot.on_message(
    anjay("getseles") & filters.me & filters.user(OWNER_ID)
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



@bot.on_message(filters.command("setexp"))
async def _(client, message):
    if message.from_user.id not in await get_seles():
        await message.reply( "<code> Tidak punya akses</code>.")
        return
    try:
        user_id = int(message.text.split()[1])
        duration = int(message.text.split()[2])
    except (IndexError, ValueError) as error:
        return await message.reply("Gunakan format : /setexp [user id] [jangka hari]\n\nContoh : /setexp 2930302929 30")
    now = datetime.now(timezone("Asia/Jakarta"))
    expire_date = now + timedelta(days=duration)
    await set_expired_date(user_id, expire_date)
    await message.reply(f"User {user_id} telah diaktifkan selama {duration} hari.")


@bot.on_message(filters.command("delexp") & filters.user(OWNER_ID))
@ubot.on_message(
    anjay("delexp") & filters.me & filters.user(OWNER_ID)
)
async def _(client, message):
    user_id = int(message.text.split()[1])
    await rem_expired_date(user_id)
    await message.reply(f"User {user_id} telah dihapus expired.")


@bot.on_message(filters.command("bcast") & filters.user(OWNER_ID))
async def bacotan(_, message: Message):
    await message.delete()
    siapa = message.from_user.id
    if len(message.command) > 1:
        text = " ".join(message.command[1:])
    elif message.reply_to_message is not None:
        text = message.reply_to_message.text
    else:
        return await message.reply(
            "<code>Silakan sertakan pesan atau balas pesan yang ingin disiarkan.</code>"
        )
    kntl = 0
    mmk = []
    jmbt = len(await get_served_users())
    babi = await get_served_users()
    for x in babi:
            mmk.append(int(x["user_id"]))
    if OWNER_ID in mmk:
            mmk.remove(OWNER_ID)
    for i in mmk:
        try:
            await bot.send_message(i, text)
            kntl += 1
        except:
            pass
    return await message.reply(f"**Berhasil mengirim pesan ke `{kntl}` pengguna, dari `{jmbt}` pengguna.**")
    
    


@bot.on_message(filters.command("ultraprem", ["!", "/"]))
@ubot.on_message(anjay("ultraprem") & filters.me)
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
    sudoers = await get_ultraprem()
    sudoers2 = await get_prem()
    if user.id in sudoers and user.id in sudoers2:
        return await message.reply_text("Sudah Menjadi Pengguna Ultra Premium.")
    added = await add_ultraprem(user.id)
    added2 = await add_prem(user.id)
    if added and added2:
        await message.reply_text(f"{user.mention} Sebagai Pengguna Ultra Premium")
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


@bot.on_message(filters.command("delultra", ["!", "/"]) & filters.user(OWNER_ID))
@ubot.on_message(
    anjay("delultra") & filters.me & filters.user(OWNER_ID)
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
    sudoers = await get_ultraprem()
    sudoers2 = await get_prem()
    if user.id not in sudoers and user.id not in sudoers2:
        return await message.reply_text("Tidak Ditemukan Pengguna Ultra Premium Tersebut.")
    removed = await remove_ultraprem(user.id)
    removed2 = await remove_prem(user.id)
    if removed and removed2:
        await message.reply_text(
            f"{user.mention} Berhasil Dihapus Dari Pengguna Ultra Premium"
        )
    else:
        await message.reply_text("Terjadi kesalahan, periksa log.")


@bot.on_message(filters.command("getultra", ["!", "/"]) & filters.user(OWNER_ID))
@ubot.on_message(
    anjay("getultra") & filters.me & filters.user(OWNER_ID)
)
async def _(client, message):
    sudoers = await get_ultraprem()
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