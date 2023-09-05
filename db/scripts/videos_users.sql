select title, users.name from videos 
 join channel_user 
 on videos.channel_id=channel_user.channel_id 
join users 
on users.chat_id=channel_user.user_id 
order by name;
