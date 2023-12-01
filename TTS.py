import discord
from discord.ext import commands
import os
import json
import asyncio
from queue import Queue
from gtts import gTTS

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.voice_states = True
intents.members = True
intents.typing = False
intents.message_content = True
intents.presences = False

bot = commands.Bot(command_prefix='.', intents=intents)

channel_settings = {}
voice_clients = {}

SETTINGS_FILE = "settings.json"

def load_settings():
    try:
        with open(SETTINGS_FILE, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return {}

def save_settings(data):
    with open(SETTINGS_FILE, 'w') as file:
        json.dump(data, file, indent=4)

tts_queue = Queue()
tts_playing = False
current_tts_file_path = None

@bot.event
async def on_ready():
    print(f'{bot.user.name} 온라인')
    global channel_settings
    channel_settings = load_settings()

@bot.command(name='도움')
async def help(ctx):
    await ctx.send('- ``도움말``\n - ``.채널설정: TTS를 사용할 채널을 설정해요.``\n - ``.퇴장: 음성채널에서 퇴장합니다.``\n - ``.도움: 문서를 보여줘요.\n - ``.이용약관: 이용약관을 보여줘요.``')

@bot.command(name='이용약관')
async def what(ctx):
    await ctx.send("""
    ### ``정의``
    - ``TTS 봇이라 함은 User ID가 1180021277751246929인 봇을 말합니다.``

    ### ``개인정보 정책``
    - ``어떠한 데이터를 수집 하나요?``

    - ``이용자의 메세지 데이터``
     - ``TTS를 실행시키기 위해 수집하는 데이터로 TTS 파일을 실행시킨 이후 즉시 삭제합니다.``
     - ``이용자의 메세지를 수집 -> mp3 파일로 변환 -> mp3 파일을 실행``

    - ``TTS 봇을 사용하는 서버의 ID 및 사용하는 채널 ID``
     - ``TTS 봇을 입장시키기 위한 데이터로 수집합니다.``
     - ``봇이 통화방을 입장하기 위해 필수로 수집 됩니다.``

    ### ``개인정보 삭제``
    - ``정보 파기는 언제 하나요?``
    - ``TTS 서비스 종료 또는 이용자의 요청시 삭제합니다.``

    - ``개인정보 삭제는 어디서 요청하나요?``
     - ``아래를 클릭해주세요.``
     - [클릭]('Your-Terms of service-Link')

    ### ``이 정책에 동의하는 기준은 무엇인가요?``
    - ``TTS봇을 이용한 이후부터 즉시 동의하게 됩니다.``
    """)

@bot.command(name='퇴장')
async def leave_channel(ctx):
    server_id = ctx.guild.id
    if server_id in channel_settings and 'channel_id' in channel_settings[server_id]:
        channel_id = channel_settings[server_id]['channel_id']
        voice_channel = discord.utils.get(ctx.guild.voice_channels, id=channel_id)

        if voice_channel:
            vc = discord.utils.get(bot.voice_clients, guild=ctx.guild)
            if vc:
                await vc.disconnect()
                await ctx.send('음성 채널에서 나갔습니다.')
            else:
                await ctx.send('봇이 음성 채널에 연결되어 있지 않습니다.')
        else:
            await ctx.send('설정된 음성 채널이 존재하지 않습니다.')
    else:
        await ctx.send('음성 채널이 설정되어 있지 않습니다.')

@bot.command(name='채널설정')
async def set_channel(ctx):
    server_id = ctx.guild.id
    channel_settings.setdefault(server_id, {})
    channel_settings[server_id]['channel_id'] = ctx.channel.id
    save_settings(channel_settings)
    await ctx.send(f'``TTS 채널이 {ctx.channel.name}으로 설정되었습니다.\n해당 채널에서 메세지를 입력 해주세요.``')

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

bot.run('Your-bot-token')