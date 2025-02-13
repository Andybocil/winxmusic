from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS
from strings import get_command
from AmonMusic import app
from AmonMusic.core.call import Amon
from AmonMusic.utils.database import is_muted, mute_on
from AmonMusic.utils.decorators import AdminRightsCheck
from AmonMusic.utils.inline import close_markup

# Commands
MUTE_COMMAND = get_command("MUTE_COMMAND")


@app.on_message(filters.command(MUTE_COMMAND) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def mute_admin(cli, message: Message, _, chat_id):
    if not len(message.command) == 1 or message.reply_to_message:
        return await message.reply_text(_["general_2"])
    if await is_muted(chat_id):
        return await message.reply_text(_["admin_5"], disable_web_page_preview=True)
    await mute_on(chat_id)
    await Amon.mute_stream(chat_id)
    await message.reply_text(
        _["admin_6"].format(message.from_user.mention), reply_markup=close_markup(_)
    )
