import json
from typing import Any

from asyncblink import signal  # type: ignore
from fastapi import APIRouter, Depends, WebSocket
from fastapi.encoders import jsonable_encoder

from ..d1_response import D1Encoder
from ..deps import read_access_websocket, write_access
from ..models.environment_info import (
    EnvironmentInfoWrapper,
    Version,
    VersionWrapper,
)
from ..models.server_stats import ServerStatsListWrapper, ServerStatsWrapper
from ..signals import (
    APP_LOG,
    DATA_REMOTES_UPDATE,
    NOTEBOOKS_UPDATED,
    RCLONE_UPDATE,
    SERVER_STATS_UPDATE,
    WATCHDOG_FILE_SYSTEM_EVENT,
)
from ..storage import environment_dump, stats_manager
from ..utils import websocket_poll
from ..version import version_dict
from ..settings import settings
from ..models.token import MothershipAuthToken

router = APIRouter()


@router.get("/version", response_model=VersionWrapper)
def get_server_version() -> Any:
    """
    Get D1 server version number
    """
    return VersionWrapper(version=Version(**version_dict))


@router.get("/stats", response_model=ServerStatsListWrapper)
def get_server_stats(limit: int = 100, skip: int = 0) -> Any:
    """
    Get server stats about memory, cpu, disk, and gpu
    """
    stats = stats_manager.get_stats(skip, skip + limit)
    return ServerStatsListWrapper(server_stats=stats)


@router.get("/latest_stats", response_model=ServerStatsWrapper)
def get_latest_server_stats(limit: int = 100, skip: int = 0) -> Any:
    """
    Get latest server stats about memory, cpu, disk, and gpu
    """
    latest_stats = stats_manager.get_latest()
    return ServerStatsWrapper(server_stats=latest_stats)


@router.websocket("/ws")
async def server_stats_websocket(
    websocket: WebSocket, read_access: bool = Depends(read_access_websocket)
):
    await websocket.accept()
    msgs = []

    async def receive_notebooks_updated(sender, notebooks, **kwargs):
        nb_dicts = [
            {"uuid": nb_uuid, "name": nb.metadata.jupyter_d1.name}
            for (nb_uuid, nb) in notebooks.items()
        ]
        wrapper_dict = {"notebooks": nb_dicts}
        json_string = json.dumps(wrapper_dict, cls=D1Encoder)
        msgs.append(json_string)

    signal(NOTEBOOKS_UPDATED).connect(receive_notebooks_updated)

    async def receive_rclone_update(sender, stats, **kwargs):
        wrapper_dict = {"rclone_stats": stats}
        json_string = json.dumps(wrapper_dict, cls=D1Encoder)
        msgs.append(json_string)

    signal(RCLONE_UPDATE).connect(receive_rclone_update)

    async def receive_watchdog_event(
        sender, event_type, src_path, dest_path, **kwargs
    ):
        wrapper_dict = {
            "watchdog_event": {
                "event_type": event_type,
                "src_path": src_path,
                "dest_path": dest_path,
            }
        }
        json_string = json.dumps(wrapper_dict, cls=D1Encoder)
        msgs.append(json_string)

    signal(WATCHDOG_FILE_SYSTEM_EVENT).connect(receive_watchdog_event)

    async def receive_server_stats(sender, server_stats, **kwargs):
        wrapper_dict = {"server_stats": server_stats.dict()}
        json_string = json.dumps(wrapper_dict, cls=D1Encoder)
        msgs.append(json_string)

    signal(SERVER_STATS_UPDATE).connect(receive_server_stats)

    async def receive_app_log(sender, msg, **kwargs):
        wrapper_dict = {"log": msg}
        json_string = json.dumps(wrapper_dict, cls=D1Encoder)
        msgs.append(json_string)

    signal(APP_LOG).connect(receive_app_log)

    async def receive_data_remotes_update(sender, data_remotes, **kwargs):
        wrapper_dict = {
            "data_remotes_update": {
                "data_remotes": jsonable_encoder(data_remotes)
            }
        }
        json_string = json.dumps(wrapper_dict, cls=D1Encoder)
        msgs.append(json_string)

    signal(DATA_REMOTES_UPDATE).connect(receive_data_remotes_update)

    await websocket_poll(websocket, msgs)


@router.get("/environment", response_model=EnvironmentInfoWrapper)
def get_environment() -> Any:
    """
    Get environment info
    """
    environment_info = environment_dump.dump_environment()
    return EnvironmentInfoWrapper(environment_info=environment_info)


@router.post("/mothership_auth_token", dependencies=[Depends(write_access)])
def get_set_mothership_auth_token(token: MothershipAuthToken) -> Any:
    """
    Set mothership auth token
    """
    settings.mothership_auth_token = token.access_token
