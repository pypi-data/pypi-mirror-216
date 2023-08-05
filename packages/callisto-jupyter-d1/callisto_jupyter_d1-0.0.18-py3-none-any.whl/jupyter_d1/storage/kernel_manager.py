import asyncio
import json
import os
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

from jupyter_client import AsyncMultiKernelManager  # type: ignore
from jupyter_client import KernelClient
from jupyter_core.paths import jupyter_runtime_dir  # type: ignore
from jupytext.languages import same_language

from ..kernels import get_kernel_definition
from ..logger import logger
from ..settings import callisto_env, settings
from ..utils import BoolObject
from .kernel_listener import KernelListener

try:
    from nb_conda_kernels import CondaKernelSpecManager as KernelSpecManager

    logger.debug("Successfully loaded nb_conda_kernels.")
except ImportError as e:
    from jupyter_client.kernelspec import KernelSpecManager

    logger.debug(f"nb_conda_kernels disabled.  Failed to import - {e}")


class KernelManager:
    def __init__(self):
        self._specManager = KernelSpecManager()
        self._kmanager = AsyncMultiKernelManager(
            kernel_spec_manager=self._specManager
        )
        self._kmanager.connection_dir = jupyter_runtime_dir()
        if not os.path.exists(self._kmanager.connection_dir):
            os.makedirs(
                self._kmanager.connection_dir, mode=0o700, exist_ok=True
            )

        self.clients: Dict[
            UUID, KernelClient
        ] = {}  # map of notebook uuid to client objects
        self.listeners: Dict[UUID, KernelListener] = {}

        self.parent_warmup_task: Optional[asyncio.Task] = None
        self.warmup_tasks: List[asyncio.Task] = []
        self.kernels_warmed = False

    async def _async_warmup_kernels(self, kernel_names: List[str]):
        for kernel_name in kernel_names:
            self.warmup_tasks.append(
                asyncio.create_task(self.warmup(kernel_name))
            )
        try:
            await asyncio.wait_for(asyncio.gather(*self.warmup_tasks), 40)
        except Exception as e:
            logger.error(f"Kernel warmup failed: {e}")
        self.kernels_warmed = True

    def warmup_kernels(
        self,
        warmup_kernel_names: List[str],
        prewarmed_kernels_file: Optional[str] = None,
    ):
        """
        Takes a list of kernel names and an optional location of a json file
        describing kernels warmth status ({"python3": True, "ir": False}),
        warms up the kernels that need it
        """
        prewarmed_kernels = {}
        if prewarmed_kernels_file is not None:
            try:
                with open(prewarmed_kernels_file, "r") as f:
                    prewarmed_kernels = json.load(f)
            except Exception as e:
                logger.error(f"Failed to parse PREWARMED_KERNELS_FILE, {e}")
        kernel_names = []
        for kernel in warmup_kernel_names:
            if (
                kernel not in prewarmed_kernels
                or prewarmed_kernels[kernel] is False
            ):
                kernel_names.append(kernel)
        logger.info(f"Warming kernels: {kernel_names}")

        if len(kernel_names) > 0:
            self.parent_warmup_task = asyncio.create_task(
                self._async_warmup_kernels(kernel_names)
            )
        else:
            self.kernels_warmed = True

    def shutdown_warmups(self):
        for task in self.warmup_tasks:
            try:
                task.cancel()
            except Exception:
                pass
        if self.parent_warmup_task is not None:
            try:
                self.parent_warmup_task.cancel()
            except Exception:
                pass

    async def warmup(
        self, kernel_name: Optional[str] = None, timeout: int = 120
    ):
        """
        Run a simple command in a kernel, serves to combat the issue on work
        nodes where the first cell is slow to run on work node creation
        """
        if kernel_name is None:
            kernel_name, _ = self.get_default_kernelspec()
        logger.info(f"Kernel ({kernel_name}) warming up")
        try:
            _, kernelspec = self.get_kernelspec_by_name(kernel_name)
        except Exception as e:
            logger.info(f"Kernel ({kernel_name}) not found, {e}")
            return False

        kernel_definition = get_kernel_definition(
            kernelspec["spec"]["language"]
        )
        kernel_options = []
        if kernel_definition is None or not kernel_definition.warmup_command:
            logger.info(
                f"Kernel ({kernel_name}) warmup failed, no kernel definition "
                "or no warmup command"
            )
            return False
        if kernel_definition is not None:
            kernel_options = kernel_definition.kernel_options

        kernel_id = await self._kmanager.start_kernel(
            kernel_name=kernel_name,
            extra_arguments=kernel_options,
        )
        kernel = self._kmanager.get_kernel(kernel_id)
        client = kernel.client()
        client.start_channels()

        waiting = BoolObject(value=True)

        def check_finished(msg, parent_msg_id):
            if (
                msg.get("parent_header", {}).get("msg_id", None)
                == parent_msg_id
                and msg.get("msg_type", None) == "status"
                and msg.get("content", {}).get("execution_state", None)
                == "idle"
            ):
                nonlocal waiting
                waiting.value = False

        msg_id = client.execute(kernel_definition.warmup_command)
        counter = 0
        while waiting:
            if await client.iopub_channel.msg_ready():
                iopub_msg = await client.get_iopub_msg()
                check_finished(iopub_msg, msg_id)

            if await client.shell_channel.msg_ready():
                shell_msg = await client.get_shell_msg()
                check_finished(shell_msg, msg_id)

            if await client.stdin_channel.msg_ready():
                stdin_msg = await client.get_stdin_msg()
                check_finished(stdin_msg, msg_id)

            if await client.control_channel.msg_ready():
                control_msg = await client.get_control_msg()
                check_finished(control_msg, msg_id)

            if await client.control_channel.msg_ready():
                control_msg = await client.get_hb_msg()
                check_finished(control_msg, msg_id)

            counter += 1
            # Wait for seconds specifid by timeout
            if counter * 0.1 > timeout:
                logger.info(
                    f"Failed to warm up kernel ({kernel_name}), no response"
                )
                break
            await asyncio.sleep(0.1)

        logger.info(f"Kernel ({kernel_name}) warmed up")
        client.stop_channels()
        await self._kmanager.shutdown_kernel(str(kernel_id))
        success = not waiting
        return success

    async def shutdown_all(self):
        # make a copy so we don't change the array during iteration
        uuids = list(self.clients.keys())

        for uuid in uuids:
            await self.shutdown_kernel(uuid)

    async def shutdown_kernel(self, uuid: UUID) -> None:
        listener = self.listeners.get(uuid)
        if listener is not None:
            await listener.shutdown_listener()
        self.clients[uuid].stop_channels()
        del self.clients[uuid]
        await self._kmanager.shutdown_kernel(str(uuid))

    async def restart_kernel(self, uuid: UUID) -> None:
        await self._kmanager.restart_kernel(str(uuid))

    async def interrupt_kernel(self, uuid: UUID) -> None:
        await self._kmanager.interrupt_kernel(str(uuid))

    async def kernel_is_alive(self, uuid: UUID) -> bool:
        return await self._kmanager.is_alive(str(uuid))

    async def start_kernel(
        self,
        kernel_name: str,
        uuid: UUID,
        directory: Optional[str],
        kernel_options: Optional[Any] = None,
    ) -> None:
        if uuid in self.clients.keys():
            logger.info(f"replacing kernel for {uuid}")
            await self.shutdown_kernel(uuid)
        else:
            logger.info(f"starting kernel for {uuid}")
        if kernel_options is None:
            kernel_options = []
        await self._kmanager.start_kernel(
            kernel_name=kernel_name,
            kernel_id=str(uuid),
            cwd=directory,
            extra_arguments=kernel_options,
        )
        kernel = self._kmanager.get_kernel(str(uuid))

        client = kernel.client()
        client.start_channels()
        self.clients[uuid] = client

        # start the event listener
        listener = KernelListener(client, uuid)
        self.listeners[uuid] = listener
        listener.run()

    async def execute(
        self,
        uuid: UUID,
        code: str,
        silent: bool = False,
        store_history: bool = True,
    ) -> str:
        client = self.clients[uuid]
        msg_id = client.execute(
            code,
            silent=silent,
            store_history=store_history,
        )
        return msg_id

    async def complete(
        self, uuid: UUID, code: str, cursor_pos: int = None
    ) -> str:
        client = self.clients[uuid]
        msg_id = client.complete(code, cursor_pos=cursor_pos)
        return msg_id

    async def get_history(self, uuid: UUID) -> str:
        client = self.clients[uuid]
        msg_id = client.history(output=True)
        return msg_id

    def get_all_kernelspecs(self) -> Dict[str, Any]:
        kspecs = self._specManager.get_all_specs()

        tmp_specs = {}
        for key, val in kspecs.items():
            tmp_spec = val
            tmp_spec["kernel_name"] = key
            # Exclude d1 conda environment python kernel
            if callisto_env in ("staging", "prod") and (
                tmp_spec["spec"]["metadata"].get("conda_env_name", None)
                == "jupyter_d1"
                or tmp_spec["resource_dir"] == "/home/ubuntu"
                "/anaconda3/envs/jupyter_d1/share/jupyter/kernels/python3"
            ):
                continue
            tmp_specs[key] = tmp_spec
        return tmp_specs

    def kernel_names(self) -> List[str]:
        kspecs = self.get_all_kernelspecs()
        return list(kspecs.keys())

    def get_kernelspec(self, uuid: UUID) -> Tuple[str, Dict[str, Any]]:
        kernelspec = self._kmanager.get_kernel(str(uuid)).kernel_spec
        # kernelspec.name isn't always populated but the name is defined as
        # the basename of it's resource directory
        # https://minrk-jupyter-client.readthedocs.io/en/latest/kernels.html#kernel-specs
        kspec_name = os.path.basename(kernelspec.resource_dir)
        kspec = self.get_kernelspec_by_name(kspec_name)
        return kspec

    def get_kernelspec_by_name(
        self, name: Optional[str], language: Optional[str] = None
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Get kernelspec by provided name, if not found fallback to first
        kernelspec matching provided language, else fallback to default kernelspec.
        """
        all_specs = self.get_all_kernelspecs()
        if name is not None and name in all_specs:
            return name, all_specs[name]
        elif language is not None:
            for spec_name, ks in all_specs.items():
                if (
                    "spec" in ks
                    and "language" in ks["spec"]
                    and same_language(ks["spec"]["language"], language)
                ):
                    return spec_name, ks

        return self.get_default_kernelspec()

    def get_default_kernelspec(self) -> Tuple[str, Dict[str, Any]]:
        """Default kernel for the server"""
        all_specs = self.get_all_kernelspecs()

        name = settings.DEFAULT_KERNEL_NAME

        if name is None:
            name = list(
                filter(lambda x: "python" in x, list(all_specs.keys()))
            ).pop()
        return name, all_specs[name]
