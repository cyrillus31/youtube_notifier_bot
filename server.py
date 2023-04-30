import aiohttp
import asyncio
import os

from c31_telegram_bot_api import Connection 
from message_handler import message_handler
import events
# from google_api import 


TOKEN = os.getenv("TELEGRAM_YOUTUBE_NOTIFIER_TOKEN")
connection = Connection(TOKEN)

async def main():
    async with aiohttp.ClientSession() as session:
        connection.session = session

        while True:
            update = await connection.get_updates()

            # this part handles incoming messages
            for update_id in sorted(update):
                message, chat_id, username = update[update_id]
                response = message_handler(message, chat_id, username)

                # check if you want preview on the message
                if "/get_favorites" in message:
                    disable_preview = True
                else:
                    disable_preview = False

                await connection.send_message(chat_id, response, disable_web_page_preview=disable_preview)
            
            #this part handles business logic and sends updates
            videos_added = events.add_new_videos() 
            print(videos_added)
            for url, chat_id in videos_added:
                await connection.send_message(text="NEW VIDEO!\n{}".format(url), chat_id=chat_id)

            videos_added = []
            await asyncio.sleep(3) 


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


