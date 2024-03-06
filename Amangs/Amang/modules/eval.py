import sys
import traceback
from io import BytesIO, StringIO
import asyncio
import os
import subprocess
import time
import psutil
from os import execvp
from sys import executable
from subprocess import Popen, PIPE, TimeoutExpired
from time import perf_counter

from Amang import *
from Amang.utils import *
from Amang.config import *

async def restart():
    execvp(executable, [executable, "-m", "Amang"])
  
  
@bot.on_message(filters.command("update") & filters.user(AMANG))
@ubot.on_message(anjay("update") & filters.user(AMANG) & filters.me)
async def update_restart(_, message):
    try:
        out = subprocess.check_output(["git", "pull"]).decode("UTF-8")
        if "Already up to date." in str(out):
            return await message.reply_text("Its already up-to date!")
        await message.reply_text(f"```{out}```")
    except Exception as e:
        return await message.reply_text(str(e))
    m = await message.reply_text("**Updated with default branch, restarting now.**")
    await restart()

@bot.on_message(filters.command(["sh"]) & filters.user(AMANG))
@ubot.on_message(filters.me & anjay("sh") & filters.user(AMANG))
async def shell_command(client: Client, message: Message):
    if message.from_user.id not in AMANG:
        return await message.reply_text("**Lu bukan AMANG**")
  
    if len(message.command) < 2:
        return await message.reply_text("<b>Specify the command in message text</b>")

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

    reply_message = await message.reply_text(text + "<b>Running...</b>")
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
    await reply_message.edit_text(text)
    cmd_obj.kill()


@ubot.on_message(filters.me & anjay("dump"))
async def _(client, message):
    msgs = message.reply_to_message
    if message.reply_to_message:
        try:
            if len(message.command) < 2:
                if len(str(message.reply_to_message)) > 4096:
                    with BytesIO(str.encode(str(message.reply_to_message))) as out_file:
                        out_file.name = "trash.txt"
                        return await message.reply_document(document=out_file)
                else:
                    return await message.reply(msgs)
            else:
                value = eval(f"message.reply_to_message.{message.command[1]}")
                return await message.reply(value)
        except Exception as error:
            return await message.reply(str(error))
    else:
        return await message.reply("bukan gitu caranya")



@bot.on_message(filters.command(["ev"]) & filters.user(AMANG))
@ubot.on_message(filters.user(AMANG) & filters.command("ev", "."))
async def _(client, message):
    cmd = message.text.split(" ", maxsplit=1)[1]
    if not cmd:
        return await eor(message, "`Give me commands dude...`")
    else:
        ajg = await eor(message, "`Processing ...`")
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
    await ajg.delete()
