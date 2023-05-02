from googleapiclient.discovery import build
import bs4
import os
import requests


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
            if m.attrs["itemprop"] == "channelId":
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
    # print(response)

    playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    request = service.playlistItems().list(
        part='snippet',
        playlistId=playlist_id,
        maxResults=1,
        # pageToken=next_page_token
    )

    res = request.execute()
    # print(res["items"][0]["snippet"]["title"])
    videoId = res["items"][0]["snippet"]["resourceId"]["videoId"]
    videoTitle = res["items"][0]["snippet"]["title"]


    url = "https://www.youtube.com/watch?v=" + videoId


    return videoTitle, url

def create_dict_of_latest_vids(channels_id: list[str]) -> dict:
    "Returns a dictionary where key is a title of a video and values are (url, channel_id)"
    result = {}
    for channel_id in channels_id:
        title, url = get_latest_video_for_channel(channel_id)
        result[title] = url, channel_id
    return result

service.close()
