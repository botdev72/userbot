from asyncio import sleep

from ubot import *
from ubot.utils import *

__MODULE__ = "Zombies"
__HELP__ = """
Bantuan Untuk Zombies

• Perintah: <code>{0}zombie</code>
• Penjelasan: Untuk mengeluarkan akun depresi digrup anda.
"""


@KY.UBOT("zombie", sudo=True)
async def _(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    chat_id = message.chat.id
    deleted_users = []
    banned_users = 0
    m = await eor(
        message,
        f"{emo.proses} <b>Sedang mencari akun-akun depresi ditinggal kawin...</b>",
    )
    await sleep(2)

    async for i in client.get_chat_members(chat_id):
        if i.user.is_deleted:
            deleted_users.append(i.user.id)
    if len(deleted_users) > 0:
        for deleted_user in deleted_users:
            try:
                await message.chat.ban_member(deleted_user)
            except Exception:
                pass
            banned_users += 1
        await m.edit(
            f"{emo.sukses} <b>Berhasil mengkawinkan {banned_users} Akun Depresi Ditinggal Kawin.</b>"
        )
    else:
        await m.edit(
            f"{emo.gagal} <b>Saya tidak menemukan akun depresi di tinggal kawin.</b>"
        )
