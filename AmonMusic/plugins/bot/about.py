from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from AmonMusic import app
from config import BOT_USERNAME

start_txt = """**
<blockquote>
๏ ᴛʜɪs ɪs ˹ᴀᴍᴏɴ 〆 ᴍᴜsɪᴄ˼ ♪ ʙᴏᴛ - ʏᴏᴜʀ ᴍᴜsɪᴄ ᴄᴏᴍᴘᴀɴɪᴏɴ !

➻ ᴅɪsᴄᴏᴠᴇʀ ᴀ ᴡᴏʀʟᴅ ᴏғ ᴇɴᴅʟᴇss ᴍᴜsɪᴄ ᴘᴏssɪʙɪʟɪᴛɪᴇs ᴡɪᴛʜ  ˹ᴀᴍᴏɴ 〆 ᴍᴜsɪᴄ˼ ♪ , ᴛʜᴇ ᴜʟᴛɪᴍᴀᴛᴇ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴜsɪᴄ ʙᴏᴛ ᴡɪᴛʜ sᴏᴍᴇ ᴀᴡᴇsᴏᴍᴇ ғᴇᴀᴛᴜʀᴇs.

• ᴄᴀɴ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ
• ɴᴏ ɪᴘ ʙʟᴏᴄᴋ ᴘʀᴏʙʟᴇᴍs ᴀᴛ ᴀʟʟ
• 24 ʜʀ ᴜᴘᴛɪᴍᴇ.
• ʟᴀɢ ғʀᴇᴇ sᴍᴏᴏᴛʜ ᴍᴜsɪᴄ ᴇxᴘᴇʀɪᴇɴᴄᴇ.

ᴀᴅᴅ ˹ᴀᴍᴏɴ 〆 ᴍᴜsɪᴄ˼ ♪ ɴᴏᴡ ᴀɴᴅ ʟᴇᴛ ᴛʜᴇ ᴍᴜsɪᴄ ᴛᴀᴋᴇ ᴏᴠᴇʀ ʏᴏᴜʀ ᴡᴏʀʟᴅ
**</blockquote>"""




@app.on_message(filters.command("about"))
async def start(_, msg):
    buttons = [
     
            [ 
            InlineKeyboardButton("✪ ᴀᴅᴅ ᴍᴇ ✪", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
            ],
     
            [
             InlineKeyboardButton("ᴏʀᴅᴇʀ", url="https://t.me/ownercpkoid"),
             InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/memekpro"),
             ],
     
             [
             InlineKeyboardButton("ɢʀᴏᴜᴘ", url="https://t.me/memexprojectback"),          
             InlineKeyboardButton("ᴅᴏɴᴀᴛᴇ", url="https://telegra.ph//file/d71d3b154aa2350962ce9.jpg"),
             ],
     
              ]
 
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await msg.reply_video(
        video="https://graph.org/file/65d4917fdf3ace03aed53-c3f2b8a1f7092ed093.mp4",
        caption=start_txt,
        reply_markup=reply_markup
    )
