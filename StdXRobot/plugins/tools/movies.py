from pyrogram import Client, filters
from StdXRobot.mongo.moviesdb import add_movie_db, search_movie_db

from config import MOVIES_CHANNEL_ID

# Automatically add movies to DB when posted in channel
@Client.on_message(filters.chat(MOVIES_CHANNEL_ID) & (filters.video | filters.document))
async def save_movies(client, message):
    title = message.caption or "Untitled"
    file_id = message.video.file_id if message.video else message.document.file_id
    file_type = "video" if message.video else "document"

    await add_movie_db(title, file_id, file_type)
    print(f"✅ Added to DB: {title}")

# Search movies and send to user
@Client.on_message(filters.command("movies"))
async def get_movie(client, message):
    if len(message.command) < 2:
        return await message.reply_text("⚠️ Usage: `/movies Movie Name`", quote=True)

    query = " ".join(message.command[1:])
    movie = await search_movie_db(query)

    if not movie:
        return await message.reply_text("❌ Movie not found.", quote=True)

    try:
        if movie["file_type"] == "video":
            await client.send_video(message.from_user.id, movie["file_id"], caption=f"🎬 {movie['title']}")
        else:
            await client.send_document(message.from_user.id, movie["file_id"], caption=f"🎬 {movie['title']}")

        await message.reply_text("✅ Movie sent to your DM!", quote=True)

    except Exception as e:
        await message.reply_text(f"⚠️ Error: {e}", quote=True)
