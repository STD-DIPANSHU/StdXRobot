from pymongo import MongoClient
from config import MOVIE_DB_URI

# Connect to Movie DB
movie_mongo = MongoClient(MOVIE_DB_URI)
movie_db = movie_mongo["MovieBot"]
movie_collection = movie_db["movies"]

# Add movie
def add_movie_db(title: str, file_id: str):
    movie_collection.insert_one({
        "title": title,
        "file_id": file_id
    })

# Search movie
def search_movie_db(query: str):
    return movie_collection.find_one({"title": {"$regex": query, "$options": "i"}})

# Get all movies
def get_all_movies():
    return list(movie_collection.find())
