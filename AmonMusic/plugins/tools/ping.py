from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS
from strings import get_command
from AmonMusic import app
from AmonMusic.core.call import Auput
from AmonMusic.utils import bot_sys_stats
from AmonMusic.utils.inline import supp_markup
from AmonMusic.utils.decorators.language import language

### Commands
PING_COMMAND = get_command("PING_COMMAND")


@app.on_message(
    filters.command(PING_COMMAND)    
    & ~BANNED_USERS
)
@language
async def ping_com(client, message: Message, _):
    response = await message.reply_video(
        video="https://graph.org/file/6a1cc00dd294562d5f03a-65f43fe56a9ff6b909.mp4",
        caption=_["ping_1"].format(app.mention),
    )
    start = datetime.now()
    pytgping = await Auput.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    resp = (datetime.now() - start).microseconds / 1000
    await response.edit_text(
        _["ping_2"].format(resp, app.mention, UP, RAM, CPU, DISK, pytgping),
        reply_markup=supp_markup(_),
    )
