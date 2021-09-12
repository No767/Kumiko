from discord.ext import commands
import discord
from deep_translator import GoogleTranslator
#made with https://github.com/nidhaloff/deep-translator
class Utility(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(
        name='translate',
        help='Translates the given message',
        pass_context=True
        )
    async def translate(self, ctx):
        def check(ms):
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author
        await ctx.send('Enter the message you wish to be translated:')
        msg = await self.bot.wait_for('message', check=check)
        translated = GoogleTranslator(source='auto', target='english').translate(msg.content)
        translate_embed = discord.Embed(
            title='Translation',
            description=translated
        )
        translate_embed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        await ctx.send(embed=translate_embed)

def setup(bot):
    bot.add_cog(Utility(bot))
