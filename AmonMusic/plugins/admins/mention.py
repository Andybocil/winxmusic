from pyrogram import filters
from pyrogram.types import(InlineKeyboardButton, InlineKeyboardMarkup)
from pyrogram.types import Message
import os
import asyncio 
from pyrogram import enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import ChatPermissions
from pyrogram.errors import UserNotParticipant
from pyrogram.errors import FloodWait
from AmonMusic.utils.memex_ban import admin_filter
from AmonMusic import app
import config

chatQueue = []

stopProcess = False

@app.on_message(filters.command("tagall") & admin_filter)
async def everyone(_, message):
  global stopProcess
  try: 
    try:
      sender = await app.get_chat_member(message.chat.id, message.from_user.id)
      has_permissions = sender.privileges
    except:
      has_permissions = message.sender_chat  
    if has_permissions:
      if len(chatQueue) > 500:
        await message.reply("➠ sᴀʏᴀ sᴜᴅᴀʜ ᴍᴇɴɢᴇʀᴊᴀᴋᴀɴ ᴊᴜᴍʟᴀʜ ᴍᴀᴋsɪᴍᴜᴍ 𝟻𝟶𝟶 ᴏʙʀᴏʟᴀɴ sᴀᴀᴛ ɪɴɪ. ᴄᴏʙᴀ sᴇʙᴇɴᴛᴀʀ ʟᴀɢɪ ᴍᴇᴋ.")
      else:  
        if message.chat.id in chatQueue:
          await message.reply("➠ sᴜᴅᴀʜ ᴀᴅᴀ ᴘʀᴏsᴇs ʏᴀɴɢ sᴇᴅᴀɴɢ ʙᴇʀʟᴀɴɢsᴜɴɢ ᴅᴀʟᴀᴍ ᴏʙʀᴏʟᴀɴ ɪɴɪ. sɪʟᴀᴋᴀɴ / sᴛᴏᴘ ᴜɴᴛᴜᴋ ᴍᴇᴍᴜʟᴀɪ ʏᴀɴɢ ʙᴀʀᴜ.")
        else:  
          chatQueue.append(message.chat.id)
          if message.reply_to_message:
              inputText = message.reply_to_message.text
          else:
              inputText = message.text.split(None, 1)[1]
          membersList = []
          async for member in app.get_chat_members(message.chat.id):
            if member.user.is_bot == True:
              pass
            elif member.user.is_deleted == True:
              pass
            else:
              membersList.append(member.user)
          i = 0
          lenMembersList = len(membersList)
          if stopProcess: stopProcess = False
          while len(membersList) > 0 and not stopProcess :
            j = 0
            text1 = f"{inputText}\n\n"
            try:    
              while j < 10:
                user = membersList.pop(0)
                if user.username == None:
                  text1 += f"⦿ {user.mention}\n"
                  j+=1
                else:
                  text1 += f"⦿ @{user.username}\n"
                  j+=1
              try:     
                await app.send_message(message.chat.id, text1)
              except Exception:
                pass  
              await asyncio.sleep(2) 
              i+=10
            except IndexError:
              try:
                await app.send_message(message.chat.id, text1)  
              except Exception:
                pass  
              i = i+j
          if i == lenMembersList:    
            await message.reply(f"➠ ʙᴇʀʜᴀsɪʟ ᴛᴀɢᴀʟʟ **ᴊᴜᴍʟᴀʜ ᴛᴏᴛᴀʟ {i} ᴍᴇᴍʙᴇʀ**.\n➠ ʙᴏᴛ ᴅᴀɴ ᴀᴋᴜɴ ʏᴀɴɢ ᴅɪʜᴀᴘᴜs ᴅɪᴛᴏʟᴀᴋ.",
                               reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"๏ sᴜᴘᴘᴏʀᴛ ๏", url=config.SUPPORT_CHANNEL)]])) 
          else:
            await message.reply(f"➠ ʙᴇʀʜᴀsɪʟ ᴛᴀɢᴀʟʟ **{i} ᴍᴇᴍʙᴇʀ.**\n➠ ʙᴏᴛ ᴅᴀɴ ᴀᴋᴜɴ ʏᴀɴɢ ᴅɪʜᴀᴘᴜs ᴅɪᴛᴏʟᴀᴋ.", 
          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"๏ sᴜᴘᴘᴏʀᴛ ๏", url=config.SUPPORT_CHANNEL)]]))
          chatQueue.remove(message.chat.id)
    else:
      await message.reply("➠ ᴍᴀᴀғ, **ʜᴀɴʏᴀ ᴀᴅᴍɪɴ** ʏᴀɴɢ ᴅᴀᴘᴀᴛ ᴍᴇɴᴊᴀʟᴀɴᴋᴀɴ ᴘᴇʀɪɴᴛᴀʜ ɪɴɪ.")  
  except FloodWait as e:
    await asyncio.sleep(e.value)                    
        
@app.on_message(filters.command("batal") & admin_filter)
#@admin_filter("can_change_info")
async def stop(_, message):
  global stopProcess
  try:
    try:
      sender = await app.get_chat_member(message.chat.id, message.from_user.id)
      has_permissions = sender.privileges
    except:
      has_permissions = message.sender_chat  
    if has_permissions:
      if not message.chat.id in chatQueue:
        await message.reply("➠ ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴘʀᴏsᴇs ʏᴀɴɢ ʙᴇʀᴋᴇʟᴀɴᴊᴜᴛᴀɴ ᴜɴᴛᴜᴋ ᴅɪʜᴇɴᴛɪᴋᴀɴ.")
      else:
        stopProcess = True
        await message.reply("➠ sᴛᴏᴘᴘᴇᴅ.")
    else:
      await message.reply("➠ ᴍᴀᴀғ, **ʜᴀɴʏᴀ ᴀᴅᴍɪɴ** ʏᴀɴɢ ᴅᴀᴘᴀᴛ ᴍᴇɴᴊᴀʟᴀɴᴋᴀɴ ᴘᴇʀɪɴᴛᴀʜ ɪɴɪ.")
  except FloodWait as e:
    await asyncio.sleep(e.value)
