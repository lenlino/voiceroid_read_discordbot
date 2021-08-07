import asyncio
import re

import discord
import pyvcroid2

token = "ODE0Njg3ODE2MjQ0MTMzODg4.YDhfJw.atwA_oPf1TuGULBzAyEQsAV6iT8"

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
        if message.author.voice is None:
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
        pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
        pattern_emoji = "\<.+?\>"

        output = re.sub(pattern,"URL省略",message.content)
        output = re.sub(pattern_emoji,"",output)
        if (len(output)>50):
            output = "長文省略"
        print(output)

        while message.guild.voice_client.is_playing():
            await asyncio.sleep(0.1)
        source = discord.FFmpegPCMAudio(text2wav(vc, output))
        message.guild.voice_client.play(source)
        return
    else:
        return


@client.event
async def on_voice_state_update(member, before, after):
    voicestate = member.guild.voice_client
    if voicestate is None:
        print("none")
        return
    if len(voicestate.channel.members) == 1:
        await voicestate.disconnect()


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
    #listの値の変更で声の変更が可能
    vc.loadVoice(voice_list[1])
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
