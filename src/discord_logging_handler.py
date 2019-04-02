from logging import StreamHandler

class DiscordLoggingHandler(StreamHandler):

    def __init__(self, client, output_channel_id):
        StreamHandler.__init__(self)
        self.client = client
        self.output_channel = client.get_channel(output_channel_id)

    async def emit(self, record):
        msg = self.format(record)
        await self.client.send_message(self.output_channel, msg)