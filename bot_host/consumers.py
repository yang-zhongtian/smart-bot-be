import asyncio
import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from bot_host.models import Host
from .utils import analyze_face

host_group_prefix = "host_"
cam_group_prefix = "cam_"
command_group_prefix = "command_"
analyze_group_prefix = "analyze_"


class HostConsumer(AsyncWebsocketConsumer):
    host_id = None
    host_group_name = None

    async def connect(self):
        self.host_id = self.scope["url_route"]["kwargs"]["host_id"]
        self.host_group_name = f"{host_group_prefix}{self.host_id}"

        await self.channel_layer.group_add(self.host_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.host_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        if not 1 <= len(data) <= 2:
            return

        command = data[0]

        if command in ('videoStream', 'led', 'capture'):
            await self.channel_layer.group_send(
                cam_group_prefix + self.host_id,
                {"type": "send.command", "data": text_data}
            )
            return

        if command in ('monitor', 'autoAvoidance', 'forward', 'backward', 'turnLeft', 'turnRight', 'stand'):
            await self.channel_layer.group_send(
                command_group_prefix + self.host_id,
                {"type": "send.command", "data": text_data}
            )
            return

        print(command)

    async def tx_video(self, event):
        await self.send(bytes_data=event["data"])

    async def tx_command(self, event):
        print(event)
        await self.send(text_data=event["data"])


class ClientCamConsumer(AsyncWebsocketConsumer):
    host_id = None
    cam_group_name = None

    async def connect(self):
        self.host_id = self.scope["url_route"]["kwargs"]["host_id"]
        self.cam_group_name = f"{cam_group_prefix}{self.host_id}"

        await self.channel_layer.group_add(self.cam_group_name, self.channel_name)
        await self.accept()
        async for bot in Host.objects.filter(id=self.host_id):
            bot.status_cam = True
            await bot.asave(update_fields=["status_cam"])

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.cam_group_name, self.channel_name)
        async for bot in Host.objects.filter(id=self.host_id):
            bot.status_cam = False
            await bot.asave(update_fields=["status_cam"])

    async def receive(self, _=None, bytes_data=None):
        if bytes_data:
            await self.channel_layer.group_send(
                host_group_prefix + self.host_id,
                {"type": "tx.video", "data": bytes_data}
            )

    async def send_command(self, event):
        await self.send(text_data=event["data"])


class ClientCommandConsumer(AsyncWebsocketConsumer):
    host_id = None
    command_group_name = None

    async def connect(self):
        self.host_id = self.scope["url_route"]["kwargs"]["host_id"]
        self.command_group_name = f"{command_group_prefix}{self.host_id}"

        await self.channel_layer.group_add(self.command_group_name, self.channel_name)
        await self.accept()
        async for bot in Host.objects.filter(id=self.host_id):
            bot.status_command = True
            await bot.asave(update_fields=["status_command"])

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.command_group_name, self.channel_name)
        async for bot in Host.objects.filter(id=self.host_id):
            bot.status_command = False
            await bot.asave(update_fields=["status_command"])

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        if not 1 <= len(data) <= 2:
            return

        command = data[0]

        match command:
            case 'servo':
                await self.channel_layer.group_send(
                    host_group_prefix + self.host_id,
                    {"type": "tx.command", "data": text_data}
                )
            case 'obstacle':
                await self.channel_layer.group_send(
                    cam_group_prefix + self.host_id,
                    {"type": "send.command", "data": '["capture"]'}
                )
                await self.channel_layer.group_send(
                    host_group_prefix + self.host_id,
                    {"type": "tx.command", "data": text_data}
                )

    async def send_command(self, event):
        await self.send(text_data=event["data"])


class ClientAnalyzeConsumer(AsyncWebsocketConsumer):
    host_id = None
    analyze_group_name = None

    async def connect(self):
        self.host_id = self.scope["url_route"]["kwargs"]["host_id"]
        self.analyze_group_name = f"{analyze_group_prefix}{self.host_id}"

        await self.channel_layer.group_add(self.analyze_group_name, self.channel_name)
        await self.accept()
        async for bot in Host.objects.filter(id=self.host_id):
            bot.status_analyze = True
            await bot.asave(update_fields=["status_analyze"])

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.analyze_group_name, self.channel_name)
        async for bot in Host.objects.filter(id=self.host_id):
            bot.status_analyze = False
            await bot.asave(update_fields=["status_analyze"])

    async def receive(self, text_data=None, bytes_data=None):
        result = await sync_to_async(analyze_face)(self.host_id, bytes_data)
        if result:
            await asyncio.sleep(5)
        await self.channel_layer.group_send(
            command_group_prefix + self.host_id,
            {"type": "send.command", "data": '["continue"]'}
        )
