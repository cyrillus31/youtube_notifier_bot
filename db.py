import os

import sqlite3
import uuid

conn = sqlite3.connect("db/data.db")
cur = conn.cursor()

MAX_CHANNELS_CONSTRAINT = 10

# create the database tables
with open("db/new_tables.sql", "r", encoding="UTF-8") as file:
    script = file.read()
cur.executescript(script)
conn.commit()

def remove_square_brackets(s):
    s = s.replace("[", "")
    s = s.replace("]", "")
    return s
    

def add_user(name: str, chat_id: str, id = str(uuid.uuid4())):
    try:
        query = """INSERT INTO users VALUES(?, ?, datetime('now', '+3 hours'))"""
        cur.execute(query, (chat_id, name))
        conn.commit()
        return 1

    except sqlite3.IntegrityError as e:
        print("Can't insert new user due to {}".format(e))
        return 0


def add_video(channel_id: str, title: str, url: str):
    try:
        query = """INSERT INTO videos VALUES(?, Null, ?, ?,  datetime('now', '+3 hours'))"""
        cur.execute(query, (channel_id, title, url))
        conn.commit()
        return 1
    except Exception as e:
        # print("Can't insert new video", e)
        return 0


def get_channels():
    query = "SELECT id FROM channels"
    cur.execute(query)
    return cur.fetchall()


def count_channels(user_id=None) -> list[tuple]:
    # query = """SELECT id FROM channels"""
    query = """
    SELECT COUNT(*) FROM channels 
        JOIN channel_user
        JOIN users
        ON channel_id = id AND user_id = chat_id
        WHERE user_id = ?
    """
    cur.execute(query, (user_id,))
    return cur.fetchone()[0]

def get_users():
    query = """SELECT telegram_chat_id FROM channels"""
    cur.execute(query)
    return cur.fetchall()

def get_videos():
    query = """SELECT url FROM videos"""
    cur.execute(query)
    return cur.fetchall()

def get_latest_videos_for_user(user_id: str, amount: int = MAX_CHANNELS_CONSTRAINT, prettify = True) -> list[tuple]:
    "Returns a list of tuples for five latests videos (id, title, url)"
    query = """SELECT * FROM (SELECT id, title, url FROM videos 
                JOIN channel_user 
                 ON videos.channel_id=channel_user.channel_id
                 WHERE channel_user.user_id=?
                ORDER BY id DESC
                LIMIT ?)
               ORDER BY id ASC
               """
    cur.execute(query, (user_id, amount))
    list_of_results = cur.fetchall()
    if prettify: 
        return "\n\n".join([f"{id}) [{remove_square_brackets(title)}]({url})" for id, title, url in list_of_results])
    return list_of_results


def add_channel(user_id: str, channel_id: str, yt_handle: str):
    admin_chat_id = os.getenv("ADMIN_USER_CHAT_ID")
    if admin_chat_id != user_id:
        amount_of_channels = int(count_channels(user_id))
        if amount_of_channels >= 10:
            return f"Channel can't be added. The max limit of channels is: {MAX_CHANNELS_CONSTRAINT}. And you have: {amount_of_channels}"

    try:
        query = """INSERT INTO channels VALUES(?, ?)"""
        cur.execute(query, (channel_id, yt_handle))
    except:
        pass

    try:
        query = "INSERT INTO channel_user VALUES(?, ?)"
        cur.execute(query, (channel_id, user_id))
        conn.commit()
        return 1

    except:
        print("Can't insert new channel")
        return 0


def add_to_favorite(video_id: str, user_id: str):
    # check if the video user is trying to add belongs to him
    query = """SELECT * FROM videos 
               JOIN channel_user ON channel_user.channel_id=videos.channel_id
               WHERE videos.id=? and channel_user.user_id=?"""
    
    cur.execute(query, (video_id, user_id))
    if cur.fetchall() == []:
        return "This video doesn't belong to you"

    query = """INSERT INTO favorites VALUES(?, ?)"""
    try:
        cur.execute(query, (video_id, user_id))
        conn.commit()
        return f"Video {video_id} was added to favorites"
    except:
        return "Video is already in favorites"

def unsubsciribe(user_id: int, channel_id: int):
    query = """DELETE FROM channel_user
               WHERE channel_id=? AND user_id=?"""
    cur.execute(query, (channel_id, user_id))
    conn.commit()
    

def get_favorites(user_id):
    "Returns a list containing video_title and vidoe_url"
    query = """SELECT videos.id, videos.title, videos.url FROM videos
               JOIN favorites ON videos.id=favorites.video_id
               WHERE favorites.user_id=?"""
    cur.execute(query, (user_id,))
    try:
        return "\n\n".join([f"{id}) [{remove_square_brackets(title)}]({url})" for (id, title, url) in cur.fetchall()])
    except:
        return "No videos in favorites"



def get_channel_id_and_user_id_relation() -> dict:
    "Returns a dictionary where the key is channel_id and values are chat_ids"
    query = "SELECT channel_id, user_id FROM channel_user ORDER BY user_id"
    cur.execute(query)
    result = {}
    for channel_id, user_id in cur.fetchall():
        if not user_id in result:
            result[channel_id] = [user_id]
        else:
            result[channel_id].append(user_id)

    return result

def get_url_by_id(video_id, user_id) -> str:
    """Returns url from a database"""
    query = """SELECT url FROM VIDEOS
            JOIN channel_user 
            ON channel_user.channel_id=videos.channel_id
            WHERE videos.id=? AND channel_user.user_id=?"""
    cur.execute(query, (video_id, user_id))
    url = cur.fetchone() # tuple unpacking to get the string right away
    if not url:
        return ""
    url, = url
    return url
