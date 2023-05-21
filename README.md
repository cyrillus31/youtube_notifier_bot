# youtube_notifier_bot
A telegram bot that allows users to receive notifications from the youtube channels they chose and download videos' audio streams. The bot is deployed and can be accessed at: https://t.me/youtube_notifier31_bot

```
python3 -m venv venv; source venv/bin/activate
pip install -r requirements.txt
```
## SYSTEMD service config file example
`cd /etc/systemd/system; sudo touch yt_notifier_bot.service; sudo vi yt_notifier_bot.service`

Fill in yt_notifier_bot.service file with your own data where needed:
```
[Unit]
Description=Youtube notifier bot
After=network.target
Requires=network.target
StartLimitIntervalSec=360
StartLimitBurst=12

[Service]
Type=simple
WorkingDirectory=/path/to/bot's/directory/
Environment="TELEGRAM_YOUTUBE_NOTIFIER_TOKEN=ENTER-YOUR-TOKEN-HERE"
Environment="GOOGLE_YOUTUBE_API_KEY=ENTER-YOUR-KEY-HERE"

User=username
Group=username

ExecStart=/path/to/venv/bin/python /path/to/youtube_notifier_bot/server.py --start
ExecReload=/path/to/venv/bin/python /path/to/youtube_notifier_bot/server.py --restart
TimeoutSec=900
Restart=always
RestartSec=300

[Install]
WantedBy=multi-user.target
```

### Run
`sudo systemctl daemon-reload; sudo systemctl start yt_notifier_bot`
