import os
import discord
from discord.ext import commands
import config
from gtts import gTTS

intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix=config.PREFIX, intents=intents)
token = config.TOKEN

voice_dict = {
  "default": None,
  "hoaimy": "vi-VN-Wavenet-C",
  "namminh": "vi-VN-Standard-C"
}


class Speak(commands.Cog):

  def __init__(self, client):
    self.client = client

  @client.command()
  async def s(self, ctx, *args):
    text = " ".join(args)
    user = ctx.author
    if not user.voice:
      await ctx.send("Vui lòng vào room voice để sử dụng lệnh này")
      return
      
    try:
      vc = await user.voice.channel.connect()
    except:
      vc = ctx.voice_client

    if not vc:
      await ctx.send("Bot chưa kết nối với kênh âm thanh.")
      return

    voice_name = "hoaimy"  # Thay đổi giọng nói tại đây
    voice = voice_dict.get(voice_name)

    sound = gTTS(text=text, lang="vi", slow=False)
    if voice is not None:
      sound.voice = voice
    sound.save("tts.mp3")

    if vc.is_playing():
      vc.stop()

    source = await discord.FFmpegOpusAudio.from_probe(
      "tts.mp3", method="fallback", executable="C:/ffmpeg/bin/ffmpeg.exe")
    vc.play(source)

