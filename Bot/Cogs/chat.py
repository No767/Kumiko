from discord.ext import commands
import discord
import json


class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="chathelp",
        help="The chat is automatically generated based on prewritten responses. Responses that are not documented will be ignored",
    )
    async def chathelp(self, ctx):
        await ctx.send(
            "The chat is automatically generated based on prewritten responses. Responses that are not documented will be ignored"
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            # message has multiple different sub definitions like content author channel
            msg = message.content.lower()
            if msg.startswith(
                "rinupdate"
            ):  # Use rinupdate instead, so if someone is saying update in the chat, this will not trigger
                msg = msg.replace("rinupdate ", "")  # trunicate off update
                inputs = msg.split(",")
                try:
                    msg_responses = dict(ping=inputs[0], pong=inputs[1])
                    response_file = open("chat/responses.json", "a")
                    response_file.write(f"{json.dumps(msg_responses)}\n")
                except Exception as e:
                    await message.channel.send(
                        'The syntax is incorrect. Please type in the format "update [input word], [response]". \nThis will make it so that when a user types [input word], the bot will say [response].'
                    )
                    print(e)
            else:
                try:
                    msg_save = open("chat/responses.json", "r")
                    msg_responses = msg_save.readlines()
                    msg_responses = [
                        json.loads(s.replace("\n", "")) for s in msg_responses
                    ]
                    msg_save.close()
                    for i in msg_responses:
                        if i["ping"] == msg:
                            await message.channel.send(i["pong"])
                            return
                    await message.channel.send(
                        f'Sorry, a response to *"{msg}"* has not yet been added.'
                    )
                except Exception as e:
                    await message.channel.send(e)


def setup(bot):
    bot.add_cog(Chat(bot))
