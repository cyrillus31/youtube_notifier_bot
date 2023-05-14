import logging
import json

logging.basicConfig(level=logging.INFO, 
                    format=f"%(asctime)s %(levelname)s: %(message)s",
                    datefmt="%d-%m-%Y %H:%M:%S",
                    filename="logs/telegram_api.logs")

class Connection():
    
    url = "https://api.telegram.org/bot"

    def __init__(self, token: str):
        self.url = Connection.url+token
        self.session = None
        self.offset = -50
    

    async def get_updates(self, limit=100, timeout=1) -> dict:
        response = await self.session.get(self.url+f"/getUpdates?offset={self.offset}&limit={limit}&timeout={timeout}")
        response = await response.json()

        if response["result"]:
            logging.info("JSON with updates:\n%s", [result["message"] for result in response["result"]])

        updates = dict()
        for item in response["result"]:
            try:
                chat_id = item["message"]["chat"]["id"]
                username = item["message"]["from"]["first_name"]
                update_id = item["update_id"]
                text = item["message"]["text"]

                updates[update_id] = text, chat_id, username
                self.offset = update_id + 1

            except:
                logging.exception(msg="Something wrong with the response form Telegram")
                logging.info("The following response was recieved:\n%s", response)
                continue

        if updates:
            logging.info("The following UPDATES object was created:\n%s", updates)
        return updates


    async def send_message(self, chat_id, text, parse_mode="Markdown", disable_web_page_preview=False, disable_notification=False):
        "Sends a message back"
        payload = {'text': text, 
                   'chat_id': chat_id,
                   "disable_web_page_preview": disable_web_page_preview,
                   "disable_notification": disable_notification,
                   "parse_mode": parse_mode 
                   }

        logging.info("The following message is going to be sent: %s", text)

        try:
            response = await self.session.post(self.url+"/sendMessage", json=payload)
            logging.info(f"The payloiad was sent to the telegram server:\n{payload}\nAnd the following response was recieved:\n{await response.text()}")
            if (await response.json())["ok"] != True:
                logging.warning("The check the response above! It wasn't OK!")
        except:
            logging.exception("The message wasn't send.")
    

