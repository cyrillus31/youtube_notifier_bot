import re

from server import connection
from video_downloader import download_audio

url_pattern = r"url=(.*)"
chat_pattern = r"chat_id=(.*)"


async def callback_query_parser(data):
    if "download" in data:
        url_match = re.search(url_pattern, data)
        chat_id_match = re.search(chat_pattern, data)
        if url_match and chat_id_match:
            download_audio(url_match)
            await connection.send_audio(chat_id_match)
