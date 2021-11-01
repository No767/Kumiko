import discord
from discord.ext import commands


def discord_colors():
    colors = [0x8B77BE, 0xA189E2, 0xCF91D1, 0x5665AA, 0xA3A3D2]
    from random import choice

    return choice(colors)


def fast_embed(content):
    embed = discord.Embed(description=content, color=discord_colors())
    return embed


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="botinfo", help="Statistics about this bot")
    async def botinfo(self, ctx):
        bot = self.bot
        name = bot.user.name
        guilds = bot.guilds
        total_members = 0
        for guild in guilds:
            total_members += guild.member_count
        average_members_per_guild = total_members / len(guilds)
        embed = discord.Embed(color=discord_colors())
        embed.title = "Bot Info"
        embed.description = f"""
        Name: {name}\n
        Servers: {len(guilds)}\n
        Total Users: {total_members}\n
        Average Users Per Server: {average_members_per_guild}\n
        """
        embed.set_thumbnail(url=bot.user.avatar_url)
        await ctx.send(embed=embed)


class Bot_Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(
        name="botgrowth",
        help="Tips based on bot statistics on how to reach more people!",
    )
    async def botgrowth(self, ctx):
        total_users = 0
        for guild in self.bot.guilds:
            total_users += guild.member_count
        total_guilds = len(self.bot.guilds)
        embed = discord.Embed(color=discord_colors())
        embed.title = "Tips"
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        if total_guilds > 75:
            if total_users / total_guilds > 150:
                embed.description = """
                You have good server densities on this bot which means that it isn't worth trimming as there just isn't enough small servers to make a noticable difference.\n
                - You can try to verify your bot with discord which means providing your ID to bypass the 100 server limit.
                - Or you can add another bot to function as a clone of this bot through the launcher with the add command.
                """
            else:
                embed.description = """
                Your server density is still quite low on this bot which means trimming smaller servers can make space to reach more users
                - You should try using the prune command to trim smaller servers. A size of 5-10 can help ensure that you have enough space in your server limits
                - Alternatively you can verify your bot with discord which means providing your ID to bypass the 100 server limit.
                """
        else:
            embed.description = """
            Your bot is stil relatively small and has space to grow.
            - You should try advertising your bot on bot finder pages like top.gg to get more attention.
            - Also try inviting your friends to invite this bot to their servers as well!
            The more popular your bot is, the more people that will use it!"""
            if total_users / total_guilds < 50:
                embed.description += """\nAdditionally, your server density is still fairly low
                - If the theme of the bot matches try asking owners of larger servers to invite your bot!"""
        await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.command(
        name="prune", help="Removes bot from servers smaller than the specified limit"
    )
    async def purge(self, ctx, minimum):
        guilds_left = 0
        embed = discord.Embed(color=discord_colors())
        embed.title = "Notice of Leave"
        embed.description = f"""{self.bot.user.name} will be leaving your server due to a lack of users;
        This is done to ensure the bot can reach as many people as possible as discord limits the amount of servers one bot can be in to 100.
        This limit is out of our control and the best solution is to trim down the number of smaller servers such that more people can enjoy this bot
        It's been a joy working with you and your patrons!
        If you wish to invite me again, use https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=8\n\n\n
        \tMay we meet again soon,
        {self.bot.user.name}"""
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        for guild in self.bot.guilds:
            if guild.member_count < int(minimum):
                for channel in guild.channels:
                    try:
                        await channel.send(embed=embed)
                        break
                    except:
                        pass
                guilds_left += 1
                await guild.leave()
        await ctx.send(f"Left {guilds_left} server(s)!")

    @commands.is_owner()
    @commands.command(
        name="broadcast",
        help="Sends a broadcast to all servers this bot is connected to; Only use this for serious messages!",
    )
    async def broadcast(self, ctx):
        def check(ms):
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author

        await ctx.send("Enter your message:")
        msg = await self.bot.wait_for("message", check=check)
        embed = discord.Embed(color=discord_colors())
        embed.title = f"{self.bot.user.name} Admin Broadcast"
        embed.description = msg.content
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        for guild in self.bot.guilds:
            for channel in guild.channels:
                try:
                    await channel.send(embed=embed)
                except Exception as e:
                    await channel.send(f"There has been something wrong.\nReason: {e}")
        await ctx.send("Message broadcasted to all servers connected")


def setup(bot):
    bot.add_cog(Utility(bot))
    bot.add_cog(Bot_Admin(bot))
