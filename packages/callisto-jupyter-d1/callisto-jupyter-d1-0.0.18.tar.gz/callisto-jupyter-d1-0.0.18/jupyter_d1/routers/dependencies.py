import asyncio
from http.client import HTTPException
from typing import Any, Dict, Optional
from uuid import UUID

from asyncblink import signal  # type: ignore
from fastapi import APIRouter, Depends, WebSocket
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from ..d1_response import D1Response
from ..dependency import get_dependency_manager
from ..deps import write_access_websocket
from ..logger import logger
from ..models.dependency import (
    CompleteResponse,
    DependencyCommand,
    FailedResponse,
    ReceivedResponse,
    UpdateResponse,
)
from ..signals import (
    DEPENDENCIES_COMPLETE,
    DEPENDENCIES_FAILED,
    DEPENDENCIES_RECEIVED,
    DEPENDENCIES_UPDATE,
)
from ..storage import kmanager, manager
from ..utils import websocket_send_and_receive

router = APIRouter(default_response_class=D1Response)


def parse_command(
    raw_command: dict[str, Any], msg_queue: asyncio.queues.Queue
) -> Optional[DependencyCommand]:
    try:
        command = DependencyCommand(**raw_command)
        return command
    except ValidationError as e:
        msg_queue.put_nowait(
            FailedResponse(
                request_id=raw_command.get("request_id", "unknown"),
                info=f"Failed to parse command: {jsonable_encoder(e.errors())}",
            )
        )
        return None


@router.websocket("/ws")
async def websocket_dependencies(
    websocket: WebSocket,
    write_access: bool = Depends(write_access_websocket),
    kernel_name: Optional[str] = None,
    notebook_uuid: Optional[UUID] = None,
):
    if notebook_uuid is not None:
        # Get kernel_name for notebook
        kernel_name, kernelspec = manager.get_notebook_kernelspec(
            notebook_uuid
        )

    if kernel_name is None:
        # Use default kernel for the server if one isn't specified
        kernel_name, kernelspec = kmanager.get_default_kernelspec()

    dependency_manager = get_dependency_manager(kernel_name, kernelspec)
    if dependency_manager is None:
        raise HTTPException(
            400, "This kernel does not support dependency management"
        )

    await dependency_manager.connect(websocket)
    await websocket.accept()
    msg_queue: asyncio.queues.Queue = asyncio.queues.Queue()

    request_ids = []

    async def receive_dependencies_received(
        sender: Any,
        request_id: UUID,
        **kwargs,
    ):
        logger.debug("receiving DEPENDENCIES_RECEIVED")
        if request_id in request_ids:
            msg_queue.put_nowait(ReceivedResponse(request_id=request_id))

    signal(DEPENDENCIES_RECEIVED).connect(receive_dependencies_received)

    async def receive_dependencies_update(
        sender: Any,
        request_id: UUID,
        stdout: Optional[str] = None,
        stderr: Optional[str] = None,
        **kwargs,
    ):
        logger.debug("receiving DEPENDENCIES_UPDATE")
        if request_id in request_ids:
            msg_queue.put_nowait(
                UpdateResponse(
                    request_id=request_id, stdout=stdout, stderr=stderr
                )
            )

    signal(DEPENDENCIES_UPDATE).connect(receive_dependencies_update)

    async def receive_dependencies_complete(
        sender: Any,
        request_id: UUID,
        payload: Optional[Dict[str, Any]],
        **kwargs,
    ):
        logger.debug("receiving DEPENDENCIES_COMPLETE")
        if request_id in request_ids:
            msg_queue.put_nowait(
                CompleteResponse(request_id=request_id, payload=payload)
            )
            # request_ids.remove(request_id)

    signal(DEPENDENCIES_COMPLETE).connect(receive_dependencies_complete)

    async def receive_dependencies_failed(
        sender: Any,
        request_id: UUID,
        info: str,
        **kwargs,
    ):
        logger.debug("receiving DEPENDENCIES_FAILED")
        if request_id in request_ids:
            msg_queue.put_nowait(
                FailedResponse(request_id=request_id, info=info)
            )

    signal(DEPENDENCIES_FAILED).connect(receive_dependencies_failed)

    async def on_receive(data):
        command = parse_command(data, msg_queue)
        if command is None:
            return
        request_ids.append(command.request_id)
        command_executed = await dependency_manager.execute(
            command.request_id,
            command.command,
            command.subcommand,
            command.args,
        )
        msg_queue.put_nowait(
            UpdateResponse(
                request_id=command.request_id,
                stdout=command_executed + "\n",
            )
        )

    async def on_disconnect():
        await dependency_manager.disconnect(websocket)

    await websocket_send_and_receive(
        websocket, msg_queue, on_receive, on_disconnect
    )
