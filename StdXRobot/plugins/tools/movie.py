# movie.py

from pyrogram import filters
from StdXRobot import app
from config import MOVIE_CHANNEL_ID

# /movie <movie name>
@app.on_message(filters.command("movie"))
async def movie_handler(client, message):
    if len(message.command) < 2:
        return await message.reply("⚠️ Usage: /movie <movie name>")

    query = " ".join(message.command[1:]).lower()
    user_id = message.from_user.id

    found = False
    async for msg in client.search_messages(MOVIE_CHANNEL_ID, query=query):
        if msg.video or msg.document:  # only send media files
            try:
                # try to send in DM
                await msg.copy(chat_id=user_id)
                await message.reply("✅ Movie sent in your DM!")
                found = True
                break
            except Exception:
                # fallback: send in the same chat
                await msg.copy(chat_id=message.chat.id)
                await message.reply("⚠️ Couldn't DM you. Sent here instead.")
                found = True
                break

    if not found:
        await message.reply("❌ Movie not found in database.")

