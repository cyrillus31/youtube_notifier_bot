CREATE TABLE IF NOT EXISTS videos (
                channel_id VARCHAR,
                id INTEGER PRIMARY KEY,
                title VARCHAR,
                url VARCHAR UNIQUE,
                date_added TIMESTAMP);

CREATE TABLE IF NOT EXISTS channels (
                        id VARCHAR PRIMARY KEY,
                        yt_handle VARCHAR 
                        );

CREATE TABLE IF NOT EXISTS users (
                        chat_id VARCHAR PRIMARY KEY,
                        name VARCHAR UNIQUE, 
                        date_added TIMESTAMP
                        );

CREATE TABLE IF NOT EXISTS favorites (
                        video_id VARCHAR,
                        user_id VARCHAR,
                        UNIQUE(video_id, user_id)
                        );

CREATE TABLE IF NOT EXISTS channel_user (
                        channel_id VARCHAR,
                        user_id VARCHAR,
			UNIQUE (channel_id, user_id)
                        );
