import aiohttp
import asyncio
import os

from c31_telegram_bot_api import Connection 
from message_handler import message_handler
# from google_api import 


TOKEN = os.getenv("TELEGRAM_YOUTUBE_NOTIFIER_TOKEN")
connection = Connection(TOKEN)

async def main():
    async with aiohttp.ClientSession() as session:
        connection.session = session

        while True:
            update = await connection.get_updates()

            for update_id in sorted(update):
                message, chat_id, username = update[update_id]
                response = message_handler(message, chat_id, username)
                await connection.send_message(chat_id, response)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


