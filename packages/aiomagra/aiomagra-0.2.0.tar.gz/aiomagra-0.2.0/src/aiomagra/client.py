import asyncio
import pprint
from typing import Callable

import aiohttp
from aiohttp import WSMsgType
import async_timeout

from .const import LOGGER
from .metadata_pb2 import DeviceMetadata
from .pubsub_pb2 import (
    REPLY_TYPE_ERROR,
    REQUEST_TYPE_DATA,
    CommandReply,
    CommandReplyData,
    CommandRequest,
    CommandRequestData,
)
from .structure_pb2 import (
    StructureRequest,
    StructureResponse,
)
from .websocket_pb2 import WebsocketMessage


class Client:
    def __init__(
        self, host: str, session: aiohttp.ClientSession, on_close: Callable
    ) -> None:
        self._host = host
        self.session = session
        self._calls: dict[int, Call] = {}
        self._call_id = 0
        self._consumers = []
        self.on_close = on_close

    @property
    def _next_id(self) -> int:
        self._call_id += 1
        return self._call_id

    async def connect(self):
        LOGGER.debug("Trying to connect to device at %s", self._host)
        self._client = await self.session.ws_connect(
            f"http://{self._host}/rpc", autoping=False
        )
        self._rx_task = asyncio.create_task(self._rx_msgs())
        LOGGER.info("Connected to %s", self._host)

    async def _rx_msgs(self) -> None:
        while not self._client.closed:
            msg = await self._client.receive()
            LOGGER.info("Received msg (%s): %s", self._host, msg)

            if not self._client.closed:
                m = WebsocketMessage()
                m.ParseFromString(msg.data)

                pp = pprint.PrettyPrinter(indent=4)
                LOGGER.info("MSG: %s", pp.pprint(m))

                if m.frame_id > 0:
                    if m.frame_id not in self._calls:
                        LOGGER.warning(
                            "Response for an unknown request id: %s", m.frame_id
                        )
                        return
                    call = self._calls.pop(m.frame_id)
                    if not call.resolve.cancelled():
                        call.resolve.set_result(m.reply)
                else:
                    for consumer in self._consumers:
                        consumer(m.gateway_report)

        LOGGER.debug("Websocket client connection from %s closed", self._host)

        for call_item in self._calls.values():
            if not call_item.resolve.done():
                call_item.resolve.set_exception(Exception())
        self._calls.clear()

        if not self._client.closed:
            await self._client.close()

        self._client = None
        self.on_close()

    async def add_consumer(self, consumer):
        self._consumers.append(consumer)

    async def close(self):
        if self._rx_task:
            self._rx_task.cancel()
        if self._client:
            await self._client.close()

    async def get_structure(self) -> StructureResponse:
        data = CommandRequestData()
        data.GetStructure.CopyFrom(StructureRequest())
        reply = await self._call("Structure/GetStructure", data)
        return reply.GetStructure

    async def switch_on(self, device_id: bytes) -> None:
        data = CommandRequestData()
        data.SwitchOn.metadata.CopyFrom(self._metadata(device_id))
        await self._call("Switch/SwitchOn", data)

    async def switch_off(self, device_id: bytes) -> None:
        data = CommandRequestData()
        data.SwitchOff.metadata.CopyFrom(self._metadata(device_id))
        await self._call("Switch/SwitchOff", data)

    async def _call(
        self, method: str, data: CommandRequestData, timeout: int = 10
    ) -> CommandReplyData:
        call = Call(self._next_id, method, data)
        self._calls[call.frame_id] = call
        LOGGER.debug("%s: send request", call.frame_id)
        try:
            async with async_timeout.timeout(timeout):
                await call.send_request(self._client)
                reply: CommandReply = await call.resolve
        except asyncio.TimeoutError as exc:
            LOGGER.debug("%s: call timeout", call.frame_id)
            call.resolve.cancel()
            await call.resolve
            raise exc
        except ConnectionResetError as exc:
            LOGGER.debug("%s: connection reset", call.frame_id)
            raise exc

        LOGGER.debug("%s: %s -> %s", call.frame_id, call.method, reply)
        if reply.type == REPLY_TYPE_ERROR:
            raise Exception(reply.error.message)

        return reply.data

    def _metadata(self, device_id: bytes) -> DeviceMetadata:
        metadata = DeviceMetadata()
        metadata.mqtt.device_id = device_id
        return metadata


class Call:
    def __init__(self, frame_id, method: str, data: CommandRequestData) -> None:
        self.frame_id = frame_id
        self.method = method
        self.data = data
        self.resolve: asyncio.Future = asyncio.Future()

    async def send_request(self, client: Client):
        req = CommandRequest()
        req.method = self.method
        req.type = REQUEST_TYPE_DATA
        req.data.CopyFrom(self.data)
        msg = WebsocketMessage()
        msg.frame_id = self.frame_id
        msg.request.CopyFrom(req)
        await client.send_bytes(msg.SerializeToString())
