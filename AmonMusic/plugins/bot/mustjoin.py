
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden
from AmonMusic import app

#--------------------------

MUST_JOIN = "kucingsupport"
#------------------------
@app.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(app: Client, msg: Message):
    if not MUST_JOIN:
        return
    try:
        try:
            await app.get_chat_member(MUST_JOIN, msg.from_user.id)
        except UserNotParticipant:
            if MUST_JOIN.isalpha():
                link = "https://t.me/" + MUST_JOIN
            else:
                chat_info = await app.get_chat(MUST_JOIN)
                link = chat_info.invite_link
            try:
                await msg.reply_photo(
                    photo="https://telegra.ph/file/77ca22a13468c03f33c7a.jpg", caption=f"<blockquote>ʏᴏᴜ ᴍᴜꜱᴛ ᴊᴏɪɴ [ᴛʜɪꜱ ᴄʜᴀɴɴᴇʟ]({link}) ᴛᴏ ᴜꜱᴇ ᴍᴇ 👀 ᴀꜰᴛᴇʀ ᴊᴏɪɴɪɴɢ ᴄʟɪᴄᴋ ᴛʀʏ ᴀɢᴀɪɴ ⚡️</blockquote>",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("ᴊᴏɪɴ ɴᴏᴡ ⚡", url=link)],
                        [InlineKeyboardButton(text = 'ᴛʀʏ ᴀɢᴀɪɴ ↺', url=f"https://t.me/{app.username}?start=help")]
                    ])
                )
                await msg.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        print(f"๏ ᴘʀᴏᴍᴏᴛᴇ ᴍᴇ ᴀs ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴇ ᴍᴜsᴛ_Jᴏɪɴ ᴄʜᴀᴛ ๏: {MUST_JOIN} !")
