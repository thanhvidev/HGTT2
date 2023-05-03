import discord
from discord.ext import commands
import config

intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix=config.PREFIX, intents=intents)
token = config.TOKEN


class Avatar(commands.Cog):
    def __init__(self, client):
        self.client = client

    @client.command()
    async def av(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        if not user.avatar:
            av_url = "Không có ảnh hồ sơ"
        else:
            av_url = user.avatar.url

        if not user.guild.icon:
            server_url = "Không có ảnh máy chủ"
        else:
            server_url = user.guild.icon.url

        embed = discord.Embed(title=f"{user.name}'s Avatar")
        embed.set_image(url=av_url)

        await ctx.send(embed=embed)

        # embed = discord.Embed(title=f"{user.name}'s Server Icon")
        # embed.set_image(url=server_url)

        # await ctx.send(embed=embed)
