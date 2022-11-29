#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

import os
import re
import textwrap

import aiofiles
import aiohttp
from PIL import (Image, ImageDraw, ImageEnhance, ImageFilter,
                 ImageFont, ImageOps)
from youtubesearchpython.__future__ import VideosSearch

from config import MUSIC_BOT_NAME, YOUTUBE_IMG_URL


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newHeight, newWidth))
    return newImage


async def gen_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}.png"):
        return f"cache/{videoid}.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
            except:
                title = "Unsupported Title"
            try:
                duration = result["duration"]
            except:
                duration = "Unknown Mins"
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            try:
                views = result["viewCount"]["short"]
            except:
                views = "Unknown Views"
            try:
                channel = result["channel"]["name"]
            except:
                channel = "Unknown Channel"

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(
                        f"cache/thumb{videoid}.png", mode="wb"
                    )
                    await f.write(await resp.read())
                    await f.close()

        youtube = Image.open(f"cache/thumb{videoid}.png")
        image1 = changeImageSize(1280, 720, youtube)
        image2 = image1.convert("RGBA")
        background = image2.filter(filter=ImageFilter.BoxBlur(35))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.8)
        Xcenter = youtube.width / 2
        Ycenter = youtube.height / 2
        x1 = Xcenter - 400
        y1 = Ycenter - 400
        x2 = Xcenter + 400
        y2 = Ycenter + 400
        logo = youtube.crop((x1, y1, x2, y2))
        logo.thumbnail((300, 300), Image.ANTIALIAS)
        logo = ImageOps.expand(logo, border=10, fill="midnightblue")
        background.paste(logo, (300, 150))
        draw = ImageDraw.Draw(background)
        draw.polygon(((200, 200), (300, 100), (250, 50)), fill=(255, 255, 0), outline=(0, 0, 0))
        font = ImageFont.truetype("assets/font2.ttf", 40)
        font2 = ImageFont.truetype("assets/font2.ttf", 70)
        font3 = ImageFont.truetype("assets/font.ttf", 40)
        jokerman = ImageFont.truetype("assets/font2.ttf", 30)
        name_font = ImageFont.truetype("assets/font.ttf", 35)
        para = textwrap.wrap(title, width=32)
        j = 0
        draw.text(
            (10, 10), f"{MUSIC_BOT_NAME}", fill="white", font=font
        )
        draw.text(
            (800, 520),
            "Enjoy the song!",
            fill="white",
            stroke_width=2,
            stroke_fill="black",
            font=font2,
        ) 
        draw.text(
            (50, 500),
            "PLAYING NOW!",
            fill="white",
            stroke_width=2,
            stroke_fill="black",
            font=font2,
        )
        for line in para:
            if j == 1:
                j += 1
                draw.text(
                    (50, 690),
                    f"{line}",
                    fill="white",
                    stroke_width=1,
                    stroke_fill="black",
                    font=font3,
                )
            if j == 0:
                j += 1
                draw.text(
                    (50, 630),
                    f"{line}",
                    fill="white",
                    stroke_width=1,
                    stroke_fill="black",
                    font=font3,
                )

        draw.text(
            (100, 800),
            f"Views : {views[:23]}",
            (255, 255, 255),
            font=jokerman,
            stroke_width=1,
            stroke_fill="black",
        )
        draw.text(
            (100, 850),
            f"Duration : {duration[:23]} Mins",
            (255, 255, 255),
            font=jokerman,
            stroke_width=1,
            stroke_fill="black",
        )
        draw.text(
            (100, 900),
            f"Channel : {channel}",
            (255, 255, 255),
            font=jokerman,
            stroke_width=1,
            stroke_fill="black",
        )
        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass
        background.save(f"cache/{videoid}.png")
        return f"cache/{videoid}.png"
    except Exception:
        return YOUTUBE_IMG_URL
