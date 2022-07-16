import logging
import os

import aiormq
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
RABBITMQ_USER = os.getenv("RabbitMQ_Username_Dev")
RABBITMQ_PASSWORD = os.getenv("RabbitMQ_Password_Dev")
RABBITMQ_SERVER_IP = os.getenv("RabbitMQ_Server_IP_Dev")

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] | %(asctime)s >> %(message)s",
    datefmt="[%m/%d/%Y] [%I:%M:%S %p %Z]",
)


async def rabbitPub(price):
    connection = await aiormq.connect(
        f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_SERVER_IP}/"
    )

    # Creating a channel
    channel = await connection.channel()

    await channel.exchange_declare(exchange="auction_house", exchange_type="fanout")

    body = bytes(price, "utf-8")
    # Sending the message
    await channel.basic_publish(body, routing_key="info", exchange="auction_house")

    await connection.close()


class AuctionHouseV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    auctionHouse = SlashCommandGroup(
        "auction", "Auction off your highest items here", guild_ids=[970159505390325842]
    )

    @auctionHouse.command(name="bid")
    async def bindForPrice(self, ctx, *, price: Option(int, "The price to bid")):
        """Bid for a higher price for an item"""
        await rabbitPub(str(price))
        await ctx.respond(f"bid placed ({price})")

    @auctionHouse.command(name="add")
    async def addItemToAuctionHouse(
        self,
        ctx,
        *,
        name: (str, "The item that you are putting up for bidding"),
        price: (int, "The initial price of the item"),
    ):
        """Adds an item to the Auction House"""


def setup(bot):
    bot.add_cog(AuctionHouseV1(bot))
