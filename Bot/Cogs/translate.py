import discord
from deep_translator import GoogleTranslator
from discord.ext import commands


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="translate", help="Translates the given message", pass_context=True
    )
    async def translate(self, ctx):
        try:

            def check(ms):
                return (
                    ms.channel == ctx.message.channel
                    and ms.author == ctx.message.author
                )

            await ctx.send("Enter the message you wish to be translated:")
            msg = await self.bot.wait_for("message", check=check)
            await ctx.send("Enter which language you wish to have this translated in:")
            lang = await self.bot.wait_for("message", check=check)
            translatev2 = GoogleTranslator(
                source="auto", target=lang.content
            ).translate(text=str(msg.content).lower())
            translate_embed = discord.Embed(description=translatev2)
            translate_embed.set_footer(
                text=f"Requested by {ctx.message.author.name}",
                icon_url=ctx.message.author.avatar_url,
            )
            await ctx.send(embed=translate_embed)
        except Exception as e:
            await ctx.send(f"The query failed.\nReason: {e}")


def setup(bot):
    bot.add_cog(Utility(bot))
