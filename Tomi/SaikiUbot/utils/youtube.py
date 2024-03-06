from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL

from SaikiUbot.utils import run_sync


def YouTubeSearch(query):
    search = VideosSearch(query, limit=1).result()
    data = search["result"][0]
    videoid = data["id"]
    title = data["title"]
    duration = data["duration"]
    url = f"https://youtu.be/{videoid}"
    views = data["viewCount"]["text"]
    channel = data["channel"]["name"]
    thumbnail = data["thumbnails"][0]["url"].split("?")[0]
    return [videoid, title, duration, url, views, channel, thumbnail]


async def YoutubeDownload(url, as_video=False):
    if as_video:
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
    else:
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
    ytdl_data = await run_sync(ydl.extract_info, url, download=True)
    file_name = ydl.prepare_filename(ytdl_data)
    videoid = ytdl_data["id"]
    title = ytdl_data["title"]
    url = f"https://youtu.be/{videoid}"
    duration = ytdl_data["duration"]
    channel = ytdl_data["uploader"]
    views = f"{ytdl_data['view_count']:,}".replace(",", ".")
    thumb = f"https://img.youtube.com/vi/{videoid}/hqdefault.jpg"
    return file_name, title, url, duration, views, channel, thumb
