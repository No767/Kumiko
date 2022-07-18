import os
import re
import uuid
from datetime import datetime

import aiormq
import discord
import yaml
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands
from dotenv import load_dotenv
from economy_utils import KumikoAuctionHouseUtils

load_dotenv()
RABBITMQ_USER = os.getenv("RabbitMQ_Username_Dev")
RABBITMQ_PASSWORD = os.getenv("RabbitMQ_Password_Dev")
RABBITMQ_SERVER_IP = os.getenv("RabbitMQ_Server_IP_Dev")


auctionHouseUtils = KumikoAuctionHouseUtils()


async def rabbitPub(price):
    connection = await aiormq.connect(
        f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_SERVER_IP}/"
    )
    channel = await connection.channel()
    await channel.exchange_declare(exchange="auction_house", exchange_type="fanout")
    body = bytes(price, "utf-8")
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
        name: Option(str, "The item that you are putting up for bidding"),
        description: Option(str, "The description of the item"),
        price: Option(int, "The initial price of the item"),
    ):
        """Adds an item to the Auction House"""
        dateAdded = datetime.now().isoformat()
        auctionHouseItemUUID = str(uuid.uuid4())
        userID = ctx.user.id
        filterFile = os.path.join(
            os.path.dirname(__file__), "config", "marketplace_filters.yml"
        )
        try:
            with open(filterFile, "r") as stream:
                try:
                    filterList = yaml.safe_load(stream)
                    mainFilterList = filterList["filters"]
                    mainFilter = re.compile(
                        "|".join([str(item) for item in mainFilterList]), re.IGNORECASE
                    )
                    filteredItemName = re.sub(mainFilter, "item", str(name))
                    filteredItemDescription = re.sub(
                        mainFilter, "item", str(description)
                    )
                    await auctionHouseUtils.addAuctionHouseItem(
                        auctionHouseItemUUID,
                        userID,
                        filteredItemName,
                        filteredItemDescription,
                        dateAdded,
                        price,
                    )
                    await auctionHouseUtils.setItemKey(auctionHouseItemUUID, price)
                    await ctx.respond("Item added to the auction house")
                except yaml.YAMLError:
                    await ctx.respond(
                        "Oops, something went wrong with the yaml file! Please try again."
                    )
        except Exception:
            await ctx.respond(
                embed=discord.Embed(
                    description="Oops, something went wrong! Please try again."
                )
            )


def setup(bot):
    bot.add_cog(AuctionHouseV1(bot))
