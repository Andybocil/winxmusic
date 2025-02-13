import json
from pyrogram import filters
from pyrogram.types import Message
import requests
from AmonMusic import app
import string

@app.on_message(filters.command("adzan", prefixes="/"))
async def adzan_handler(client, message):
    # Extract the location from the message (assuming user provides it after the command)
    text_split = message.text.split()
    
    # If there's no location provided after the command, set `lok` to None
    lok = text_split[1] if len(text_split) > 1 else None

    # Notify the user that the process has started
    pros = await message.reply("Processing...")

    # If no location is provided, inform the user and stop further execution
    if not lok:
        return await pros.edit("Please provide a location.")

    # Fetch prayer times from the MuslimSalat API
    url = f"http://muslimsalat.com/{lok}.json?key=bd099c5825cbedb9aa934e255a81a5fc"    
    req = requests.get(url)

    # Check if the API request was successful
    if req.status_code != 200:
        return await pros.edit(f"Could not retrieve prayer times for {lok}. Please check the location and try again.")

    # Parse the result from the API response
    result = json.loads(req.text)
    tanggal = result["items"][0]["date_for"]
    kueri = result["query"]
    negara = result["country"]
    terbit = result["items"][0]["shurooq"]
    pajar = result["items"][0]["fajr"]
    juhur = result["items"][0]["dhuhr"]
    asar = result["items"][0]["asr"]
    magrip = result["items"][0]["maghrib"]
    isa = result["items"][0]["isha"]

    # Format the response message
    txt = f"<b>👨‍💻 Jᴀᴅᴡᴀʟ sʜᴀʟᴀᴛ ʜᴀʀɪ ɪɴɪ:\n</b>"
    txt += f"<b>📆 ᴛᴀɴɢɢᴀʟ:</b> {tanggal}\n"
    txt += f"<b>📍 ʟᴏᴋᴀsɪ:</b> {kueri}, {negara}\n"
    txt += "------------------------\n"
    txt += f"<blockquote><b>➥ ᴛᴇʀʙɪᴛ:</b> {terbit}\n</blockquote>"
    txt += f"<blockquote><b>➥ sʜᴜʙᴜʜ:</b> {pajar}\n</blockquote>"
    txt += f"<blockquote><b>➥ ᴢᴜʜᴜʀ:</b> {juhur}\n</blockquote>"
    txt += f"<blockquote><b>➥ ᴀsʜᴀʀ:</b> {asar}\n</blockquote>"
    txt += f"<blockquote><b>➥ ᴍᴀɢʜʀɪʙ:</b> {magrip}\n</blockquote>"
    txt += f"<blockquote><b>➥ ɪsʏᴀ:</b> {isa}\n</blockquote>"
    txt += "------------------------"

    # Send the prayer times to the user
    await message.reply(txt)

    # Delete the "Processing..." message
    await pros.delete()
