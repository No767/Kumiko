import discord
from discord.ext import commands

class rinhelp(commands.Cog):        
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="rinhelp")
    async def rinhelp(self, ctx):
        bot = self.bot
        name = bot.user.name
        id = bot.user.id
        embedVar = discord.Embed(title="Rin Help", color=14414079)
        embedVar.description = f'''
        **NOTE**: Currently the amount of commands are not complete, hence why this is in alpha. 
        
        Full List of Cmds (including ones from EasyBot.py):
        
        - .rinhelp

        - .rininfo

        - .valid

        - .ping 
        
        - .rintwitter

        - .meme (from EasyBot.py)

        - .reddit (from EasyBot.py)

        - .devartfind (**NOT COMPLETE YET**)

        - .devartsearch (**NOT COMPLETE YET**)

        - .image (from EasyBot.py)

        - .invite (from EasyBot.py)

        - .botinfo (from EasyBot.py)

        - .translate (from EasyBot.py, missing lib)

        - .botgrowth

        - .prune

        - .broadcast

        - .makeyourownbot
        
        More are still to come...
        '''
        embedVar.set_thumbnail(url=bot.user.avatar_url)
        await ctx.send(embed=embedVar)

def setup(bot):
    bot.add_cog(rinhelp(bot))