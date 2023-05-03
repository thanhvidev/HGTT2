import discord
from discord.ext import commands
import typing
import config

intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix=config.PREFIX, intents=intents)
token = config.TOKEN

class Club(commands.Cog):
    def __init__(self, client):
        self.client = client

    @client.command()
    async def club(self, ctx, *, role: typing.Union[discord.Role, str]):
        if isinstance(role, discord.Role):
            role_name = role.name
        else:
            role_name = role.replace(" ", "_")
            role = discord.utils.get(ctx.guild.roles, name=role_name)

        if role_name == "hoilamdi":
            role = discord.utils.get(ctx.guild.roles, name="hội làm di~")
        elif role_name == "choichay":
            role = discord.utils.get(ctx.guild.roles, name="🔥 CLUB | Chơi Cháy")
        elif role_name == "casino":
            role = discord.utils.get(ctx.guild.roles, name="🎲 CLUB | Casino")
        elif role_name == "hoimohon":
            role = discord.utils.get(ctx.guild.roles, name="💋 CLUB | Hội mỏ hỗn")

        if role:
            members = role.members
            member_list = "\n".join([member.mention for member in members])
            embed = discord.Embed(title=f"Danh sách thành viên trong club {role_name}",
                                description=member_list,
                                color=0x00ff00)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Không tìm thấy club có tên là {role_name}")
