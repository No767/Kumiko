import os

import requests
import ujson
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

Refresh_Token = os.getenv("DeviantArt_Refresh_Token")
Client_ID = os.getenv("DeviantArt_Client_ID")
Client_Secret = os.getenv("DeviantArt_Client_Secret")
Auth_Code = os.getenv("DeviantArt_Auth_Code")


class tokenRefresher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(hours=1)
    async def refresher(self):
        link = f"https://www.deviantart.com/oauth2/token?client_id={Client_ID}&client_secret={Client_Secret}&grant_type=refresh_token&refresh_token={Refresh_Token}"
        r = requests.get(link)
        data = ujson.loads(r.text)
        Access_Token = data["access_token"]
        file = open("../.env", "wr")
        line = file.readlines()
        line[32] = f"DeviantArt_Access_Token={Access_Token}\n"
        writer = file.writelines(line)
        writer.close()
