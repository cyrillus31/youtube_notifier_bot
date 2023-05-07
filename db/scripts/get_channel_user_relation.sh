#! /bin/sh
query='select yt_handle, users.name from channels join channel_user on channel_user.channel_id=channels.id join users on users.chat_id=channel_user.user_id;'
echo $query | sqlite3 ../data.db 
# sqlite3 ../data.db 

