from googleapiclient.discovery import build
import bs4
import os
import requests
from dotenv import load_dotenv

import logging 

# create custom looger object
logger = logging.getLogger(__name__)

# create custor formatter class
formatter = logging.Formatter(fmt="\n%(asctime)s %(levelname)s: %(message)s",
                              datefmt="%d-%m-%Y %H:%M:%S")

# create custom file handler_object
file_handler = logging.FileHandler("logs/google_api.log")

# pass fromater object into file_handler object
file_handler.setFormatter(formatter)

# add cutom updated file_handler orbject to my custom logger object and set logging level 
logger.addHandler(file_handler)
logger.setLevel(logging.ERROR)

# logging.basicConfig(filename='logs/google_api.log', 
#                     level=logging.INFO,
#                     datefmt="%d-%m-%Y %H:%M:%S",
#                     format="%(asctime)s %(levelname)s: %(message)s")


load_dotenv()
API_KEY = os.getenv("GOOGLE_YOUTUBE_API_KEY").strip()
service = build("youtube", "v3", developerKey=API_KEY)

def get_channel_id(url: str) -> tuple:
    "Parses the link and gets the channelId meta information"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.MissingSchema:
        return False, False

    soup = bs4.BeautifulSoup(response.text, "lxml")
    meta = soup.find_all("meta")

    channel_id = "Unknown"

    yt_handle = False
    channel_id = False
    for m in meta:
        if yt_handle and channel_id:
            break
        try:
            if m.attrs["itemprop"] == "channelId" or m.attrs["itemprop"] == "identifier":
                channel_id = m.attrs["content"]
        except:
            pass
        try:
            if m.attrs["itemprop"] == "name":
                yt_handle = m.attrs["content"]
        except:
            continue
    return channel_id, yt_handle


collection = service.channels()

def get_latest_video_for_channel(channel_id: str) -> tuple:
    
    request = collection.list(
        part="contentDetails",
        id=channel_id
    )

    response = request.execute()
    logger.info(f"While trying to get the playlist ID the following response war recieved:\n{response}")
    try:
        playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    except Exception as e:
        logger.exception(f"The error while trying to parse the playlist ID:\n{e}")

    request = service.playlistItems().list(
        part='snippet',
        playlistId=playlist_id,
        maxResults=1,
        # pageToken=next_page_token
    )

    res = request.execute()
    logger.info(f"While trying to access VIDEO ID the following reponse war recieved:\n{res}")
    try:
        videoId = res["items"][0]["snippet"]["resourceId"]["videoId"]
        videoTitle = res["items"][0]["snippet"]["title"]
    except Exception as e:
        logger.exception(f"While trying to access the videoId and videoTitle the following error was recieved:\n{e}")

    url = "https://www.youtube.com/watch?v=" + videoId


    return videoTitle, url

def create_dict_of_latest_vids(channels_id: list[str]) -> dict:
    "Returns a dictionary where key is a title of a video and values are (url, channel_id)"
    result = {}
    for channel_id in channels_id:
        try:
            title, url = get_latest_video_for_channel(channel_id)
            result[title] = url, channel_id
        except Exception as e:
            pass
    return result

service.close()
