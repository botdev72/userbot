import asyncio
import re
import urllib
import urllib.request

from search_engine_parser import GoogleSearch

from ubot import *
from ubot.utils import *

__MODULE__ = "Google"
__HELP__ = """
Bantuan Untuk Google

• Perintah: <code>{0}google</code> [query]
• Penjelasan: Untuk mencari something.
"""


opener = urllib.request.build_opener()
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
opener.addheaders = [("User-agent", useragent)]


@KY.UBOT("google")
async def gsearch(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    webevent = await message.reply(f"{emo.proses} **Searching Google...**")
    await asyncio.sleep(2)
    match = get_arg(message)
    if not match:
        await webevent.edit(f"{emo.gagal} **Give me some to search...**")
        return
    page = re.findall(r"page=\d+", match)
    try:
        page = page[0]
        page = page.replace("page=", "")
        match = match.replace("page=" + page[0], "")
    except IndexError:
        page = 1
    search_args = (str(match), int(page))
    gsearch = GoogleSearch()
    gresults = await gsearch.async_search(*search_args)
    msg = ""
    for i in range(len(gresults["links"])):
        try:
            title = gresults["titles"][i]
            link = gresults["links"][i]
            desc = gresults["descriptions"][i]
            msg += f"- [{title}]({link})\n**{desc}**\n\n"
        except IndexError:
            break
    await webevent.edit(
        f"{emo.proses} **Search Query:**\n`" + match + "`\n\n**Results:**\n" + msg
    )
