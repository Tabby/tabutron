import boto3
import discord
import asyncio
import datetime

client = discord.Client()
with open("token.txt", "r") as token_file:
    token = token_file.read()

purge_channel_ids = {"503927900790063114", "503928427049385994", "503926807892852736", "503928190578720778"}
output_channel_id = "491405337341984769"

def is_not_pinned(m: discord.Message):
    return (not m.pinned)

async def main():
    await client.login(token)
    asyncio.ensure_future(client.connect())
    await client.wait_until_ready()

    out_channel = client.get_channel(output_channel_id)
    before_date = datetime.datetime.now() - datetime.timedelta(weeks=2)
    for id in purge_channel_ids:
        channel = client.get_channel(id)
        messages = client.logs_from(channel, limit=100000, before=before_date)
        count = 0
        async for m in messages:
            if is_not_pinned(m):
                count += 1
                await client.delete_message(m)
        if count > 0:
            await client.send_message(out_channel, "{} messages deleted from {}".format(count, channel.name))
    await client.logout()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()