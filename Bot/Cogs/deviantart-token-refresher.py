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

    @tasks.loop(seconds=5)
    async def refresher(self):
        link = f"https://www.deviantart.com/oauth2/token?client_id={Client_ID}&client_secret={Client_Secret}&grant_type=refresh_token&refresh_token={Refresh_Token}"
        r = requests.get(link)
        data = ujson.loads(r.text)
        access_token = data["access_token"]
        refresh_token = data["refresh_token"]
        file = open("../.env", "r")
        file_data = file.readlines()
        file_data[37] = f'DeviantArt_Access_Token = "{access_token}"\n'
        file_data[38] = f'DeviantArt_Refresh_Token = "{refresh_token}"\n'
        file.close()
        file = open("../.env", "w")
        file.writelines(file_data)
        file.close()


def setup(bot):
    bot.add_cog(tokenRefresher(bot))
