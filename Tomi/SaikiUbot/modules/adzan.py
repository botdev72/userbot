import json

import requests

from .. import *

__MODULE__ = "ADZAN"
__HELP__ = f"""
Perintah:
         <code>{PREFIX[0]}adzan</code> [nama kota]
Penjelasan:
           Untuk mengetahui jadwal adzan di lokasi anda
"""


@PY.UBOT("adzan", PREFIX)
async def _(client, message):
    LOKASI = message.text.split(None, 1)[1]
    if len(message.command) < 2:
        return await message.reply("<b>Silahkan Masukkan Nama Kota Anda</b>")
    url = f"http://muslimsalat.com/{LOKASI}.json?key=bd099c5825cbedb9aa934e255a81a5fc"
    request = requests.get(url)
    if request.status_code != 200:
        await message.reply(f"<b>Maaf Tidak Menemukan Kota <code>{LOKASI}</code>")
    result = json.loads(request.text)
    catresult = f"""
Jadwal Shalat Hari Ini

<b>Tanggal</b> <code>{result['items'][0]['date_for']}</code>
<b>Kota</b> <code>{result['query']} | {result['country']}</code>

<b>Terbit:</b> <code>{result['items'][0]['shurooq']}</code>
<b>Subuh:</b> <code>{result['items'][0]['fajr']}</code>
<b>Zuhur:</b> <code>{result['items'][0]['dhuhr']}</code>
<b>Ashar:</b> <code>{result['items'][0]['asr']}</code>
<b>Maghrib:</b> <code>{result['items'][0]['maghrib']}</code>
<b>Isya:</b> <code>{result['items'][0]['isha']}</code>
"""
    await message.reply(catresult)
