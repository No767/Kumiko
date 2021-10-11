import os
import qrcode


import discord
import discord.ext
from discord.ext import commands

    
class qrcode_maker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="qrcode")
    async def on_message(self, ctx, *, link:str):
        img = qrcode.make(link)
        img.save(f'./qrcode/qrcode.png')
        file = discord.File(f'./qrcode/qrcode.png')
        embedVar = discord.Embed()
        embedVar.set_image(url=f"attachment://qrcode.png")
        await ctx.send(embed=embedVar, file=file)

def setup(bot):
    bot.add_cog(qrcode_maker(bot))