import aiohttp
import asyncio
import os

# create a folder for logs in c31_telegram_bot_api module
if not os.path.exists("logs"):
    os.makedirs("logs")

from c31_telegram_bot_api import Connection 
from message_handler import message_handler
import events


TOKEN = os.getenv("TELEGRAM_YOUTUBE_NOTIFIER_TOKEN")
connection = Connection(TOKEN)

async def incoming():
    "This funcion handlins incoming messages"
    while True:
        update = await connection.get_updates()
        # this part handles incoming messages
        for update_id in sorted(update):
            message, chat_id, username = update[update_id]
            response = await message_handler(message, chat_id, username)

            # check if you want preview on the message
            if "/get_favorites" in message or "/latest" in message:
                disable_preview = True
            else:
                disable_preview = False

            await connection.send_message(chat_id, response, disable_web_page_preview=disable_preview)
            await asyncio.sleep(1)

async def send_updates():
    "This function checks for new vidoes and sends updates to users"
    while True:
        #this part handles business logic and sends updates
        videos_added = events.add_new_videos() 
        for url, chat_id in videos_added:
            await connection.send_message(text="NEW VIDEO!\n{}".format(url), chat_id=chat_id, parse_mode="HTML")

        videos_added = []
        await asyncio.sleep(900) 


async def main():
    async with aiohttp.ClientSession() as session:
        connection.session = session
        await asyncio.gather(incoming(), send_updates())
            

if __name__ == "__main__":
    asyncio.run(main())

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
