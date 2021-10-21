import asyncio
import re

import discord
import pyvcroid2

token = "TOKEN"

bot = discord.Client()

vclist = {}
mclist = {}
filelist = ["temp1.wav","temp2.wav","temp3.wav","temp4.wav","temp5.wav","temp6.wav","temp7.wav","temp8.wav","temp9.wav","temp10.wav"]
counter = 0

async def vc(ctx):
    if ctx.author.voice is None:
        await ctx.channel.send("音声チャンネルに入っていないため操作できません")
        return
    if ctx is not None:
        del vclist[ctx.guild.id]
        await ctx.guild.voice_client.disconnect()
        await ctx.channel.send("切断しました")
        return
    else:
        vclist[ctx.guild.id] = ctx.channel.id
        await ctx.author.voice.channel.connect()
        await ctx.channel.send("接続しました。読み上げを開始します")
        return

@bot.event
async def on_ready():
    print("起動しました")

@bot.event
async def on_message(message):
    if message.content=="!vc":
        if message.author.voice is None:
            await message.channel.send("音声チャンネルに入っていないため操作できません")
            return
        if message.guild.voice_client is not None:
            del vclist[message.guild.id]
            await message.guild.voice_client.disconnect()
            await message.channel.send("切断しました")
            return
        else:
            vclist[message.guild.id] = message.channel.id
            await message.author.voice.channel.connect()
            await message.channel.send("接続しました。読み上げを開始します")
            return
    voice = discord.utils.get(bot.voice_clients, guild=message.guild)

    if voice and voice.is_connected and message.channel.id == vclist[message.guild.id]:
        pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
        pattern_emoji = "\<.+?\>"

        output = re.sub(pattern, "URL省略", message.content)
        output = re.sub(pattern_emoji, "", output)
        if (len(output) > 50):
            output = "長文省略"
        print(output)

        while message.guild.voice_client.is_playing():
            await asyncio.sleep(0.1)
        source = discord.FFmpegPCMAudio(text2wav(vc, output))
        message.guild.voice_client.play(source)
        return
    else:
        return


@bot.event
async def on_voice_state_update(member, before, after):
    voicestate = member.guild.voice_client
    if voicestate is None:
        return
    if len(voicestate.channel.members) == 1:
        await voicestate.disconnect()


def text2wav(vc, text):
    global counter
    counter += 1
    if (counter > 9):
        counter = 0
    filename = filelist[counter]
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
    # listの値の変更で声の変更が可能
    vc.loadVoice(voice_list[1])
else:
    raise Exception("No voice library")
vc.param.volume = 1.0
vc.param.speed = 1.2
vc.param.pitch = 1.0
vc.param.emphasis = 1.0
vc.param.pauseMiddle = -1
vc.param.pauseLong = -1
vc.param.pauseSentence = 200
vc.param.masterVolume = 1.0

bot.run(token)
