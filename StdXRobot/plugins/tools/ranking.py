from datetime import datetime
import random
from pymongo import MongoClient
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from StdXRobot import app
from config import MONGO_DB_URI

# ----------------- Database ----------------- #
mongo_client = MongoClient(MONGO_DB_URI)
db = mongo_client["natu_rankings"]
collection = db["ranking"]

today = {}
MISHI = [
    "https://graph.org/file/f86b71018196c5cfe7344.jpg",
    "https://graph.org/file/5b344a55f3d5199b63fa5.jpg",
    "https://graph.org/file/84de4b440300297a8ecb3.jpg",
]

# ----------------- Watcher ----------------- #
@app.on_message(filters.group)
def message_counter(_, message):
    user_id = message.from_user.id

    # --- today ---
    chat_id = message.chat.id
    if chat_id not in today:
        today[chat_id] = {}
    if user_id not in today[chat_id]:
        today[chat_id][user_id] = {"total_messages": 1}
    else:
        today[chat_id][user_id]["total_messages"] += 1

    # --- overall / week / month in DB ---
    now = datetime.utcnow()
    collection.update_one(
        {"_id": user_id},
        {
            "$inc": {
                "total_messages": 1,
                f"weekly.{now.isocalendar()[1]}": 1,  # week number
                f"monthly.{now.month}": 1,           # month number
            }
        },
        upsert=True,
    )

# ----------------- Helper ----------------- #
async def make_leaderboard(title, data, key="total_messages"):
    response = f"**✦ 📈 {title.upper()} LEADERBOARD**\n\n"
    total_count = 0
    for idx, (uid, count) in enumerate(data, start=1):
        try:
            user = await app.get_users(uid)
            name = user.first_name
        except:
            name = str(uid)
        response += f"**{idx}.** {name} ➠ {count}\n"
        total_count += count
    response += f"\n✉️ **Total messages:** {total_count}"
    return response

def leaderboard_buttons(active="overall"):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(f"Overall {'✅' if active=='overall' else ''}", callback_data="overall"),
        InlineKeyboardButton(f"Today {'✅' if active=='today' else ''}", callback_data="today"),
    ],[
        InlineKeyboardButton(f"Week {'✅' if active=='week' else ''}", callback_data="week"),
        InlineKeyboardButton(f"Month {'✅' if active=='month' else ''}", callback_data="month"),
    ]])

# ----------------- Callback Handlers ----------------- #
@app.on_callback_query(filters.regex("overall"))
async def cb_overall(_, query):
    top = collection.find().sort("total_messages", -1).limit(10)
    data = [(m["_id"], m["total_messages"]) for m in top]
    msg = await make_leaderboard("Overall", data)
    await query.message.edit_text(msg, reply_markup=leaderboard_buttons("overall"))

@app.on_callback_query(filters.regex("today"))
async def cb_today(_, query):
    chat_id = query.message.chat.id
    if chat_id not in today:
        return await query.answer("No data today yet.")
    users_data = [(uid, d["total_messages"]) for uid, d in today[chat_id].items()]
    sorted_users = sorted(users_data, key=lambda x: x[1], reverse=True)[:10]
    msg = await make_leaderboard("Today", sorted_users)
    await query.message.edit_text(msg, reply_markup=leaderboard_buttons("today"))

@app.on_callback_query(filters.regex("week"))
async def cb_week(_, query):
    week = datetime.utcnow().isocalendar()[1]
    pipeline = [
        {"$project": {"uid": "$_id", "count": {"$ifNull": [f"$weekly.{week}", 0]}}},
        {"$sort": {"count": -1}},
        {"$limit": 10},
    ]
    top = list(collection.aggregate(pipeline))
    data = [(m["uid"], m["count"]) for m in top if m["count"] > 0]
    msg = await make_leaderboard("Week", data)
    await query.message.edit_text(msg, reply_markup=leaderboard_buttons("week"))

@app.on_callback_query(filters.regex("month"))
async def cb_month(_, query):
    month = datetime.utcnow().month
    pipeline = [
        {"$project": {"uid": "$_id", "count": {"$ifNull": [f"$monthly.{month}", 0]}}},
        {"$sort": {"count": -1}},
        {"$limit": 10},
    ]
    top = list(collection.aggregate(pipeline))
    data = [(m["uid"], m["count"]) for m in top if m["count"] > 0]
    msg = await make_leaderboard("Month", data)
    await query.message.edit_text(msg, reply_markup=leaderboard_buttons("month"))
