import asyncio
import os
import shlex
import textwrap

from PIL import Image, ImageDraw, ImageFont
from pymediainfo import MediaInfo


class Media_Info:
    def data(media):
        found = False
        media_info = MediaInfo.parse(media)
        for track in media_info.tracks:
            if track.track_type == "Video":
                found = True
                type_ = track.track_type
                format_ = track.format
                duration_1 = track.duration
                other_duration_ = track.other_duration
                duration_2 = (
                    f"{other_duration_[0]} - ({other_duration_[3]})"
                    if other_duration_
                    else None
                )
                pixel_ratio_ = [track.width, track.height]
                aspect_ratio_1 = track.display_aspect_ratio
                other_aspect_ratio_ = track.other_display_aspect_ratio
                aspect_ratio_2 = other_aspect_ratio_[0] if other_aspect_ratio_ else None
                fps_ = track.frame_rate
                fc_ = track.frame_count
                media_size_1 = track.stream_size
                other_media_size_ = track.other_stream_size
                media_size_2 = (
                    [
                        other_media_size_[1],
                        other_media_size_[2],
                        other_media_size_[3],
                        other_media_size_[4],
                    ]
                    if other_media_size_
                    else None
                )

        dict_ = (
            {
                "media_type": type_,
                "format": format_,
                "duration_in_ms": duration_1,
                "duration": duration_2,
                "pixel_sizes": pixel_ratio_,
                "aspect_ratio_in_fraction": aspect_ratio_1,
                "aspect_ratio": aspect_ratio_2,
                "frame_rate": fps_,
                "frame_count": fc_,
                "file_size_in_bytes": media_size_1,
                "file_size": media_size_2,
            }
            if found
            else None
        )
        return dict_


def get_arg(message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])


async def resize_media(media, video, fast_forward):
    if video:
        info_ = Media_Info.data(media)
        width = info_["pixel_sizes"][0]
        height = info_["pixel_sizes"][1]
        sec = info_["duration_in_ms"]
        s = round(float(sec)) / 1000

        if height == width:
            height, width = 512, 512
        elif height > width:
            height, width = 512, -1
        elif width > height:
            height, width = -1, 512

        resized_video = f"{media}.webm"
        if fast_forward:
            if s > 3:
                fract_ = 3 / s
                ff_f = round(fract_, 2)
                set_pts_ = ff_f - 0.01 if ff_f > fract_ else ff_f
                cmd_f = f"-filter:v 'setpts={set_pts_}*PTS',scale={width}:{height}"
            else:
                cmd_f = f"-filter:v scale={width}:{height}"
        else:
            cmd_f = f"-filter:v scale={width}:{height}"
        fps_ = float(info_["frame_rate"])
        fps_cmd = "-r 30 " if fps_ > 30 else ""
        cmd = f"ffmpeg -i {media} {cmd_f} -ss 00:00:00 -to 00:00:03 -an -c:v libvpx-vp9 {fps_cmd}-fs 256K {resized_video}"
        _, error, __, ___ = await run_cmd(cmd)
        os.remove(media)
        return resized_video

    image = Image.open(media)
    maxsize = 512
    scale = maxsize / max(image.width, image.height)
    new_size = (int(image.width * scale), int(image.height * scale))

    image = image.resize(new_size, Image.LANCZOS)
    resized_photo = "sticker.png"
    image.save(resized_photo)
    os.remove(media)
    return resized_photo


async def add_text_img(image_path, text):
    font_size = 12
    stroke_width = 1

    if ";" in text:
        upper_text, lower_text = text.split(";")
    else:
        upper_text = text
        lower_text = ""

    img = Image.open(image_path).convert("RGBA")
    img_info = img.info
    image_width, image_height = img.size
    font = ImageFont.truetype(
        font="userbot/resource/default.ttf",
        size=int(image_height * font_size) // 100,
    )
    draw = ImageDraw.Draw(img)

    char_width, char_height = font.getsize("A")
    chars_per_line = image_width // char_width
    top_lines = textwrap.wrap(upper_text, width=chars_per_line)
    bottom_lines = textwrap.wrap(lower_text, width=chars_per_line)

    if top_lines:
        y = 10
        for line in top_lines:
            line_width, line_height = font.getsize(line)
            x = (image_width - line_width) / 2
            draw.text(
                (x, y),
                line,
                fill="white",
                font=font,
                stroke_width=stroke_width,
                stroke_fill="black",
            )
            y += line_height

    if bottom_lines:
        y = image_height - char_height * len(bottom_lines) - 15
        for line in bottom_lines:
            line_width, line_height = font.getsize(line)
            x = (image_width - line_width) / 2
            draw.text(
                (x, y),
                line,
                fill="white",
                font=font,
                stroke_width=stroke_width,
                stroke_fill="black",
            )
            y += line_height

    final_image = os.path.join("memify.webp")
    img.save(final_image, **img_info)
    return final_image


async def aexec(code, user, message):
    exec(
        "async def __aexec(user, message): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](user, message)


async def bash(cmd):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    err = stderr.decode().strip()
    out = stdout.decode().strip()
    return out, err


async def run_cmd(cmd):
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )
