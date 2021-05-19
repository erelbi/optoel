from channels.generic.websocket import AsyncJsonWebsocketConsumer


class NoseyConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("notifiy", self.channel_name)
        print(f"Added {self.channel_name} channel to notifiy")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notifiy", self.channel_name)
        print(f"Removed {self.channel_name} channel to notifiy")

    async def send_notifiy(self, event):
        await self.send_json(event)
        print(f"Got message {event} at {self.channel_name}")