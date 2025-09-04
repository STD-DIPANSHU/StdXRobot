# StdXRobot/plugins/tools/biocheck.py

import re
from pyrogram import filters
from pyrogram.types import ChatPermissions
from StdXRobot import app  # ✅ correct import

# Bio check on/off toggle per chat
BIO_CHECK_ENABLED = {}

# Warning counter per chat per user
WARNINGS = {}

# URL regex
URL_PATTERN = re.compile(r"https?://\S+|t\.me/\S+|@[\w\d_]+")


# ---------- Utility: Admin Check ----------
async def is_admin(chat_id: int, user_id: int) -> bool:
    try:
        member = await app.get_chat_member(chat_id, user_id)
        print(f"[DEBUG] User {user_id} status = {member.status}")  # Debug log
        return member.status in ["administrator", "creator"]
    except Exception as e:
        print(f"[ERROR] Admin check failed: {e}")
        return False


# ---------- Command: Toggle bio check ----------
@app.on_message(filters.command("biocheck", prefixes=["/", "!", "."]) & filters.group)
async def toggle_biocheck(_, message):
    if not message.from_user:
        return

    chat_id = message.chat.id
    user_id = message.from_user.id

    # Admin check
    if not await is_admin(chat_id, user_id):
        return await message.reply("❌ Only admins can toggle bio check.")

    # Toggle ON/OFF
    status = BIO_CHECK_ENABLED.get(chat_id, False)
    BIO_CHECK_ENABLED[chat_id] = not status

    await message.reply(
        f"✅ Bio link check is now {'ENABLED 🟢' if not status else 'DISABLED 🔴'} in this group."
    )


# ---------- Listener: Monitor messages ----------
@app.on_message(filters.group & ~filters.service)
async def check_user_bio(_, message):
    if not message.from_user:
        return

    chat_id = message.chat.id
    user_id = message.from_user.id

    # Agar group me bio check off hai → skip
    if not BIO_CHECK_ENABLED.get(chat_id, False):
        return

    # Admin skip
    if await is_admin(chat_id, user_id):
        return

    try:
        user = await app.get_chat(user_id)
        bio = user.bio or ""
    except Exception as e:
        print(f"[ERROR] Cannot fetch bio for {user_id}: {e}")
        return

    if URL_PATTERN.search(bio):
        # Warn user
        WARNINGS.setdefault(chat_id, {})
        WARNINGS[chat_id][user_id] = WARNINGS[chat_id].get(user_id, 0) + 1
        count = WARNINGS[chat_id][user_id]

        if count < 3:
            await message.reply(
                f"⚠️ {message.from_user.mention}, link detected in your bio!\n"
                f"Warning {count}/3 — remove link or you will be muted."
            )
        else:
            try:
                await app.restrict_chat_member(chat_id, user_id, ChatPermissions())
                await message.reply(
                    f"🔇 {message.from_user.mention} has been muted for having links in bio."
                )
                WARNINGS[chat_id][user_id] = 0  # reset warnings after mute
            except Exception as e:
                await message.reply(f"❌ Failed to mute user: {e}")
