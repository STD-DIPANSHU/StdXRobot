import re
from pyrogram import filters
import random
from SACHIN_MUSIC import app


@app.on_message(filters.command(["ppy bdy","PPY BDY","bd","BD","appy birthday","APPY BIRTHDAY"], prefixes=["/","h","H"]))
def goodnight_command_handler(_, message):
    sender = message.from_user.mention
    send_sticker = random.choice([True, False])
    if send_sticker:
        sticker_id = get_random_sticker()
        app.send_sticker(message.chat.id, sticker_id)
        message.reply_text(f"**❖ Ҩ፝֟ɴ P᷅᷄᷅ʀᴀᴛɪᷟʙᷝʜᷤᴀᷤ ♡゙ - ᴅʜᴀɴʏᴀᴡᴀᴅ 🐣 ❖**\n\n**❍  {sender} 🍷 **\n\n**❖ ᴘᴀʀᴛʏ ʜᴀɪ sʜʏᴀᴍ ᴋᴏ ᴊᴀʀᴜʀ ᴀᴀɴᴀ**")
    else:
        emoji = get_random_emoji()
        app.send_message(message.chat.id, emoji)
        message.reply_text(f"**❖ Ҩ፝֟ɴ P᷅᷄᷅ʀᴀᴛɪᷟʙᷝʜᷤᴀᷤ ♡゙ - ᴅʜᴀɴʏᴀᴡᴀᴅ 🐣 ❖**\n\n**❍  {sender} {emoji} **\n\n**❖ ᴘᴀʀᴛʏ ʜᴀɪ sʜʏᴀᴍ ᴋᴏ ᴊᴀʀᴜʀ ᴀᴀɴᴀ**")


def get_random_sticker():
    stickers = [
        "CAACAgUAAxkDAAJHbmLuy2NEfrfh6lZSohacEGrVjd5wAAIOBAACl42QVKnra4sdzC_uKQQ", # Sticker 1
        "CAACAgUAAxkDAAJHbmLuy2NEfrfh6lZSohacEGrVjd5wAAIOBAACl42QVKnra4sdzC_uKQQ", # Sticker 2
        "CAACAgUAAxkDAAJHbmLuy2NEfrfh6lZSohacEGrVjd5wAAIOBAACl42QVKnra4sdzC_uKQQ", # Sticker 3
        "CAACAgUAAxkDAAJHbmLuy2NEfrfh6lZSohacEGrVjd5wAAIOBAACl42QVKnra4sdzC_uKQQ",
        "CAACAgUAAxkDAAJHbmLuy2NEfrfh6lZSohacEGrVjd5wAAIOBAACl42QVKnra4sdzC_uKQQ",
    ]
    return random.choice(stickers)


def get_random_emoji():
    emojis = [
        "🎊",
        "🎂",
        "🎉",
    ]
    return random.choice(emojis)
