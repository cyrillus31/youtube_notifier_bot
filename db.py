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
    "Returns a list of tuples for five latests videos (id, title)"
    query = """SELECT id, title FROM videos 
               JOIN channel_user 
               ON videos.channel_id=channel_user.channel_id
               WHERE channel_user.user_id=?
               ORDER BY id
               LIMIT 10
               """
    cur.execute(query, (user_id,))
    return "\n".join([f"{id}) {title}" for id, title in cur.fetchall()])

def add_to_favorite(video_id: str, user_id: str):
    query = """INSERT INTO favorites VALUES(?, ?)"""
    try:
        cur.execute(query, (video_id, user_id))
        conn.commit()
        return "Video {video_id} was added to favorites"
    except:
        return "Video is already in favorites"


def get_favorites(user_id):
    "Returns a list containing video_title and vidoe_url"
    query = """SELECT videos.title, videos.url FROM videos
               JOIN favorites ON videos.id=favorites.video_id
               WHERE favorites.user_id=?"""
    cur.execute(query, (user_id,))
    return "\n".join([f"{title}: {url}" for (title, url) in cur.fetchall()])



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

