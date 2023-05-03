import random
import discord
from discord.ext import commands
import pytz
from pytz import timezone
from datetime import datetime, timedelta
import asyncio
import typing
from pytimeparse import parse as parse_time
import config

intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix=config.PREFIX, intents=intents)
token = config.TOKEN

giveaways = {}

class Giveaway(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.current_winner = None
        self.prize = ""
    
    @client.command()
    async def ga(self, ctx, duration: str, winners: str, *, prize_name: str):
        global my_emoji
        
        global current_winner
        global prize
        prize = prize_name
        emojis = await ctx.guild.fetch_emoji(1100838235908882512)
        def get_vn_time():
            utc_now = pytz.utc.localize(datetime.utcnow())
            vn_tz = timezone('Asia/Ho_Chi_Minh')
            vn_time = utc_now.astimezone(vn_tz)
            return vn_time

        vn_time = get_vn_time()

        # Tính thời gian kết thúc giveaway
        duration_seconds = parse_time(duration)
        duration_timedelta = timedelta(seconds=duration_seconds)
        end_time = vn_time + duration_timedelta
        # Tạo tin nhắn embed
        if winners.endswith("w"):
            winners = int(winners[:-1])

            embed = discord.Embed(title="",
                      description="",
                      color=discord.Color.from_rgb(255, 0, 255))
            embed.set_author(name=f"{prize}", icon_url=ctx.guild.icon.url)
            embed.add_field(name=f"✧ Người tổ chức:",
                            value=f"{ctx.author.mention} \u200b",
                            inline=True)
            embed.add_field(name=f"✧ Thời gian còn lại:",
                            value=f"\u200b",
                            inline=False)
            embed.set_footer(text=f"{winners} giải | Quay thưởng vào")
            embed.timestamp = end_time
            message = await ctx.send(embed=embed)
            # Lưu thông tin của giveaway
            giveaways[message.id] = {
                'message': message,
                'prize': prize,
                'users_list': []
            }
            try:
                await ctx.message.delete()
            except discord.NotFound:
            # Nếu không tìm thấy tin nhắn để xóa, không làm gì cả
                pass
            # Thêm reaction để tham gia giveaway
            await message.add_reaction(emojis)
            # Đặt làm biến toàn cục
            my_emoji = emojis
            # Bắt đầu đếm ngược
            while True:
            # Lấy thời gian hiện tại
                now_utc = pytz.utc.localize(datetime.utcnow())
                now_vn = now_utc.astimezone(timezone('Asia/Ho_Chi_Minh'))
                # Tính toán thời gian còn lại cho đến khi kết thúc giveaway
                delta_time = end_time - now_vn
                delta_seconds = delta_time.total_seconds()
                if delta_seconds <= 0:
                    # Đếm ngược thời gian và chọn người thắng cuộc
                    await asyncio.sleep(duration_seconds)
                    message = await ctx.fetch_message(message.id)
                    reaction = discord.utils.get(message.reactions, emoji=emojis)
                    users = [user async for user in reaction.users() if not user.bot]
                    users_list = list(users)
                    if client.user in users_list:
                        users_list.remove(client.user)
                    if len(users_list) < winners:
                        winners = len(users_list)
                    if not users_list:
                        await message.reply("Không có ai tham gia giveaway.")
                        return
                    winners_list = random.sample(users_list, winners)
                    winner_mentions = " ".join(
                    [current_winner.mention for current_winner in winners_list])

                    # Chỉnh sửa embed của tin nhắn Giveaway kết thúc
                    embed = discord.Embed(title="",
                                        description=F"",
                                        color=discord.Color.from_rgb(255, 0, 255))
                    embed.set_author(name=f"{prize}", icon_url=ctx.guild.icon.url)
                    embed.add_field(name="️🏆 Người thắng",
                                    value=winner_mentions,
                                    inline=False)
                    embed.add_field(name="🎗️ Được tổ chức bởi",
                                    value=ctx.author.mention,
                                    inline=False)
                    embed.set_footer(icon_url=ctx.author.avatar.url,
                    text=f"Đã quay thưởng vào")
                    embed.timestamp = end_time
                    await message.edit(embed=embed)

                    # Tạo một embed mới để thông báo cho người thắng cuộc
                    await message.reply(
                    content=
                    f"**Chúc mừng** {winner_mentions}, đã thắng giải thưởng **{prize}** trong giveaway này!"
                    )
                    break
                # Cập nhật embed với thời gian đếm ngược hiện tại
                if duration_seconds < 60:
                    countdown = f"{int(delta_seconds)} Giây"
                    await asyncio.sleep(1)    
                else:
                    days = delta_time.days
                    hours, remainder = divmod(delta_seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    countdown = f"{int(hours)}H{int(minutes)}M{int(seconds)}S"
                embed.set_field_at(
                    1,
                    name="✧ Thời Gian Còn Lại:",
                    value=f"`ㅤㅤㅤ{countdown}ㅤㅤㅤ` ",
                    inline=False)
                await message.edit(embed=embed)
                if duration_seconds > 60:
                    await asyncio.sleep(duration_seconds)
        else:
            await ctx.send("nhập số người thắng là <số+w>")

    @client.command()
    async def end(self, ctx, message_id: int):
        global my_emoji
        global current_winner
        global prize

        # Kiểm tra xem giveaway có tồn tại không
        if message_id not in giveaways:
            await ctx.send("Không tìm thấy giveaway.")
            return
        
        giveaway = giveaways[message_id]
        message = giveaway['message']
        prize = giveaway['prize']
        users_list = giveaway['users_list']
        # Lấy tin nhắn giveaway
        try:
            message = await ctx.fetch_message(message_id)
        except discord.NotFound:
            await ctx.send("Không tìm thấy tin nhắn.")
            return

        # Lấy reaction của tin nhắn
        reaction = discord.utils.get(message.reactions, emoji=my_emoji)
        if reaction is None:
            await ctx.send("Không tìm thấy tin nhắn.")
            return

        # Lấy tất cả người tham gia giveaway
        users = [user async for user in reaction.users() if not user.bot]
        users_list = list(users)
        if client.user in users_list:
            users_list.remove(client.user)
        if not users_list:
            await ctx.send("Không có ai tham gia giveaway.")
            return

        # Chọn người thắng cuộc
        current_winner = random.choice(users_list)
        winner_mentions = current_winner.mention
        await message.reply(
            content=
            f"**Chúc mừng** {winner_mentions}, đã thắng giải thưởng **{prize}** trong giveaway này!"
        )
        embed = discord.Embed(title=f"**{prize}**",
                                description=F"",
                                color=discord.Color.from_rgb(255, 0, 255))
        # embed.set_thumbnail(url=str(ctx.guild.icon.url))
        embed.add_field(name="️🏆 Người thắng", value=winner_mentions, inline=True)
        embed.add_field(name="🎗️ Được tổ chức bởi",
                        value=ctx.author.mention,
                        inline=True)
        embed.set_footer(
            text=f"Đã quay thưởng bằng lệnh zend") 
        await message.edit(embed=embed)
        await message.clear_reactions()



    # Lệnh reroll
    @client.command()
    async def rr(self, ctx, message_id: int):
    # Lấy tin nhắn giveaway
        global my_emoji
        global current_winner
        global prize

        # Kiểm tra xem giveaway có tồn tại không
        if message_id not in giveaways:
            await ctx.send("Không tìm thấy giveaway.")
            return
        
        giveaway = giveaways[message_id]
        message = giveaway['message']
        prize = giveaway['prize']
        users_list = giveaway['users_list']

        # Lấy tin nhắn giveaway
        try:
            message = await ctx.fetch_message(message_id)
        except discord.NotFound:
            await ctx.send("Không tìm thấy tin nhắn.")
            return

        # Lấy reaction của tin nhắn
        reaction = discord.utils.get(message.reactions, emoji=my_emoji)
        if reaction is None:
            await ctx.send("Không tìm thấy tin nhắn.")
            return

        # Lấy tất cả người tham gia giveaway
        users = [user async for user in reaction.users() if not user.bot]
        users_list = list(users)
        if client.user in users_list:
            users_list.remove(client.user)
        if not users_list:
            await ctx.send("Không có ai tham gia giveaway.")
            return

        # Chọn người thắng cuộc
        current_winner = random.choice(users_list)
        winner_mentions = current_winner.mention
        embed = message.embeds[0]
        embed.set_field_at(0,
                            name="️🏆 Người thắng",
                            value=winner_mentions,
                            inline=True)
        await message.edit(embed=embed)
        await message.reply(
            content=
            f"**Chúc mừng** {winner_mentions}, đã thắng giải thưởng **{prize}** trong giveaway này!"
        )




# Hàm chuyển đổi thời gian từ định dạng "5h", "10m", "30s" sang giây
    def parse_time(duration: str) -> int:
        if duration.endswith("s"):
            return int(duration[:-1])
        elif duration.endswith("m"):
            return int(duration[:-1]) * 60
        elif duration.endswith("h"):
            return int(duration[:-1]) * 3600
        else:
            raise ValueError("Định dạng thời gian không hợp lệ.")