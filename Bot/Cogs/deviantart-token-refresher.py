import asyncio
import datetime
import os
import time

import aiohttp
import ujson
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

Refresh_Token = os.getenv("DeviantArt_Refresh_Token")
Client_ID = os.getenv("DeviantArt_Client_ID")
Client_Secret = os.getenv("DeviantArt_Client_Secret")
Access_Token = os.getenv("DeviantArt_Access_Token")
os.chmod("../.env", 777)


class tokenRefresher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.index = 0
        self.refresher.start()

    @tasks.loop()
    async def refresher(self):
        self.index = self.index + 1
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        await asyncio.sleep(5)
        async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
            params = {
                "client_id": f"{Client_ID}",
                "client_secret": f"{Client_Secret}",
                "grant_type": "refresh_token",
                "refresh_token": f"{Refresh_Token}",
            }
            async with session.get(
                "https://www.deviantart.com/oauth2/token", params=params
            ) as r:
                data = await r.json()
                access_token = data["access_token"]
                refresh_token = data["refresh_token"]
                print(
                    f"Current DA Access Token: {Access_Token}\nCurrent DA Refresh Token: {Refresh_Token}"
                )
                print(
                    f"----------DeviantArt Token Refresher - Request #{self.index} - {st}-----------------\n"
                )
                print(f"{data}\n")
                print(f"New DeviantArt Access Token: {access_token}\n")
                print(f"New DeviantArt Refresh Token: {refresh_token}\n")
                print(
                    "----------------------------------------------------------------------------\n"
                )
                await asyncio.sleep(5)
                async with open("../.env", "r+") as file:
                    file_data = await file.readlines()
                    file_data[37] = f'DeviantArt_Access_Token = "{access_token}"\n'
                    file_data[38] = f'DeviantArt_Refresh_Token = "{refresh_token}"\n'
                    await file.write(file_data[37])
                    await file.write(file_data[38])
                print(
                    f"Newly Added Access Token: {file_data[37]}\nNewly Added Refresh Token: {file_data[38]}"
                )


#    @refresher.error
#    async def refresher_error(self):
#        start_link = f"https://www.deviantart.com/oauth2/authorize?response_type=code&client_id={Client_ID}&redirect_uri=https://github.com/No767/Rin&scope=user browse collection gallery"
#        r = requests.get(start_link)
#        print(r.history)


def setup(bot):
    bot.add_cog(tokenRefresher(bot))
