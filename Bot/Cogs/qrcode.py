import os

import discord
import discord.ext
import qrcode
from discord.ext import commands


class qrcode_maker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="qrcode")
    async def on_message(self, ctx, *, link: str):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        if not os.path.isfile("/qrcode/qrcode.png"):
            img = qrcode.make(link)
            img.save("./qrcode/qrcode.png")
        else: 
            img = qrcode.make(link)
            img.save("./qrcode/qrcode.png")
        file = discord.File("./qrcode/qrcode.png")
        embedVar = discord.Embed()
        embedVar.set_image(url="attachment://qrcode.png")
        await ctx.send(embed=embedVar, file=file)


def setup(bot):
    bot.add_cog(qrcode_maker(bot))
