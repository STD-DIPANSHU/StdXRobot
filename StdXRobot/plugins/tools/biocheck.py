from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
from StdXRobot import app

# Dictionaries to store toggle status and warnings
bio_check_enabled = {}  # group_id: True/False
warning_counts = {}     # group_id: {user_id: count}

# Helper: Check if user is admin
async def is_admin(chat_id: int, user_id: int) -> bool:
    member = await app.get_chat_member(chat_id, user_id)
    return member.status in ("administrator", "owner")

# Command: /biocheck toggle
@app.on_message(filters.command("biocheck") & filters.group)
async def toggle_biocheck(_, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not await is_admin(chat_id, user_id):
        return await message.reply("❌ Only admins can toggle bio check.")

    # Toggle feature
    current = bio_check_enabled.get(chat_id, False)
    bio_check_enabled[chat_id] = not current
    status = "✅ Bio check enabled." if not current else "⚠️ Bio check disabled."
    await message.reply(status)

# Monitor messages when feature is ON
@app.on_message(filters.group)
async def monitor_bio(_, message: Message):
    chat_id = message.chat.id
    user = message.from_user

    if not user or not bio_check_enabled.get(chat_id, False):
        return

    # Get bio from chat member
    try:
        member = await app.get_chat_member(chat_id, user.id)
        bio = member.user.bio or ""
    except Exception:
        return  # skip if unable to fetch bio

    if "http://" in bio or "https://" in bio:
        # Initialize warning count
        if chat_id not in warning_counts:
            warning_counts[chat_id] = {}
        if user.id not in warning_counts[chat_id]:
            warning_counts[chat_id][user.id] = 0

        warning_counts[chat_id][user.id] += 1
        count = warning_counts[chat_id][user.id]

        if count >= 3:
            try:
                await app.restrict_chat_member(
                    chat_id,
                    user.id,
                    ChatPermissions(can_send_messages=False)
                )
                await message.reply(
                    f"🚫 {user.mention} muted for having link in bio (3 warnings reached)."
                )
            except Exception:
                pass  # mute failed
        else:
            await message.reply(
                f"⚠️ {user.mention}, link detected in your bio. Warning {count}/3."
            )
