from pyrogram import filters
from StdXRobot import app
from config import MOVIE_CHANNEL_ID

@app.on_message(filters.command("movie"))
async def movie_handler(client, message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Please provide a movie name.\n\nUsage: `/movie pushpa`")

    query = " ".join(message.command[1:]).lower()

    try:
        # Channel me search karo (sab type)
        async for msg in client.search_messages(
            chat_id=MOVIE_CHANNEL_ID,
            query=query,
            filter="all",   # sab check karega: video, doc, text, photo
            limit=1
        ):
            if msg:
                try:
                    # Forward user ke DM me
                    await msg.copy(message.from_user.id)
                    return await message.reply_text("✅ Movie sent in your DM! Check your private chat.")
                except Exception as e:
                    return await message.reply_text("⚠️ Start the bot in DM first, then try again.")

        # Agar kuch na mila
        await message.reply_text("❌ Movie not found. Check spelling or ask owner to upload it.")

    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")
