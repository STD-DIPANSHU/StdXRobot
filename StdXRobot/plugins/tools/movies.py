from pyrogram import filters
from pyrogram.enums import MessagesFilter
from StdXRobot import app
from config import MOVIES_CHANNEL_ID


@app.on_message(filters.command("movies", prefixes=["/", "!", "."]))
async def movies_handler(client, message):
    if not MOVIES_CHANNEL_ID:
        return await message.reply_text("❌ Please set `MOVIES_CHANNEL_ID` in config.py")

    if len(message.command) < 2:
        return await message.reply_text("⚠️ Usage: /movies <movie name>")

    query = " ".join(message.command[1:]).strip().lower()
    wait = await message.reply_text(f"🔎 Searching for **{query}** ...", quote=True)

    try:
        found = None
        async for msg in client.search_messages(
            chat_id=int(MOVIES_CHANNEL_ID),
            query=query,
            filter=MessagesFilter.VIDEO,   # sirf video
            limit=100                      # jitna zyada utna acha
        ):
            caption_text = (msg.caption or "").lower()
            file_name = ""
            if msg.video and msg.video.file_name:
                file_name = msg.video.file_name.lower()

            # Match check in caption or file name
            if query in caption_text or query in file_name:
                found = msg
                break

        if not found:
            return await wait.edit("❌ Movie not found.\nCheck spelling or make sure it's uploaded in the channel.")

        # Send movie
        try:
            await found.copy(chat_id=message.from_user.id)
            await wait.edit("✅ Movie sent in your DM.")
        except Exception:
            await found.copy(chat_id=message.chat.id)
            await wait.edit("⚠️ Couldn't DM you, sent here instead.")

    except Exception as e:
        await wait.edit(f"⚠️ API error: `{e}`")
