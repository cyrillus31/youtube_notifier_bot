async def callback_query_parser(data) -> dict:
    result = {"action": None, "channel_id": None, "url": None, "user_id": None}
    d = data.split()
    if d[0] == "d":
        result["action"] = "download"
        result["url"] = d[1]
        result["user_id"] = d[2]
    if d[0] == "u":
        result["action"] = "unsubscribe"
        result["channel_id"] = d[1] 
        result["user_id"] = d[2]
    return result
        
