from pyrogram import Client, filters
from StdXRobot.mongo.moviesdb import add_movie_db, search_movie_db, get_all_movies

# Command to add movies manually
@Client.on_message(filters.command("addmovie") & filters.reply)
async def add_movie(client, message):
    if len(message.command) < 2:
        return await message.reply_text("⚠️ Usage: reply to a file with `/addmovie Movie Name`")

    title = " ".join(message.command[1:])
    if not message.reply_to_message.document and not message.reply_to_message.video:
        return await message.reply_text("⚠️ Reply to a document or video file to save as movie.")

    file_id = (
        message.reply_to_message.document.file_id
        if message.reply_to_message.document
        else message.reply_to_message.video.file_id
    )

    await add_movie_db(title, file_id)
    await message.reply_text(f"✅ **{title}** added to database.")


# Command to fetch movies by name
@Client.on_message(filters.command("movies"))
async def get_movie(client, message):
    if len(message.command) < 2:
        return await message.reply_text("⚠️ Usage: `/movies Movie Name`")

    query = " ".join(message.command[1:])
    movie = await search_movie_db(query)

    if movie:
        try:
            await client.send_document(
                chat_id=message.from_user.id,
                document=movie["file_id"],
                caption=f"🎬 **{movie['title']}**"
            )
            await message.reply_text("✅ Movie sent in your DM.")
        except Exception as e:
            await message.reply_text(f"⚠️ Error sending movie: {e}")
    else:
        await message.reply_text("❌ Movie not found in database.")


# Command to list all movies
@Client.on_message(filters.command("allmovies"))
async def list_movies(client, message):
    movies = await get_all_movies()
    if not movies:
        return await message.reply_text("❌ No movies in database.")

    text = "🎬 **Available Movies:**\n\n"
    text += "\n".join([f"• {movie['title']}" for movie in movies])

    await message.reply_text(text)
