import asyncio

from pyrogram import *
from pyrogram.types import *

from ubot import *
from ubot.config import DEVS
from ubot.utils import *

flood = {}
flood2 = {}


DEFAULT_TEXT = """
<b>Saya adalah {} yang menjaga Room Chat Ini . Jangan Spam Atau Anda Akan Diblokir Otomatis.</b>
"""

PM_WARN = """
<b>PM Security Of {} !!</b>

<b>{}</b>

<b>Warning `{}` of `{}` !!</b>
"""

LIMIT = 5

"""
@KY.UBOT("antipm|pmpermit")
async def permitpm(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    user_id = client.me.id
    babi = await message.reply(f"{emo.proses} **Processing...**")
    await asyncio.sleep(2)
    bacot = get_arg(message)
    if not bacot:
        return await babi.edit(
            f"{emo.gagal} **Gunakan Format : `{message.text} on or off`.**"
        )
    is_already = await get_var(user_id, "ENABLE_PM_GUARD")
    if bacot.lower() == "on":
        if is_already:
            return await babi.edit(f"{emo.sukses} **PMPermit Sudah DiHidupkan.**")
        await set_var(user_id, "ENABLE_PM_GUARD", True)
        await babi.edit(f"{emo.sukses} **PMPermit Berhasil DiHidupkan.**")
    elif bacot.lower() == "off":
        if not is_already:
            return await babi.edit(f"{emo.gagal} **PMPermit Sudah DiMatikan.**")
        await set_var(user_id, "ENABLE_PM_GUARD", False)
        await babi.edit(f"{emo.gagal} **PMPermit Berhasil DiMatikan.**")
    else:
        await babi.edit(
            f"{emo.gagal} **Gunakan Format : `{message.text}pmpermit on or off`.**"
        )
"""


@KY.UBOT("ok|a")
async def approve(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    babi = await message.reply(f"{emo.proses} **Processing...**")
    chat_type = message.chat.type
    getc_pm_warns = await get_var(client.me.id, "CUSTOM_PM_WARNS_LIMIT")
    custom_pm_warns = getc_pm_warns if getc_pm_warns else LIMIT
    if chat_type == "me":
        return await babi.edit(f"{emo.gagal} **Apakah anda sudah gila ?**")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        if not message.reply_to_message:
            return await babi.edit(
                f"{emo.gagal} **Balas ke pesan pengguna, untuk disetujui.**"
            )
        user_id = message.reply_to_message.from_user.id
    elif chat_type == enums.ChatType.PRIVATE:
        user_id = message.chat.id
    else:
        return
    already_apprvd = await check_user_approved(user_id)
    if already_apprvd:
        return await babi.edit(f"{emo.sukses} **Pengguna ini sudah disetujui.**")
    async for m in client.get_chat_history(message.from_user.id, limit=custom_pm_warns):
        if m.reply_markup:
            await m.delete()
    await add_approved_user(user_id)
    await babi.edit(
        f"{emo.sukses} **Baiklah, pengguna ini disetujui untuk mengirim pesan.**"
    )


@KY.UBOT("no|d")
async def disapprove(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    babi = await message.reply(f"{emo.proses} **Processing...**")
    await asyncio.sleep(2)
    client.me.id
    chat_type = message.chat.type
    if chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        if not message.reply_to_message.from_user:
            return await babi.edit(
                f"{emo.gagal} **Balas ke pesan pengguna, untuk ditolak.**"
            )
        user_id = message.reply_to_message.from_user.id
    elif chat_type == enums.ChatType.PRIVATE:
        user_id = message.chat.id
    else:
        return
    already_apprvd = await check_user_approved(user_id)
    if not already_apprvd:
        return await babi.edit(
            f"{emo.gagal} **Pengguna ini memang belum disetujui untuk mengirim pesan.**"
        )
    await rm_approved_user(user_id)
    await babi.edit(
        f"{emo.sukses} **Baiklah, pengguna ini ditolak untuk mengirim pesan.**"
    )


@KY.UBOT("setmsg")
async def set_msg(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    babi = await message.reply(f"{emo.proses} **Processing...**")
    await asyncio.sleep(2)
    user_id = client.me.id
    r_msg = message.reply_to_message
    args_txt = get_arg(message)
    if r_msg:
        if r_msg.text:
            pm_txt = r_msg.text
        else:
            return await babi.edit(
                f"{emo.gagal} **Silakan balas ke pesan untuk dijadikan teks PMPermit !**"
            )
    elif args_txt:
        pm_txt = args_txt
    else:
        return await babi.edit(
            f"{emo.gagal} **Silakan balas ke pesan atau berikan pesan untuk dijadikan teks PMPermit !\nContoh :`{message.text} Halo saya anuan.`**"
        )
    await set_var(user_id, "CUSTOM_PM_TEXT", pm_txt)
    await babi.edit(
        f"{emo.sukses} **Pesan PMPemit berhasil diatur menjadi : `{pm_txt}`.**"
    )


@KY.UBOT("setlimit")
async def set_limit(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    babi = await message.reply(f"{emo.proses} **Processing...**")
    await asyncio.sleep(2)
    user_id = client.me.id
    args_txt = get_arg(message)
    if args_txt:
        if args_txt.isnumeric():
            pm_warns = int(args_txt)
        else:
            return await babi.edit(
                f"{emo.gagal} **Silakan berikan untuk angka limit !**"
            )
    else:
        return await babi.edit(
            f"{emo.gagal} **Silakan berikan pesan untuk dijadikan angka limit !\nContoh :` {message.text}setlimit 5.`**"
        )
    await set_var(user_id, "CUSTOM_PM_WARNS_LIMIT", pm_warns)
    await babi.edit(
        f"{emo.sukses} **Pesan Limit berhasil diatur menjadi : `{args_txt}`.**"
    )


@ubot.on_message(
    filters.private
    & filters.incoming
    & ~filters.me
    & ~filters.bot
    & ~filters.via_bot
    & ~filters.service,
    group=69,
)
async def handle_pmpermit(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    user_id = client.me.id
    chat_id = message.chat.id
    apaiya = await check_user_approved(chat_id)
    is_pm_guard_enabled = await get_var(user_id, "ENABLE_PM_GUARD")
    if not is_pm_guard_enabled:
        return
    if apaiya:
        return
    if message.from_user.is_fake or message.from_user.is_scam:
        await message.reply(f"{emo.gagal} **Sepertinya anda mencurigakan...**")
        return await client.block_user(message.from_user.id)
    if (
        message.from_user.is_support
        or message.from_user.is_verified
        or message.from_user.is_self
    ):
        return
    if chat_id in DEVS:
        try:
            await add_approved_user(chat_id)
            await client.send_message(
                chat_id,
                f"{emo.sukses} <b>Menerima Pesan Dari {message.from_user.mention} !!\nTerdeteksi Founder Dari {bot.me.mention}.</b>",
                parse_mode=enums.ParseMode.HTML,
            )
        except BaseException:
            pass
        return
    if not apaiya:
        try:
            x = await client.get_inline_bot_results(
                bot.me.username, f"pmpermit {chat_id}"
            )
            await client.send_inline_bot_result(chat_id, x.query_id, x.results[0].id)
        except BaseException:
            pass
        return

    # if in_user.is_fake or in_user.is_scam:
    # await message.reply(f"{emo.gagal} **Sepertinya anda mencurigakan...**")
    # return await client.block_user(in_user.id)
    # if in_user.is_support or in_user.is_verified or in_user.is_self:
    # return


@KY.CALLBACK("^(approve|block|to_scam_you|approve_me)")
async def pmpermit_cq(_, cq):
    lah = cq.from_user.id
    data = cq.data.split()
    lis = []
    for x in ubot._ubot:
        lis.append(x.me.id)
    getc_pm_txt = await get_var(int(x.me.id), "CUSTOM_PM_TEXT")
    getc_pm_txt if getc_pm_txt else DEFAULT_TEXT
    getc_pm_warns = await get_var(int(x.me.id), "CUSTOM_PM_WARNS_LIMIT")
    getc_pm_warns if getc_pm_warns else LIMIT
    if data[0] == "approve":
        if lah not in lis:
            await cq.answer("Tombol Ini Bukan Untuk Anda !", True)
        else:
            await add_approved_user(int(data[1]))
            return await bot.edit_inline_text(
                cq.inline_message_id, "Pengguna Di Setujui Untuk Mengirim Pesan."
            )

    elif data[0] == "block":
        if lah not in lis:
            await cq.answer("Tombol Ini Bukan Untuk Anda !", True)
        else:
            await bot.edit_inline_text(
                cq.inline_message_id, "Pengguna Berhasil Di Blokir."
            )
            try:
                await x.block_user(int(data[1]))
                return await x.invoke(
                    DeleteHistory(
                        peer=(await x.resolve_peer(int(data[1]))), max_id=0, revoke=True
                    )
                )
            except PeerIdInvalid:
                pass


@KY.INLINE("^pmpermit")
async def pmpermit_func(client, inline_query):
    victim = inline_query.from_user.id
    data = inline_query.query.split()
    # m = [obj for obj in get_objects() if id(obj) == int(data[1])][0]
    # rpk = f"[{m.from_user.first_name} {m.from_user.last_name or ''}](tg://user?id={m.from_user.id})"

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
            async for m in x.get_chat_history(int(data[1]), limit=custom_pm_warns):
                if m.reply_markup:
                    await m.delete()
            caption = PM_WARN.format(
                x.me.first_name,
                custom_pm_txt.format(bot.me.first_name),
                flood2[int(data[1])],
                custom_pm_warns,
            )
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


"""
@ubot.on_message(
    filters.private
    & filters.incoming
    & ~filters.me
    & ~filters.bot
    & ~filters.via_bot
    & ~filters.service,
    group=69,
)
async def handle_pmpermit(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    user_id = client.me.id
    siapa = message.from_user.id
    biji = message.from_user.mention
    chat_id = message.chat.id
    in_user = message.from_user
    fsdj = await check_user_approved(chat_id)
    is_pm_guard_enabled = await get_var(user_id, "ENABLE_PM_GUARD")
    if not is_pm_guard_enabled:
        return

    if fsdj:
        return

    if in_user.is_fake or in_user.is_scam:
        await message.reply(f"{emo.gagal} **Sepertinya anda mencurigakan...**")
        return await client.block_user(in_user.id)
    if in_user.is_support or in_user.is_verified or in_user.is_self:
        return
    if siapa in DEVS:
        try:
            await add_approved_user(chat_id)
            await client.send_message(
                chat_id,
                f"{emo.sukses} <b>Menerima Pesan Dari {biji} !!\nTerdeteksi Founder Dari {bot.me.mention}.</b>",
                parse_mode=enums.ParseMode.HTML,
            )
        except BaseException:
            pass
        return
    if siapa in await get_seles():
        try:
            await add_approved_user(chat_id)
            await client.send_message(
                chat_id,
                f"{emo.sukses} <b>Menerima Pesan Dari {biji} !!\nTerdeteksi Admin Dari {bot.me.mention}.</b>",
                parse_mode=enums.ParseMode.HTML,
            )
        except BaseException:
            pass
        return

    master = await client.get_me()
    getc_pm_txt = await get_var(user_id, "CUSTOM_PM_TEXT")
    getc_pm_warns = await get_var(user_id, "CUSTOM_PM_WARNS_LIMIT")
    custom_pm_txt = getc_pm_txt if getc_pm_txt else DEFAULT_TEXT
    custom_pm_warns = getc_pm_warns if getc_pm_warns else LIMIT
    if in_user.id in flood:
        try:
            if message.chat.id in PM_GUARD_MSGS_DB:
                await client.delete_messages(
                    chat_id=message.chat.id,
                    message_ids=PM_GUARD_MSGS_DB[message.chat.id],
                )
        except BaseException:
            pass
        flood[in_user.id] += 1
        if flood[in_user.id] >= custom_pm_warns:
            await eor(
                message,
                f"{emo.gagal} Saya sudah memberi tahu `{custom_pm_warns}` peringatan\nTunggu tuan saya menyetujui pesan anda, atau anda akan diblokir !**",
            )
            return await client.block_user(in_user.id)
        else:
            rplied_msg = await eor(
                message,
                PM_WARN.format(
                    emo.alive,
                    master.first_name,
                    custom_pm_txt.format(bot.me.first_name),
                    emo.gagal,
                    flood[in_user.id],
                    custom_pm_warns,
                ),
            )
    else:
        flood[in_user.id] = 1
        rplied_msg = await eor(
            message,
            PM_WARN.format(
                emo.alive,
                master.first_name,
                custom_pm_txt.format(bot.me.first_name),
                emo.gagal,
                flood[in_user.id],
                custom_pm_warns,
            ),
        )
    PM_GUARD_MSGS_DB[message.chat.id] = rplied_msg.id
"""

__MODULE__ = "Security"
__HELP__ = """
Bantuan Untuk Security

• Perintah: <code>{0}setdb antipm</code> [on atau off]
• Penjelasan: Untuk menghidupkan atau mematikan antipm

• Perintah: <code>{0}setmsg</code> [balas atau berikan pesan]
• Penjelasan: Untuk mengatur pesan antipm.

• Perintah: <code>{0}setlimit</code> [angka]
• Penjelasan: Untuk mengatur peringatan pesan blokir.

• Perintah: <code>{0}ok</code>
• Penjelasan: Untuk menyetujui pesan.

• Perintah: <code>{0}no</code>
• Penjelasan: Untuk menolak pesan.
"""
