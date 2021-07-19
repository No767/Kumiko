import discord
from discord.ext import commands
import time
import os


class PingCog(commands.Cog, name="ping command"):
	def __init__(self, bot:commands.bot):
		self.bot = bot
        
	@commands.command(name = "ping",
					usage="",
					description = "Display the bot's ping.")
	@commands.cooldown(1, 2, commands.BucketType.member)
	async def ping(self, ctx):
		before = time.monotonic()
		message = await ctx.send("🏓 Pong !")
		ping = (time.monotonic() - before) * 1000
		await message.edit(content=f"🏓 Pong !  `{int(ping)} ms`")

def setup(bot:commands.Bot):
	bot.add_cog(PingCog(bot))
 
 
 
client = discord.Client()
client.run(os.getenv('TOKEN'))