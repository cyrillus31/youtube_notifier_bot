"This module checks if a new video was added to one of the channels"
import google_api
import db
import asyncio

async def check_updates(chat_id):
    pass

def add_new_videos() -> list[tuple]: #should retunr (chat_id, url)
    "Returns a list of tuples (url, user_id)"
    channel_ids_list = [id for (id,) in db.get_channels()]
    new_videos = google_api.create_dict_of_latest_vids(channel_ids_list)

    channel2user = db.get_channel_id_and_user_id_relation()
    videos_added = []
    for title in new_videos:
        url, channel_id = new_videos[title]
        print(url, channel_id, title)
        if db.add_video(title=title, url=url, channel_id=channel_id):
            for user_id in channel2user[channel_id]:
                videos_added.append((url, user_id))

    return videos_added

