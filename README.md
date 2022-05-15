# slack-cabinet-bot
automatically upload files uploaded to a channel and sync them with file cabinet  
![image](https://user-images.githubusercontent.com/38074802/168463348-0f411bfc-83c1-426a-8601-c25fc5fd3d5b.png)

## Setup
1. Integrate app to the channel and invite it to a channel

2. run server
```bash
./ngrok 3000
```

3. Run application
```bash
python3 bot.py
```

4. Setup certification
   1. Copy ngrok puiblic url to Oath redirect URL
   2. Input `URL`/slack/events to event redirect URL and interaction URL

