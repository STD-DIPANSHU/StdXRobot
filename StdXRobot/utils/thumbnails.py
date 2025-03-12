#
# Copyright (C) 2024 by THE-VIP-BOY-OP@Github, < https://github.com/THE-VIP-BOY-OP >.
#
# This file is part of < https://github.com/THE-VIP-BOY-OP/VIP-MUSIC > project,
# and is released under the MIT License .
# Please see < https://github.com/THE-VIP-BOY-OP/VIP-MUSIC/blob/master/LICENSE >
#
# All rights reserved.
#

from youtubesearchpython.__future__ import VideosSearch
import os
import re
import textwrap
import aiofiles
import aiohttp
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from config import YOUTUBE_IMG_URL

def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


def add_corners(im):
    bigsize = (im.size[0] * 3, im.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    ImageDraw.Draw(mask).ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(im.size, Image.LANCZOS)
    mask = ImageChops.darker(mask, im.split()[-1])
    im.putalpha(mask)


def circle(img):
    h, w = img.size
    a = Image.new('L', [h, w], 0)
    b = ImageDraw.Draw(a)
    b.pieslice([(0, 0), (h, w)], 0, 360, fill=255, outline="white")
    c = np.array(img)
    d = np.array(a)
    e = np.dstack((c, d))
    return Image.fromarray(e)


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
                duration = "Unknown"
            try:
                views = result["viewCount"]["short"]
            except:
                views = "Unknown"  
            try:
                channel = result["channel"]["name"]
            except:
                channel = "Unknown"  
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f"cache/thumb{videoid}.png", mode="wb")
                    await f.write(await resp.read())
                    await f.close()

        

        youtube = Image.open(f"StdXRobot/assets/20241227_105436.png")
        zyoutube = Image.open(f"cache/thumb{videoid}.png")
        bg = Image.open(f"StdXRobot/assets/20241226_150720.png")
        image1 = youtube.resize((1280, 720))
        image2 = image1.convert("RGBA")
        #background = image2.filter(filter=ImageFilter.BoxBlur(30))
        enhancer = ImageEnhance.Brightness(image2)
        background = enhancer.enhance(1.1)
        y = circle(zyoutube).resize((405, 405))
        enhancer = ImageEnhance.Brightness(y)
        y = enhancer.enhance(1.1)
        background.paste(y, (96, 144), mask=y)  
        image3 = bg.resize((1280, 720))
        image5 = image3.convert("RGBA")
        result_img = Image.alpha_composite(background, image5)
        
        draw = ImageDraw.Draw(result_img)
        font = ImageFont.truetype("assets/font2.ttf", 47)
        font2 = ImageFont.truetype("assets/font2.ttf", 48)
        font3 = ImageFont.truetype("assets/font2.ttf", 30)
        font4 = ImageFont.truetype("assets/font2.ttf", 30)
        para = textwrap.wrap(title, width=33)
        try:
            if para[0]:
                draw.text(
                    (10, 10),
                    f"Powered By :- Izzyyir",
                    fill="white",
                    stroke_width=1,
                    stroke_fill="orange",
                    font=font4,
                ),
                draw.text(
                    (570, 210),
                    f"Title: {para[0]}",
                    fill="white",
                    stroke_width=1,
                    stroke_fill="black",
                    font=font,
                ),
                draw.text(
                    (570, 300),
                    f"Views: {views} ",
                    fill="white",
                    stroke_width=1,
                    stroke_fill="black",
                     font=font,
                ),
                draw.text(
                   (570, 390),
                   f"Channel: {channel}",
                   fill="white",
                   stroke_width=1,
                   stroke_fill="black",
                   font=font,
                )
                draw.text(
                   (530, 520),
                   f"00:00",
                   fill="white",
                   stroke_width=1,
                   stroke_fill="black",
                   font=font3,
                )
            else:
                draw.text(
                    (10, 10),
                    f"Powered By :- Taitan",
                    fill="white",
                    stroke_width=1,
                    stroke_fill="black",
                    font=font4,
                ),
                draw.text(
                    (570, 210),
                    f"Title: {para[0]}",
                    fill="white",
                    stroke_width=1,
                    stroke_fill="black",
                    font=font,
                ),
                draw.text(
                    (1900, 250),
                    f"{para[1]}",
                    fill="white",
                    stroke_width=1,
                    stroke_fill="black",
                    font=font,
                ),
                draw.text(
                    (570, 300),
                    f"Views: {views} ",
                    fill="white",
                    stroke_width=1,
                    stroke_fill="black",
                     font=font,
                ),
                draw.text(
                   (570, 390),
                   f"Channel: {channel}",
                   fill="white",
                   stroke_width=1,
                   stroke_fill="black",
                   font=font,
                )
                draw.text(
                   (530, 520),
                   f"00:00",
                   fill="white",
                   stroke_width=1,
                   stroke_fill="black",
                   font=font3,
                )
        except:
            pass
        text_w, text_h = draw.textsize(f"{duration}", font=font3)
        draw.text(
            ((2350 - text_w) / 2, 515),
            f"{duration}",
            fill="white",
            stroke_width=1,
            stroke_fill="black",
            font=font3,
           )
       
        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass
            
        result_img.save(f"cache/{videoid}.png")
        return f"cache/{videoid}.png"

    except Exception as e:
        print(e)
        return YOUTUBE_IMG_URL
    


async def gen_qthumb(vidid):
    try:
        query = f"https://www.youtube.com/watch?v={vidid}"
        results = VideosSearch(query, limit=1)
        for result in (await results.next())["result"]:
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        return thumbnail
    except Exception as e:
        return YOUTUBE_IMG_URL


from youtubesearchpython.__future__ import VideosSearch


async def get_thumb(videoid):
    try:
        # Search for the video using video ID
        query = f"https://www.youtube.com/watch?v={videoid}"
        results = VideosSearch(query, limit=1)
        for result in (await results.next())["result"]:
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        return thumbnail
    except Exception as e:
        return config.YOUTUBE_IMG_URL


async def get_thumb(vidid):
    try:
        # Search for the video using video ID
        query = f"https://www.youtube.com/watch?v={vidid}"
        results = VideosSearch(query, limit=1)
        for result in (await results.next())["result"]:
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        return thumbnail
    except Exception as e:
        return config.YOUTUBE_IMG_URL
        
