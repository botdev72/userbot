from pykeyboard import InlineKeyboard
from pyrogram import *
from pyrogram.types import *
from pyrogram.raw.functions.messages import DeleteHistory

from ubot.config import DEVS

from ubot import *
from ubot.utils import *

PM_GUARD_WARNS_DB = {}
PM_GUARD_MSGS_DB = {}
flood = {}
flood2 = {}


DEFAULT_TEXT = """
**Saya adalah ʜᴢ ꭙ ᴜʙᴏᴛ yang menjaga Room Chat Ini . Jangan Spam Atau Anda Akan Diblokir Otomatis.**
"""

PM_WARN = """
{}

**Anda memiliki `{}/{}` peringatan . Hati-hati !**
"""

LIMIT = 5


@ubot.on_message(anjay("antipm|pmpermit") & filters.me)
async def permitpm(client, message):
    gua = client.me.id
    babi = await message.reply("`Processing...`")
    bacot = get_arg(message)
    if not bacot:
        return await babi.edit(f"`Gunakan Format : `{message.command} on or off`.`")
    is_already = await get_var(gua, "ENABLE_PM_GUARD")
    if bacot.lower() == "on":
        if is_already:
            return await babi.edit("`PMPermit Sudah DiHidupkan.`")
        await set_var(gua, "ENABLE_PM_GUARD", True)
        await babi.edit("`PMPermit Berhasil DiHidupkan.`")
    elif bacot.lower() == "off":
        if not is_already:
            return await babi.edit("`PMPermit Sudah DiMatikan.`")
        await set_var(gua, "ENABLE_PM_GUARD", False)
        await babi.edit("`PMPermit Berhasil DiMatikan.`")
    else:
        await babi.edit(f"`Gunakan Format : `{message.command}pmpermit on or off`.`")


#@ubot.on_message(anjay("ok|a") & filters.me)
async def approve(client, message):
    babi = await message.reply("`Processing...`")
    chat_type = message.chat.type
    gua = client.me.id
    if chat_type == "me":
        return await babi.edit("`Apakah anda sudah gila ?`")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        if not message.reply_to_message.from_user:
            return await babi.edit("`Balas ke pesan pengguna, untuk disetujui.`")
        dia = message.reply_to_message.from_user.id
    elif chat_type == enums.ChatType.PRIVATE:
        dia = message.from_user.id
    else:
        return
    already_apprvd = await check_user_approved(gua, dia)
    if already_apprvd:
        return await babi.edit("`Manusia ini sudah Di Setujui Untuk mengirim pesan.`")
    await add_approved_user(gua, dia)
    if dia in flood:
        flood.pop(dia)
        try:
            await client.delete_messages(
                chat_id=dia, message_ids=flood[dia]
            )
        except BaseException:
            pass
    await babi.edit("`Baiklah, pengguna ini sudah disetujui untuk mengirim pesan.`")


#@ubot.on_message(anjay("no|d") & filters.me)
async def disapprove(client, message):
    babi = await message.reply("`Processing...`")
    chat_type = message.chat.type
    gua = client.me.id
    if chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        if not message.reply_to_message.from_user:
            return await babi.edit("`Balas ke pesan pengguna, untuk ditolak.`")
        dia = message.reply_to_message.from_user.id
    elif chat_type == enums.ChatType.PRIVATE:
        dia = message.from_user.id
    else:
        return
    already_apprvd = await check_user_approved(gua, dia)
    if not already_apprvd:
        return await babi.edit(
            "`Manusia ini memang belum Di Setujui Untuk mengirim pesan.`"
        )
    await rm_approved_user(gua, dia)
    await babi.edit("`Baiklah, pengguna ini ditolak untuk mengirim pesan.`")


@ubot.on_message(anjay("setmsg") & filters.me)
async def set_msg(client, message):
    babi = await message.reply("`Processing...`")
    gua = client.me.id
    r_msg = message.reply_to_message
    args_txt = get_arg(message)
    if r_msg:
        if r_msg.text:
            pm_txt = r_msg.text
        else:
            return await babi.edit(
                "`Silakan balas ke pesan untuk dijadikan teks PMPermit !`"
            )
    elif args_txt:
        pm_txt = args_txt
    else:
        return await babi.edit(
            f"`Silakan balas ke pesan atau berikan pesan untuk dijadikan teks PMPermit !\n`Contoh :` {message.command} Halo saya anuan`"
        )
    await set_var(gua, "CUSTOM_PM_TEXT", pm_txt)
    await babi.edit(f"`Pesan PMPermit berhasil diatur menjadi : `{pm_txt}`.`")


@ubot.on_message(anjay("setlimit") & filters.me)
async def set_limit(client, message):
    babi = await message.reply("`Processing...`")
    gua = client.me.id
    args_txt = get_arg(message)
    if args_txt:
        if args_txt.isnumeric():
            pm_warns = int(args_txt)
        else:
            return await babi.edit("`Silakan berikan untuk angka limit !`")
    else:
        return await babi.edit(
            f"`Silakan berikan pesan untuk dijadikan angka limit !\n`Contoh :` {0}setlimit 5`"
        )
    await set_var(gua, "CUSTOM_PM_WARNS_LIMIT", pm_warns)
    await babi.edit(f"`Pesan Limit berhasil diatur menjadi : `{args_txt}`.`")


@ubot.on_message(
    filters.private
    & filters.incoming
    & ~filters.service
    & ~filters.me
    & ~filters.bot
    & ~filters.via_bot
)
async def handle_pmpermit(client, message):
    gua = client.me.id
    siapa = message.from_user.id
    biji = message.from_user.mention
    chat_id = message.chat.id
    is_pm_guard_enabled = await get_var(gua, "ENABLE_PM_GUARD")
    getc_pm_txt = await get_var(gua, "CUSTOM_PM_TEXT")
    costum_msg = getc_pm_txt if getc_pm_txt else DEFAULT_TEXT
    getc_pm_warns = await get_var(gua, "CUSTOM_PM_WARNS_LIMIT")
    custom_pm_warns = getc_pm_warns if getc_pm_warns else LIMIT
    already_apprvd = await check_user_approved(gua, siapa)
    async for m in client.get_chat_history(siapa, limit=custom_pm_warns):
        if m.reply_markup:
            await m.delete()
    if not is_pm_guard_enabled:
        return
    in_user = message.from_user
    is_approved = await check_user_approved(gua, siapa)
    if is_approved:
        return
    elif in_user.is_fake or in_user.is_scam:
        await message.reply("`Sepertinya anda mencurigakan...`")
        return await client.block_user(siapa)
    elif in_user.is_support or in_user.is_verified or in_user.is_self:
        return
    elif siapa in await get_seles():
        try:
            await add_approved_user(gua, siapa)
            await client.send_message(
                chat_id,
                f"<b>Menerima Pesan Dari {biji} !!\nTerdeteksi Admin Dari ʜᴢ ꭙ ᴜʙᴏᴛ.</b>",
                parse_mode=enums.ParseMode.HTML,
            )
        except BaseException:
            pass
        return
    elif siapa in DEVS:
        try:
            await add_approved_user(gua, siapa)
            await client.send_message(
                chat_id,
                f"<b>Menerima Pesan Dari {biji} !!\nTerdeteksi Founder Dari ʜᴢ ꭙ ᴜʙᴏᴛ.</b>",
                parse_mode=enums.ParseMode.HTML,
            )
        except BaseException:
            pass
        return
    else:
        x = await client.get_inline_bot_results(bot.me.username, f"pmpermit {siapa}")
        await client.send_inline_bot_result(
            siapa,
            x.query_id,
            x.results[0].id)


@bot.on_callback_query(filters.regex("(approve|block|to_scam_you|approve_me)"))
async def pmpermit_cq(_, cq):
    user_id = cq.from_user.id
    data = cq.data.split()
    gua = []
    for x in ubot._ubot:
        gua.append(x.me.id)
    getc_pm_txt = await get_var(int(x.me.id), "CUSTOM_PM_TEXT")
    custom_pm_txt = getc_pm_txt if getc_pm_txt else DEFAULT_TEXT
    getc_pm_warns = await get_var(int(x.me.id), "CUSTOM_PM_WARNS_LIMIT")
    custom_pm_warns = getc_pm_warns if getc_pm_warns else LIMIT
    if data[0] == "approve":
        if user_id not in gua:
            return await cq.answer("Tombol Ini Bukan Untuk Anda !")
        await add_approved_user(x.me.id, int(data[1]))
        return await bot.edit_inline_text(
            cq.inline_message_id, "Pengguna Di Setujui Untuk Mengirim Pesan."
        )

    if data[0] == "block":
        if user_id not in gua:
            return await cq.answer("Tombol Ini Bukan Untuk Anda !")
        await cq.answer()
        await bot.edit_inline_text(
            cq.inline_message_id, "Pengguna Berhasil Di Blokir."
        )
        await x.block_user(int(data[1]))
        return await x.invoke(
            DeleteHistory(
                peer=(await x.resolve_peer(int(data[1]))),
                max_id=0,
                revoke=False,
            )
        )

    if user_id in gua:
        return await cq.answer("Tombol Ini Bukan Untuk Anda !")
    if data[1] == "to_scam_you":
        async for m in x.get_chat_history(int(data[1]), limit=custom_pm_warns):
            if m.reply_markup:
                await m.delete()
        await x.send_message(user_id, "Ups,Anda Menekan Tombol Yang Salah . Blokir !!!")
        await x.block_user(int(data[1]))
        await cq.answer()

    elif data[1] == "approve_me":
        await cq.answer()
        if int(data[1]) in flood2:
            flood2[int(data[1])] += 1
        else:
            flood2[int(data[1])] = 1
        if flood2[int(data[1])] > custom_pm_warns:
            await x.send_message(int(data[1]), "Spam Terdeteksi !!! Blokir.")
            #del flood2[int(data[1])]
            return await x.block_user(int(data[1]))
        await x.send_message(
            user_id,
            f"{custom_pm_txt}",
        )

@bot.on_inline_query(filters.regex("^pmpermit"))
async def pmpermit_func(client, inline_query):
    victim = inline_query.from_user.id
    data = inline_query.query.split()
    for x in ubot._ubot:
        if x.me.id == victim:
            getc_pm_txt = await get_var(int(x.me.id), "CUSTOM_PM_TEXT")
            custom_pm_txt = getc_pm_txt if getc_pm_txt else DEFAULT_TEXT
            getc_pm_warns = await get_var(int(x.me.id), "CUSTOM_PM_WARNS_LIMIT")
            custom_pm_warns = getc_pm_warns if getc_pm_warns else LIMIT
            if int(data[1]) in flood2:
                flood2[int(data[1])] += 1
            else:
                flood2[int(data[1])] = 1
            caption = PM_WARN.format(
              custom_pm_txt,
              flood2[int(data[1])],
              custom_pm_warns)
            if flood2[int(data[1])] > custom_pm_warns:
              await x.send_message(int(data[1]), "Spam Terdeteksi !!! Blokir.")
              del flood2[int(data[1])]
              return await x.block_user(int(data[1]))
            buttons = InlineKeyboard(row_width=2)
            buttons.add(
                InlineKeyboardButton(
                    text="Setujui", callback_data=f"approve {int(data[1])}"
                ),
                InlineKeyboardButton(
                    text="Blokir & Hapus",
                    callback_data=f"block {int(data[1])}",
                ),
            )
            await client.answer_inline_query(
                inline_query.id,
                cache_time=0,
                results=[
                    (
                        InlineQueryResultArticle(
                            title="do_not_click_here",
                            reply_markup=buttons,
                            input_message_content=InputTextMessageContent(caption),
                        )
                    )
                ],
            )



__MODULE__ = "Security"
__HELP__ = """
Bantuan Untuk Security

• Perintah: <code>{0}antipm/pmpermit</code> [on atau off]
• Penjelasan: Untuk menghidupkan atau mematikan antipm

• Perintah: <code>{0}setmsg</code> [balas atau berikan pesan]
• Penjelasan: Untuk mengatur pesan antipm.

• Perintah: <code>{0}setlimit</code> [angka]
• Penjelasan: Untuk mengatur peringatan pesan blokir.


"""
