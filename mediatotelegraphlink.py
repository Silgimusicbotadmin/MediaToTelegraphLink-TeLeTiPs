#Copyright ©️ 2022 TeLe TiPs. All Rights Reserved
#You are free to use this code in any of your project, but you MUST include the following in your README.md (Copy & paste)
# ##Credits - [MediaToTelegraphLink bot by TeLe TiPs] (https://github.com/teletips/MediaToTelegraphLink-TeLeTiPs)

from pyrogram import Client, filters
from pyrogram.types import Message
from telegraph import upload_file
import os

teletips=Client(
    "MediaToTelegraphLink",
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"],
    bot_token = os.environ["BOT_TOKEN"]
)

@teletips.on_message(filters.command('start') & filters.private)
async def start(client, message):
    text = f"""
Heya {message.from_user.mention},
I am here to generate Telegraph links for your media files.

Simply send a valid media file directly to this chat.
Valid file types are 'jpeg', 'jpg', 'png', 'mp4' and 'gif'.

To generate links in **group chats**, add me to your supergroup and send the command <code>/tl</code> as a reply to a valid media file.

🏠 | [Home](https://t.me/teletipsofficialchannel)
            """
    await teletips.send_message(message.chat.id, text, disable_web_page_preview=True)
    

@teletips.on_message(filters.media & filters.private)
async def get_link_private(client, message):
    text = await message.reply("Processing...")

    async def progress(current, total):
        await text.edit_text(f"📥 Downloading media... {current * 100 / total:.1f}%")

    try:
        location = "./media/private/"
        os.makedirs(location, exist_ok=True)  # Qovluğu yaradın, əgər mövcud deyilsə.
        local_path = await message.download(location, progress=progress)

        await text.edit_text("📤 Uploading to Telegraph...")
        
        upload_path = upload_file(local_path)  # Bu, siyahı qaytarmalıdır.
        
        if not isinstance(upload_path, list) or not upload_path:
            raise ValueError("Invalid response from Telegraph API.")

        await text.edit_text(f"**🌐 | Telegraph Link**:\n\n<code>https://telegra.ph{upload_path[0]}</code>")

    except Exception as e:
        await text.edit_text(f"**❌ | File upload failed**\n\n<i>**Reason**: {e}</i>")

    finally:
        if os.path.exists(local_path):
            os.remove(local_path)
@teletips.on_message(filters.command('tl'))
async def get_link_group(client, message):
    try:
        text = await message.reply("Processing...")
        async def progress(current, total):
            await text.edit_text(f"📥 Downloading media... {current * 100 / total:.1f}%")
        try:
            location = f"./media/group/"
            local_path = await message.reply_to_message.download(location, progress=progress)
            await text.edit_text("📤 Uploading to Telegraph...")
            upload_path = upload_file(local_path) 
            await text.edit_text(f"**🌐 | Telegraph Link**:\n\n<code>https://telegra.ph{upload_path[0]}</code>")     
            os.remove(local_path) 
        except Exception as e:
            await text.edit_text(f"**❌ | File upload failed**\n\n<i>**Reason**: {e}</i>")
            os.remove(local_path) 
            return         
    except Exception:
        pass                                           

print("Bot is alive!")
teletips.run()

#Copyright ©️ 2022 TeLe TiPs. All Rights Reserved
