SELECT title, name FROM (
  select title, users.name, users.date_added from videos 
    join channel_user 
      on videos.channel_id=channel_user.channel_id 
    join users 
      on users.chat_id=channel_user.user_id 
    order by videos.date_added DESC
  limit 50
) as subquery
order by date_added ASC;
