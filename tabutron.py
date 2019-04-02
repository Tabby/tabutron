import boto3
import discord
import asyncio
import datetime
import logging
from sys import stdout
from os import environ

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

client = discord.Client()
token = environ['DISCORD_API_KEY']

TWO_WEEKS_AGO = datetime.timedelta(weeks=2)
ONE_DAY_AGO = datetime.timedelta(days=1)
purge_channel_ids = [
    ("503927900790063114", TWO_WEEKS_AGO), #sfw-18
    ("503928427049385994", TWO_WEEKS_AGO), #nsfw-18
    ("503926807892852736", TWO_WEEKS_AGO), #kink-18
    ("503928190578720778", TWO_WEEKS_AGO), #nsfw-media
    ("562252547541434370", ONE_DAY_AGO)    #daily-venting
]
output_channel_id = "491405337341984769"

def is_not_pinned(m: discord.Message):
    return (not m.pinned)

async def main():
    await client.login(token)
    asyncio.ensure_future(client.connect())
    await client.wait_until_ready()

    out_channel = client.get_channel(output_channel_id)
    now = datetime.datetime.now()
    logger.info("Logged in and running ^_^")
    for id, delta in purge_channel_ids:
        before_date = now - delta
        channel = client.get_channel(id)
        logger.info("Checking #{}".format(channel.name))
        messages = client.logs_from(channel, limit=100000, before=before_date)
        logger.info("Got messages, deleting unpinned ones older than {}".format(before_date))
        count = 0
        total = 0
        async for m in messages:
            total += 1
            if is_not_pinned(m):
                count += 1
                await client.delete_message(m)
        logger.info("{} messages found in #{}({}), {} deleted".format(total, channel.name, id, count))
        if count > 0:
            await client.send_message(out_channel, "{} messages deleted from {}".format(count, channel.name))
    await client.logout()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()