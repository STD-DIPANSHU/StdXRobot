from pyrogram import filters
from pyrogram.types import ChatPermissions
from StdXRobot import app  # ✅ tere bot ka main client

# in-memory storage
BIO_CHECK_ENABLED = {}
USER_WARNINGS = {}

# 🔹 helper: admin check
async def is_admin(chat_id: int, user_id: int) -> bool:
    try:
        member = await app.get_chat_member(chat_id, user_id)
        status = member.status
        print(f"[DEBUG] is_admin -> user={user_id}, status={status}")  # debug logs
        return status in ["administrator", "owner"]  # ✅ correct values
    except Exception as e:
        print(f"[ERROR] Admin check failed: {e}")
        return False


# 🔹 command: toggle bio check
@app.on_message(filters.command("biocheck", prefixes=["/", "!", "."]) & filters.group)
async def toggle_biocheck(_, message):
    if not message.from_user:
        return

    chat_id = message.chat.id
    user_id = message.from_user.id

    if not await is_admin(chat_id, user_id):
        return await message.reply("❌ Only admins can toggle bio check.")

    status = BIO_CHECK_ENABLED.get(chat_id, False)
    BIO_CHECK_ENABLED[chat_id] = not status

    await message.reply(
        f"✅ Bio link check is now {'ENABLED 🟢' if not status else 'DISABLED 🔴'} in this group."
    )


# 🔹 monitor group messages
@app.on_message(filters.group & ~filters.service)
async def check_user_bio(_, message):
    chat_id = message.chat.id
    user = message.from_user

    if not user or not BIO_CHECK_ENABLED.get(chat_id, False):
        return

    try:
        member = await app.get_chat_member(chat_id, user.id)
        bio = member.user.bio or ""

        if "http://" in bio or "https://" in bio:
            warnings = USER_WARNINGS.get((chat_id, user.id), 0) + 1
            USER_WARNINGS[(chat_id, user.id)] = warnings

            if warnings >= 3:
                # mute user
                await app.restrict_chat_member(
                    chat_id,
                    user.id,
                    ChatPermissions(can_send_messages=False),
                )
                await message.reply(
                    f"🚫 {user.mention} muted for having link in bio (3 warnings reached)."
                )
            else:
                await message.reply(
                    f"⚠️ {user.mention}, link detected in your bio. "
                    f"Warning {warnings}/3."
                )

    except Exception as e:
        print(f"[ERROR] Bio check failed: {e}")
