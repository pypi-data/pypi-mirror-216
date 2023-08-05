import json
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, Dict, List
from uuid import UUID

from asyncblink import signal  # type: ignore

from ..logger import logger
from ..models.execution_state import ExecutionState
from ..signals import (
    CONTROL_CHANNEL,
    DEPENDENCIES_COMPLETE,
    DEPENDENCIES_FAILED,
    DEPENDENCIES_RECEIVED,
    DEPENDENCIES_UPDATE,
    HB_CHANNEL,
    IOPUB_CHANNEL,
    SHELL_CHANNEL,
    STDIN_CHANNEL,
)
from ..storage.background_kernel_runner import BackgroundKernelRunner
from ..utils import Connection


class CommandType(Enum):
    PIP_LIST = auto()
    PIP_INSTALL = auto()
    PIP_UNINSTALL = auto()
    UNKOWNN = auto()


class DependencyCommand:
    def __init__(self, command_type: CommandType, request_id: UUID, **kwargs):
        self.type = command_type
        self.request_id = request_id
        self.failed = False
        self.output = ""
        self.extras = kwargs


class DependencyManager(ABC):
    def __init__(
        self,
        kernel_name: str,
        kernelspec: Dict[str, Any],
        bg_kernel_runner: BackgroundKernelRunner,
    ):
        self.kernel_name = kernel_name
        self.kernelspec = kernelspec
        self.bg_kernel_runner: BackgroundKernelRunner = bg_kernel_runner

        # mapping of message id to command id
        self.msg_to_command: Dict[str, DependencyCommand] = {}

        signal(IOPUB_CHANNEL).connect(self.receive_channel_message)
        signal(SHELL_CHANNEL).connect(self.receive_channel_message)
        signal(STDIN_CHANNEL).connect(self.receive_channel_message)
        signal(HB_CHANNEL).connect(self.receive_channel_message)
        signal(CONTROL_CHANNEL).connect(self.receive_channel_message)

    async def connect(self, connection: Connection):
        await self.bg_kernel_runner.connect(
            self.kernel_name, connection, kernel_options=[]
        )

    async def disconnect(self, connection: Connection):
        await self.bg_kernel_runner.disconnect(self.kernel_name, connection)

    async def receive_channel_message(
        self, sender, msg, kernel_id, channel, **kwargs
    ):
        if kernel_id != self.bg_kernel_runner.get_kernel_id(self.kernel_name):
            return

        parent_header = msg.get("parent_header")
        msg_type = msg.get("msg_type")
        content = msg.get("content")
        if parent_header is None:
            logger.debug("Can't get parent header")
            return

        parent_id = parent_header.get("msg_id")
        if parent_id is None:
            logger.debug("Can't get parent id")
            return

        dependency_command = self.msg_to_command.get(parent_id)
        if dependency_command is None:
            logger.debug(f"Msg ({parent_id}) not found in msg_to_command")
            return

        if msg_type == "status" and content is not None:
            execution_state = content.get(
                "execution_state"
            )  # busy/idle/starting

            if execution_state == ExecutionState.busy:
                pass
            if execution_state == ExecutionState.idle:
                if dependency_command.failed:
                    # Don't send complete event if we've sent the failed event
                    pass
                elif dependency_command.type == CommandType.PIP_LIST:
                    payload = None
                    try:
                        payload = json.loads(dependency_command.output)
                    except Exception as e:
                        logger.error(f"Failed to parse list response: {e}")

                    if payload is not None:
                        signal(DEPENDENCIES_COMPLETE).send(
                            request_id=dependency_command.request_id,
                            payload={"data": payload},
                        )
                    else:
                        output = dependency_command.extras.get(
                            "output", "<no output>"
                        )
                        signal(DEPENDENCIES_FAILED).send(
                            request_id=dependency_command.request_id,
                            info=f"Failed to parse list output json"
                            f"\n{output}",
                        )
                else:
                    payload = (
                        {"data": dependency_command.output}
                        if len(dependency_command.output) > 0
                        else None
                    )
                    signal(DEPENDENCIES_COMPLETE).send(
                        request_id=dependency_command.request_id,
                        payload=payload,
                    )

        elif msg_type == "execute_result":
            payload = None
            try:
                payload = json.loads(content["data"])
            except Exception as e:
                logger.error(f"Failed to parse execute_result data: {e}")

            if payload is None:
                payload = content["data"]

            dependency_command.output += payload
        elif msg_type == "stream":
            if (
                dependency_command.type == CommandType.PIP_LIST
                and content.get("name", None) == "stdout"
            ):
                payload = None
                try:
                    payload = json.loads(content["text"])
                except Exception as e:
                    logger.error(f"Failed to parse pip list response: {e}")

                if "you may need to restart" not in content["text"]:
                    dependency_command.output += content["text"]
            else:
                if content.get("name", None) in ("stdout", "stderr"):
                    kwargs = {content["name"]: content["text"]}
                else:
                    kwargs = {"stdout": content["text"]}
                signal(DEPENDENCIES_UPDATE).send(
                    request_id=dependency_command.request_id, **kwargs
                )
        elif msg_type == "error":
            signal(DEPENDENCIES_FAILED).send(
                request_id=dependency_command.request_id,
                info=f"{content['ename']}, {content['evalue']}, {content['traceback']}",
            )
            dependency_command.failed = True

    @abstractmethod
    async def execute(
        self, request_id: UUID, command: str, subcommand: str, args: List[str]
    ) -> str:
        raise NotImplementedError

    async def dispatch_execute(
        self, request_id: UUID, source: str, command_type: CommandType
    ) -> str:
        msg_id = await self.bg_kernel_runner.execute(self.kernel_name, source)
        self.msg_to_command[msg_id] = DependencyCommand(
            command_type=command_type, request_id=request_id
        )
        signal(DEPENDENCIES_RECEIVED).send(request_id=request_id)

        return msg_id
