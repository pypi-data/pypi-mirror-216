import os
import sys

from importlib_resources import files

from ...utils import Connection
from ..dependency_manager import CommandType, DependencyManager
from . import startup

startup_script = files(startup).joinpath("dependency_startup.py")

# --no-raise-error for no error kernel response
run_pip = f"""
%%sh -s "$python_executable"
$1 -m pip"""

# WJL -- for iPad, just use %pip magic to avoid shell problems.
if sys.platform == "darwin" and os.uname().machine.startswith("iP"):
    run_pip = "%pip"


class PythonDependencyManager(DependencyManager):
    async def connect(self, connection: Connection):
        await self.bg_kernel_runner.connect(
            self.kernel_name,
            connection,
            kernel_options=[f"--IPKernelApp.exec_files='{startup_script}'"],
        )

    async def execute(self, request_id, command, subcommand, args) -> str:

        command_type = CommandType.UNKOWNN
        if command == "pip":
            command = run_pip
            if subcommand == "list":
                command_type = CommandType.PIP_LIST
                args = [
                    "--disable-pip-version-check",
                    "--format",
                    "json",
                ] + args
            elif subcommand == "install":
                command_type = CommandType.PIP_INSTALL
            elif subcommand == "uninstall":
                command_type = CommandType.PIP_UNINSTALL
                if "-y" not in args:
                    args = ["-y"] + args

        source = " ".join(
            [
                p
                for p in [command, subcommand] + args
                if p is not None and len(p) > 0
            ]
        )
        await self.dispatch_execute(
            request_id=request_id, source=source, command_type=command_type
        )

        return source
