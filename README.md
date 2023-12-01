# Discord-TTS-BOT

마이크를 사용할 수 없는 이용자들을 위한 간단한 디스코드 봇

##  Installation
#### 다운해야 하는 것은 아래 링크와 같습니다.
- [ffmpeg](https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip)
- [Python](https://www.python.org/downloads/release/python-3115/)

**구동 전 다운로드** 해주세요, 만약 다운로드 하지 않으면 Discord BOT 구동에 **치명적인 오류**가 발생할 수 있습니다

## How it works

1. settings.json 안에 있는 server_id를 받아옵니다.
2. 메세지를 server_id/tts.mp3로 변환합니다.
3. 해당 tts.mp3를 읽습니다.

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

<img src="https://simpleicons.org/icons/python.svg"
