import os
from datetime import timedelta

import wget
from youtubesearchpython import VideosSearch

from .. import *

__MODULE__ = "YOUTUBE"
__HELP__ = f"""
Perintah:
         <code>{PREFIX[0]}song</code> [song title]
Penjelasan:
           Untuk mendownload music yang diinginkan

Perintah:
         <code>{PREFIX[0]}vsong</code> [song title]
Penjelasan:
           Untuk mendownload video yang diinginkan
"""


@PY.UBOT("vsong", PREFIX)
async def yt_video(client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "❌ <b>Video tidak ditemukan,</b>\nmohon masukan judul video dengan benar.",
        )
    infomsg = await message.reply_text("<b>🔍 Pencarian...</b>", quote=False)
    try:
        search = VideosSearch(message.text.split(None, 1)[1], limit=1).result()[
            "result"
        ][0]
        link = f"https://youtu.be/{search['id']}"
    except Exception as error:
        return await infomsg.edit(f"<b>🔍 Pencarian...\n\n❌ Error: {error}</b>")
    await infomsg.edit(f"<b>📥 Downloader...</b>")
    try:
        file_name, title, url, duration, views, channel, thumb = await YoutubeDownload(
            link, as_video=True
        )
    except Exception as error:
        return await infomsg.edit(f"<b>📥 Downloader...\n\n❌ Error: {error}</b>")
    thumbnail = wget.download(thumb)
    await client.send_video(
        message.chat.id,
        video=file_name,
        thumb=thumbnail,
        file_name=title,
        duration=duration,
        supports_streaming=True,
        caption="<b>💡 Informasi {}</b>\n\n<b>🏷 Nama:</b> {}\n<b>🧭 Durasi:</b> {}\n<b>👀 Dilihat:</b> {}\n<b>📢 Channel:</b> {}\n<b>🔗 Tautan:</b> <a href={}>Youtube</a>\n\n<b>⚡ Powered By:</b> {}".format(
            "video",
            title,
            timedelta(seconds=duration),
            views,
            channel,
            url,
            bot.me.mention,
        ),
        reply_to_message_id=message.id,
    )
    await infomsg.delete()
    for files in (thumbnail, file_name):
        if files and os.path.exists(files):
            os.remove(files)


@PY.UBOT("song", PREFIX)
async def yt_audio(client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "❌ <b>Audio tidak ditemukan,</b>\nmohon masukan judul video dengan benar.",
        )
    infomsg = await message.reply_text("<b>🔍 Pencarian...</b>", quote=False)
    try:
        search = VideosSearch(message.text.split(None, 1)[1], limit=1).result()[
            "result"
        ][0]
        link = f"https://youtu.be/{search['id']}"
    except Exception as error:
        return await infomsg.edit(f"<b>🔍 Pencarian...\n\n❌ Error: {error}</b>")
    await infomsg.edit(f"<b>📥 Downloader...</b>")
    try:
        file_name, title, url, duration, views, channel, thumb = await YoutubeDownload(
            link, as_video=False
        )
    except Exception as error:
        return await infomsg.edit(f"<b>📥 Downloader...\n\n❌ Error: {error}</b>")
    thumbnail = wget.download(thumb)
    await client.send_audio(
        message.chat.id,
        audio=file_name,
        thumb=thumbnail,
        file_name=title,
        performer=channel,
        duration=duration,
        caption="<b>💡 Informasi {}</b>\n\n<b>🏷 Nama:</b> {}\n<b>🧭 Durasi:</b> {}\n<b>👀 Dilihat:</b> {}\n<b>📢 Channel:</b> {}\n<b>🔗 Tautan:</b> <a href={}>Youtube</a>\n\n<b>⚡ Powered By:</b> {}".format(
            "Audio",
            title,
            timedelta(seconds=duration),
            views,
            channel,
            url,
            bot.me.mention,
        ),
        reply_to_message_id=message.id,
    )
    await infomsg.delete()
    for files in (thumbnail, file_name):
        if files and os.path.exists(files):
            os.remove(files)
