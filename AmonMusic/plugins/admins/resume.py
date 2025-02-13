from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS
from strings import get_command
from AmonMusic import app
from AmonMusic.core.call import Amon
from AmonMusic.utils.database import is_music_playing, music_on
from AmonMusic.utils.decorators import AdminRightsCheck
from AmonMusic.utils.inline import close_markup

# Commands
RESUME_COMMAND = get_command("RESUME_COMMAND")


@app.on_message(filters.command(RESUME_COMMAND) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def resume_com(cli, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text(_["general_2"])
    if await is_music_playing(chat_id):
        return await message.reply_text(_["admin_3"], disable_web_page_preview=True)
    await music_on(chat_id)
    await Amon.resume_stream(chat_id)
    await message.reply_text(
        _["admin_4"].format(message.from_user.mention), reply_markup=close_markup(_)
    )
