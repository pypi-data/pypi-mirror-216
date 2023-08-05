import asyncio
import json
from typing import Any, Awaitable, Callable, Dict, List, Union

import nbformat  # type: ignore
from asyncblink import signal  # type: ignore
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from websockets.exceptions import ConnectionClosedError

from .logger import logger
from .signals import APP_SHUTDOWN

NotebookNode = nbformat.notebooknode.NotebookNode

# The Connection object could really be any object, WebSocket is convenient at
# the moment, could add more with typing.Union
Connection = WebSocket


def add_to_node_metadata(node: NotebookNode, **kwargs):
    if node.metadata.hasattr("jupyter_d1") is False:
        node.metadata.jupyter_d1 = {}
    node.metadata.jupyter_d1.update(kwargs)


def add_to_dict_metadata(someDict, **kwargs):
    if someDict.get("metadata") is None:
        someDict["metadata"] = {}
    metadata = someDict["metadata"]

    if metadata.get("jupyter_d1") is None:
        metadata["jupyter_d1"] = {}
    jupyter_d1 = metadata["jupyter_d1"]

    jupyter_d1.update(kwargs)


class BoolObject:
    def __init__(self, value=False):
        self.value = value

    def __bool__(self):
        return self.value


async def websocket_poll(websocket: WebSocket, msgs: List[str]):
    # use an object to communicate across coroutines
    connected = BoolObject(value=True)

    async def shutdown_listener(*args, **kwargs):
        connected.value = False

    signal(APP_SHUTDOWN).connect(shutdown_listener)

    while connected:
        await asyncio.sleep(0.1)
        if len(msgs) != 0:
            msg = msgs.pop(0)
            try:
                await websocket.send_text(msg)
            except ConnectionClosedError:
                logger.debug("client closed connection to websocket service")
                connected.value = False

    await websocket.close()


async def websocket_send_and_receive(
    websocket: WebSocket,
    msg_queue: asyncio.queues.Queue,
    on_receive: Callable[[Dict[str, Any]], Union[Awaitable[None], None]],
    on_disconnect: Callable[[], Union[Awaitable[None], None]] = None,
):

    task_list = []

    async def read_from_socket(websocket: WebSocket):
        async for data in websocket.iter_json():
            if asyncio.iscoroutinefunction(on_receive):
                task = asyncio.create_task(on_receive(data))
                task_list.append(task)
            else:
                on_receive(data)

    async def send_data():
        while True:
            data = await msg_queue.get()
            payload = json.dumps(jsonable_encoder(data))
            await websocket.send_text(payload)

    try:
        await asyncio.gather(read_from_socket(websocket), send_data())
    except WebSocketDisconnect:
        for task in task_list:
            task.cancel()
        if on_disconnect is not None:
            if asyncio.iscoroutinefunction(on_disconnect):
                await on_disconnect()
            else:
                on_disconnect()
