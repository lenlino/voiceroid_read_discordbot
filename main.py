import asyncio

import discord
import pyvcroid2

token = "ODYwODI3MTc0NTQxNzIxNjAw.YOA5xw.EP_2t-mAipSejnueBIAjLN0APxk"

client = discord.Client()

chlist = {}


@client.event
async def on_ready():
    print("起動しました")


@client.event
async def on_message(message):
    if message.author.bot:
        return
    voice = discord.utils.get(client.voice_clients, guild=message.guild)

    if message.content == ".vc":
        if message.author.voice.channel is None:
            await message.channel.send("音声チャンネルに入っていないため操作できません")
            return
        if voice is not None:
            del chlist[message.guild.id]
            await message.guild.voice_client.disconnect()
            await message.channel.send("切断しました")
            return
        else:
            chlist[message.guild.id] = message.channel.id
            await message.author.voice.channel.connect()
            await message.channel.send("接続しました。読み上げを開始します")
            return

    if voice and voice.is_connected and message.channel.id == chlist[message.guild.id]:
        while message.guild.voice_client.is_playing():
            await asyncio.sleep(0.1)
        source = discord.FFmpegPCMAudio(text2wav(vc, message.content))
        message.guild.voice_client.play(source)
        return
    else:
        return


def text2wav(vc, text):
    filename = "temp.wav"
    speech, tts_events = vc.textToSpeech(text)

    with open(filename, mode="wb") as f:
        f.write(speech)
    return filename


vc = pyvcroid2.VcRoid2()
lang_list = vc.listLanguages()
if "standard" in lang_list:
    vc.loadLanguage("standard")
else:
    raise Exception("No language library")

voice_list = vc.listVoices()
if 0 < len(voice_list):
    vc.loadVoice(voice_list[0])
else:
    raise Exception("No voice library")
vc.param.volume = 2.0
vc.param.speed = 1.2
vc.param.pitch = 1.0
vc.param.emphasis = 1.0
vc.param.pauseMiddle = -1
vc.param.pauseLong = -1
vc.param.pauseSentence = 200
vc.param.masterVolume = 1.0

client.run(token)
