import sqlite3
import uuid

conn = sqlite3.connect("db/data.db")
cur = conn.cursor()

# create the database tables
with open("db/new_tables.sql", "r", encoding="UTF-8") as file:
    script = file.read()
cur.executescript(script)
conn.commit()


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

def add_channel(user_id: str, channel_id: str, yt_handle: str):
    try:
        query = """INSERT INTO channels VALUES(?, ?)"""
        cur.execute(query, (channel_id, yt_handle))

        query = "INSERT INTO channel_user VALUES(?, ?)"
        cur.execute(query, (channel_id, user_id))
        conn.commit()
        return 1

    except:
        print("Can't insert new channel")
        return 0

def get_channels() -> list[tuple]:
    query = """SELECT id FROM channels"""
    cur.execute(query)
    return cur.fetchall()

def get_users():
    query = """SELECT telegram_chat_id FROM channels"""
    cur.execute(query)
    return cur.fetchall()

def get_videos():
    query = """SELECT url FROM videos"""
    cur.execute(query)
    return cur.fetchall()

def get_10_latest_videos_for_user(user_id: str) -> list[tuple]:
    "Returns a list of tuples for five latests videos (id, title, url)"
    query = """SELECT * FROM (SELECT id, title, url FROM videos 
               JOIN channel_user 
               ON videos.channel_id=channel_user.channel_id
               WHERE channel_user.user_id=?
               ORDER BY id DESC
               LIMIT 10)
               ORDER BY id ASC
               """
    cur.execute(query, (user_id,))
    return "\n\n".join([f"{id}) [{title}]({url})" for id, title, url in cur.fetchall()])

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


def get_favorites(user_id):
    "Returns a list containing video_title and vidoe_url"
    query = """SELECT videos.id, videos.title, videos.url FROM videos
               JOIN favorites ON videos.id=favorites.video_id
               WHERE favorites.user_id=?"""
    cur.execute(query, (user_id,))
    try:
        return "\n\n".join([f"{id}) [{title}]({url})" for (id, title, url) in cur.fetchall()])
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
    query = """SELECT url FROM VIDEOS
            JOIN channel_user 
            ON channel_user.channel_id=videos.channel_id
            WHERE video_id=?, user_id=?"""
    cur.execute(query, (video_id, user_id))
    url, = cur.fetchone() # tuple unpacking to get the string right away
    return url

