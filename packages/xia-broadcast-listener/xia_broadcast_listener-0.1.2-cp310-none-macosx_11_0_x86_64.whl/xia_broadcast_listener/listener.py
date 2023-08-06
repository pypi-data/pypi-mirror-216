import json
import logging
import websockets
import asyncio
from xia_fields import StringField, OsEnvironField
from xia_engine import EmbeddedDocument


class ConnectionHeader(EmbeddedDocument):
    app_name: str = StringField(description="Application Name")
    api_key: bytes = OsEnvironField(description="Application API Key Value")


class BroadcastListener:
    """Listener to Broadcast"""
    def __init__(self, uri: str, header: dict, channel_config: dict):
        self.uri = uri
        self.header = ConnectionHeader.from_db(**header)
        self.channel_config = channel_config

    async def connect(self, on_open, on_error, on_close, id_only: bool = False):
        """Connect to websocket server

        Args:
            on_open: Callback when connection is open
            on_close: Callback when connection is closes
            on_error: Callback when error occurs
            id_only: Only get document id in the message body
        """
        header_info = self.header.get_display_data(lazy=False)
        handshake_info = {
            "_header": {
                "X-App-Name": header_info["app_name"],
                "X-Api-Key": header_info["api_key"],
            },
        }
        handshake_info.update(self.channel_config)
        if id_only:
            for key, value in self.channel_config.items():
                if key not in self.channel_config:
                    continue
                self.channel_config[key]["catalog"] = {"_id": None}
        while True:
            try:
                async with websockets.connect(self.uri, open_timeout=30) as websocket:
                    await websocket.send(json.dumps(handshake_info, ensure_ascii=False))
                    confirmation = await websocket.recv()
                    logging.info(f"Websocket Server: {self.uri} connected")
                    logging.debug(confirmation)
                    on_open()  # Call back when connection is opened
                    yield websocket
            except websockets.ConnectionClosedError as e:
                on_close(1001, "")  # Call back when connection is closed
                continue  # Auto-Reconnection
            except websockets.InvalidStatusCode as e:
                on_close(4000+e.args[0], "")  # Call back when connection is closed
                if e.args[0] == 429:
                    # HTTP Too many connection error, retry in 1 second
                    await asyncio.sleep(1)
                    continue  # Auto-Retry
                else:
                    on_error(websocket, e)  # Call back when connection meets error
                    break
            except asyncio.exceptions.IncompleteReadError:
                on_close(1006, "IncompleteReadError")  # Call back when connection is closed
                continue  # It is a temporary disconnect
            except RuntimeError:  # Parent process is ended. No need to continue
                # on_close(1006, "Parent process is ended")
                break
            except Exception as e:
                on_error(e)
                break

    async def listen(self, on_open, on_message, on_error, on_close, id_only: bool = False):
        """Get message from broadcast

        Args:
            on_open: Callback when connection is open
            on_message: The callback function (sync), accept message as output
            on_close: Callback when connection is closes
            on_error: Callback when error occurs
            id_only: Only get document id in the message body

        Returns:
            None
        """
        async for websocket in self.connect(on_open, on_error, on_close, id_only=id_only):
            while True:
                message = await websocket.recv()
                on_message(json.loads(message))
                await asyncio.sleep(0)
