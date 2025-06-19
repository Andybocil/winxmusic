import asyncio
from AmonMusic import app
from config import OWNER_ID
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import ChatMemberAdministrator
from AmonMusic.misc import SUDOERS

BOT_ID = app.me.id  

@app.on_message(filters.command("banalll") & SUDOERS)
async def ban_all(_, msg):
    chat_id = msg.chat.id
    banned = 0
    skipped = 0

    bot_member = await app.get_chat_member(chat_id, BOT_ID)

   
    if bot_member.status != ChatMemberStatus.ADMINISTRATOR or not isinstance(bot_member, ChatMemberAdministrator):
        return await msg.reply_text("❌ Bot bukan admin atau tidak bisa membanned anggota.")

    if not bot_member.can_restrict_members:
        return await msg.reply_text("❌ Bot tidak punya izin Ban Users di grup ini.")

    async for member in app.get_chat_members(chat_id):
        user_id = member.user.id

        if (
            member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER) or
            user_id in [BOT_ID, msg.from_user.id, OWNER_ID]
        ):
            skipped += 1
            continue

        try:
            await app.ban_chat_member(chat_id, user_id)
            banned += 1
            await asyncio.sleep(0.2)
        except Exception as e:
            print(f"Gagal ban {user_id}: {e}")
            skipped += 1

    await msg.reply_text(
        f"✅ Proses selesai.\n\n"
        f"🔨 Dibanned: {banned} user\n"
        f"⏭️ Dilewati: {skipped} user"
    )
