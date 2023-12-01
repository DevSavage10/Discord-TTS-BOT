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

<svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><title>Python</title><path d="M14.25.18l.9.2.73.26.59.3.45.32.34.34.25.34.16.33.1.3.04.26.02.2-.01.13V8.5l-.05.63-.13.55-.21.46-.26.38-.3.31-.33.25-.35.19-.35.14-.33.1-.3.07-.26.04-.21.02H8.77l-.69.05-.59.14-.5.22-.41.27-.33.32-.27.35-.2.36-.15.37-.1.35-.07.32-.04.27-.02.21v3.06H3.17l-.21-.03-.28-.07-.32-.12-.35-.18-.36-.26-.36-.36-.35-.46-.32-.59-.28-.73-.21-.88-.14-1.05-.05-1.23.06-1.22.16-1.04.24-.87.32-.71.36-.57.4-.44.42-.33.42-.24.4-.16.36-.1.32-.05.24-.01h.16l.06.01h8.16v-.83H6.18l-.01-2.75-.02-.37.05-.34.11-.31.17-.28.25-.26.31-.23.38-.2.44-.18.51-.15.58-.12.64-.1.71-.06.77-.04.84-.02 1.27.05zm-6.3 1.98l-.23.33-.08.41.08.41.23.34.33.22.41.09.41-.09.33-.22.23-.34.08-.41-.08-.41-.23-.33-.33-.22-.41-.09-.41.09zm13.09 3.95l.28.06.32.12.35.18.36.27.36.35.35.47.32.59.28.73.21.88.14 1.04.05 1.23-.06 1.23-.16 1.04-.24.86-.32.71-.36.57-.4.45-.42.33-.42.24-.4.16-.36.09-.32.05-.24.02-.16-.01h-8.22v.82h5.84l.01 2.76.02.36-.05.34-.11.31-.17.29-.25.25-.31.24-.38.2-.44.17-.51.15-.58.13-.64.09-.71.07-.77.04-.84.01-1.27-.04-1.07-.14-.9-.2-.73-.25-.59-.3-.45-.33-.34-.34-.25-.34-.16-.33-.1-.3-.04-.25-.02-.2.01-.13v-5.34l.05-.64.13-.54.21-.46.26-.38.3-.32.33-.24.35-.2.35-.14.33-.1.3-.06.26-.04.21-.02.13-.01h5.84l.69-.05.59-.14.5-.21.41-.28.33-.32.27-.35.2-.36.15-.36.1-.35.07-.32.04-.28.02-.21V6.07h2.09l.14.01zm-6.47 14.25l-.23.33-.08.41.08.41.23.33.33.23.41.08.41-.08.33-.23.23-.33.08-.41-.08-.41-.23-.33-.33-.23-.41-.08-.41.08z"/></svg>
