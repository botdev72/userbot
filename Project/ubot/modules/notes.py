from pyrogram import errors
from pyrogram.types import *

from ubot import KY, Emo, bot, ubot
from ubot.core.database import notes_sql as db
from ubot.core.helpers.dibut import build_keyboard, parse_button
from ubot.core.helpers.msg_types import Types, get_note_type
from ubot.utils.PyroHelpers import ReplyCheck

# TODO: Add buttons support in some types
# TODO: Add group notes, but whats for? since only you can get notes

__MODULE__ = "Notes"
__HELP__ = """Bantuan Untuk Notes


• Perintah: <code>{0}save</code> [nama catatan] [balas pesan]
• Penjelasan: Untuk menyimpan catatan.

• Perintah: <code>{0}get</code> [nama catatan]
• Penjelasan: Untuk mengambil catatan.

• Perintah: <code>{0}rm</code> [nama catatan]
• Penjelasan: Untuk menghapus catatan.

• Perintah: <code>{0}notes</code>
• Penjelasan: Untuk melihat semua catatan.

• Button Format :
-> Teks [Klik](buttonurl:link)
-> Teks 2 [Klik 2](buttonurl:link:same)
"""


@KY.UBOT("save", sudo=True)
async def save_note(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    note_name, text, data_type, content = get_note_type(message)
    xx = await message.reply(f"{emo.proses} **Processing...**")

    if not note_name:
        return await xx.edit(
            f"{emo.gagal} <b>Gunakan format :</b> <code>save</code> [nama catatan] [balas ke pesan]."
        )

    if data_type == Types.TEXT:
        teks, _ = parse_button(text)
        if not teks:
            return await xx.edit(f"{emo.gagal} <b>Teks tidak dapat kosong.</b>")
    db.save_selfnote(client.me.id, note_name, text, data_type, content)
    await xx.edit(
        f"{emo.sukses} <b>Catatan <code>{note_name}</code> berhasil disimpan.</b>"
    )


@KY.UBOT("get", sudo=True)
async def get_note(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    xx = await message.reply(f"{emo.proses} **Processing...**")
    note = None
    if len(message.text.split()) >= 2:
        note = message.text.split()[1]
    else:
        await xx.edit(f"{emo.gagal} **Give me a note tag!**")

    getnotes = db.get_selfnote(client.me.id, note)
    teks = None
    file_id = getnotes.get("file")
    if not getnotes:
        return await xx.edit(f"{emo.gagal} **This note does not exist!**")

    if getnotes["type"] == Types.TEXT:
        teks, button = parse_button(getnotes.get("value"))
        button = build_keyboard(button)
        if button:
            button = InlineKeyboardMarkup(button)
        else:
            button = None
        if button:
            try:
                inlineresult = await client.get_inline_bot_results(
                    bot.me.username, f"get_note_ {note}"
                )
                await message.delete()
                await client.send_inline_bot_result(
                    message.chat.id,
                    inlineresult.query_id,
                    inlineresult.results[0].id,
                    reply_to_message_id=ReplyCheck(message),
                )
            except IndexError:
                return await xx.edit(
                    "An error has accured! Check your assistant for more information!"
                )
        else:
            await message.reply(teks)
            # await xx.edit(teks)
    elif getnotes["type"] == Types.PHOTO:
        teks, button = parse_button(getnotes.get("value"))
        button = build_keyboard(button)
        if button:
            button = InlineKeyboardMarkup(button)
        else:
            button = None
        if file_id is not None:
            try:
                inlineresult = await client.get_inline_bot_results(
                    bot.me.username, f"get_note_ {note}"
                )
                await message.delete()
                await client.send_inline_bot_result(
                    message.chat.id,
                    inlineresult.query_id,
                    inlineresult.results[0].id,
                    reply_to_message_id=ReplyCheck(message),
                )
            except Exception as e:
                return await xx.edit(f"Error {e}")
        else:
            await client.send_photo(
                message.chat.id,
                file_id,
                caption=getnotes["value"],
                reply_to_message_id=ReplyCheck(message),
            )
    elif getnotes["type"] == Types.VIDEO:
        await client.send_video(
            message.chat.id,
            getnotes["file"],
            caption=getnotes["value"],
            reply_to_message_id=ReplyCheck(message),
        )
    elif getnotes["type"] == Types.STICKER:
        await client.send_sticker(
            message.chat.id, getnotes["file"], reply_to_message_id=ReplyCheck(message)
        )
    elif getnotes["type"] == Types.VOICE:
        await client.send_voice(
            message.chat.id,
            getnotes["file"],
            caption=getnotes["value"],
            reply_to_message_id=ReplyCheck(message),
        )
    elif getnotes["type"] == Types.VIDEO_NOTE:
        await client.send_video_note(
            message.chat.id,
            getnotes["file"],
            # caption=getnotes["value"],
            reply_to_message_id=ReplyCheck(message),
        )
    elif getnotes["type"] == Types.ANIMATED_STICKER:
        await client.send_sticker(
            message.chat.id,
            getnotes["file"],
            # caption=getnotes["value"],
            reply_to_message_id=ReplyCheck(message),
        )
    else:
        if getnotes.get("value"):
            teks, button = parse_button(getnotes.get("value"))
            button = build_keyboard(button)
            if button:
                button = InlineKeyboardMarkup(button)
            else:
                button = None
        else:
            teks = None
            button = None
        if button:
            try:
                inlineresult = await client.get_inline_bot_results(
                    bot.me.username, f"get_note_ {note}"
                )
            except errors.exceptions.bad_request_400.BotInlineDisabled:
                await message.edit(
                    "Your bot inline isn't available!\nCheck your bot for more information!"
                )
                return
            try:
                await message.delete()
                await client.send_inline_bot_result(
                    message.chat.id,
                    inlineresult.query_id,
                    inlineresult.results[0].id,
                    reply_to_message_id=ReplyCheck(message),
                )
            except IndexError:
                await message.edit(
                    "An error has accured! Check your assistant for more information!"
                )
                return
        else:
            await client.send_media_group(
                message.chat.id,
                getnotes["file"],
                caption=teks,
                reply_to_message_id=ReplyCheck(message),
            )
    await xx.delete()


@KY.UBOT("notes", sudo=True)
async def local_notes(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    xx = await message.reply(f"{emo.proses} **Processing...**")
    getnotes = db.get_all_selfnotes(client.me.id)
    if not getnotes:
        await xx.edit(f"{emo.gagal} **There are no notes in local notes!**")
        return
    rply = f"{emo.alive} **Local notes:**\n"
    for x in getnotes:
        if len(rply) >= 1800:
            await xx.edit(rply)
            rply = f"{emo.alive} **Local notes:**\n"
        rply += f"{emo.sukses} `{x}`\n"

    await xx.edit(rply)


@KY.UBOT("rm", sudo=True)
async def clear_note(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    xx = await message.reply(f"{emo.proses} **Processing...**")
    if len(message.text.split()) <= 1:
        return await xx.edit(f"{emo.gagal} **What do you want to clear?**")

    note = message.text.split()[1]
    getnote = db.rm_selfnote(client.me.id, note)
    if not getnote:
        return await xx.edit(f"{emo.gagal} **This note does not exist!**")

    await xx.edit(f"{emo.sukses} **Deleted note `{note}`!**")


@KY.INLINE("^get_note_")
# @bot.on_inline_query()
async def catet(client, inline_query):
    for x in ubot._ubot:
        x.me.id
    q = inline_query.query.split(None, 1)
    # q2 = inline_query.query.split()
    # ky = [obj for obj in get_objects() if id(obj) == int(q2[1])][0]
    notetag = q[1]
    noteval = db.get_selfnote(inline_query.from_user.id, notetag)
    # noteval["file"] = await get_var(inline_query.from_user.id, "note_pic")
    if not noteval:
        return
    note, button = parse_button(noteval.get("value"))
    button = build_keyboard(button)
    if noteval["type"] == Types.TEXT:
        akhir = [
            (
                InlineQueryResultArticle(
                    title="Tombol Notes!",
                    input_message_content=InputTextMessageContent(note),
                    reply_markup=InlineKeyboardMarkup(button),
                )
            )
        ]
    else:
        if noteval["file"] and (
            noteval["file"].startswith("http://")
            or noteval["file"].startswith("https://")
        ):
            duanya = (
                InlineQueryResultVideo
                if noteval["file"].endswith(".mp4")
                else InlineQueryResultPhoto
            )
            link_nya = (
                {"video_url": noteval["file"], "thumb_url": noteval["file"]}
                if noteval["file"].endswith(".mp4")
                else {"photo_url": noteval["file"]}
            )
            akhir = [
                duanya(
                    **link_nya,
                    title="Tombol Notes!",
                    caption=note,
                    reply_markup=InlineKeyboardMarkup(button),
                ),
            ]
    await client.answer_inline_query(
        inline_query.id,
        cache_time=0,
        results=akhir,
    )


"""
    if noteval["type"] == Types.TEXT:
        await client.answer_inline_query(
            inline_query.id,
            cache_time=0,
            results=[

            ],
        )

    elif noteval["type"] == Types.PHOTO:
        await client.answer_inline_query(
            inline_query.id,
            cache_time=0,
            results=[
                (
                    InlineQueryResultPhoto(
                        title="Note Photo",
                        photo_url=noteval["file"].photo,
                        caption=noteval["value"],
                        reply_markup=InlineKeyboardMarkup(button),
                    )
                )
            ],
        )
    elif noteval["type"] == Types.VIDEO:
        await client.answer_inline_query(
            inline_query.id,
            cache_time=0,
            results=[
                (
                    InlineQueryResultVideo(
                        title="Note Video",
                        video_url=note["file"],
                        caption=note["value"],
                        reply_markup=InlineKeyboardMarkup(button),
                    )
                )
            ],
        )



    allnotes = db.get_all_selfnotes_inline(inline_query.from_user.id)
    if not allnotes:
        return
    if len(allnotes) >= 30:
        rng = 30
    else:
        rng = len(allnotes)
        for x in range(rng):
            note = allnotes[(allnotes)[x]]
            noteval = note["value"]
            # note["type"]
            # note["file"]
            
    
    
"""
