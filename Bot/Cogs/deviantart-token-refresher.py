import os

import requests
import ujson
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

Refresh_Token = os.getenv("DeviantArt_Refresh_Token")
Client_ID = os.getenv("DeviantArt_Client_ID")
Client_Secret = os.getenv("DeviantArt_Client_Secret")


class tokenRefresher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.refresher.start()

    @tasks.loop(minutes=30)
    async def refresher(self):
        link = f"https://www.deviantart.com/oauth2/token?client_id={Client_ID}&client_secret={Client_Secret}&grant_type=refresh_token&refresh_token={Refresh_Token}"
        r = requests.get(link)
        data = ujson.loads(r.text)
        access_token = data["access_token"]
        refresh_token = data["refresh_token"]
        line = open("../.env", "r").readlines()
        line[34] = f'DeviantArt_Access_Token = "{access_token}"\n'
        line[35] = f'DeviantArt_Refresh_Token = "{refresh_token}"\n'
        file2 = open("../.env", "w+")
        file2.writelines(line)
        file2.close()


def setup(bot):
    bot.add_cog(tokenRefresher(bot))
