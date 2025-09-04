import os
import aiohttp
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from StdXRobot import app

# ENV vars
SIGHT_USER = os.getenv("624344670")
SIGHT_SECRET = os.getenv("h76kxr8c4PgRYBnmCq7WG29tWCoKMHqW")

# in-memory db
nsfw_db = {}
nsfw_mode = {}

POLICE = [
    [
        InlineKeyboardButton(
            text="• ᴀᴅᴅ ᴍᴇ •",
            url=f"https://t.me/{app.username}?startgroup=true",
        ),
    ],
]

# ---- API CALL ---- #
async def check_nsfw(file_path: str) -> bool:
    """
    Uploads media to Sightengine API and returns True if NSFW detected.
    """
    url = "https://api.sightengine.com/1.0/check.json"
    data = {
        "models": "nudity,wad,offensive",
        "api_user": SIGHT_USER,
        "api_secret": SIGHT_SECRET,
    }

    async with aiohttp.ClientSession() as session:
        with open(file_path, "rb") as f:
            form = aiohttp.FormData()
            form.add_field("media", f, filename=os.path.basename(file_path))
            for k, v in data.items():
                form.add_field(k, v)

            async with session.post(url, data=form) as resp:
                result = await resp.json()

    try:
        nudity = result.get("nudity", {})
        if nudity.get("sexual_activity", 0) > 0.7 or nudity.get("sexual_display", 0) > 0.7:
            return True
        if result.get("offensive", {}).get("prob", 0) > 0.8:
            return True
    except Exception as e:
        print("NSFW check error:", e)

    return False


# ---- commands ---- #
@app.on_message(filters.command("nsfwcheck") & ~filters.private)
async def nsfw_switch(_, message):
    chat_id = message.chat.id
    if len(message.command) < 2:
        return await message.reply_text("⚠️ Usage: **/nsfwcheck [on|off]**")

    status = message.text.split(None, 1)[1].lower()
    if status == "on":
        nsfw_db[chat_id] = True
        await message.reply_text("✅ **NSFW check enabled in this chat.**")
    elif status == "off":
        nsfw_db[chat_id] = False
        await message.reply_text("🚫 **NSFW check disabled in this chat.**")
    else:
        await message.reply_text("⚠️ Usage: **/nsfwcheck [on|off]**")


@app.on_message(filters.command("nsfwmode") & ~filters.private)
async def nsfw_mode_set(_, message):
    chat_id = message.chat.id
    if len(message.command) < 2:
        return await message.reply_text("⚠️ Usage: **/nsfwmode [ban|mute]**")

    mode = message.text.split(None, 1)[1].lower()
    if mode in ["ban", "mute"]:
        nsfw_mode[chat_id] = mode
        await message.reply_text(f"⚙️ **NSFW punishment mode set to:** {mode.upper()}")
    else:
        await message.reply_text("⚠️ Usage: **/nsfwmode [ban|mute]**")


# ---- detector ---- #
@app.on_message(filters.group & (filters.photo | filters.video | filters.animation))
async def nsfw_detector(_, message):
    chat_id = message.chat.id
    user = message.from_user

    if not nsfw_db.get(chat_id):
        return

    # download media
    try:
        file_path = await app.download_media(message, file_name="nsfw_temp")
    except Exception as e:
        print("Download error:", e)
        return

    # api check
    is_nsfw = await check_nsfw(file_path)

    # cleanup temp file
    try:
        os.remove(file_path)
    except:
        pass

    if is_nsfw:
        try:
            await message.delete()
        except:
            pass

        punishment = nsfw_mode.get(chat_id, "mute")
        caption = f"""
🚫 NSFW Media Detected 🥵⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣⁣

 • Sᴇɴᴛ Bʏ » {user.mention if user else "Unknown"}
 • Uꜱᴇʀ ɪᴅ » `{user.id if user else 0}`

✅ 𝙸'ᴠᴇ ᴅᴇʟᴇᴛᴇᴅ ᴛʜᴀᴛ ᴍᴇᴅɪᴀ.
👉 ɢɪᴠᴇ ᴍᴇ 'ʙᴀɴ ᴩᴏᴡᴇʀ' ᴛᴏ {punishment.upper()} ᴜꜱᴇʀ.
"""
        await app.send_message(
            chat_id,
            caption,
            reply_markup=InlineKeyboardMarkup(POLICE),
            reply_to_message_id=message.id if message else None
        )

        # apply punishment
        try:
            if punishment == "mute":
                await app.restrict_chat_member(
                    chat_id,
                    user.id,
                    enums.ChatPermissions(),
                )
            elif punishment == "ban":
                await app.ban_chat_member(chat_id, user.id)
        except Exception as e:
            print("Punishment failed:", e)


__mod__ = "ɴsғᴡ"
__help__ = """
**✦ /nsfwcheck [on|off]** - Enable or disable NSFW media check in group  
**✦ /nsfwmode [ban|mute]** - Set punishment for NSFW users  
"""
