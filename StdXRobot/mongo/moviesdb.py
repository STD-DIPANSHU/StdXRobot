from motor.motor_asyncio import AsyncIOMotorClient
from config import MOVIES_DB_URI

client = AsyncIOMotorClient(MOVIES_DB_URI)
db = client["movies_db"]
collection = db["movies"]

async def add_movie_db(title, file_id, file_type):
    movie = {"title": title.lower(), "file_id": file_id, "file_type": file_type}
    await collection.update_one({"file_id": file_id}, {"$set": movie}, upsert=True)

async def search_movie_db(query: str):
    return await collection.find_one({"title": {"$regex": query.lower(), "$options": "i"}})

async def get_all_movies():
    return collection.find({})
