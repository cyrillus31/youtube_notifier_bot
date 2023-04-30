import responses
import db
import google_api

async def message_handler(incoming, chat_id, username):
    if "/start" == incoming:
        if db.add_user(username, chat_id):
            return responses.start.format(username)
        return "User is already registered"

    elif "/add_channel" in incoming and len(incoming.split()) == 2:
        url = incoming.split()[1]
        yt_id, yt_handle = google_api.get_channel_id(url)
        if db.add_channel(chat_id, yt_id, yt_handle):
            return responses.added
        else:
            return "Channel is already added"

    elif "/latest" == incoming:
        return db.get_10_latest_videos_for_user(chat_id)
    
    elif "/add_favorite" in incoming and len(incoming.split()) ==2:
        return db.add_to_favorite(incoming.split()[1], chat_id)
    
    elif "/get_favorites" in incoming:
        return db.get_favorites(chat_id)
    
    elif "/help" in incoming:
        return responses.help

    return "I don't understand you"

