import sqlite3
import uuid

conn = sqlite3.connect("data.db")
cur = conn.cursor()

create_table_videos = """CREATE TABLE IF NOT EXISTS videos (
                channel_id VARCHAR,
                id VARCHAR PRIMARY KEY,
                title VARCHAR,
                url VARCHAR UNIQUE,
                date_added TIMESTAMP
               )"""

create_table_channels = """CREATE TABLE IF NOT EXISTS channels (
                        id VARCHAR PRIMARY KEY,
                        yt_handle VARCHAR UNIQUE
                        )"""

create_table_users= """CREATE TABLE IF NOT EXISTS users (
                        id VARCHAR PRIMARY KEY,
                        name VARCHAR UNIQUE, 
                        chat_id VARCHAR UNIQUE,
                        date_added TIMESTAMP
                        )"""

create_table_fav= """CREATE TABLE IF NOT EXISTS favorites (
                        video_id VARCHAR,
                        user_id VARCHAR
                        )"""

cur.execute(create_table_videos)
cur.execute(create_table_channels)
cur.execute(create_table_users)
cur.execute(create_table_fav)
conn.commit()

def add_user(name: str, chat_id: str, id = str(uuid.uuid4())):
    try:
        query = """INSERT INTO users VALUES(?, ?, ?, datetime('now', '+3 hours'))"""
        cur.execute(query, (id, name, chat_id))
        conn.commit()
        return 1

    except sqlite3.IntegrityError as e:
        print("Can't insert new user due to {}".format(e))
        return 0


def add_video(channel_id: str, title: str, url: str,  id = str(uuid.uuid4())):
    try:
        query = """INSERT INTO videos VALUES(?, ?, ?, ?,  datetime('now', '+3 hours'))"""
        cur.execute(query, (channel_id, id, title, url))
        conn.commit()
        return 1
    except:
        print("Can't insert new video")
        return 0

def add_channel(id: str, yt_handle: str):
    try:
        query = """INSERT INTO channels VALUES(?, ?)"""
        cur.execute(query, (id, yt_handle))
        conn.commit()
        return 1
    except:
        print("Can't insert new channel")
        return 0

def get_channels() -> list[tuple]:
    query = """SELECT url FROM channels"""
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
