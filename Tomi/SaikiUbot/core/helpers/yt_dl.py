import asyncio

from pyrogram.raw.functions.messages import DeleteHistory

from SaikiUbot import ubot
from SaikiUbot.utils.unpack import unpackInlineMessage


class YT:
    async def DOWNLOAD(callback_query, message, audio_or_video):
        try:
            text = f"{message.text.split(None, 1)[1]}"
            await callback_query.edit_message_text("<b>Tunggu Sebentar...</b>")
            if audio_or_video == "Ad":
                try:
                    x = await message._client.get_inline_bot_results("lybot", text)
                    saved = await message._client.send_inline_bot_result(
                        message._client.me.id, x.query_id, x.results[0].id
                    )
                except:
                    return await callback_query.edit_message_text(
                        "<b>❌ Music tidak ditemukan</b>"
                    )
                saved = await message._client.get_messages(
                    message._client.me.id, int(saved.updates[1].message.id)
                )
                await message._client.send_audio(
                    message.chat.id, saved.audio.file_id, reply_to_message_id=message.id
                )
                try:
                    unPacked = unpackInlineMessage(callback_query.inline_message_id)
                    for my in ubot._ubot:
                        if callback_query.from_user.id == int(my.me.id):
                            await my.delete_messages(
                                unPacked.chat_id,
                                unPacked.message_id,
                            )
                except:
                    await callback_query.edit_message_text(
                        "<b>Music Berhasil Didownload</b>"
                    )
                return await saved.delete()
            else:
                await message._client.unblock_user("@youtubednbot")
                try:
                    x = await message._client.get_inline_bot_results("vid", text)
                    await message._client.send_inline_bot_result(
                        "@youtubednbot", x.query_id, x.results[0].id
                    )
                except:
                    return await callback_query.edit_message_text(
                        "<b>❌ Video tidak ditemukan</b>"
                    )
                await asyncio.sleep(15)
                async for vsong in message._client.search_messages("@youtubednbot"):
                    if vsong.video:
                        await message._client.send_video(
                            message.chat.id,
                            vsong.video.file_id,
                            reply_to_message_id=message.id,
                        )
                        try:
                            unPacked = unpackInlineMessage(
                                callback_query.inline_message_id
                            )
                            for my in ubot._ubot:
                                if callback_query.from_user.id == int(my.me.id):
                                    await my.delete_messages(
                                        unPacked.chat_id,
                                        unPacked.message_id,
                                    )
                        except:
                            await callback_query.edit_message_text(
                                "<b>Video Berhasil Didownload</b>"
                            )
                user_info = await message._client.resolve_peer("@youtubednbot")
                return await message._client.invoke(
                    DeleteHistory(peer=user_info, max_id=0, revoke=True)
                )
        except Exception:
            return await callback_query.edit_message_text(
                "<b>❌ Terjadi kesalahan yang tidak diketahui</b>"
            )
