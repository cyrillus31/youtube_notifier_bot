select yt_handle, users.name from channels 
join channel_user 
  on channel_user.channel_id=channels.id 
join users 
  on users.chat_id=channel_user.user_id 
order by users.date_added;
