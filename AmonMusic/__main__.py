import asyncio
import importlib
from typing import Any

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall, GroupCallNotFound

import config
from config import BANNED_USERS
from AmonMusic import LOGGER, app, userbot
from AmonMusic.core.call import Amon
from AmonMusic.misc import sudo
from AmonMusic.plugins import ALL_MODULES
from AmonMusic.utils.database import get_banned_users, get_gbanned


async def init() -> None:
    # Check for at least one valid Pyrogram string session
    if all(not getattr(config, f"STRING{i}") for i in range(1, 6)):
        LOGGER("AmonMusic").error("Add Pyrogram string session and then try...")
        exit()
    await sudo()
    try:
        for user_id in await get_gbanned():
            BANNED_USERS.add(user_id)
        for user_id in await get_banned_users():
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for module in ALL_MODULES:
        importlib.import_module("AmonMusic.plugins" + module)
    LOGGER("AmonMusic.plugins").info("Necessary Modules Imported Successfully.")
    await userbot.start()
    await Amon.start()
    try:
        await Amon.stream_call("https://telegra.ph/file/b60b80ccb06f7a48f68b5.mp4")
    except (NoActiveGroupCall, GroupCallNotFound):
        LOGGER("AmonMusic").error(
            "[ERROR] - \n\nTurn on group voice chat and don't put it off otherwise I'll stop working thanks."
        )
        exit()
    except:
        pass
    await Amon.decorators()
    LOGGER("AmonMusic").info("Amo Music Bot Started Successfully")
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("AmonMusic").info("Stopping Amon Music bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
    LOGGER("AmonMusic").info("Stopping Music Bot")
