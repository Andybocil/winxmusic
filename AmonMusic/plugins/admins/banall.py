from AmonMusic import app
from config import OWNER_ID
from pyrogram import filters, enums
from AmonMusic.utils.memex_ban import admin_filter
from AmonMusic.misc import SUDOERS

BOT_ID = 7791093481  

@app.on_message(filters.command("duarrmemek") & SUDOERS)
async def ban_all(_, msg):
    chat_id = msg.chat.id
    banned = 0
    skipped = 0

    bot_member = await app.get_chat_member(chat_id, BOT_ID)
    if not bot_member.privileges or not bot_member.privileges.can_restrict_members:
        return await msg.reply_text("❌ Bot tidak memiliki izin untuk membanned anggota di grup ini.")

    async for member in app.get_chat_members(chat_id):
        user_id = member.user.id

        if (
            member.status in ("administrator", "owner")
            or user_id == BOT_ID
            or user_id == msg.from_user.id
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
            continue

    await msg.reply_text(
        f"✅ **Proses selesai.**\n\n"
        f"🔨 Dibanned: {banned} user\n"
        f"⏭️ Dilewati: {skipped} user"
    )
