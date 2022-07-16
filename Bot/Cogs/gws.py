import asyncio
import os

import discord
import uvloop
from discord.commands import SlashCommandGroup
from discord.ext import commands, pages


class KumikoGWSBanners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    gws = SlashCommandGroup(
        "gws", "Commands for Kumiko's Genshin Wish Sim", guild_ids=[970159505390325842]
    )
    gwsEvents = gws.create_subgroup(
        "events",
        "Commands for Kumiko's Genshin Wish Sim",
        guild_ids=[970159505390325842],
    )

    @gwsEvents.command(name="available")
    async def getGWSEventsBanner(self, ctx):
        """Lists out all available events"""
        curPath = os.path.dirname(__file__)
        listDirItems = os.listdir(os.path.join(curPath, "Kumiko-GWS-Banners"))
        mainPages = pages.Paginator(
            pages=[
                discord.Embed().set_image(
                    url=f'https://raw.githubusercontent.com/No767/Kumiko/dev/Bot/Cogs/Kumiko-GWS-Banners/{str(items).replace("[", "").replace("]", "")}'
                )
                for items in listDirItems
            ],
            loop_pages=True,
        )
        await mainPages.respond(ctx.interaction, ephemeral=False)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(KumikoGWSBanners(bot))
