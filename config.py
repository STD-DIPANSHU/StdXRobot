import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

API_ID = "6435225"
# -------------------------------------------------------------
API_HASH = "4e984ea35f854762dcde906dce426c2d"

BOT_TOKEN = getenv("BOT_TOKEN", "7838414129:AAGHT0FAW3d9aFTIFbjqP58hO2hbqDJMBZc")
OWNER_USERNAME = getenv("OWNER_USERNAME", "deepanshuxd")
BOT_USERNAME = getenv("BOT_USERNAME", "stdxrobot")
BOT_NAME = getenv("BOT_NAME", "ꜱɪɴɢᴇʀ ᴠɪʙᴇs")
ASSUSERNAME = getenv("ASSUSERNAME", "STDBOTZ")
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://deepxrobot:a@cluster0.9pzoqlf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 17000))
LOGGER_ID = int(getenv("LOGGER_ID", -1002182804742))
OWNER_ID = int(getenv("OWNER_ID", 7394590844))
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HRKU-1e980a6d-beb2-4fd7-8f13-7921cef9c27b")
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/STD-DEEPANSHU/StdXRobot",)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv("GIT_TOKEN", None)
PRIVACY_LINK = getenv("PRIVACY_LINK", "https://telegra.ph/Privacy-Policy-for-YukkiMusic-08-30")
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/STDBOTZ")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/STDBOTZ")
AUTO_LEAVING_ASSISTANT = getenv("AUTO_LEAVING_ASSISTANT", "False")
AUTO_LEAVE_ASSISTANT_TIME = int(getenv("ASSISTANT_LEAVE_TIME", "9000"))
SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION", "9999999"))
SONG_DOWNLOAD_DURATION_LIMIT = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "9999999"))
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "1c21247d714244ddbb09925dac565aed")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "709e1a2969664491b58200860623ef19")
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", "5242880000"))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", "5242880000"))
STRING1 = getenv("STRING_SESSION", "AQGv1ZgAwo1HUyWIV5mpQ64vPxkk-Iq_7f6AVBEDkErYrLVzU3DCaPaYQICvM2B_i_EeX_L2M8lK2nkk5-PgTrK6trkSW0Iw_wmTHleSWQCIRGJewQ1iQq2ja6K72-zizuzGeTA6XJJmH8xXl9OW5m72qj3A0n_JAvJgdVkWEoN4s0T_W-f7RxYtt8TWJfkmMogANUWEwt6WXFX8Ijzbdtj5gU-zEyEP6VjE-jUcco4zM_nIIwTPTIjLi2-Sfd8HbxqwYAGbptpQYZ35saAGlZAVGJlCLsqN2xdOrVGH5KoPO9xI5Jc5QdG8HHW-tQyudTbn3HXW-h6ucMzSPAAijgCUzThh1gAAAAFHYzSOAA")
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)
STRING6 = getenv("STRING_SESSION6", None)
STRING7 = getenv("STRING_SESSION7", None)
BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}
START_IMG_URL = getenv("START_IMG_URL", "https://telegra.ph/file/cfbdee8103102bcb2e5da.jpg")
PING_IMG_URL = getenv("PING_IMG_URL", "https://telegra.ph/file/00360393a15daf7fc4e9d.jpg")
PLAYLIST_IMG_URL = "https://telegra.ph/file/79547e01862628bb85df0.jpg"
STATS_IMG_URL = "https://telegra.ph/file/d30d11c4365c025c25e3e.jpg"
TELEGRAM_AUDIO_URL = "https://telegra.ph/file/79547e01862628bb85df0.jpg"
TELEGRAM_VIDEO_URL = "https://telegra.ph/file/e575ae40d6635250974e1.jpg"
STREAM_IMG_URL = "https://telegra.ph/file/03efec694e41e891b29dc.jpg"
SOUNCLOUD_IMG_URL = "https://telegra.ph/file/d723f4c80da157fca1678.jpg"
YOUTUBE_IMG_URL = "https://telegra.ph/file/4dc854f961cd3ce46899b.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://telegra.ph/file/d723f4c80da157fca1678.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://telegra.ph/file/6c741a6bc1e1663ac96fc.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://telegra.ph/file/6c741a6bc1e1663ac96fc.jpg"
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))
DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))
if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://"
        )
        
