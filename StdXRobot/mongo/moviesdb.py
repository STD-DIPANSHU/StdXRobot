from motor.motor_asyncio import AsyncIOMotorClient
import os

# Alag MOVIE_DB_URI rakho (Heroku config me set karna mat bhoolna)
MOVIE_DB_URI = os.getenv("MOVIE_DB_URI", None)
if not MOVIE_DB_URI:
    raise Exception("❌ MOVIE_DB_URI is not set in environment variables.")

client = AsyncIOMotorClient(MOVIE_DB_URI)
db = client["MovieDatabase"]
movies_collection = db["movies"]

# Add movie
async def add_movie_db(title: str, file_id: str):
    movie = {"title": title, "file_id": file_id}
    await movies_collection.update_one(
        {"title": {"$regex": f"^{title}$", "$options": "i"}},
        {"$set": movie},
        upsert=True
    )

# Search movie
async def search_movie_db(title: str):
    return await movies_collection.find_one(
        {"title": {"$regex": f"{title}", "$options": "i"}}
    )

# Get all movies
async def get_all_movies():
    cursor = movies_collection.find({})
    return await cursor.to_list(length=1000)
