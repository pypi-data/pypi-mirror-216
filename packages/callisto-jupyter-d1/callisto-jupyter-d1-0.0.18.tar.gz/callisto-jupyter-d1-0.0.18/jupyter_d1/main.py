import asyncio
import logging
import sys
from typing import Optional

from asyncblink import signal  # type: ignore
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.wsgi import WSGIMiddleware
from starlette.responses import JSONResponse
from uvicorn.main import Server  # type: ignore

from jupyter_d1.signals import APP_LOG, APP_SHUTDOWN, APP_STARTUP

from .d1_response import D1Response
from .dav import dav, dav_manager
from .deps import read_access
from .logger import logger
from .routers import (
    convert,
    dependencies,
    hello,
    kernels,
    login,
    notebooks,
    rclone,
    server,
)
from .settings import settings
from .storage import kmanager, stats_manager
from .storage.notebook_manager import NBMException

# Monkey patch the uvicorn exit handler. The standard
# uvicorn 'shutdown' event comes too late to properly
# shutdown active websockets. There are no other hooks
# so this is the only way to do so.
# See https://stackoverflow.com/a/59887076/436040
uvicorn_handle_exit = Server.handle_exit


def handle_exit(self, *args, **kwargs):
    logger.debug("Sending APP_SHUTDOWN signal")
    signal(APP_SHUTDOWN).send()
    uvicorn_handle_exit(self, *args, **kwargs)


Server.handle_exit = handle_exit

# Begin logging setup

# Logs from other libraries will propagate up to the root logger
root_logger = logging.getLogger()
root_logger.setLevel(settings.LOG_LEVEL)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class AsyncBlinkHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET):
        super().__init__(level=level)

    def emit(self, record):
        msg = self.format(record)
        signal(APP_LOG).send(msg=msg)


async_blink_handler = AsyncBlinkHandler()
async_blink_handler.setFormatter(formatter)
logger.addHandler(async_blink_handler)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)

# Begin FastAPI setup

rclone_stats_task: Optional[asyncio.Task] = None
server_stats_task: Optional[asyncio.Task] = None

app = FastAPI(default_response_class=D1Response)
app.mount("/dav", WSGIMiddleware(dav))


@app.on_event("startup")
def startup_event():
    logger.debug(f"App startup")
    signal(APP_STARTUP).send()
    loop = asyncio.get_event_loop()

    kmanager.warmup_kernels(
        settings.WARMUP_KERNEL_NAMES, settings.PREWARMED_KERNELS_FILE
    )

    if settings.RCLONE_STATS_POLL:
        global rclone_stats_task
        global server_stats_task
        rclone_stats_task = loop.create_task(rclone.stats_periodic())
        server_stats_task = loop.create_task(
            stats_manager.server_stats_periodic()
        )
    if settings.WATCHDOG_ENABLED:
        dav_manager.start_watchdog(loop)


@app.on_event("shutdown")
async def shutdown_event():
    logger.debug("App shutdown")
    try:
        rclone_stats_task.cancel()
    except Exception:
        pass

    try:
        server_stats_task.cancel()
    except Exception:
        pass

    dav_manager.stop_watchdog()
    kmanager.shutdown_warmups()


not_found_resp = {
    "error": "NOT_FOUND",
    "reason": "Not found.",
    "detail": None,
}

app.include_router(
    hello.router,
    prefix="/hello",
    tags=["hello"],
    responses={404: not_found_resp},
)

app.include_router(
    notebooks.router,
    prefix="/notebooks",
    tags=["notebooks"],
    dependencies=[Depends(read_access)],
    responses={404: not_found_resp},
)

app.include_router(
    dependencies.router,
    prefix="/dependencies",
    tags=["dependencies"],
    dependencies=[Depends(read_access)],
    responses={404: not_found_resp},
)

app.include_router(
    convert.router,
    prefix="/convert",
    tags=["convert"],
    dependencies=[Depends(read_access)],
    responses={404: not_found_resp},
)

app.include_router(
    kernels.router,
    prefix="/kernels",
    tags=["kernels"],
    dependencies=[Depends(read_access)],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    rclone.router,
    prefix="/rclone",
    tags=["rclone"],
    dependencies=[Depends(read_access)],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    server.router,
    prefix="/server",
    tags=["server"],
    dependencies=[Depends(read_access)],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    login.router,
    tags=["login"],
    responses={404: {"description": "Not found"}},
)


@app.exception_handler(NBMException)
async def notebook_manager_exception_handler(
    request: Request, exc: NBMException
):

    return JSONResponse(
        status_code=404,
        content={
            "error": exc.error_code,
            "reason": exc.message,
            "detail": None,
        },
    )
