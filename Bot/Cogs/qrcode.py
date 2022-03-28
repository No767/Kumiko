import asyncio
import os

import discord
import discord.ext
import qrcode
import uvloop
from discord.commands import slash_command
from discord.ext import commands


class qrcode_maker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="qrcode",
        description="Creates a QR Code based on given input",
        guild_ids=[866199405090308116],
    )
    async def code(self, ctx, *, link: str):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        if str(os.path.isfile("/qrcode/qrcode.png")) == "False":
            img = qrcode.make(link)
            img.save("./qrcode/qrcode.png")
        else:
            img = qrcode.make(link)
            img.save("./qrcode/qrcode.png")
        file = discord.File("./qrcode/qrcode.png")
        embedVar = discord.Embed()
        embedVar.set_image(url="attachment://qrcode.png")
        await ctx.respond(embed=embedVar, file=file)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(qrcode_maker(bot))
