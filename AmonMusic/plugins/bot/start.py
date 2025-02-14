import asyncio
import random
import time

from pyrogram import filters
from pyrogram import enums, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch

import config
from config import BANNED_USERS
from config.config import OWNER_ID
from strings import get_command, get_string
from AmonMusic import Telegram, YouTube, app
from AmonMusic.misc import SUDOERS
from AmonMusic.plugins.play.playlist import del_plist_msg
from AmonMusic.plugins.sudo.sudoers import sudoers_list
from AmonMusic.utils.database import (
    add_served_chat,
    is_served_user,
    add_served_user,
    blacklisted_chats,
    get_assistant,
    get_lang,
    get_userss,
    is_on_off,
    is_served_private_chat,
)
from AmonMusic.utils.decorators.language import LanguageStart
from AmonMusic.utils.inline import help_pannel, private_panel, start_pannel
from AmonMusic.utils.command import commandpro

loop = asyncio.get_running_loop()

MEMEK_VID = [
    "https://graph.org/file/1404e3461e264573bcdd0-c9085890741d6e2544.mp4",
    "https://graph.org/file/ff95ce8c6331d23839ae7-23d71017965a73c4db.mp4",
    "https://graph.org/file/65d4917fdf3ace03aed53-c3f2b8a1f7092ed093.mp4",
    "https://graph.org/file/a70393b449b8b111b5c29-810411fbd1d2958f64.mp4",
    "https://graph.org/file/43279d739b5f5a18642c6-042b438a156ac6453f.mp4",
    "https://graph.org/file/1404e3461e264573bcdd0-c9085890741d6e2544.mp4",
    "https://graph.org/file/ff95ce8c6331d23839ae7-23d71017965a73c4db.mp4",
    "https://graph.org/file/65d4917fdf3ace03aed53-c3f2b8a1f7092ed093.mp4",
    "https://graph.org/file/a70393b449b8b111b5c29-810411fbd1d2958f64.mp4",
    "https://graph.org/file/43279d739b5f5a18642c6-042b438a156ac6453f.mp4"
]

STICKERS = [
    "CAACAgUAAxkBAAImjWbWuytdCwYiXAMFuJE0mByhchSZAAJyBgACiJXZVa9ttR9_hcuwNAQ",
    "CAACAgUAAxkBAAImj2bWu13gsWHeAxbgIdB1ccrQDUoGAAJ5CwACfJLZVf2js5lbq0cdNAQ",
    "CAACAgEAAx0Cd6nKUAACATVl_rtAi9KCVQf8vcUC4FMDUfLP8wACHQEAAlEpDTnhphyRDaTrPR4E",
    "CAACAgUAAx0Cd6nKUAACATJl_rsEJOsaaPSYGhU7bo7iEwL8AAPMDgACu2PYV8Vb8aT4_HUPHgQ",

]

async def delete_sticker_after_delay(message, delay):
    await asyncio.sleep(delay)
    await message.delete()

@app.on_message(
    filters.command(get_command("START_COMMAND")) & filters.private & ~BANNED_USERS
)
@LanguageStart
async def start_comm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = first_page(_)
            sticker_message = await message.reply_sticker(sticker=random.choice(STICKERS))
            asyncio.create_task(delete_sticker_after_delay(sticker_message, 2))  # Delete sticker after 2 seconds
            await message.reply_video(
                random.choice(MEMEK_VID),
                caption=_["help_1"].format(config.SUPPORT_GROUP),
                reply_markup=keyboard,
            )
        if name[0:4] == "song":
            return await message.reply_text(_["song_2"])
        if name[0:3] == "sta":
            m = await message.reply_text(
                "🔎 Fetching your personal stats.!"
            )
            stats = await get_userss(message.from_user.id)
            tot = len(stats)
            if not stats:
                await asyncio.sleep(1)
                return await m.edit(_["ustats_1"])

            def get_stats():
                msg = ""
                limit = 0
                results = {}
                for i in stats:
                    top_list = stats[i]["spot"]
                    results[str(i)] = top_list
                    list_arranged = dict(
                        sorted(
                            results.items(),
                            key=lambda item: item[1],
                            reverse=True,
                        )
                    )
                if not results:
                    return m.edit(_["ustats_1"])
                tota = 0
                videoid = None
                for vidid, count in list_arranged.items():
                    tota += count
                    if limit == 10:
                        continue
                    if limit == 0:
                        videoid = vidid
                    limit += 1
                    details = stats.get(vidid)
                    title = (details["title"][:35]).title()
                    if vidid == "telegram":
                        msg += f"🔗[Telegram Files and Audios](https://t.me/telegram) ** played {count} times**\n\n"
                    else:
                        msg += f"🔗 [{title}](https://www.youtube.com/watch?v={vidid}) ** played {count} times**\n\n"
                msg = _["ustats_2"].format(tot, tota, limit) + msg
                return videoid, msg

            try:
                videoid, msg = await loop.run_in_executor(
                    None, get_stats
                )
            except Exception as e:
                print(e)
                return
            thumbnail = await YouTube.thumbnail(videoid, True)
            await m.delete()
            await message.reply_photo(photo=thumbnail, caption=msg)
            return
        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(config.LOG):
                sender_id = message.from_user.id
                sender_name = message.from_user.first_name
                return await app.send_message(
                    config.LOG_GROUP_ID,
                    f"{message.from_user.mention} has just started bot to check <code>SUDOLIST</code>\n\n**USER ID:** {sender_id}\n**USER NAME:** {sender_name}",
                )
            return
        if name[0:3] == "lyr":
            query = (str(name)).replace("lyrics_", "", 1)
            lyrical = config.lyrical
            lyrics = lyrical.get(query)
            if lyrics:
                return await Telegram.send_split_text(message, lyrics)
            else:
                return await message.reply_text(
                    "Failed to get lyrics."
                )
        if name[0:3] == "del":
            await del_plist_msg(client=client, message=message, _=_)
        if name[0:3] == "inf":
            m = await message.reply_text("🔎 Fetching Info!")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[
                    0
                ]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = f"""
🔍__**Video Track Information**__

❇️**Title:** {title}

⏳**Duration:** {duration} Mins
👀**Views:** `{views}`
⏰**Published Time:** {published}
🎥**Channel Name:** {channel}
📎**Channel Link:** [Visit From Here]({channellink})
🔗**Video Link:** [Link]({link})

⚡️ __Searched Powered By {config.MUSIC_BOT_NAME}__"""
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🎥 Watch ", url=f"{link}"
                        ),
                        InlineKeyboardButton(
                            text="🔄 Close", callback_data="close"
                        ),
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(
                message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=key,
            )
            if await is_on_off(config.LOG):
                sender_id = message.from_user.id
                sender_name = message.from_user.first_name
                return await app.send_message(
                    config.LOG_GROUP_ID,
                    f"{message.from_user.mention} has just started bot to check <code>VIDEO INFORMATION</code>\n\n**USER ID:** {sender_id}\n**USER NAME:** {sender_name}",
                )
    else:
        out = private_panel(_, app.username)
        sticker_message = await message.reply_sticker(sticker=random.choice(STICKERS))
        asyncio.create_task(delete_sticker_after_delay(sticker_message, 2))  # Delete sticker after 2 seconds
        served_chats = len(await get_served_chats())
        served_users = len(await get_served_users())
        UP, CPU, RAM, DISK = await bot_sys_stats()
        await message.reply_video(
            random.choice(MEMEK_VID),
            caption=random.choice(MEKI).format(message.from_user.mention, app.mention, UP, DISK, CPU, RAM, served_users, served_chats),
            reply_markup=InlineKeyboardMarkup(out),
        )
        if await is_on_off(config.LOG):
            sender_id = message.from_user.id
            sender_name = message.from_user.first_name
            return await app.send_message(
                config.LOG_GROUP_ID,
                f"{message.from_user.mention} has just started Bot.\n\n**USER ID:** {sender_id}\n**USER NAME:** {sender_name}",
            )



@app.on_message(
    filters.command(get_command("START_COMMAND")) & filters.group & ~BANNED_USERS
)
@LanguageStart
async def testbot(client, message: Message, _):
    out = start_pannel(_)
    uptime = int(time.time() - _boot_)
    await message.reply_video(
        random.choice(MEMEK_VID),
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat(message.chat.id)
    

welcome_group = 2


@app.on_message(filters.new_chat_members, group=welcome_group)
async def welcome(client, message: Message):
    chat_id = message.chat.id
    if config.PRIVATE_BOT_MODE == str(True):
        if not await is_served_private_chat(message.chat.id):
            await message.reply_text(
                "**ᴩʀɪᴠᴀᴛᴇ ᴍᴜsɪᴄ ʙᴏᴛ**\n\nᴏɴʟʏ ғᴏʀ ᴛʜᴇ ᴄʜᴀᴛs ᴀᴜᴛʜᴏʀɪsᴇᴅ ʙʏ ᴍʏ ᴏᴡɴᴇʀ, ʀᴇǫᴜᴇsᴛ ɪɴ ᴍʏ ᴏᴡɴᴇʀ's ᴩᴍ ᴛᴏ ᴀᴜᴛʜᴏʀɪsᴇ ʏᴏᴜʀ ᴄʜᴀᴛ ᴀɴᴅ ɪғ ʏᴏᴜ ᴅᴏɴ'ᴛ ᴡᴀɴᴛ ᴛᴏ ᴅᴏ sᴏ ᴛʜᴇɴ ғᴜ*ᴋ ᴏғғ ʙᴇᴄᴀᴜsᴇ ɪ'ᴍ ʟᴇᴀᴠɪɴɢ."
            )
            return await app.leave_chat(message.chat.id)
    else:
        await add_served_chat(chat_id)
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if member.id == app.id:
                chat_type = message.chat.type
                if chat_type != enums.ChatType.SUPERGROUP:
                    await message.reply_text(_["start_6"])
                    return await app.leave_chat(message.chat.id)
                if chat_id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_7"].format(
                            f"https://t.me/{app.username}?start=sudolist"
                        )
                    )
                    return await app.leave_chat(chat_id)
                userbot = await get_assistant(message.chat.id)
                out = start_pannel(_)
                await message.reply_text(
                    _["start_3"].format(
                        config.MUSIC_BOT_NAME,
                        userbot.username,
                        userbot.id,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
            if member.id in config.OWNER_ID:
                return await message.reply_text(
                    _["start_4"].format(config.MUSIC_BOT_NAME, member.mention)
                )
            if member.id in SUDOERS:
                return await message.reply_text(
                    _["start_5"].format(config.MUSIC_BOT_NAME, member.mention)
                )
            return
        except:
            return


@app.on_message(commandpro(["/alive", "Alexa"]))
async def alive(client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/125f531d44a9999290cac.jpg",
        caption=f"""━━━━━━━━━━━━━━━━━━━━━━━━\n\n✪ ʜᴇʟʟᴏ, ˹ᴀᴍᴏɴ 〆 ᴍᴜsɪᴄ˼ ɪs ᴡᴏʀᴋɪɴɢ ᴀɴᴅ ғᴜɴᴄᴛɪᴏɴɪɴɢ ᴘʀᴏᴘᴇʀʟʏ\n✪ ᴛʜᴀɴᴋs ᴛᴏ ᴛᴇᴀᴍ 🌼 ..\n\n┏━━━━━━━━━━━━━━━━━┓\n┣★ ᴏᴡɴᴇʀ    : [ғʀ ʀᴀsᴛᴀ](https://t.me/ownercpkoid)\n┣★ ᴜᴘᴅᴀᴛᴇs › : [˹ᴀᴍᴏɴ 〆 ᴍᴜsɪᴄ˼](https://t.me/memexprojectback)┓\n┗━━━━━━━━━━━━━━━━━┛\n\n💞 ɪғ ʏᴏᴜ ʜᴀᴠᴇ ᴀɴʏ ǫᴜᴇsᴛɪᴏɴs ᴛʜᴇɴ\nᴅᴍ ᴛᴏ ᴍʏ [ᴏᴡɴᴇʀ](https://t.me/ownercpkoid) ᴍᴀᴋᴇ sᴜʀᴇ ᴛᴏ sᴛᴀʀ ᴏᴜʀ ᴘʀᴏᴊᴇᴄᴛ ...\n\n━━━━━━━━━━━━━━━━━━━━━━━━""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🌼 sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ 💮", url=config.SUPPORT_GROUP)]]
        ),
    )


@app.on_message(commandpro(["/verify", "amonverification"]))
async def verify(client, message: Message):
    if await is_served_user(message.from_user.id):
        await message.reply_text(
            text="😂 ᴅᴇᴀʀ ʏᴏᴜ ᴀʀᴇ ᴀʟʀᴇᴀᴅʏ ᴠᴇʀɪғɪᴇᴅ",
        )
        return
    await add_served_user(message.from_user.id)
    await message.reply_photo(
        photo=f"https://telegra.ph/file/7f08acd78577f99f60ff5.png",
        caption=f"""━━━━━━━━━━━━━━━━━━━━━━━━\n\n✪ **ᴄᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴ** 🎉\n✪ ɴᴏᴡ ʏᴏᴜ ᴀʀᴇ ˹ᴀᴍᴏɴ 〆 ᴍᴜsɪᴄ˼ ᴠᴇʀɪғɪᴇᴅ ᴍᴇᴍʙᴇʀ ɢᴏ ʙᴀᴄᴋ ᴀɴᴅ ᴇɴᴊᴏʏ ᴏᴜʀ sᴇʀᴠɪᴄᴇ ᴀɴᴅ ᴘʟᴀʏ ᴍᴜsɪᴄ 🌼 ..\n\n━━━━━━━━━━━━━━━━━━━━━━━━""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🌼 sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ 💮", url=config.SUPPORT_GROUP)]]
        ),
    )
