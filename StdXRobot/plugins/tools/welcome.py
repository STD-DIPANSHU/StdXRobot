import sqlite3
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from StdXRobot import app  # ye tera main bot instance import karega

# === DB Setup ===
conn = sqlite3.connect("messages.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    user_id INTEGER,
    chat_id INTEGER,
    count_today INTEGER DEFAULT 0,
    count_week INTEGER DEFAULT 0,
    count_month INTEGER DEFAULT 0,
    count_overall INTEGER DEFAULT 0,
    PRIMARY KEY(user_id, chat_id)
)""")
conn.commit()

# === Functions ===
def update_message_count(user_id, chat_id):
    cursor.execute("SELECT * FROM messages WHERE user_id=? AND chat_id=?", (user_id, chat_id))
    if cursor.fetchone():
        cursor.execute("""
            UPDATE messages 
            SET count_today = count_today + 1,
                count_week = count_week + 1,
                count_month = count_month + 1,
                count_overall = count_overall + 1
            WHERE user_id=? AND chat_id=?
        """, (user_id, chat_id))
    else:
        cursor.execute("""
            INSERT INTO messages (user_id, chat_id, count_today, count_week, count_month, count_overall) 
            VALUES (?, ?, 1, 1, 1, 1)
        """, (user_id, chat_id))
    conn.commit()

def get_leaderboard(chat_id, period="overall"):
    column = f"count_{period}"
    cursor.execute(f"SELECT user_id, {column} FROM messages WHERE chat_id=? ORDER BY {column} DESC LIMIT 10", (chat_id,))
    return cursor.fetchall()

# === Message Counter ===
@app.on_message(filters.group & ~filters.service)
async def count_messages(_, message):
    if message.from_user:
        update_message_count(message.from_user.id, message.chat.id)

# === Command /ranking ===
@app.on_message(filters.command("ranking", prefixes=["/", "!", "."]) & filters.group)
async def ranking_cmd(_, message):
    buttons = [
        [InlineKeyboardButton("📅 Today", callback_data="today"),
         InlineKeyboardButton("📆 Week", callback_data="week")],
        [InlineKeyboardButton("🗓 Month", callback_data="month"),
         InlineKeyboardButton("🌍 Overall", callback_data="overall")]
    ]
    await message.reply_text(
        "📊 **Select Leaderboard Type**",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# === Button Handler ===
@app.on_callback_query()
async def leaderboard_callback(_, query):
    period = query.data
    chat_id = query.message.chat.id
    leaderboard = get_leaderboard(chat_id, period)

    text = f"📊 **{period.capitalize()} Leaderboard** 📊\n\n"
    if leaderboard:
        rank = 1
        for user_id, count in leaderboard:
            try:
                user = await app.get_users(user_id)
                name = user.first_name
            except:
                name = "Unknown"
            text += f"**{rank}.** {name} — `{count}` messages\n"
            rank += 1
    else:
        text += "No data yet ❌"

    await query.message.edit_text(
        text,
        reply_markup=query.message.reply_markup
    )
