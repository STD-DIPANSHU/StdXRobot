from pyrogram import filters
from StdXRobot import app
from StdXRobot.mongo.moviesdb import add_movie_db, search_movie_db, get_all_movies

# ============= ADD MOVIE ============= #
@app.on_message(filters.command("addmovie") & filters.user([123456789]))  # apna admin ID daal
async def add_movie(client, message):
    if not message.reply_to_message or not message.reply_to_message.video:
        return await message.reply("⚠️ Reply to a video with `/addmovie Movie Name`")

    if len(message.command) < 2:
        return await message.reply("⚠️ Usage: `/addmovie Inception`")

    movie_title = " ".join(message.command[1:])
    file_id = message.reply_to_message.video.file_id

    add_movie_db(movie_title, file_id)

    await message.reply(f"✅ Movie **{movie_title}** saved in DB!")


# ============= SEARCH MOVIE ============= #
@app.on_message(filters.command("movies"))
async def movie_search(client, message):
    if len(message.command) < 2:
        return await message.reply("⚠️ Usage: `/movies Inception`")

    query = " ".join(message.command[1:]).lower()
    movie = search_movie_db(query)

    if not movie:
        return await message.reply("❌ Movie not found.")

    try:
        await client.send_video(
            chat_id=message.from_user.id,
            video=movie["file_id"],
            caption=f"🎬 **{movie['title']}**"
        )
        await message.reply("✅ Movie sent in your DM.")
    except Exception as e:
        await message.reply(f"⚠️ Error: `{e}`")


# ============= LIST ALL MOVIES ============= #
@app.on_message(filters.command("allmovies"))
async def all_movies(client, message):
    movies = get_all_movies()
    if not movies:
        return await message.reply("📭 No movies in database.")

    response = "🎬 **Movie List:**\n\n"
    for idx, movie in enumerate(movies, start=1):
        response += f"**{idx}.** {movie['title']}\n"

    await message.reply(response)
