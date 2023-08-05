import asyncio

import nest_asyncio
from uvicorn.config import LOGGING_CONFIG
from uvicorn.workers import UvicornWorker

try:
    nest_asyncio.apply()
except Exception:
    pass
import tornado  # noqa

LOGGING_CONFIG["formatters"]["default"][
    "fmt"
] = "%(asctime)s %(levelprefix)s - %(message)s"
LOGGING_CONFIG["formatters"]["access"][
    "fmt"
] = '%(asctime)s %(levelprefix)s - "%(request_line)s" %(status_code)s'


class D1UvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {
        "loop": "asyncio",
        "http": "auto",
        "log_config": LOGGING_CONFIG,
    }

    async def pre_serve(self):
        # Fixes the error mentioned in this thread
        # https://github.com/jupyter/notebook/issues/6164
        # Patch the loop at the earliest opportunity
        nest_asyncio.apply()

        await self._serve()

    def run(self) -> None:
        return asyncio.run(self.pre_serve())
