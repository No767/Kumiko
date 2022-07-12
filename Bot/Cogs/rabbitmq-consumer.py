import asyncio
import logging
import os

import aiormq
import aiormq.types
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


async def on_queue_message(message: aiormq.types.DeliveredMessage) -> None:
    logging.info("[x] %r" % (message.body,))

    await message.channel.basic_ack(message.delivery.delivery_tag)


class RabbitMQConsumerProcess:
    def __init__(self):
        self.self = self

    async def mainProc(self):
        """The main process of the RabbitMQ consumer"""
        connection = await aiormq.connect(
            f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_SERVER_IP}/"
        )
        channel = await connection.channel()
        await channel.basic_qos(prefetch_count=1)
        await channel.exchange_declare(exchange="auction_house", exchange_type="fanout")
        declareAuctionHouseQueue = await channel.queue_declare(exclusive=True)
        await channel.queue_bind(declareAuctionHouseQueue.queue, "auction_house")
        await channel.basic_consume(declareAuctionHouseQueue.queue, on_queue_message)


class InitRabbitMQConsumer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(ctx):
        mainProcesses = RabbitMQConsumerProcess()
        task = asyncio.create_task(mainProcesses.mainProc(), name="RabbitMQConsumer")
        background_tasks = set()
        background_tasks.add(await task)
        task.add_done_callback(background_tasks.discard)
        logging.info("Successfully started RabbitMQ consumer")


def setup(bot):
    bot.add_cog(InitRabbitMQConsumer(bot))
