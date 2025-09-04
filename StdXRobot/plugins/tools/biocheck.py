# StdXRobot/plugins/tools/biocheck.py

import re
from pyrogram import filters
from pyrogram.types import ChatPermissions
from StdXRobot import app

# Regex to detect links in bio
URL_PATTERN = re.compile(r"(https?://|t\.me/|www\.)", re.IGNORECASE)

# In-memory DB
user_warnings = {}   # {(chat_id, user_id): count}
biocheck_enabled = {}  # {chat_id: True/False}

MAX_WARNINGS = 2


# -----------------------------
# Command: /biocheck on | off
# -----------------------------
@app.on_message(filters.command("biocheck", prefixes=["/", "!", "."]) & filters.group)
async def toggle_biocheck(_, message):
    chat_id = message.chat.id
    user = message.from_user

    # only admins allowed
    try:
        member = await app.get_chat_member(chat_id, user.id)
        if member.status not in ("administrator", "owner"):
            return await message.reply_text("❌ Only admins can toggle bio check.")
    except Exception:
        return

    if len(message.command) < 2:
        status = "enabled ✅" if biocheck_enabled.get(chat_id, True) else "disabled ❌"
        return await message.reply_text(f"🔎 BioCheck is currently **{status}**")

    arg = message.command[1].lower()
    if arg == "on":
        biocheck_enabled[chat_id] = True
        await message.reply_text("✅ BioCheck enabled in this group.")
    elif arg == "off":
        biocheck_enabled[chat_id] = False
        await message.reply_text("❌ BioCheck disabled in this group.")
    else:
        await message.reply_text("Usage: `/biocheck on` or `/biocheck off`")


# -----------------------------
# Auto bio checker
# -----------------------------
@app.on_message(filters.group & ~filters.service)
async def bio_check_handler(_, message):
    chat_id = message.chat.id
    user = message.from_user

    if not user:  # Ignore system / anonymous
        return

    # check if disabled
    if not biocheck_enabled.get(chat_id, True):
        return

    # ignore admins
    try:
        member = await app.get_chat_member(chat_id, user.id)
        if member.status in ("administrator", "creator"):
            return
    except Exception:
        return

    # fetch bio
    try:
        user_info = await app.get_users(user.id)
        bio = user_info.bio or ""
    except Exception:
        bio = ""

    # detect link
    if URL_PATTERN.search(bio):
        warn_key = (chat_id, user.id)
        warn_count = user_warnings.get(warn_key, 0) + 1
        user_warnings[warn_key] = warn_count

        if warn_count < MAX_WARNINGS:
            await message.reply_text(
                f"🚨 **Warning {warn_count}/{MAX_WARNINGS}**\n\n"
                f"👤 {user.mention} (`{user.id}`)\n"
                "❌ Reason: Link detected in bio\n\n"
                "⚠️ Remove links from your bio, or you will be muted!"
            )
        else:
            try:
                await app.restrict_chat_member(
                    chat_id,
                    user.id,
                    ChatPermissions(can_send_messages=False)
                )
                await message.reply_text(
                    f"🔇 {user.mention} has been muted for having a link in their bio."
                )
                # reset warn counter
                user_warnings.pop(warn_key, None)
            except Exception as e:
                await message.reply_text(f"❌ Could not mute {user.mention}: `{e}`")
