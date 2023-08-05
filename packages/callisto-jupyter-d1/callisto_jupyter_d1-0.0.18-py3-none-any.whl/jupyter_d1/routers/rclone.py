import asyncio
import functools
from pathlib import Path
from typing import Any, List

import requests
from asyncblink import signal  # type: ignore
from fastapi import APIRouter, Depends, Request
from fastapi.concurrency import run_in_threadpool

from jupyter_d1.signals import DATA_REMOTES_UPDATE, RCLONE_UPDATE

from ..d1_response import D1Response
from ..deps import write_access
from ..models.data_remote import DataRemote, DataRemoteIn, DataRemotesWrapper
from ..settings import settings

data_remotes: List[DataRemote] = []


router = APIRouter(default_response_class=D1Response)


@router.post("/{api_path:path}", dependencies=[Depends(write_access)])
async def rclone_api(api_path: str, request: Request) -> Any:
    body = await request.body()
    r = await run_in_threadpool(
        requests.post,
        f"http://127.0.0.1:5572/{api_path}",
        params=request.query_params,
        headers=request.headers,
        data=body,
    )
    return r.json()


@router.patch("/data_remotes/", dependencies=[Depends(write_access)])
async def update_data_remotes(data_remotes_in: List[DataRemoteIn]) -> Any:
    new_data_remotes = []
    for dr in data_remotes_in:
        dr_raw = dr.dict()
        path = Path(settings.ROOT_DIR) / Path(f"data/{dr.name}")
        dr_raw["path"] = str(path.resolve())
        new_data_remotes.append(DataRemote(**dr_raw))

    global data_remotes

    if new_data_remotes != data_remotes:
        data_remotes = new_data_remotes
        signal(DATA_REMOTES_UPDATE).send(data_remotes=data_remotes)


@router.get("/data_remotes/", response_model=DataRemotesWrapper)
async def get_data_remotes() -> Any:
    global data_remotes
    return DataRemotesWrapper(data_remotes=data_remotes)


async def dispatch_rclone_stats():
    r = None
    try:
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(
            None,
            functools.partial(
                requests.post, f"http://127.0.0.1:5572/core/stats", timeout=3
            ),
        )
    except Exception:
        pass
    if r is not None:
        signal(RCLONE_UPDATE).send(stats=r.json())


async def stats_periodic():
    while True:
        await dispatch_rclone_stats()
        await asyncio.sleep(settings.RCLONE_STATS_POLLING_INTERVAL)
