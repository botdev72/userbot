import datetime
from gc import get_objects
from random import randint

from pykeyboard import InlineKeyboard
from pyrogram import filters
from pyrogram.errors import MessageNotModified, QueryIdInvalid
from pyrogram.raw.functions.phone import CreateGroupCall
from pyrogram.types import *
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import (HighQualityAudio,
                                                  HighQualityVideo)
from yt_dlp import YoutubeDL

from ubot import *
from ubot.core.pytgcalls import queues


# from ubot.utils import require_admin
# @require_admin("can_manage_video_chats", "Hak admin yang diperlukan: <code>Manage Live Streams</code>",)


play_id = []



async def play_nya(client, message):
    if message.reply_to_message:
        if len(message.command) < 2:
            chat_id = message.chat.id
        else:
            chat_id = int(message.text.split()[1])
        if message.reply_to_message.audio or message.reply_to_message.voice:
            if chat_id in play_id:
                return await message.reply(
                    "<b>Ada proses yang sedang berlangsung...</b>"
                )
            play_id.append(chat_id)
            _play_ = await message.reply_to_message.reply("<b>❏ Processing Audio...</b>")
            dl = await client.download_media(message.reply_to_message)
            link = message.reply_to_message.link
            if chat_id in client.call_py.calls:
                pos = await queues.put(chat_id, file=AudioPiped(dl, HighQualityAudio()))
                await _play_.delete()
                __play__ = await message.reply_to_message.reply(
                    f"<b>❏ <a href={link}>Audio</a> Antrian » {pos}</b>",
                    disable_web_page_preview=True,
                )
                await message.delete()
                play_id.remove(chat_id)
            else:
                await client.call_py.join_group_call(
                    chat_id,
                    AudioPiped(dl, HighQualityAudio()),
                    
                )
                await _play_.delete()
                __play__ = await message.reply_to_message.reply(
                    f"<b>❏ Memutar <a href={link}>Audio</a></b>",
                    disable_web_page_preview=True,
                )
                await message.delete()
                play_id.remove(chat_id)
        if message.reply_to_message.video or message.reply_to_message.document:
            if chat_id in play_id:
                return await message.reply(
                    "<b>Ada proses yang sedang berlangsung...</b>"
                )
            play_id.append(chat_id)
            _play_ = await message.reply_to_message.reply("<b>❏ Processing Video...</b>")
            dl = await client.download_media(message.reply_to_message)
            link = message.reply_to_message.link
            if chat_id in client.call_py.calls:
                pos = await queues.put(
                    chat_id,
                    file=AudioVideoPiped(dl, HighQualityAudio(), HighQualityVideo()),
                )
                await _play_.delete()
                __play__ = await message.reply_to_message.reply(
                    f"<b>❏ <a href={link}>Video</a> Antrian » {pos}</b>",
                    disable_web_page_preview=True,
                )
                await message.delete()
                play_id.remove(chat_id)
            else:
                await client.call_py.join_group_call(
                    chat_id,
                    AudioVideoPiped(dl, HighQualityAudio(), HighQualityVideo()),
                    
                )
                await _play_.delete()
                __play__ = await message.reply_to_message.reply(
                    f"<b>❏ Memutar <a href={link}>Video</a></b>",
                    disable_web_page_preview=True,
                )
                await message.delete()
                play_id.remove(chat_id)
    else:
        if len(message.text.split()) < 2:
            return await message.reply_text(
                "<b>Silakan masukkan judul lagu atau video.</b>",
            )
        if "-1001" not in message.text:
            query = f"_yts {id(message)}"
            chat_id = message.chat.id
        else:
            query = f"_x {id(message)}"
            chat_id = int(message.text.split()[1])
        if chat_id in play_id:
            return await message.reply(
                "<b>Ada proses yang sedang berlangsung...</b>"
            )
        play_id.append(chat_id)
        infomsg = await message.reply_text("<b>❏ Searching...</b>")
        x = await client.get_inline_bot_results(bot.me.username, query)
        try:
            await message.reply_inline_bot_result(x.query_id, x.results[0].id)
            play_id.remove(chat_id)
            await infomsg.delete()
            await message.delete()
        except Exception as error:
            await message.reply(error)
            play_id.remove(chat_id)


async def inline_play1(_, q: InlineQuery):
    m = [obj for obj in get_objects() if id(obj) == int(q.query.split(None, 1)[1])][0]
    query = (m.text or m.caption).split(None, 1)[1]
    results = YouTubeSearch(query, max_results=10).to_dict()
    videoid = results[0]["id"]
    title = results[0]["title"]
    duration = results[0]["duration"]
    thumb = f"https://img.youtube.com/vi/{videoid}/hqdefault.jpg"
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="📀 Music",
                    callback_data=f"_p 0|{videoid}|{q.query.split(None, 1)[1]}",
                ),
                InlineKeyboardButton(
                    text="Video 📽️",
                    callback_data=f"_v 0|{videoid}|{q.query.split(None, 1)[1]}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔍 Selanjutnya",
                    callback_data=f"_s 0|0|{q.query.split(None, 1)[1]}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="≪",
                    callback_data=f"_c B|0|{q.query.split(None, 1)[1]}",
                ),
                InlineKeyboardButton(
                    text="Tutup",
                    callback_data=f"1_cls {m.from_user.id}",
                ),
                InlineKeyboardButton(
                    text="≫",
                    callback_data=f"_c F|0|{q.query.split(None, 1)[1]}",
                ),
            ],
        ]
    )
    msg = f"""
❏ <b>Judul: <a href='https://youtu.be/{videoid}'>{title}</a></b>
 <b>├ Durasi:</b> {duration}
 <b>╰  <a href='https://t.me/{bot.me.username}?start=InfoLagu_{videoid}'>More information</a></b>"""
    await q.answer(
        [
            InlineQueryResultPhoto(
                photo_url=thumb,
                title="search",
                caption=msg,
                reply_markup=buttons,
            )
        ]
    )



async def call_back1(_, cq):
    try:
        await cq.answer()
    except QueryIdInvalid:
        pass
    what, type, idm = cq.data.strip().split(None, 1)[1].split("|")
    m = [obj for obj in get_objects() if id(obj) == int(idm)][0]
    if not cq.from_user or cq.from_user.id != int(m.from_user.id):
        return
    what = str(what)
    type = int(type)
    if what == "F":
        if type == 9:
            query_type = 0
        else:
            query_type = int(type + 1)
        query = (m.text or m.caption).split(None, 1)[1]
        results = YouTubeSearch(query, max_results=10).to_dict()
        videoid = results[query_type]["id"]
        title = results[query_type]["title"]
        duration = results[query_type]["duration"]
        thumb = f"https://img.youtube.com/vi/{videoid}/hqdefault.jpg"
        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="📀 Music",
                        callback_data=f"_p {query_type}|{videoid}|{idm}",
                    ),
                    InlineKeyboardButton(
                        text="Video 📽️",
                        callback_data=f"_v {query_type}|{videoid}|{idm}",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="🔍 Selanjutnya",
                        callback_data=f"_s 0|0|{idm}",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="≪",
                        callback_data=f"_c B|{query_type}|{idm}",
                    ),
                    InlineKeyboardButton(
                        text="Tutup",
                        callback_data=f"1_cls {m.from_user.id}",
                    ),
                    InlineKeyboardButton(
                        text="≫",
                        callback_data=f"_c F|{query_type}|{idm}",
                    ),
                ],
            ]
        )
        med = InputMediaPhoto(
            media=thumb,
            caption=f"""
❏ <b>Judul: <a href='https://youtu.be/{videoid}'>{title}</a></b>
 <b>├ Durasi:</b> {duration}
 <b>╰ <a href='https://t.me/{bot.me.username}?start=InfoLagu_{videoid}'>More information</a></b>""",
        )
        return await cq.edit_message_media(
            media=med,
            reply_markup=buttons,
        )
    if what == "B":
        if type == 0:
            query_type = 9
        else:
            query_type = int(type - 1)
        query = (m.text or m.caption).split(None, 1)[1]
        results = YouTubeSearch(query, max_results=10).to_dict()
        videoid = results[query_type]["id"]
        title = results[query_type]["title"]
        duration = results[query_type]["duration"]
        thumb = f"https://img.youtube.com/vi/{videoid}/hqdefault.jpg"
        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="📀 Music",
                        callback_data=f"_p {query_type}|{videoid}|{idm}",
                    ),
                    InlineKeyboardButton(
                        text="Video 📽️",
                        callback_data=f"_v {query_type}|{videoid}|{idm}",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="🔍 Selanjutnya",
                        callback_data=f"_s 0|0|{idm}",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="≪",
                        callback_data=f"_c B|{query_type}|{idm}",
                    ),
                    InlineKeyboardButton(
                        text="Tutup",
                        callback_data=f"1_cls {m.from_user.id}",
                    ),
                    InlineKeyboardButton(
                        text="≫",
                        callback_data=f"_c F|{query_type}|{idm}",
                    ),
                ],
            ]
        )
        med = InputMediaPhoto(
            media=thumb,
            caption=f"""
❏ <b>Judul: <a href='https://youtu.be/{videoid}'>{title}</a></b>
 <b>├ Durasi:</b> {duration}
 <b>╰ <a href='https://t.me/{bot.me.username}?start=InfoLagu_{videoid}'>More information</a></b>""",
        )
        return await cq.edit_message_media(
            media=med,
            reply_markup=buttons,
        )


async def call_back2(_, cq: CallbackQuery):
    try:
        await cq.answer()
    except QueryIdInvalid:
        pass
    s, x, idm = cq.data.strip().split(None, 1)[1].split("|")
    m = [obj for obj in get_objects() if id(obj) == int(idm)][0]
    if not cq.from_user or cq.from_user.id != int(m.from_user.id):
        return
    query = (m.text or m.caption).split(None, 1)[1]
    results = YouTubeSearch(query, max_results=10).to_dict()
    if len(results) < 6:
        return
    if int(x) == 0:
        msg = ""
        emoji_list: Iterable[str] = ("𝟏", "𝟐", "𝟑", "𝟒", "𝟓")
        buttons = InlineKeyboard(row_width=3)
        keyboard: List[InlineKeyboardButton] = []
        for i in range(min(5, len(results))):
            msg += f"{emoji_list[i]} <b><a href='https://youtu.be/{results[i]['id']}'>{results[i]['title'][:25]}</a></b>\n"
            msg += f" <b>├ Durasi</b> {results[i]['duration']}\n"
            msg += f" <b>╰ <a href='https://t.me/{bot.me.username}?start=InfoLagu_{results[i]['id']}'>More information</a></b>\n\n"
            keyboard.append(
                InlineKeyboardButton(
                    f"{emoji_list[i]}",
                    callback_data=f"_s {results[i]['id']}|3|{idm}",
                )
            )
        buttons.add(*keyboard)
        if len(results) > 5:
            buttons.row(InlineKeyboardButton("≫", callback_data=f"_s 0|2|{idm}"))
        buttons.row(
            InlineKeyboardButton("Tutup", callback_data=f"1_cls {m.from_user.id}")
        )
        try:
            await cq.edit_message_media(
                InputMediaPhoto(
                    "https://telegra.ph/file/0dda72dec9ddb21650f63.jpg",
                    caption=msg,
                ),
                reply_markup=buttons,
            )
        except MessageNotModified:
            pass
    elif int(x) == 1:
        msg = ""
        emoji_list: Iterable[str] = ("𝟏", "𝟐", "𝟑", "𝟒", "𝟓")
        buttons = InlineKeyboard(row_width=3)
        keyboard: List[InlineKeyboardButton] = []
        for i in range(min(5, len(results))):
            msg += f"{emoji_list[i]} <b><a href='https://youtu.be/{results[i]['id']}'>{results[i]['title'][:25]}</a></b>\n"
            msg += f" <b>├ Durasi</b> {results[i]['duration']}\n"
            msg += f" <b>╰ <a href='https://t.me/{bot.me.username}?start=InfoLagu_{results[i]['id']}'>More information</a></b>\n\n"
            keyboard.append(
                InlineKeyboardButton(
                    f"{emoji_list[i]}",
                    callback_data=f"_s {results[i]['id']}|3|{idm}",
                )
            )
        buttons.add(*keyboard)
        if len(results) > 5:
            buttons.row(InlineKeyboardButton("≫", callback_data=f"_s 0|2|{idm}"))
        buttons.row(
            InlineKeyboardButton("Tutup", callback_data=f"1_cls {m.from_user.id}")
        )
        try:
            await cq.edit_message_text(
                msg,
                reply_markup=buttons,
            )
        except MessageNotModified:
            pass
    elif int(x) == 2:
        msg = ""
        emoji_list: Iterable[str] = (
            "𝟏",
            "𝟐",
            "𝟑",
            "𝟒",
            "𝟓",
            "𝟔",
            "𝟕",
            "𝟖",
            "𝟗",
            "𝟏𝟎",
        )
        buttons = InlineKeyboard(row_width=3)
        keyboard: List[InlineKeyboardButton] = []
        for i in range(5, len(results)):
            msg += f"{emoji_list[i]} <b><a href='https://youtu.be/{results[i]['id']}'>{results[i]['title'][:25]}</a></b>\n"
            msg += f" <b>├ Durasi</b> {results[i]['duration']}\n"
            msg += f" <b>╰ <a href='https://t.me/{bot.me.username}?start=InfoLagu_{results[i]['id']}'>More information</a></b>\n\n"
            keyboard.append(
                InlineKeyboardButton(
                    f"{emoji_list[i]}",
                    callback_data=f"_s {results[i]['id']}|3|{idm}",
                )
            )
        buttons.add(*keyboard)
        buttons.row(InlineKeyboardButton("≪", callback_data=f"_s 0|1|{idm}"))
        buttons.row(
            InlineKeyboardButton("Tutup", callback_data=f"1_cls {m.from_user.id}")
        )
        try:
            await cq.edit_message_text(
                msg,
                reply_markup=buttons,
            )
        except MessageNotModified:
            pass
    elif int(x) == 3:
        with YoutubeDL({"quiet": True}) as ytdl:
            data = ytdl.extract_info(f"https://youtu.be/{s}", download=False)
        title = data["title"]
        duration = datetime.timedelta(seconds=data["duration"])
        videoid = data["id"]
        thumb = f"https://img.youtube.com/vi/{videoid}/hqdefault.jpg"
        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="📀 Music",
                        callback_data=f"_p 0|{videoid}|{idm}",
                    ),
                    InlineKeyboardButton(
                        text="Video 📽️",
                        callback_data=f"_v 0|{videoid}|{idm}",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="≪",
                        callback_data=f"_s 0|0|{idm}",
                    ),
                    InlineKeyboardButton(
                        text="Tutup",
                        callback_data=f"1_cls {m.from_user.id}",
                    ),
                ],
            ]
        )
        msg = f"""
❏ <b>Judul: <a href='https://youtu.be/{videoid}'>{title}</a></b>
 <b>├ Durasi:</b> {duration}
 <b>╰ <a href='https://t.me/{bot.me.username}?start=InfoLagu_{videoid}'>More information</a></b>
"""
        await cq.edit_message_media(
            InputMediaPhoto(thumb, caption=msg), reply_markup=buttons
        )



async def call_back3(_, cq: CallbackQuery):
    try:
        await cq.answer()
    except QueryIdInvalid:
        pass
    what, type, idm = cq.data.strip().split(None, 1)[1].split("|")
    m = [obj for obj in get_objects() if id(obj) == int(idm)][0]
    if cq.from_user.id != m.from_user.id:
        return
    await cq.edit_message_text(f"<b>❏ Processing...</b>")
    url = f"https://youtu.be/{type}"
    ydl = YoutubeDL(
        {
            "quiet": True,
            "no_warnings": True,
            "format": "bestaudio[ext=m4a]",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "nocheckcertificate": True,
            "geo_bypass": True,
        }
    )
    yt = await run_sync(ydl.extract_info, url, download=True)
    title = yt["title"]
    duration = yt["duration_string"]
    file_path = ydl.prepare_filename(yt)
    thumb = f"https://img.youtube.com/vi/{yt['id']}/hqdefault.jpg"
    pl_btn = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="• Tutup •",
                    callback_data=f"1_cls {m.from_user.id}",
                ),
            ],
        ]
    )
    capt1 = f"""
<b>❏ Nama:</b> <a href={url}>{title}</a>
<b>├ Durasi:</b> <code>{duration}</code>
<b>├ <a href=https://t.me/{bot.me.username}?start=InfoLagu_{yt["id"]}>Information</a></b>
<b>╰ Atas Permintaan:</b> <a href=tg://openmessage?user_id={cq.from_user.id}>{cq.from_user.first_name} {cq.from_user.last_name or ''}</a>
"""
    if m.chat.id in m._client.call_py.calls:
        position = await queues.put(
            m.chat.id, file=AudioPiped(file_path, HighQualityAudio())
        )
        capt2 = (
            f"<b>📝 Music Ditambahkan Ke Antrian</b> » <code>{position}</code>\n" + capt1
        )
        await cq.edit_message_media(
            InputMediaPhoto(thumb, caption=capt2), reply_markup=pl_btn
        )
    else:
        try:
            await m._client.call_py.join_group_call(
                m.chat.id,
                AudioPiped(file_path, HighQualityAudio()),
                
            )
        except Exception as e:
            if "Already joined into group call" not in str(e):
                if "No active group call" in str(e):
                    try:
                        await m._client.invoke(
                            CreateGroupCall(
                                peer=await m._client.resolve_peer(m.chat.id),
                                random_id=randint(0, 2147483647),
                            )
                        )
                    except Exception:
                        await m._client.send_message(
                            m.chat.id,
                            "❏ Maaf, <b>tidak</b> ada obrolan video yang aktif!\n\n• untuk menggunakan saya, <b>mulai obrolan video</b>.",
                        )
                        unPacked = unpackInlineMessage(cq.inline_message_id)
                        return await m._client.delete_messages(
                            unPacked.chat_id, unPacked.message_id
                        )
                    await m._client.call_py.join_group_call(
                        m.chat.id,
                        AudioPiped(file_path, HighQualityAudio()),
                        
                    )
                else:
                    await m._client.send_message(
                        m.chat.id,
                        str(e),
                    )
                    unPacked = unpackInlineMessage(cq.inline_message_id)
                    return await m._client.delete_messages(
                        unPacked.chat_id, unPacked.message_id
                    )
        await cq.edit_message_media(
            InputMediaPhoto(thumb, caption="<b>❏ Sedang Memutar Music</b>\n" + capt1),
            reply_markup=pl_btn,
        )


async def call_back4(_, cq: CallbackQuery):
    try:
        await cq.answer()
    except QueryIdInvalid:
        pass
    what, type, idm = cq.data.strip().split(None, 1)[1].split("|")
    m = [obj for obj in get_objects() if id(obj) == int(idm)][0]
    if not cq.from_user or cq.from_user.id != m.from_user.id:
        return
    await cq.edit_message_text(f"<b>❏ Processing...</b>")
    url = f"https://youtu.be/{type}"
    ydl = YoutubeDL(
        {
            "quiet": True,
            "no_warnings": True,
            "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "nocheckcertificate": True,
            "geo_bypass": True,
        }
    )
    yt = await run_sync(ydl.extract_info, url, download=True)
    title = yt["title"]
    duration = yt["duration_string"]
    file_path = ydl.prepare_filename(yt)
    thumb = f"https://img.youtube.com/vi/{yt['id']}/hqdefault.jpg"
    pl_btn = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="• Tutup •",
                    callback_data=f"1_cls {m.from_user.id}",
                ),
            ],
        ]
    )
    capt1 = f"""
<b>❏ Nama:</b> <a href={url}>{title}</a>
<b>├ Durasi:</b> <code>{duration}</code>
<b>╰ <a href=https://t.me/{bot.me.username}?start=InfoLagu_{yt["id"]}>Information</a></b>
<b>╰ Atas Permintaan:</b> <a href=tg://openmessage?user_id={cq.from_user.id}>{cq.from_user.first_name} {cq.from_user.last_name or ''}</a>
"""
    if m.chat.id in m._client.call_py.calls:
        position = await queues.put(
            m.chat.id,
            file=AudioVideoPiped(file_path, HighQualityAudio(), HighQualityVideo()),
        )
        capt2 = (
            f"<b>❏ Video Ditambahkan Ke Antrian</b> » <code>{position}</code>\n" + capt1
        )
        await cq.edit_message_media(
            InputMediaPhoto(thumb, caption=capt2), reply_markup=pl_btn
        )
    else:
        try:
            await m._client.call_py.join_group_call(
                m.chat.id,
                AudioVideoPiped(file_path, HighQualityAudio(), HighQualityVideo()),
                
            )
        except Exception as e:
            if "Already joined into group call" not in str(e):
                if "No active group call" in str(e):
                    try:
                        await m._client.invoke(
                            CreateGroupCall(
                                peer=await m._client.resolve_peer(m.chat.id),
                                random_id=randint(0, 2147483647),
                            )
                        )
                    except Exception:
                        await m._client.send_message(
                            m.chat.id,
                            "❏ Maaf, <b>tidak</b> ada obrolan video yang aktif!\n\n• untuk menggunakan saya, <b>mulai obrolan video</b>.",
                        )
                        unPacked = unpackInlineMessage(cq.inline_message_id)
                        return await m._client.delete_messages(
                            unPacked.chat_id, unPacked.message_id
                        )
                    await m._client.call_py.join_group_call(
                        m.chat.id,
                        AudioVideoPiped(
                            file_path, HighQualityAudio(), HighQualityVideo()
                        ),
                        
                    )
                else:
                    await m._client.send_message(
                        m.chat.id,
                        str(e),
                    )
                    unPacked = unpackInlineMessage(cq.inline_message_id)
                    return await m._client.delete_messages(
                        unPacked.chat_id, unPacked.message_id
                    )
        await cq.edit_message_media(
            InputMediaPhoto(thumb, caption="<b>❏ Sedang Memutar Video</b>\n" + capt1),
            reply_markup=pl_btn,
        )



async def inline_play2(_, q: InlineQuery):
    m = [obj for obj in get_objects() if id(obj) == int(q.query.split(None, 1)[1])][0]
    query = (m.text or m.caption).split(None, 2)[2]
    results = YouTubeSearch(query, max_results=10).to_dict()
    videoid = results[0]["id"]
    title = results[0]["title"]
    duration = results[0]["duration"]
    thumb = f"https://img.youtube.com/vi/{videoid}/hqdefault.jpg"
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="📀 Music",
                    callback_data=f"_xp 0|{videoid}|{q.query.split(None, 1)[1]}",
                ),
                InlineKeyboardButton(
                    text="Video 📽️",
                    callback_data=f"_mxv 0|{videoid}|{q.query.split(None, 1)[1]}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Tutup",
                    callback_data=f"1_cls {m.from_user.id}",
                ),
            ],
        ]
    )
    msg = f"""
❏ <b>Judul: <a href='https://youtu.be/{videoid}'>{title}</a></b>
 <b>├ Durasi:</b> {duration}
 <b>╰ <a href='https://t.me/{bot.me.username}?start=InfoLagu_{videoid}'>More information</a></b>"""
    await q.answer(
        [
            InlineQueryResultPhoto(
                photo_url=thumb,
                title="search",
                caption=msg,
                reply_markup=buttons,
            )
        ]
    )



async def call_back5(_, cq: CallbackQuery):
    try:
        await cq.answer()
    except QueryIdInvalid:
        pass
    what, type, idm = cq.data.strip().split(None, 1)[1].split("|")
    m = [obj for obj in get_objects() if id(obj) == int(idm)][0]
    chat_id = int((m.text or m.caption).split(None, 2)[1])
    if not cq.from_user or cq.from_user.id != m.from_user.id:
        return
    await cq.edit_message_text(f"<b>❏ Processing...</b>")
    url = f"https://youtu.be/{type}"
    ydl = YoutubeDL(
        {
            "quiet": True,
            "no_warnings": True,
            "format": "bestaudio[ext=m4a]",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "nocheckcertificate": True,
            "geo_bypass": True,
        }
    )
    yt = await run_sync(ydl.extract_info, url, download=True)
    title = yt["title"]
    duration = yt["duration_string"]
    file_path = ydl.prepare_filename(yt)
    thumb = f"https://img.youtube.com/vi/{yt['id']}/hqdefault.jpg"
    pl_btn = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Tutup",
                    callback_data=f"1_cls {m.from_user.id}",
                ),
            ],
        ]
    )
    capt1 = f"""
<b>❏ Nama:</b> <a href={url}>{title}</a>
<b>├ Durasi:</b> <code>{duration}</code>
<b>├ <a href=https://t.me/{bot.me.username}?start=InfoLagu_{yt["id"]}>Information</a></b>
<b>╰ Atas Permintaan:</b> <a href=tg://openmessage?user_id={cq.from_user.id}>{cq.from_user.first_name} {cq.from_user.last_name or ''}</a>
"""
    if chat_id in m._client.call_py.calls:
        position = await queues.put(
            chat_id, file=AudioPiped(file_path, HighQualityAudio())
        )
        capt2 = (
            f"<b>📝 Music Ditambahkan Ke Antrian</b> » <code>{position}</code>\n" + capt1
        )
        await cq.edit_message_media(
            InputMediaPhoto(thumb, caption=capt2), reply_markup=pl_btn
        )
    else:
        try:
            await m._client.call_py.join_group_call(
                chat_id,
                AudioPiped(file_path, HighQualityAudio()),
                
            )
        except Exception as e:
            if "Already joined into group call" not in str(e):
                if "No active group call" in str(e):
                    try:
                        await m._client.invoke(
                            CreateGroupCall(
                                peer=await m._client.resolve_peer(chat_id),
                                random_id=randint(0, 2147483647),
                            )
                        )
                    except Exception:
                        await m._client.send_message(
                            m.chat.id,
                            "❏ Maaf, <b>tidak</b> ada obrolan video yang aktif!\n\n• untuk menggunakan saya, <b>mulai obrolan video</b>.",
                        )
                        unPacked = unpackInlineMessage(cq.inline_message_id)
                        return await m._client.delete_messages(
                            unPacked.chat_id, unPacked.message_id
                        )
                    await m._client.call_py.join_group_call(
                        m.chat.id,
                        AudioPiped(file_path, HighQualityAudio()),
                        
                    )
                else:
                    await m._client.send_message(
                        m.chat.id,
                        str(e),
                    )
                    unPacked = unpackInlineMessage(cq.inline_message_id)
                    return await m._client.delete_messages(
                        unPacked.chat_id, unPacked.message_id
                    )
        await cq.edit_message_media(
            InputMediaPhoto(thumb, caption="<b>❏ Sedang Memutar Music</b>\n" + capt1),
            reply_markup=pl_btn,
        )



async def call_back6(_, cq: CallbackQuery):
    try:
        await cq.answer()
    except QueryIdInvalid:
        pass
    what, type, idm = cq.data.strip().split(None, 1)[1].split("|")
    m = [obj for obj in get_objects() if id(obj) == int(idm)][0]
    chat_id = int((m.text or m.caption).split(None, 2)[1])
    if not cq.from_user or cq.from_user.id != m.from_user.id:
        return
    await cq.edit_message_text(f"<b>❏ Processing...</b>")
    url = f"https://youtu.be/{type}"
    ydl = YoutubeDL(
        {
            "quiet": True,
            "no_warnings": True,
            "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "nocheckcertificate": True,
            "geo_bypass": True,
        }
    )
    yt = await run_sync(ydl.extract_info, url, download=True)
    title = yt["title"]
    duration = yt["duration_string"]
    file_path = ydl.prepare_filename(yt)
    thumb = f"https://img.youtube.com/vi/{yt['id']}/hqdefault.jpg"
    pl_btn = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Tutup",
                    callback_data=f"1_cls {m.from_user.id}",
                ),
            ],
        ]
    )
    capt1 = f"""
<b>❏ Nama:</b> <a href={url}>{title}</a>
<b>├ Durasi:</b> <code>{duration}</code>
<b>├ <a href=https://t.me/{bot.me.username}?start=InfoLagu_{yt["id"]}>Information</a></b>
<b>╰ Atas Permintaan:</b> <a href=tg://openmessage?user_id={cq.from_user.id}>{cq.from_user.first_name} {cq.from_user.last_name or ''}</a>
"""
    if chat_id in m._client.call_py.calls:
        position = await queues.put(
            chat_id,
            file=AudioVideoPiped(file_path, HighQualityAudio(), HighQualityVideo()),
        )
        capt2 = (
            f"<b>❏ Video Ditambahkan Ke Antrian</b> » <code>{position}</code>\n" + capt1
        )
        await cq.edit_message_media(
            InputMediaPhoto(thumb, caption=capt2), reply_markup=pl_btn
        )
    else:
        try:
            await m._client.call_py.join_group_call(
                chat_id,
                AudioVideoPiped(file_path, HighQualityAudio(), HighQualityVideo()),
                
            )
        except Exception as e:
            if "Already joined into group call" not in str(e):
                if "No active group call" in str(e):
                    try:
                        await m._client.invoke(
                            CreateGroupCall(
                                peer=await m._client.resolve_peer(chat_id),
                                random_id=randint(0, 2147483647),
                            )
                        )
                    except Exception:
                        await m._client.send_message(
                            m.chat.id,
                            "❏ Maaf, <b>tidak</b> ada obrolan video yang aktif!\n\n• untuk menggunakan saya, <b>mulai obrolan video</b>.",
                        )
                        unPacked = unpackInlineMessage(cq.inline_message_id)
                        return await m._client.delete_messages(
                            unPacked.chat_id, unPacked.message_id
                        )
                    await m._client.call_py.join_group_call(
                        chat_id,
                        AudioVideoPiped(
                            file_path, HighQualityAudio(), HighQualityVideo()
                        ),
                        
                    )
                else:
                    await m._client.send_message(
                        m.chat.id,
                        str(e),
                    )
                    unPacked = unpackInlineMessage(cq.inline_message_id)
                    return await m._client.delete_messages(
                        unPacked.chat_id, unPacked.message_id
                    )
        await cq.edit_message_media(
            InputMediaPhoto(thumb, caption="<b>❏ Sedang Memutar Video</b>\n" + capt1),
            reply_markup=pl_btn,
        )




async def call_back_close(_, cq):
    if not cq.from_user or cq.from_user.id != int(cq.data.split()[1]):
        return await cq.answer(
            f"Jangan Di Pencet Anjeng.",
            True,
        )
    unPacked = unpackInlineMessage(cq.inline_message_id)
    for my in ubot._ubot:
        if cq.from_user.id == int(my.me.id):
            await my.delete_messages(unPacked.chat_id, unPacked.message_id)
