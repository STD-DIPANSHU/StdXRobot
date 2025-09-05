# StdXRobot/mongo/moviesdb.py
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_DB_URI = os.getenv("MOVIES_DB_URI", None)  # alag env var rakha hai movies ke liye
DB_NAME = "movies_db"

mongo_client = AsyncIOMotorClient(MONGO_DB_URI)
db = mongo_client[DB_NAME]
movies_collection = db.movies

# add movie
async def add_movie_db(title: str, file_id: str):
    await movies_collection.update_one(
        {"title": title},
        {"$set": {"file_id": file_id}},
        upsert=True,
    )

# search by title
async def search_movie_db(title: str):
    return await movies_collection.find_one({"title": {"$regex": f"^{title}$", "$options": "i"}})

# get all movies
async def get_all_movies():
    return movies_collection.find({})
