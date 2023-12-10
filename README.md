# Discord-TTS-BOT

A simple discord bot for users who don't have access to a microphone

# Stack
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"> <img src="https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=Discord&logoColor=white"> <img src="https://img.shields.io/badge/Github-181717?style=for-the-badge&logo=Github&logoColor=white"> <img src="https://img.shields.io/badge/Replit-F26207?style=for-the-badge&logo=Replit&logoColor=white">

##  Installation
#### Download
- [ffmpeg](https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip)
- [Python](https://www.python.org/downloads/release/python-3115/)

Please **download before running**, failure to do so may result in a **fatal error** in running the Discord BOT.

## How it works

1. Get the server_id from inside settings.json.
2. Convert the message to server_id/tts.mp3.
3. Read the corresponding tts.mp3.

## Document
.채널설정

.퇴장 

.도움

.이용약관

## How to run TTS-BOT

```bash
pip install -r requirements.txt
```

```bash
python TTS.py
```

## Main source

```
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    server_id = message.guild.id
    channel_id = message.channel.id

    if server_id in channel_settings and channel_id == channel_settings[server_id].get('channel_id'):
        await read_tts(message)

    await bot.process_commands(message)

async def read_tts(message):
    global tts_queue, tts_playing, current_tts_file_path, voice_clients

    server_id = message.guild.id
    content = message.content
    current_tts_file_path = f'{server_id}/tts.mp3'  # 폴더 추가

    if not os.path.exists(str(server_id)):
        os.makedirs(str(server_id))

    voice_channel = message.author.voice.channel

    if server_id not in voice_clients:
        vc = await voice_channel.connect()
        voice_clients[server_id] = vc
    else:
        vc = voice_clients[server_id]

    while tts_playing:
        await asyncio.sleep(1)

    tts_playing = True
    
    try:
        tts = gTTS(content, lang='ko')
        tts.save(current_tts_file_path)

        while vc.is_playing():
            await asyncio.sleep(1)

        vc.play(discord.FFmpegPCMAudio(current_tts_file_path), after=lambda e: print('재생 성공', e))
        while vc.is_playing():
            await asyncio.sleep(1)
    except discord.errors.ClientException as e:
        print(f"오류: {e}")
    
    tts_playing = False
    vc.stop()
```
