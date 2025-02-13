from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from AmonMusic import app
from config import BOT_USERNAME

start_txt = """**
<blockquote>✪ ωεℓ¢σмє ᴍᴇᴍᴇx ᴘʀᴏJᴇᴄᴛ ✪
 
 ✰ 𝙅𝘼𝙎𝘼 𝘿𝙀𝙋𝙇𝙊𝙔 𝘽𝙊𝙏 𝙏𝙀𝙇𝙀𝙂𝙍𝘼𝙈 ✰
 
❏ 𝙐𝙎𝙀𝙍𝘽𝙊𝙏 𝙂𝘾𝘼𝙎𝙏 
├ ʀᴘ. 25.000  [ ʙᴜʟᴀɴᴀɴ ᴜsᴇʀʙᴏᴛ ᴜʟᴛʀᴏɪᴅ ] 
├ ʀᴘ. 20.000  [ ʙᴜʟᴀɴᴀɴ ᴜsᴇʀʙᴏᴛ ᴘʀᴇᴍɪᴜᴍ ]
╰ sɪsᴛᴇᴍ ᴛᴇʀɪᴍᴀ ᴊᴀᴅɪ
 
❏ 𝘽𝙊𝙏 𝙈𝙐𝙎𝙄𝙆
├ ʀᴘ. 100.000 [ ᴠᴘs/1ʙᴜʟᴀɴ ] 
├ ᴀᴡᴀʟᴀɴ ᴘᴀsᴀɴɢ 
╰ sɪsᴛᴇᴍ ᴛᴇʀɪᴍᴀ ᴊᴀᴅɪ
 
❏ 𝘽𝙊𝙏 𝙈𝙐𝙎𝙄𝙆 & 𝙈𝘼𝙉𝘼𝙂𝙀 
├ ʀᴘ. 10.000  [ ᴄʟᴏɴᴇ ɢʜ ]
├ ʀᴘ. 250.000  [ ᴅᴇᴘʟᴏʏ + ʜᴇʀᴏᴋᴜ + ᴠᴘs ] 
╰ sɪsᴛᴇᴍ ᴛᴇʀɪᴍᴀ ᴊᴀᴅɪ
 
❏ 𝘽𝙊𝙏 𝙈𝘼𝙉𝘼𝙂𝙀 
├ ʀᴘ. 80.000 [ ʜᴇʀᴏᴋᴜ ]
╰ sɪsᴛᴇᴍ ᴛᴇʀɪᴍᴀ ᴊᴀᴅɪ 

 ❏ ᴄᴀᴛᴀᴛᴀɴ 

❏ ᴀᴘᴀʙɪʟᴀ ʙᴏᴛ ʏᴀɴɢ ᴀɴᴅᴀ ɪɴɢɪɴᴋᴀɴ 
├ ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴅɪ ʟɪsᴛ sɪʟᴀʜᴋᴀɴ ʙᴇʀᴛᴀɴʏᴀ 
╰ ᴏᴡɴᴇʀ ᴅɪ ʙᴀᴡᴀʜ ɪɴɪ

❏ ᴄᴀᴛᴀᴛᴀɴ ʜᴇʀᴏᴋᴜ ʀᴀᴡᴀɴ sᴜsᴘᴇɴ ᴊᴀᴅɪ 
╰ sᴀʏᴀ ᴅᴇᴘʟᴏʏ ᴅɪ ᴠᴘs

❏ sɪʟᴀʜᴋᴀɴ ʜᴜʙᴜɴɢɪ ᴏᴡɴᴇʀ ᴜɴᴛᴜᴋ / 
╰ ᴍᴇʟɪʜᴀᴛ ᴍᴇɴᴀɴʏᴀᴋᴀɴ ᴄᴏɴᴛᴏʜ ʙᴏᴛ
**</blockquote>"""




@app.on_message(filters.command("jasabot"))
async def start(_, msg):
    buttons = [
     
            [ 
            InlineKeyboardButton("✪ ᴀᴅᴅ ᴍᴇ ✪", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
            ],
     
            [
             InlineKeyboardButton("ᴏʀᴅᴇʀ", url="https://t.me/ownercpkoid"),
             InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/thelightoffc"),
             ],
     
             [
             InlineKeyboardButton("ɢʀᴏᴜᴘ", url="https://t.me/memexprojectback"),          
             InlineKeyboardButton("︎ᴍᴜsɪᴄ", url=f"https://github.com/memex2711"),
             ],
     
              ]
 
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await msg.reply_photo(
        photo="https://telegra.ph/file/5c656925faa3d0265f640.jpg",
        caption=start_txt,
        reply_markup=reply_markup
    )
