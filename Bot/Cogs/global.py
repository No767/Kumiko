import asyncio

import discord
from discord.ext import commands


class Global(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_message(self, message):
        if (
            not message.author.id == self.bot.user.id
            and message.channel.name == "global"
        ):
            # creating the embed
            message_embed = discord.Embed()
            message_embed.set_footer(
                text=f"Sent by {message.author.name} at {message.author.guild.name}",
                icon_url=message.author.avatar_url,
            )

            # if image as link
            if (
                ".gif" in message.content
                or ".png" in message.content
                or ".jpg" in message.content
            ):
                seperated = message.content.split(" ")
                for strip in seperated:
                    if ".gif" in strip or ".png" in strip or ".jpg" in strip:
                        message_embed.set_image(url=strip)
                        break
            else:
                # if user uploaded image
                try:
                    message_embed.set_image(url=message.attachments[0].url)
                except:
                    await asyncio.sleep(0)
            # add message text to embed
            message_embed.description = message.content

            # send the embed to all participants
            for guild in self.bot.guilds:
                for channel in guild.channels:
                    if channel.name == "global" and channel.id != message.channel.id:
                        # if all criteria met then send
                        await channel.send(embed=message_embed)


def setup(bot):
    bot.add_cog(Global(bot))
