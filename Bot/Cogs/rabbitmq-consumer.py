import asyncio
import logging
import os

from aio_pika import ExchangeType, connect
from aio_pika.abc import AbstractIncomingMessage
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


async def on_queue_message(message: AbstractIncomingMessage) -> None:
    async with message.process():
        print(f"[x] {message.body!r}")


class InitRabbitMQConsumer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(ctx):
        connection = await connect(
            f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_SERVER_IP}/"
        )
        async with connection:
            channel = await connection.channel()
            await channel.set_qos(prefetch_count=1)
            auctionHouse = await channel.declare_exchange(
                "auction_house",
                ExchangeType.FANOUT,
            )
            queue = await channel.declare_queue(exclusive=True)
            await queue.bind(auctionHouse)
            await queue.consume(on_queue_message)
            logging.info("Successfully Started RabbitMQ Consumer")
            await asyncio.Future()


def setup(bot):
    bot.add_cog(InitRabbitMQConsumer(bot))
