import asyncio
import aiohttp
import json

class Connection():
    
    url = "https://api.telegram.org/bot"

    def __init__(self, token: str):
        self.url = Connection.url+token
        self.session = None
        self.offset = -50
    
    # async def get_session(self):
        # async with aiohttp.ClientSession() as session:
            # self.session = session
    

    async def get_updates(self, limit=100, timeout=1) -> dict:
        response = await self.session.get(self.url+f"/getUpdates?offset={self.offset}&limit={limit}&timeout={timeout}")
        response = await response.json()
        # print([result["message"] for result in response["result"]])
        updates = dict()
        for item in response["result"]:
            try:
                chat_id = item["message"]["chat"]["id"]
                username = item["message"]["from"]["first_name"]
                update_id = item["update_id"]
                text = item["message"]["text"]

                updates[update_id] = text, chat_id, username

            except KeyError:
                continue
            
            finally:
                self.offset = update_id + 1
            
        # print(updates)
        return updates


    async def send_message(self, chat_id, text, disable_web_page_preview=False, disable_notification=False):
        "Sends a message back"
        payload = {'text': text, 
                   'chat_id': chat_id,
                   "disable_web_page_preview": disable_web_page_preview,
                   "disable_notification": disable_notification,
                   "parse_mode": "Markdown"
                   }
        await self.session.post(self.url+"/sendMessage", json=payload)
        print('message sent')
    





