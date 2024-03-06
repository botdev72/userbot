import asyncio
import os
from time import time

import wget
from youtubesearchpython import VideosSearch

from ubot import *
from ubot.utils import *


@KY.UBOT("video")
async def vsong_cmd(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    infomsg = await message.reply(f"{emo.proses} **Processing...**")
    await asyncio.sleep(2)
    if len(message.command) < 2:
        return await infomsg.edit(
            f"{emo.gagal} **Silahkan masukkan judul video.**",
        )
    try:
        search = VideosSearch(message.text.split(None, 1)[1], limit=1).result()[
            "result"
        ][0]
        link = f"https://youtu.be/{search['id']}"
    except Exception as error:
        return await infomsg.edit(f"{emo.gagal} <b>Error...\n\n{error}</b>")
    try:
        (
            file_name,
            title,
            url,
            duration,
            views,
            channel,
            thumb,
            data_ytp,
        ) = await YoutubeDownload(link, as_video=True)
    except Exception as error:
        return await infomsg.edit(f"{emo.gagal} <b>Downloading...\n\n{error}</b>")
    thumbnail = wget.download(thumb)
    await client.send_video(
        message.chat.id,
        video=file_name,
        thumb=thumbnail,
        file_name=title,
        duration=duration,
        supports_streaming=True,
        caption=f"{emo.sukses} <b>Upload By:</b> {client.me.mention}",
        progress=progress,
        progress_args=(
            infomsg,
            time(),
            f"{emo.proses} <b>Downloading...</b>",
            f"{search['id']}.mp4",
        ),
        reply_to_message_id=message.id,
    )
    await infomsg.delete()
    for files in (thumbnail, file_name):
        if files and os.path.exists(files):
            os.remove(files)


@KY.UBOT("song")
async def song_cmd(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    infomsg = await message.reply(f"{emo.proses} **Processing...**")
    await asyncio.sleep(2)
    if len(message.command) < 2:
        return await infomsg.edit(
            f"{emo.gagal} **Silahkan masukkan judul lagu.**",
        )
    try:
        search = VideosSearch(message.text.split(None, 1)[1], limit=1).result()[
            "result"
        ][0]
        link = f"https://youtu.be/{search['id']}"
    except Exception as error:
        return await infomsg.edit(f"{emo.gagal} <b>Error...\n\n{error}</b>")
    try:
        (
            file_name,
            title,
            url,
            duration,
            views,
            channel,
            thumb,
            data_ytp,
        ) = await YoutubeDownload(link, as_video=False)
    except Exception as error:
        return await infomsg.edit(f"{emo.gagal} <b>Downloading...\n\n{error}</b>")
    thumbnail = wget.download(thumb)
    await client.send_audio(
        message.chat.id,
        audio=file_name,
        thumb=thumbnail,
        file_name=title,
        performer=channel,
        duration=duration,
        caption=f"{emo.sukses} <b>Upload By:</b> {client.me.mention}",
        progress=progress,
        progress_args=(
            infomsg,
            time(),
            f"{emo.proses} <b>Downloading...</b>",
            f"{search['id']}.mp3",
        ),
        reply_to_message_id=message.id,
    )
    await infomsg.delete()
    for files in (thumbnail, file_name):
        if files and os.path.exists(files):
            os.remove(files)
