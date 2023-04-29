import responses
import db
import google_api

def message_handler(incoming, chat_id, username):
    if "/start" == incoming:
        if db.add_user(username, chat_id):
            return responses.start.format(username)
        return "User is already registered"

    elif "/add_channel" in incoming and len(incoming.split()) == 2:
        url = incoming.split()[1]
        id, yt_handle = google_api.get_channel_id(url)
        if db.add_channel(id, yt_handle):
            return responses.added
        else:
            return "Channel is already added"

    return "I don't understand you"

