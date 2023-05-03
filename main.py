import discord
from discord.ext import commands, tasks
import os
from pytimeparse import parse as parse_time
from flask import Flask
from threading import Thread
from discord.utils import get
import config
from commands.giveaway import Giveaway
from commands.club import Club
from commands.avatar import Avatar
from commands.speak import Speak


intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix=config.PREFIX, intents=intents)
token = config.TOKEN



@client.event
async def on_ready():
  await client.wait_until_ready()  # thay vì client.fetch_guilds()
  print('Đã đăng nhập thành công với tên là {0.user}'.format(client))
  #status streaming
  await client.change_presence(activity=discord.Streaming(name="Hạt Giống Tâm Thần", url="https://www.twitch.tv/thanhvidev"))
  #Club
  await client.add_cog(Club(client))
  #Giveaway
  await client.add_cog(Giveaway(client))
  #Avatar
  await client.add_cog(Avatar(client))
  #Speak
  await client.add_cog(Speak(client))
#++++++++++++++++++++++++++++++BEGIN CLUB++++++++++++++++++++++++++++++++++++#

#+++++++++++++++++++++++++++++++++++END CLUB+++++++++++++++++++++++++++++++#

#++++++++++++++++++++++++++++++++BEGIN GIVEAWAY+++++++++++++++++++++++++++++#


#++++++++++++++++++++++++++++++++++END GA++++++++++++++++++++++++++++++++#
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#


# Tạo URL cho bot
if 'PING_URL' in os.environ:
  app = Flask('')

  @app.route('/')
  def main():
    return "Bot đang hoạt động"

  def run():
    app.run(host='0.0.0.0', port=8080)

  t = Thread(target=run)
  t.start()

client.run(token)
