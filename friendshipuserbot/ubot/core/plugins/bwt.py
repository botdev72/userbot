async def buat_apaam(client, message):
    if len(message.command) < 3:
        return await message.reply(
            f"Silakan ketik {message.command} untuk melihat bantuan dari modul ini."
        )
    group_type = message.command[1]
    split = message.command[2:]
    group_name = " ".join(split)
    xd = await message.reply("<code>Processing...</code>")
    desc = "Welcome To My " + ("Group" if group_type == "gc" else "Channel")
    if group_type == "gc":  # for supergroup
        _id = await client.create_supergroup(group_name, desc)
        link = await client.get_chat(_id.id)
        await xd.edit(
            f"<b>Berhasil membuat Telegram Grup : [{group_name}]({link.invite_link})</b>",
            disable_web_page_preview=True,
        )
    elif group_type == "ch":  # for channel
        _id = await client.create_channel(group_name, desc)
        link = await client.get_chat(_id.id)
        await xd.edit(
            f"<b>Berhasil membuat Telegram Channel : [{group_name}]({link.invite_link})</b>",
            disable_web_page_preview=True,
        )
