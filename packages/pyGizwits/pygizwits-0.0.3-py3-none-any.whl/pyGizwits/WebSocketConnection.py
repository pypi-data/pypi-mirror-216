import asyncio
import json
from typing import Dict

from aiohttp import ClientSession, ClientWebSocketResponse, WSMsgType

from pyGizwits.Exceptions import (
    GizwitsAuthException,
    GizwitsException,
    GizwitsIncorrectPasswordException,
    GizwitsOfflineException,
    GizwitsTokenInvalidException,
    GizwitsUserDoesNotExistException,
)
from pyGizwits.pyGizwits import ErrorCodes, logger


class WebSocketConnection:
    def __init__(self, session: ClientSession, GizwitsClient, websocket_info):
        self.client: GizwitsClient = GizwitsClient
        self.session = session
        self.url = (
            websocket_info['pre'] + websocket_info['host'] + ':' + websocket_info['port'] + websocket_info['path']
        )
        self.connection: ClientWebSocketResponse
        self.logged_in: bool = False
        self.subscribed_devices: list[str] = []
        self.ping_interval = 180
        self.ping_task: asyncio.Task = None
        self.receive_messages_task: asyncio.Task = None

    async def add_device_sub(self, did: str):
        """
        Asynchronously adds a new device to the list of subscribed devices.

        Args:
            did (str): The ID of the device to be added.
        Returns:
            The result of the subscription operation
        """
        devices = self.subscribed_devices.copy()
        devices.append(did)
        return await self.subscribe(devices)

    async def connect(self) -> ClientWebSocketResponse:
        """
        Asynchronously connects to the WebSocket server.

        Returns:
            `ClientWebSocketResponse`: a `ClientWebSocketResponse` object representing the connection.
        """
        connection = await self.session.ws_connect(f"{self.url}")
        self.connection = connection
        # Create a background task to receive messages
        self.receive_messages_task = asyncio.ensure_future(self.receive_messages(connection))
        return connection

    async def login(self):
        """
        Logs into the Websocket server.

        This asynchronous function logs in the user by sending a JSON payload to the server.
        The payload includes the user's app ID, UID, token, p0_type, heartbeat interval, and
        auto_subscribe. The function returns nothing.

        Returns:
            None
        """
        connection = self.connection
        if connection is not None:
            payload = {
                "cmd": "login_req",
                "data": {
                    "appid": self.client.app_id,
                    "uid": self.client.uid,
                    "token": self.client.token,
                    "p0_type": "attrs_v4",
                    "heartbeat_interval": self.ping_interval,
                    "auto_subscribe": False,
                },
            }
            await self.send(payload)
            self.ping_task = asyncio.create_task(self._send_ping_periodically())

    async def _send_ping(self) -> None:
        """
        Asynchronously sends a "ping" command to the WebSocket server.

        Returns:
            None
        """
        payload = {
            "cmd": "ping"
        }
        await self.send(payload)

    async def _send_ping_periodically(self):
        while True:
            await self._send_ping()
            await asyncio.sleep(self.ping_interval)

    async def subscribe(self, device_ids: list[str]):
        """
        Asynchronously subscribes to a list of device IDs and sends a 'subscribe_req' command to the server.

        Args:
            device_ids  (list[str]): A list of device IDs to subscribe to.
        Returns:
            None
        """
        payload = {
            "cmd": "subscribe_req", 
            "data": [
                {"did": did} for did in device_ids 
            ]
        }
        await self.send(payload)

    async def receive_messages(self, ws: ClientWebSocketResponse):
        """
        Asynchronously receives messages from a web socket connection.

        Args:
            ws (ClientWebSocketResponse): The web socket connection to receive messages from.
        Returns:
            None
        """
        async for message in ws:
            if message.type == WSMsgType.TEXT:
                await self.handle_message(message.data)
            elif message.type == WSMsgType.BINARY:
                # Handle binary message
                pass
            elif message.type == WSMsgType.CLOSED:
                # Connection closed
                break
            elif message.type == WSMsgType.ERROR:
                # Connection error
                break

    async def handle_message(self, message: str):
        """
        Asynchronously handles incoming messages.

        Args:
            message: A JSON-encoded string representing an incoming message.
        Returns:
            None.
        """
        try:
            data = json.loads(message)
            cmd = data.get('cmd')
            data = data.get('data')
            
            if cmd and data:
                # Handle the command and data accordingly
                if cmd == "login_res":
                    await self.handle_login_response(data)
                elif cmd == "subscribe_res":
                    await self.handle_device_subscribe_response(data)
                elif cmd == "s2c_noti":
                    await self.handle_s2c_notification (data)
                else:
                    logger.debug(f"Received unknown command: {cmd}")
                    pass
            elif cmd == "pong":
                logger.debug(f"Received pong")
            else:
                logger.warn(f"Received invalid message: {message}")
        except json.JSONDecodeError:
            logger.error("Invalid JSON format for the received message.")

    async def handle_login_response(self, data: Dict):
        """
        Asynchronously handles the login response from the server.

        Args:
            data (Dict): A dictionary containing the server's response data.
        Returns:
            None
        """
        if data.get('success') is True:
            logger.debug("Login successful")
            self.logged_in = True

    async def handle_device_subscribe_response(self, data: Dict):
        """
        Asynchronously handles the response of device subscription.

        Args:
            data (Dict): A dictionary containing the response data.
        Returns:
            None
        """
        success_list = data.get("success")
        for success_obj in success_list:
            did = success_obj['did']
            if did not in self.subscribed_devices:
                # Add the unique 'did' to your list
                self.subscribed_devices.append(did)

    async def handle_s2c_notification(self, data: Dict) -> None:
        """
        Asynchronous function that handles a notification sent from server to client.

        Args:
            data: The notification data received from the server.
        Returns:
            None
        """
        await self.client.got_device_status_update(data)

    async def close(self):
        """
        Close the connection to the server. If a ping task is running, cancel it.

        Returns:
            None
        """
        if self.ping_task:
            self.ping_task.cancel()
        if self.receive_messages_task:
            self.receive_messages_task.cancel()
        if self.connection:
            await self.connection.close()
        else:
            logger.warn("Connection already closed.")

    async def send(self, message: json) -> None:
        """
        Asynchronously sends a JSON message over the connection.

        Args:
            message (json): The JSON message to send.
        Returns:
            None
        """
        if self.connection:
            await self.connection.send_json(message)
        else:
            logger.error("Connection closed.")
