import re
from pyrogram import filters
from pyrogram.types import ChatPermissions
from stdxrobot import app  # <-- yahi tera main client hai

# --- URL regex for detecting links in bio ---
URL_PATTERN = re.compile(r"(https?://|t\.me/|www\.)", re.IGNORECASE)

# group ke hisaab se on/off toggle aur warnings track karne ke liye memory
bio_check_enabled = {}
bio_warnings = {}  # {chat_id: {user_id: warn_count}}


# --- helper: admin check ---
async def is_admin(chat_id, user_id):
    try:
        member = await app.get_chat_member(chat_id, user_id)
        return member.status in ("administrator", "creator", "owner", "admins", "admin")
    except:
        return False


# --- COMMAND: /biocheck on/off/status ---
@app.on_message(filters.command("biocheck", prefixes="/") & filters.group)
async def toggle_bio_check(client, message):
    chat_id = message.chat.id
    user = message.from_user

    if not await is_admin(chat_id, user.id):
        return await message.reply_text("❌ Only admins can toggle bio check.")

    if len(message.command) < 2:
        status = bio_check_enabled.get(chat_id, False)
        return await message.reply_text(
            f"ℹ️ Bio check is currently: **{'ON' if status else 'OFF'}**\n\nUse `/biocheck on` or `/biocheck off`",
            quote=True,
        )

    arg = message.command[1].lower()
    if arg == "on":
        bio_check_enabled[chat_id] = True
        bio_warnings[chat_id] = {}
        await message.reply_text("✅ Bio check has been **enabled** in this group.")
    elif arg == "off":
        bio_check_enabled[chat_id] = False
        bio_warnings.pop(chat_id, None)
        await message.reply_text("🚫 Bio check has been **disabled** in this group.")
    else:
        await message.reply_text("⚠️ Usage: `/biocheck on` or `/biocheck off`")


# --- AUTO CHECK: jab koi message kare group me ---
@app.on_message(filters.group & ~filters.service, group=5)
async def check_bio(client, message):
    chat_id = message.chat.id
    user = message.from_user

    if not user or user.is_bot:
        return

    # agar bio-check off hai to skip
    if not bio_check_enabled.get(chat_id, False):
        return

    # agar user admin hai to skip
    if await is_admin(chat_id, user.id):
        return

    # user ka bio le
    try:
        user_info = await client.get_chat(user.id)
        bio = user_info.bio or ""
    except:
        return

    if URL_PATTERN.search(bio):
        try:
            await message.delete()
        except:
            return await message.reply_text("⚠️ I need **delete messages** permission.")

        # warnings track karo
        user_warnings = bio_warnings.setdefault(chat_id, {})
        count = user_warnings.get(user.id, 0) + 1
        user_warnings[user.id] = count

        if count < 3:
            await message.reply_text(
                f"⚠️ Warning {count}/3 issued to [{user.first_name}](tg://user?id={user.id})\n"
                f"Reason: Link found in bio.\n\n"
                f"❌ Remove links from your bio to avoid mute.",
                disable_web_page_preview=True,
            )
        else:
            try:
                await client.restrict_chat_member(chat_id, user.id, ChatPermissions())
                await message.reply_text(
                    f"🚨 [{user.first_name}](tg://user?id={user.id}) has been **muted**.\n"
                    f"Reason: Link found in bio (3 warnings exceeded).",
                    disable_web_page_preview=True,
                )
            except:
                await message.reply_text("⚠️ I need **restrict members** permission to mute users.")
