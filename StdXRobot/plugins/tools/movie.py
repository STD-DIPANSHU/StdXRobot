from pyrogram import filters
from StdXRobot import app
from config import MOVIE_CHANNEL_ID

# -------- Movie Search Command -------- #
@app.on_message(filters.command("movie", prefixes=["/", "!", "."]))
async def movie_handler(client, message):
    if not MOVIE_CHANNEL_ID:
        return await message.reply_text("❌ Please set MOVIE_CHANNEL_ID in config.py")

    if len(message.command) < 2:
        return await message.reply_text("⚠️ Usage: /movie <movie name>")

    query = " ".join(message.command[1:]).strip()
    wait = await message.reply_text(f"🔎 Searching for **{query}** ...", quote=True)

    try:
        results = []
        async for msg in client.search_messages(
            chat_id=int(MOVIE_CHANNEL_ID),
            query=query,
            filter="all",
            limit=3
        ):
            results.append(msg)

        if not results:
            return await wait.edit("❌ Movie not found.\nCheck spelling or make sure bot has read access to the channel.")

        # Try DM
        try:
            for msg in results:
                await msg.copy(chat_id=message.from_user.id)
            await wait.edit("✅ Movie sent in your DM.")
        except Exception:
            # If DM blocked, send in group
            for msg in results:
                await msg.copy(chat_id=message.chat.id)
            await wait.edit("⚠️ Couldn't DM you, sent here instead.")

    except Exception as e:
        await wait.edit(f"⚠️ API error: `{e}`")


# -------- Debug Command -------- #
@app.on_message(filters.command("checkchannel", prefixes=["/", "!", "."]))
async def check_channel(client, message):
    try:
        chat = await client.get_chat(int(MOVIE_CHANNEL_ID))
        await message.reply_text(
            f"✅ Bot can access channel:\n\n"
            f"**Title:** {chat.title}\n"
            f"**ID:** {chat.id}\n"
            f"**Type:** {chat.type}"
        )
    except Exception as e:
        await message.reply_text(f"❌ Bot cannot access channel:\n\n`{e}`")
