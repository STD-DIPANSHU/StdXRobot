from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from StdXRobot import app
from config import BOT_USERNAME
from StdXRobot.utils.errors import capture_err
import httpx 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_txt = """
**
┌┬─────────────────⦿
│├─────────────────╮
│├ ᴛɢ ɴᴀᴍᴇ - sᴀᴄʜɪɴ sᴀɴᴀᴛᴀɴɪ
│├ ʀᴇᴀʟ ɴᴀᴍᴇ - ᴘʀɪɴᴄᴇ ʀᴀᴊᴘᴜᴛ
│├─────────────────╯
├┼─────────────────⦿
├┤~ @V_VIP_OWNER
├┤~ @STD_OWNER
├┤~ @Il_4ST_FIGHTER_lI
├┼─────────────────⦿
│├─────────────────╮
│├OWNER│ @V_VIP_OWNER
│├─────────────────╯
└┴─────────────────⦿
**
"""




@app.on_message(filters.command("ownerqwer"))
async def start(_, msg):
    buttons = [
        [ 
          InlineKeyboardButton(" 𝗦𝗔𝗖𝗛𝗜𝗡 𝗦𝗔𝗡𝗔𝗧𝗔𝗡𝗜 ", url=f"https://t.me/V_VIP_OWNER")
        ],
        [
          InlineKeyboardButton("ＨＥＬＰ", url="https://t.me/Il_4ST_FIGHTER_lI"),
          InlineKeyboardButton("ＲＥＰＯ", url="https://t.me/Il_4ST_FIGHTER_lI"),
          ],
               [
                InlineKeyboardButton("ＳＡＮＡＴＡＮＩ ＮＥＴＷＯＲＫ", url=f"https://t.me/SANATANI_TECH"),
],
[
InlineKeyboardButton("ＯＦＦＩＣＩＡＬ ＢＯＴ", url=f"https://t.me/HIMANSHI_MUSIC_BOT"),

        ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await msg.reply_photo(
        photo="https://telegra.ph/file/94f5088fdc7a0450bfa0a.jpg",
        caption=start_txt,
        reply_markup=reply_markup
    )
