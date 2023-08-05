from typing import Dict, List, Optional, Set
from uuid import UUID, uuid4

from ..utils import Connection
from .kernel_manager import KernelManager


class BackgroundKernelRunner:
    """
    Manages kernels for running commands and receiving responses.

    Maintains one kernel per kernelspec while a connection is active.
    When all connections for a kernelspec are gone, this shuts down the running kernel
    """

    def __init__(self, kmanager: KernelManager):
        self.kmanager: KernelManager = kmanager
        # kernel name to running kernel UUId
        self.kernels: Dict[str, UUID] = {}
        # kernel name to activate kernel connections
        self.kernel_connections: Dict[str, Set[Connection]] = {}

    async def clear(self):
        for uuid in self.kernels.values():
            await self.kmanager.shutdown_kernel(uuid)
        self.kernels = {}
        self.kernel_connections = {}

    def get_kernel_id(self, kernel_name: str) -> Optional[UUID]:
        return self.kernels.get(kernel_name, None)

    async def connect(
        self,
        kernel_name: str,
        connection: Connection,
        kernel_options: List[str],
    ):
        """
        Starts a kernel for the kernelspec if one isn't already
        running, and stores a connection object to represent the
        connection to the kernel
        """
        kernel_uuid = self.kernels.get(kernel_name, None)
        if kernel_uuid is None:
            kernel_uuid = uuid4()
            await self.kmanager.start_kernel(
                kernel_name=kernel_name,
                uuid=kernel_uuid,
                directory=None,
                kernel_options=kernel_options,
            )
            self.kernels[kernel_name] = kernel_uuid
        if kernel_name in self.kernel_connections:
            self.kernel_connections[kernel_name].add(connection)
        else:
            self.kernel_connections[kernel_name] = set([connection])

    async def disconnect(self, kernel_name: str, connection: Connection):
        if kernel_name not in self.kernel_connections:
            return
        self.kernel_connections[kernel_name].discard(connection)

        kernel_uuid = self.kernels.get(kernel_name, None)
        if (
            len(self.kernel_connections[kernel_name]) < 1
            and kernel_uuid is not None
        ):
            self.kernels.pop(kernel_name, None)
            await self.kmanager.shutdown_kernel(kernel_uuid)

    async def execute(self, kernel_name: str, source: str) -> str:
        kernel_uuid = self.kernels[kernel_name]
        msg_id = await self.kmanager.execute(kernel_uuid, source)
        return msg_id
