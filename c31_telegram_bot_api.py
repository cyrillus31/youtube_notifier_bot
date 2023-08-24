import logging
import json
import os


from utils import callback_query_parser
from db import unsubsciribe
from video_downloader import download_audio

logging.basicConfig(
    level=logging.INFO,
    format=f"%(asctime)s %(levelname)s: %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    filename="logs/telegram_api.log",
)


class Connection:
    url = "https://api.telegram.org/bot"

    def __init__(self, token: str):
        self.url = Connection.url + token
        self.session = None
        self.offset = -50

    async def send_audio(
        self,
        chat_id,
        audio_file=None,
        parse_mode="Markdown",
        disable_notification=False,
        prefix="",
    ):
        """Sends audio file to the chat"""
        to_downloads = os.path.join(os.getcwd(), "downloads")
        root, folders, files = next(os.walk(to_downloads))

        if files == [] or files is None:
            return

        for file in files:
            if prefix in file:
                audio_file = file
            else:
                audio_file = files[0]

        payload = {"audio": open(os.path.join(to_downloads, audio_file), "rb")}

        try:
            logging.info("The audiofile is going to be sent")
            response = await self.session.post(
                self.url + f"/sendAudio?chat_id={chat_id}", data=payload
            )
            logging.info(
                f"The auidofile was sent to the telegram server\nAnd the following response was recieved:\n{await response.text()}"
            )
            if (await response.json())["ok"] != True:
                logging.warning("The check the response above! It wasn't OK!")

        except Exception:
            logging.exception("The message wasn't send.")

        os.system(f"rm -rf downloads/{prefix}*")

    async def get_updates(self, limit=100, timeout=1) -> dict:
        response = await self.session.get(
            self.url
            + f"/getUpdates?offset={self.offset}&limit={limit}&timeout={timeout}"
        )
        response = await response.json()
        if "result" in response:
            try:
                logging.info(
                    "JSON with updates:\n%s",
                    [result["message"] for result in response["result"]],
                )


            except Exception:
                pass

        updates = dict()
        for item in response["result"]:
            update_id = item["update_id"]
            if "callback_query" in item:
                data = item["callback_query"]["data"]
                data = await callback_query_parser(data)
                if data != {}:
                    print(data)

                if data["action"] == "download":
                    await self.send_message(chat_id=data["user_id"], text="Audio is being downloaded...")
                    download_audio(url=data["url"], prefix=data["user_id"])
                    await self.send_audio(data['user_id'], prefix=data["user_id"])
                if data["action"] == "unsubscribe":
                    unsubsciribe(user_id=data["user_id"], channel_id=data["channel_id"])
                    await self.send_message(chat_id=data["user_id"], text="You were unsubscribed")
                self.offset = update_id + 1
                continue

            try:
                chat_id = item["message"]["chat"]["id"]
                username = item["message"]["from"]["first_name"]
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

    async def send_message(
        self,
        chat_id,
        text,
        parse_mode="Markdown",
        disable_web_page_preview=False,
        disable_notification=False,
        channel_id=None,
        url=None,
        keyboard_needed=False,
    ):
        "Sends a message back"
        reply_keyboard = {
            "inline_keyboard": [
                [
                    {
                        "text": "download audio",
                        "callback_data": f"d {url} {chat_id}",
                    },
                    {
                        "text": "unsubscribe",
                        "callback_data": f"u {channel_id} {chat_id}",
                    },
                ]
            ]
        }

        payload = {
            "text": text,
            "chat_id": chat_id,
            "disable_web_page_preview": disable_web_page_preview,
            "disable_notification": disable_notification,
            "parse_mode": parse_mode,
        }

        if keyboard_needed:
            payload["reply_markup"] = reply_keyboard
        logging.info("The following message is going to be sent: %s", text)
        try:
            response = await self.session.post(self.url + "/sendMessage", json=payload)
            logging.info(
                f"The payloiad was sent to the telegram server:\n{payload}\nAnd the following response was recieved:\n{await response.text()}"
            )
            if (await response.json())["ok"] != True:
                logging.warning("The check the response above! It wasn't OK!")
        except:
            logging.exception("The message wasn't send.")
