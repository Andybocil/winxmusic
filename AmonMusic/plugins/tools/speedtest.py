import asyncio
import speedtest
from pyrogram import filters
from strings import get_command
from AmonMusic import app
from AmonMusic.misc import SUDOERS

# Commands
SPEEDTEST_COMMAND = get_command("SPEEDTEST_COMMAND")


def testspeed(m):
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = m.edit("<b>⇆ 𝖱𝗎𝗇𝗇𝗂𝗇𝗀 𝖣𝗈𝗐𝗅𝗈𝖺𝖽 𝖲𝗉𝖾𝖾𝖽𝖳𝖾𝗌𝗍 ...</b>")
        test.download()
        m = m.edit("<b>⇆ 𝖱𝗎𝗇𝗇𝗂𝗇𝗀 𝖴𝗉𝗅𝗈𝖺𝖽 𝖲𝗉𝖾𝖾𝖽𝖳𝖾𝗌𝗍 ...</b>")
        test.upload()
        test.results.share()
        result = test.results.dict()
        m = m.edit("<b>↻ 𝖲𝗁𝖺𝗋𝗂𝗇𝗀 𝖲𝗉𝖾𝖾𝖽𝖳𝖾𝗌𝗍 𝖱𝖾𝗌𝗎𝗅𝗍𝗌 ...</b>")
    except Exception as e:
        return m.edit(e)
    return result


@app.on_message(filters.command(SPEEDTEST_COMMAND) & SUDOERS)
async def speedtest_function(client, message):
    m = await message.reply_text("Running Speed test")
    loop = asyncio.get_event_loop_policy().get_event_loop()
    result = await loop.run_in_executor(None, testspeed, m)
    output = f"""**✯ <b>𝖲𝗉𝖾𝖾𝖽𝖳𝖾𝗌𝗍 𝖱𝖾𝗌𝗎𝗅𝗍𝗌</b> ✯**
    
<u>**Client:**</u>
**__ISP:__** {result['client']['isp']}
**__Country:__** {result['client']['country']}
  
<u>**Server:**</u>
**__Name:__** {result['server']['name']}
**__Country:__** {result['server']['country']}, {result['server']['cc']}
**__Sponsor:__** {result['server']['sponsor']}
**__Latency:__** {result['server']['latency']}  
**__Ping:__** {result['ping']}"""
    msg = await app.send_photo(
        chat_id=message.chat.id, 
        photo=result["share"], 
        caption=output
    )
    await m.delete()
