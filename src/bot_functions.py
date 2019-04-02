import datetime

TWO_WEEKS_AGO = datetime.timedelta(weeks=2)
ONE_DAY_AGO = datetime.timedelta(days=1)
purge_channel_ids = [
    ("503927900790063114", TWO_WEEKS_AGO), #sfw-18
    ("503928427049385994", TWO_WEEKS_AGO), #nsfw-18
    ("503926807892852736", TWO_WEEKS_AGO), #kink-18
    ("503928190578720778", TWO_WEEKS_AGO), #nsfw-media
    ("562252547541434370", ONE_DAY_AGO)    #daily-venting
]

async def purge_channels(logger, client, now):
    for channel_id, delta in purge_channel_ids:
        before_date = now - delta
        channel = client.get_channel(channel_id)

        logger.info("Checking #{}".format(channel.name))
        messages = client.logs_from(channel, limit=100000, before=before_date)

        logger.info("Got messages, deleting unpinned ones older than {}".format(before_date))
        deleted_messages = 0
        total_messages = 0
        async for message in messages:
            total_messages += 1
            if (not message.pinned):
                deleted_messages += 1
                await client.delete_message(message)

        logger.info("{} messages found in #{}({}), {} deleted".format(total_messages, channel.name, channel_id, deleted_messages))
        if deleted_messages > 0:
            logger.warn("{} messages deleted from {}".format(deleted_messages, channel.name))