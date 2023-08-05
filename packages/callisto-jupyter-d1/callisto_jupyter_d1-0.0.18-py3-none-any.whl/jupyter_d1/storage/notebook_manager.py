import asyncio
import functools
import inspect
import json
import os
import pprint
import re
from copy import deepcopy
from datetime import datetime
from enum import Enum, auto
from itertools import chain
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from uuid import UUID

import jsonpatch
import nbformat  # type: ignore
from asyncblink import signal  # type: ignore
from fastapi.concurrency import run_in_threadpool

from jupyter_d1.commands import D1CommandType, execute_d1_notify
from jupyter_d1.dav import dav_manager
from jupyter_d1.signals import (
    CELL_ADDED,
    CELL_DELETED,
    CELL_EXECUTION_INPUT,
    CELL_EXECUTION_REPLY,
    CELL_EXECUTION_REQUEST,
    CELL_UPDATE,
    CELL_UPDATE_PATCH,
    CHECK_DEPENDENCIES,
    CLIENT_COMMAND,
    COMPLETE_REPLY,
    CONTROL_CHANNEL,
    HB_CHANNEL,
    HISTORY_REPLY,
    IMPORT_ERROR,
    IOPUB_CHANNEL,
    KERNEL_INTERRUPTED,
    KERNEL_RESTARTED,
    METADATA_UPDATE,
    NOTEBOOKS_UPDATED,
    PAYLOAD_PAGE,
    SCRATCH_UPDATE,
    SHELL_CHANNEL,
    STDIN_CHANNEL,
    VAR_DETAILS,
    VAR_STATISTICS,
    VARS_UPDATE,
)

from ..d1_response import D1Encoder, d1_pairs_hook
from ..kernels import (
    DependencyChecker,
    VarsManager,
    WorkDirManager,
    get_kernel_definition,
)
from ..logger import logger
from ..models.cell import CellType, CellUpdate
from ..models.execution_state import ExecutionState
from ..models.JSONType import JSONType
from ..models.kernel_variable import KernelVariable, KernelVariableStats
from ..models.notebook import Filter
from ..settings import settings
from ..undo_manager import UndoManager
from ..utils import NotebookNode
from .kernel_manager import KernelManager
from .notebook_validator import NotebookValidator

# NBFormat docs
# https://nbformat.readthedocs.io/en/latest/api.html#notebooknode-objects

jsonpatch.JsonPatch.json_dumper = functools.partial(json.dumps, cls=D1Encoder)

D1_COMMAND_DELIMITER = "___callisto_d1_command___"


# Pattern to capture newlines carriage returns
pattern = re.compile(r"(\n|\r)")


class NBMErrorCode(str, Enum):
    notebook_not_found = "NOTEBOOK_NOT_FOUND"
    cell_not_found = "CELL_NOT_FOUND"


class NBMException(Exception):
    def __init__(
        self,
        error_code: NBMErrorCode,
        a_uuid: Optional[UUID],
        message: Optional[str] = None,
    ):
        if message is None:
            if error_code == NBMErrorCode.notebook_not_found:
                message = f"Notebook not found with uuid: {a_uuid}"
            elif error_code == NBMErrorCode.cell_not_found:
                message = f"Cell not found with uuid: {a_uuid}"
        self.message = message
        self.error_code = error_code
        self.error_uuid = a_uuid


class CommandType(Enum):
    CELL_EXECUTION = auto()
    SCRATCH_EXECUTION = auto()
    VARS_REQUEST = auto()
    VAR_DETAIL_REQUEST = auto()
    VAR_STATISTICS_REQUEST = auto()
    UPDATE_WORKDIR_REQUEST = auto()
    CHANGE_WORKDIR_REQUEST = auto()
    CHECK_DEPENDENCIES = auto()
    COMPLETE_REQUEST = auto()
    HISTORY_REQUEST = auto()


class NotebookCommand:
    def __init__(
        self,
        command_type: CommandType,
        notebook_id: UUID,
        connection_id: Optional[UUID] = None,
        command_id: Optional[str] = None,
        **kwargs,
    ):
        """
        connection_id is a UUID for the websocket connection this command is associated
        with
        command_id is a passthrough that can be provided by clients to identify
        responses associated with this command
        """
        self.type = command_type
        self.notebook_id = notebook_id
        self.connection_id = connection_id
        self.command_id = command_id
        self.execution_count: Optional[int] = None
        self.extras = kwargs
        # Functions (with args and kwargs) to be called when this command finishes
        # (reaches idle state)
        self.post_execution: List[
            Tuple[Callable, List[Any], Dict[str, Any]]
        ] = []


class Notebook:
    def __init__(
        self,
        node: NotebookNode,
        vars_manager: Optional[VarsManager],
        workdir_manager: Optional[WorkDirManager],
        dependency_checker: Optional[DependencyChecker],
        autosave: bool = True,
    ):
        self.node: NotebookNode = node
        self.umanager = UndoManager()
        self.vars_manager = vars_manager
        self.workdir_manager = workdir_manager
        self.dependency_checker = dependency_checker
        self.autosave = autosave


class NotebookManager:
    def __init__(self, kmanager: KernelManager):
        self.notebooks: Dict[UUID, Notebook] = {}
        self.kmanager: KernelManager = kmanager
        self.validator: NotebookValidator = NotebookValidator()
        self.last_idle = datetime.utcnow()

        # mapping of message id to command
        self.msg_to_command: Dict[str, NotebookCommand] = {}

        signal(IOPUB_CHANNEL).connect(self.receive_channel_message)
        signal(SHELL_CHANNEL).connect(self.receive_channel_message)
        signal(STDIN_CHANNEL).connect(self.receive_channel_message)
        signal(HB_CHANNEL).connect(self.receive_channel_message)
        signal(CONTROL_CHANNEL).connect(self.receive_channel_message)

    def undo(self, nb_uuid: UUID):
        self.notebooks[nb_uuid].umanager.undo()

    def redo(self, nb_uuid: UUID):
        self.notebooks[nb_uuid].umanager.redo()

    async def create_notebook(
        self,
        kspec_name: Optional[str] = None,
        directory: Optional[str] = None,
        filename: Optional[str] = None,
        working_directory: Optional[str] = None,
    ) -> NotebookNode:
        notebook = nbformat.v4.new_notebook()

        await self.add_notebook(
            notebook,
            kspec_name=kspec_name,
            directory=directory,
            filename=filename,
            working_directory=working_directory,
        )
        return notebook

    async def open_notebook(
        self,
        filepath: str,
        kspec_name: Optional[str] = None,
        working_directory: Optional[str] = None,
    ) -> UUID:
        with open(filepath, "rb") as f:
            nb_content = f.read()
        path = Path(filepath)
        directory = str(path.parent)
        filename = str(path.parts[-1])
        if filename.endswith(".ipynb"):
            filename = filename.replace(".ipynb", "")
        return await self.add_notebook_json(
            nb_content,
            directory=directory,
            kspec_name=kspec_name,
            filename=filename,
            working_directory=working_directory,
        )

    def get_metadata(
        self,
        filepath: str,
    ) -> NotebookNode:
        for nb in self.notebooks.values():
            if nb.node.metadata.jupyter_d1.path == filepath:
                return nb.node.metadata
        with open(filepath, "rb") as f:
            nb_content = f.read()
        node = nbformat.reads(
            nb_content, as_version=4, object_pairs_hook=d1_pairs_hook
        )
        return node.metadata

    async def save_notebook(
        self,
        notebook: Optional[NotebookNode] = None,
        uuid: Optional[UUID] = None,
    ):
        nb = notebook
        if nb is None and uuid is not None and uuid in self.notebooks:
            nb = self.notebooks[uuid].node
        if nb is None:
            raise NBMException(NBMErrorCode.notebook_not_found, uuid)
        path = nb.metadata.jupyter_d1.path
        await run_in_threadpool(
            nbformat.write, nb, path, default=D1Encoder().default
        )

    async def save_notebook_as(
        self,
        uuid: UUID,
        directory: str,
        filename: str,
        delete_old: bool = False,
        just_metadata: bool = False,
    ):
        """
        Change save location of the notebook. If delete_old is set,
        the old path of the notebook is deleted (used for renaming).
        If just_metadata is True, only update the in-memory notebook's
        metadata.

        This method does not check if the path already exists and
        will overwrite it (unless just_metadata is True).
        """
        nb = self.notebooks[uuid]
        if nb is None:
            raise NBMException(NBMErrorCode.notebook_not_found, uuid)
        old_path = nb.node.metadata.jupyter_d1.path
        self.validator.validate(
            nb.node,
            directory,
            filename,
        )

        if not just_metadata:
            await self.save_notebook(nb.node)

            if delete_old:
                os.remove(old_path)

        signal(METADATA_UPDATE).send(
            notebook_id=uuid, metadata=nb.node.metadata
        )

        return nb.node.metadata.jupyter_d1.path

    async def upload_notebook(
        self, notebook_data: bytes, directory: str, filename: str
    ):
        nb = nbformat.reads(
            notebook_data, as_version=4, object_pairs_hook=d1_pairs_hook
        )
        self.validator.validate(
            nb, directory, filename, new_notebook_uuid=True
        )
        await self.save_notebook(nb)

    async def delete_notebooks(self):
        await self.kmanager.shutdown_all()
        self.notebooks = {}
        self.msg_to_command = {}
        dav_manager.clear_providers()
        signal(NOTEBOOKS_UPDATED).send(notebooks=self.get_notebook_nodes())

    async def delete_notebook(self, uuid: UUID):
        self.get_notebook(uuid)  # verify the notebook exists
        await self.kmanager.shutdown_kernel(uuid)
        self.notebooks.pop(uuid, None)
        dav_manager.remove_provider(uuid)
        signal(NOTEBOOKS_UPDATED).send(notebooks=self.get_notebook_nodes())

    def get_notebook_nodes(self) -> Dict[UUID, NotebookNode]:
        return {uuid: nb.node for (uuid, nb) in self.notebooks.items()}

    def get_vars_manager(self, nb_uuid: UUID) -> Optional[VarsManager]:
        nb = self.notebooks.get(nb_uuid)
        return nb.vars_manager if nb is not None else None

    def get_workdir_manager(self, nb_uuid: UUID) -> Optional[WorkDirManager]:
        nb = self.notebooks.get(nb_uuid)
        return nb.workdir_manager if nb is not None else None

    def get_dependency_checker(
        self, nb_uuid: UUID
    ) -> Optional[DependencyChecker]:
        nb = self.notebooks.get(nb_uuid)
        return nb.dependency_checker if nb is not None else None

    def get_notebooks_json(self) -> str:
        nb_dicts = list(map(lambda x: x.node.dict(), self.notebooks.values()))
        return json.dumps(nb_dicts, cls=D1Encoder)

    def get_notebooks_dicts(self) -> List[Dict[str, Any]]:
        return list(map(lambda x: x.node.dict(), self.notebooks.values()))

    def get_notebook(self, uuid: UUID) -> Notebook:
        nb = self.notebooks.get(uuid)
        if nb is None:
            raise NBMException(NBMErrorCode.notebook_not_found, uuid)
        return nb

    def get_notebook_kernelspec(
        self, uuid: UUID
    ) -> Tuple[str, Dict[str, Any]]:
        return self.kmanager.get_kernelspec(uuid)

    def get_notebook_node(self, uuid: UUID) -> NotebookNode:
        return self.get_notebook(uuid).node

    def get_notebook_json(self, uuid: UUID) -> str:
        node = self.get_notebook(uuid).node
        return nbformat.writes(node, default=D1Encoder().default)

    def get_notebook_dict(self, uuid: UUID) -> Dict[str, Any]:
        return self.get_notebook(uuid).node.dict()

    async def add_notebook(
        self,
        notebook_node: NotebookNode,
        kspec_name: Optional[str] = None,
        directory: Optional[str] = None,
        filename: Optional[str] = None,
        working_directory: Optional[str] = None,
        autosave: bool = True,
    ) -> UUID:
        notebook = None
        try:
            uuid = notebook_node.metadata.jupyter_d1.uuid
            notebook = self.notebooks[uuid]
        except Exception:
            pass
        if notebook is not None:
            return uuid

        resolved_workdir = (
            str(Path(working_directory).resolve())
            if working_directory is not None
            else None
        )

        self.validator.validate(
            notebook_node,
            directory,
            filename,
            working_directory=resolved_workdir,
            new_notebook_uuid=True,
            reset_state=True,
        )
        nb_uuid = notebook_node.metadata.jupyter_d1.uuid

        # Find the spec name
        if kspec_name is None:
            try:
                kspec_name = notebook_node.metadata.kernelspec.name
            except AttributeError:
                kspec_name = None

        kspec_lang = None
        try:
            kspec_lang = notebook_node.metadata.kernelspec.language
        except AttributeError:
            pass

        working_kspec_name, kernelspec = self.kmanager.get_kernelspec_by_name(
            kspec_name, language=kspec_lang
        )

        notebook_node.metadata.kernelspec = {
            "name": working_kspec_name,
            "language": kernelspec["spec"]["language"],
            "display_name": kernelspec["spec"].get(
                "display_name", working_kspec_name
            ),
        }

        work_dir = notebook_node.metadata.jupyter_d1.working_directory

        kernel_definition = get_kernel_definition(
            kernelspec["spec"]["language"]
        )
        vars_manager: Optional[VarsManager] = None
        workdir_manager: Optional[WorkDirManager] = None
        dependency_checker: Optional[DependencyChecker] = None
        kernel_options = []
        if kernel_definition is not None:
            vars_manager = kernel_definition.create_vars_manager()
            workdir_manager = kernel_definition.create_workdir_manager(
                work_dir
            )
            dependency_checker = kernel_definition.create_dependency_checker()
            kernel_options = kernel_definition.kernel_options

        await self.kmanager.start_kernel(
            kernel_name=working_kspec_name,
            uuid=nb_uuid,
            directory=work_dir,
            kernel_options=kernel_options,
        )

        if work_dir is not None:
            dav_manager.add_provider(work_dir, nb_uuid)
        self.notebooks[nb_uuid] = Notebook(
            node=notebook_node,
            vars_manager=vars_manager,
            workdir_manager=workdir_manager,
            dependency_checker=dependency_checker,
            autosave=autosave,
        )
        if autosave:
            await self.save_notebook(notebook_node)

        signal(CELL_UPDATE).send(
            cells=notebook_node.cells, notebook_id=nb_uuid
        )
        signal(NOTEBOOKS_UPDATED).send(notebooks=self.get_notebook_nodes())
        return nb_uuid

    async def add_notebook_json(
        self,
        notebook_data: bytes,
        kspec_name: Optional[str] = None,
        directory: Optional[str] = None,
        filename: Optional[str] = None,
        working_directory: Optional[str] = None,
        autosave: bool = True,
    ) -> UUID:
        node = nbformat.reads(
            notebook_data, as_version=4, object_pairs_hook=d1_pairs_hook
        )
        return await self.add_notebook(
            node,
            kspec_name=kspec_name,
            directory=directory,
            filename=filename,
            working_directory=working_directory,
            autosave=autosave,
        )

    async def execute(self, notebook_id: UUID, cell_id: UUID):
        notebook = self.get_notebook(notebook_id)
        cell = self.find_cell(notebook_id, cell_id)
        original_cell = self.clear_cell(
            cell,
            ExecutionState.pending,
            return_original=settings.CELL_UPDATE_PATCHES,
        )
        uuid = notebook.node.metadata.jupyter_d1.uuid
        source = cell.source
        msg_id = await self.kmanager.execute(uuid, source)  # returns msg_id
        self.msg_to_command[msg_id] = NotebookCommand(
            CommandType.CELL_EXECUTION,
            uuid,
            cell_id=cell.metadata.jupyter_d1.uuid,
            has_run=False,
        )
        self.post_execute_update_msg(notebook_id, original_cell, cell, msg_id)
        return msg_id

    def post_execute_update_msg(
        self,
        notebook_id: UUID,
        original_cell: Optional[NotebookNode],
        cell: NotebookNode,
        msg_id: str,
    ):
        cell_id = cell.metadata.jupyter_d1.uuid
        if settings.CELL_UPDATE_PATCHES:
            self.create_and_send_cell_patch(
                original_cell, cell, cell.metadata.jupyter_d1.uuid, notebook_id
            )
        else:
            signal(CELL_UPDATE).send(cells=[cell], notebook_id=notebook_id)
        # Repeat the execution request out to any client listening on the
        # websocket so it can keep track of requests from other clients
        signal(CELL_EXECUTION_REQUEST).send(
            notebook_id=notebook_id,
            cell_id=cell_id,
            msg_id=msg_id,
        )

    async def execute_scratch(self, notebook_id: UUID, code: str):
        notebook = self.get_notebook(notebook_id)
        uuid = notebook.node.metadata.jupyter_d1.uuid
        msg_id = await self.kmanager.execute(uuid, code, store_history=False)
        self.msg_to_command[msg_id] = NotebookCommand(
            CommandType.SCRATCH_EXECUTION,
            uuid,
            code=code,
            execution_state=ExecutionState.unknown,
        )
        return msg_id

    async def complete(
        self,
        notebook_id: UUID,
        code: str,
        cursor_pos: Optional[int] = None,
        connection_id: Optional[UUID] = None,
        command_id: Optional[str] = None,
    ):
        notebook = self.get_notebook(notebook_id)
        uuid = notebook.node.metadata.jupyter_d1.uuid
        msg_id = await self.kmanager.complete(uuid, code, cursor_pos)
        self.msg_to_command[msg_id] = NotebookCommand(
            CommandType.COMPLETE_REQUEST,
            uuid,
            connection_id=connection_id,
            command_id=command_id,
        )
        return msg_id

    async def history(self, notebook_id: UUID):
        notebook = self.get_notebook(notebook_id)
        uuid = notebook.node.metadata.jupyter_d1.uuid
        msg_id = await self.kmanager.get_history(uuid)
        self.msg_to_command[msg_id] = NotebookCommand(
            CommandType.HISTORY_REQUEST, uuid
        )
        return msg_id

    async def interrupt_kernel(self, notebook_id: UUID):
        await self.kmanager.interrupt_kernel(notebook_id)
        signal(KERNEL_INTERRUPTED).send(
            notebook_id=notebook_id,
        )

    async def perform_restart(self, notebook_id: UUID):
        await self.kmanager.restart_kernel(notebook_id)
        # TODO: Replace this with something smarter, need to wait for kernel
        # to fully start so it's ready for messages
        await asyncio.sleep(2)
        workdir_manager = self.get_workdir_manager(notebook_id)
        if (
            workdir_manager is not None
            and workdir_manager.last_set_workdir is not None
        ):
            await self.change_kernel_workdir(
                notebook_id, workdir_manager.last_set_workdir
            )

    async def restart_kernel(
        self, notebook_id: UUID, clear_output: bool = False
    ):
        notebook = self.get_notebook(notebook_id)
        await self.perform_restart(notebook_id)
        notebook = self.get_notebook(notebook_id)
        for cell in notebook.node.cells:
            if clear_output:
                if "outputs" in cell:
                    cell.outputs = []

                if "execution_count" in cell:
                    cell.execution_count = None

            cell.metadata.jupyter_d1["execution_state"] = ExecutionState.idle
        signal(KERNEL_RESTARTED).send(
            cells=notebook.node.cells,
            notebook_id=notebook_id,
            run_all_cells=False,
        )

    def clear_multiple_cells(
        self,
        notebook: Notebook,
        notebook_id: UUID,
        above_position: Optional[int] = None,
        below_position: Optional[int] = None,
        execution_state: Optional[ExecutionState] = ExecutionState.idle,
        send_signal: bool = True,
    ):
        for cell in notebook.node.cells:
            if (
                above_position
                and cell["metadata"]["jupyter_d1"]["position"]
                >= above_position
            ) or (
                below_position
                and cell["metadata"]["jupyter_d1"]["position"]
                <= below_position
            ):
                continue
            self.clear_single_cell(
                notebook_id, cell, execution_state, send_signal
            )

    def clear_single_cell(
        self,
        notebook_id: UUID,
        cell: NotebookNode,
        execution_state: Optional[ExecutionState] = ExecutionState.idle,
        send_signal: bool = True,
    ):
        original_cell = self.clear_cell(
            cell,
            execution_state,
            return_original=send_signal and settings.CELL_UPDATE_PATCHES,
        )

        if send_signal:
            if settings.CELL_UPDATE_PATCHES:
                self.create_and_send_cell_patch(
                    original_cell,
                    cell,
                    cell["metadata"]["jupyter_d1"]["uuid"],
                    notebook_id,
                )
            else:
                signal(CELL_UPDATE).send(cells=[cell], notebook_id=notebook_id)

    def clear_cell(
        self,
        cell: NotebookNode,
        execution_state: Optional[ExecutionState] = ExecutionState.idle,
        return_original: bool = settings.CELL_UPDATE_PATCHES,
    ) -> Optional[NotebookNode]:
        original_cell = None
        if return_original:
            original_cell = deepcopy(cell)

        if "outputs" in cell:
            cell.outputs = []

        if "execution_count" in cell:
            cell.execution_count = None

        if CellType(cell.cell_type) == CellType.code:
            cell.metadata.jupyter_d1["execution_state"] = execution_state

        return original_cell

    async def run_multiple_cells(
        self,
        notebook: Notebook,
        notebook_id: UUID,
        above_position: Optional[int] = None,
        below_position: Optional[int] = None,
    ):
        msg_ids = []
        for cell in notebook.node.cells:
            if (
                above_position
                and cell["metadata"]["jupyter_d1"]["position"]
                >= above_position
            ) or (
                below_position
                and cell["metadata"]["jupyter_d1"]["position"]
                <= below_position
            ):
                continue

            if CellType(cell.cell_type) == CellType.code:
                source = cell.source
                uuid = notebook.node.metadata.jupyter_d1.uuid

                original_cell = self.clear_cell(
                    cell,
                    ExecutionState.pending,
                    return_original=settings.CELL_UPDATE_PATCHES,
                )
                msg_id = await self.kmanager.execute(uuid, source)
                msg_ids.append(msg_id)
                self.msg_to_command[msg_id] = NotebookCommand(
                    CommandType.CELL_EXECUTION,
                    uuid,
                    cell_id=cell.metadata.jupyter_d1.uuid,
                    has_run=False,
                )
                self.post_execute_update_msg(
                    notebook_id, original_cell, cell, msg_id
                )
        return msg_ids

    async def restart_kernel_and_run_all_cells(self, notebook_id: UUID):
        await self.perform_restart(notebook_id)
        notebook = self.get_notebook(notebook_id)

        signal(KERNEL_RESTARTED).send(
            cells=notebook.node.cells,
            notebook_id=notebook_id,
            run_all_cells=True,
        )

        msg_ids = await self.run_multiple_cells(notebook, notebook_id)

        return msg_ids

    async def execute_all(
        self,
        notebook_id: UUID,
        above_position: Optional[int] = None,
        below_position: Optional[int] = None,
    ):
        notebook = self.get_notebook(notebook_id)
        msg_ids = await self.run_multiple_cells(
            notebook, notebook_id, above_position, below_position
        )
        return msg_ids

    async def update_kernel_vars(self, notebook_id: UUID):
        notebook = self.get_notebook(notebook_id)
        uuid = notebook.node.metadata.jupyter_d1.uuid
        vars_manager = notebook.vars_manager
        if vars_manager is None:
            return
        code = vars_manager.get_vars_code()
        msg_id = await self.kmanager.execute(uuid, code, store_history=False)
        self.msg_to_command[msg_id] = NotebookCommand(
            CommandType.VARS_REQUEST, uuid
        )

    async def get_kernel_var_details(
        self,
        nb_id: UUID,
        var_name: str,
        page_size: Optional[int],
        page: int,
        sort_by: Optional[List[Union[str, int]]] = None,
        ascending: Optional[Optional[List[bool]]] = None,
        filters: Optional[List[Filter]] = None,
    ) -> Optional[KernelVariable]:
        notebook = self.get_notebook(nb_id)
        uuid = notebook.node.metadata.jupyter_d1.uuid
        vars_manager = notebook.vars_manager
        if vars_manager is None:
            return None
        code = vars_manager.get_single_var_code(
            var_name,
            page_size=page_size,
            page=page,
            sort_by=sort_by,
            ascending=ascending,
            filters=filters,
        )
        msg_id = await self.kmanager.execute(uuid, code, store_history=False)
        self.msg_to_command[msg_id] = NotebookCommand(
            CommandType.VAR_DETAIL_REQUEST, uuid, var_name=var_name, page=page
        )
        single_var_details: Optional[KernelVariable] = None
        waiting = True

        def receive_var_details(
            sender: Any,
            notebook_id: UUID,
            parent_msg_id: str,
            single_var: KernelVariable,
            **kwargs,
        ):
            if nb_id == notebook_id and parent_msg_id == msg_id:
                nonlocal single_var_details
                nonlocal waiting
                single_var_details = single_var
                waiting = False

        signal(VAR_DETAILS).connect(receive_var_details)

        count = 0
        sleep_dur = 0.1
        # Wait ~30 seconds
        while waiting and count < (30 / sleep_dur):
            await asyncio.sleep(sleep_dur)
            count += 1

        return single_var_details

    async def get_kernel_var_statistics(
        self, nb_id: UUID, var_name: str, column: Optional[str] = None
    ) -> Optional[KernelVariableStats]:
        notebook = self.get_notebook(nb_id)
        uuid = notebook.node.metadata.jupyter_d1.uuid
        vars_manager = notebook.vars_manager
        if vars_manager is None:
            return None
        code = vars_manager.get_single_var_stats_code(var_name, column)

        msg_id = await self.kmanager.execute(uuid, code, store_history=False)
        self.msg_to_command[msg_id] = NotebookCommand(
            CommandType.VAR_STATISTICS_REQUEST, uuid, var_name=var_name
        )
        var_stats: Optional[KernelVariableStats] = None
        waiting = True

        def receive_var_statistics(
            sender: Any,
            notebook_id: UUID,
            parent_msg_id: str,
            stats: KernelVariableStats,
            **kwargs,
        ):
            if nb_id == notebook_id and parent_msg_id == msg_id:
                nonlocal var_stats
                nonlocal waiting
                var_stats = stats
                waiting = False

        signal(VAR_STATISTICS).connect(receive_var_statistics)

        count = 0
        sleep_dur = 0.1
        # Wait ~30 seconds
        while waiting and count < (30 / sleep_dur):
            await asyncio.sleep(sleep_dur)
            count += 1

        return var_stats

    async def update_kernel_workdir(self, notebook_id: UUID):
        notebook = self.get_notebook(notebook_id)
        uuid = notebook.node.metadata.jupyter_d1.uuid
        workdir_manager = notebook.workdir_manager
        if workdir_manager is None:
            return
        code = workdir_manager.get_cwd_code()
        msg_id = await self.kmanager.execute(uuid, code, store_history=False)
        self.msg_to_command[msg_id] = NotebookCommand(
            CommandType.UPDATE_WORKDIR_REQUEST, uuid
        )

    async def change_kernel_workdir(self, notebook_id: UUID, directory: str):
        notebook = self.get_notebook(notebook_id)
        uuid = notebook.node.metadata.jupyter_d1.uuid
        workdir_manager = notebook.workdir_manager
        if workdir_manager is None:
            return
        code = workdir_manager.get_chdir_code(directory)
        msg_id = await self.kmanager.execute(uuid, code, store_history=False)
        self.msg_to_command[msg_id] = NotebookCommand(
            CommandType.CHANGE_WORKDIR_REQUEST, uuid
        )
        return msg_id

    def change_dav_workdir(self, notebook_id: UUID, directory: str):
        dav_manager.add_provider(directory, notebook_id)

    async def get_vars(self, notebook_id: UUID) -> List[KernelVariable]:
        notebook = self.get_notebook(notebook_id)
        return (
            notebook.vars_manager.vars
            if notebook.vars_manager is not None
            else []
        )

    async def check_dependencies(
        self,
        nb_id: UUID,
        cell_id: UUID = None,
    ) -> List[str]:
        notebook = self.get_notebook(nb_id)
        dependency_checker = notebook.dependency_checker
        if dependency_checker is None:
            return []
        source_code = []
        if cell_id:
            cell = self.find_cell(nb_id, cell_id=cell_id)
            if CellType(cell.cell_type) == CellType.code:
                source_code.append(cell.source)
        else:
            for cell in notebook.node.cells:
                if CellType(cell.cell_type) == CellType.code:
                    source_code.append(cell.source)
        code = dependency_checker.get_check_dependencies_code(
            "\n".join(source_code)
        )
        missing_deps: List[str] = []
        if len(code) == 0:
            return missing_deps

        msg_id = await self.kmanager.execute(nb_id, code, store_history=False)
        self.msg_to_command[msg_id] = NotebookCommand(
            CommandType.CHECK_DEPENDENCIES, nb_id, cell_id=cell_id
        )

        waiting = True

        def receive_dependency_check_results(
            sender: Any,
            notebook_id: UUID,
            parent_msg_id: str,
            missing_dependencies: List[str],
            **kwargs,
        ):
            if nb_id == notebook_id and parent_msg_id == msg_id:
                nonlocal missing_deps
                nonlocal waiting
                missing_deps = missing_dependencies
                waiting = False

        signal(CHECK_DEPENDENCIES).connect(receive_dependency_check_results)

        count = 0
        sleep_dur = 0.1
        # Wait ~30 seconds
        while waiting and count < (30 / sleep_dur):
            await asyncio.sleep(sleep_dur)
            count += 1

        return missing_deps

    def find_cell(self, notebook_id: UUID, cell_id: UUID) -> NotebookNode:
        notebook = self.notebooks.get(notebook_id)
        if notebook is None:
            raise NBMException(NBMErrorCode.notebook_not_found, notebook_id)
        for cell in notebook.node.cells:
            if cell.metadata.jupyter_d1.uuid == cell_id:
                return cell
        raise NBMException(NBMErrorCode.cell_not_found, cell_id)

    def delete_cell(self, notebook_id: UUID, cell_id: UUID):
        notebook = self.get_notebook(notebook_id)
        cell = self.find_cell(notebook_id, cell_id)

        # Save cell info for redo operation
        cell_type = cell.cell_type
        source = cell.source
        try:
            # When undoing, we need to add this cell back
            # _before_ the following cell, so get the next
            # cell's uuid as the saved 'before' param
            before_idx = cell.metadata.jupyter_d1.position + 1
            before = notebook.node.cells[before_idx].metadata.jupyter_d1.uuid
        except IndexError:
            # If the indes is off the end of string, then the
            # cell is the last one, which means 'before' is None
            before = None

        notebook.node.cells.remove(cell)
        self.validator.validate(notebook.node)
        signal(CELL_DELETED).send(
            cells=notebook.node.cells, notebook_id=notebook_id
        )

        kwargs = {
            "notebook_id": notebook_id,
            "cell_id": cell_id,
            "cell_type": cell_type,
            "source": source,
            "before": before,
        }
        notebook.umanager.add_action(
            self.create_cell, kwargs=kwargs, name="Delete Cell"
        )

    def update_cell(
        self, notebook_id: UUID, cell_id: UUID, cell_update: CellUpdate
    ) -> Union[NotebookNode, List[JSONType]]:
        notebook = self.get_notebook(notebook_id)
        cell = self.find_cell(notebook_id, cell_id)

        original_cell = None
        if settings.CELL_UPDATE_PATCHES:
            original_cell = deepcopy(cell)
        # save info for undo
        undo_cell_update = CellUpdate(
            source=cell.source, cell_type=cell.cell_type
        )

        # update with new info
        if cell_update.source is not None:
            cell.source = cell_update.source
        if cell_update.cell_type is not None:
            cell.cell_type = cell_update.cell_type

        self.validator.validate(notebook.node)

        patch = None
        if settings.CELL_UPDATE_PATCHES:
            patch = self.create_and_send_cell_patch(
                original_cell, cell, cell_id, notebook_id
            )
        else:
            signal(CELL_UPDATE).send(cells=[cell], notebook_id=notebook_id)

        kwargs = {
            "notebook_id": notebook_id,
            "cell_id": cell_id,
            "cell_update": undo_cell_update,
        }
        notebook.umanager.add_action(
            self.update_cell, kwargs=kwargs, name="Update Cell"
        )
        return (
            patch
            if settings.CELL_UPDATE_PATCHES and patch is not None
            else cell
        )

    def move_cell(
        self, notebook_id: UUID, cell_id: UUID, before: Optional[UUID] = None
    ):
        notebook = self.get_notebook(notebook_id)
        moving_cell = self.find_cell(notebook_id, cell_id)

        # Find the cell before the moving cell and save
        # it for undoing this move op
        undo_before_uuid = None
        cell_index = notebook.node.cells.index(moving_cell) + 1
        if cell_index < len(notebook.node.cells):
            # Otherwise, we're already in the last position
            # so undo_before_uuid should be None
            undo_before_uuid = notebook.node.cells[
                cell_index
            ].metadata.jupyter_d1.uuid

        # Find the before_cell before doing the removal
        # to make sure the cell exists before doing
        # anything destructive
        if before is None:
            before_cell = None
        else:
            before_cell = self.find_cell(notebook_id, before)

        notebook.node.cells.remove(moving_cell)
        if before_cell is None:
            notebook.node.cells.append(moving_cell)
        else:
            position = notebook.node.cells.index(before_cell)
            notebook.node.cells.insert(position, moving_cell)

        # Make sure the new cell has a uuid and positions are renumbered
        self.validator.validate(notebook.node)

        signal(CELL_UPDATE).send(
            cells=notebook.node.cells, notebook_id=notebook_id
        )

        kwargs = {
            "notebook_id": notebook_id,
            "cell_id": cell_id,
            "before": undo_before_uuid,
        }
        notebook.umanager.add_action(
            self.move_cell, kwargs=kwargs, name="Move Cell"
        )

    def create_cell(
        self,
        notebook_id: UUID,
        cell_type: CellType = CellType.code,
        source: str = "",
        before: Optional[UUID] = None,
        cell_id: Optional[UUID] = None,
    ) -> NotebookNode:
        notebook = self.get_notebook(notebook_id)

        if cell_type == CellType.code:
            new_cell = nbformat.v4.new_code_cell(source=source)
        elif cell_type == CellType.markdown:
            new_cell = nbformat.v4.new_markdown_cell(source=source)
        elif cell_type == CellType.raw:
            new_cell = nbformat.v4.new_raw_cell(source=source)
        else:
            new_cell = nbformat.v4.new_code_cell(source=source)

        if before is None:
            notebook.node.cells.append(new_cell)
        else:
            before_cell = self.find_cell(notebook_id, before)
            position = notebook.node.cells.index(before_cell)
            notebook.node.cells.insert(position, new_cell)

        if cell_id is not None:
            if new_cell.metadata.get("jupyter_d1") is None:
                new_cell.metadata.jupyter_d1 = {}
            new_cell.metadata.jupyter_d1.uuid = cell_id

        # Make sure the new cell has a uuid and positions are renumbered
        self.validator.validate(notebook.node)

        new_cell_id = new_cell.metadata.jupyter_d1.uuid

        signal(CELL_ADDED).send(
            cells=notebook.node.cells, notebook_id=notebook_id
        )

        kwargs = {
            "notebook_id": notebook_id,
            "cell_id": new_cell_id,
        }
        notebook.umanager.add_action(
            self.delete_cell, kwargs=kwargs, name="Create Cell"
        )
        return new_cell

    def merge_cells(
        self,
        notebook_id: UUID,
        cell_id: UUID,
        above: bool = False,
        insert_new_line: bool = True,
    ):
        notebook = self.get_notebook(notebook_id)
        merge_cell = self.find_cell(notebook_id, cell_id)

        merge_cell_idx = notebook.node.cells.index(merge_cell)
        source_template = "%s\n%s" if insert_new_line else "%s%s"
        if above:
            cell_index = merge_cell_idx - 1
            if cell_index >= 0:
                merging_cell = notebook.node.cells[cell_index]
            else:
                return
            split_location = len(merging_cell.source)
            merge_cell.source = source_template % (
                merging_cell.source,
                merge_cell.source,
            )
        else:
            cell_index = merge_cell_idx + 1
            if cell_index < len(notebook.node.cells):
                merging_cell = notebook.node.cells[cell_index]
            else:
                return
            split_location = len(merge_cell.source)
            merge_cell.source = source_template % (
                merge_cell.source,
                merging_cell.source,
            )
        split_cell_type = merging_cell.cell_type

        notebook.node.cells.remove(merging_cell)

        # Make sure the new cell has a uuid and positions are renumbered
        self.validator.validate(notebook.node)

        signal(CELL_DELETED).send(
            cells=notebook.node.cells, notebook_id=notebook_id
        )

        kwargs = {
            "notebook_id": notebook_id,
            "cell_id": cell_id,
            "split_location": split_location,
            "split_cell_type": CellType(split_cell_type),
            "above": above,
            "remove_new_line": insert_new_line,
        }
        notebook.umanager.add_action(
            self.split_cell, kwargs=kwargs, name="Merge Cells"
        )

    def split_cell(
        self,
        notebook_id: UUID,
        cell_id: UUID,
        split_location: int,
        split_cell_type: Optional[CellType] = None,
        above: bool = False,
        remove_new_line: bool = False,
    ):
        notebook = self.get_notebook(notebook_id)
        split_cell = self.find_cell(notebook_id, cell_id)

        split_cell_idx = notebook.node.cells.index(split_cell)
        top_source = split_cell.source[:split_location]
        bot_source = split_cell.source[split_location:]

        if remove_new_line and bot_source.startswith("\n"):
            bot_source = bot_source[1:]

        if above:
            new_cell_index = split_cell_idx
            new_cell_source = top_source
            split_cell_source = bot_source
        else:
            new_cell_index = split_cell_idx + 1
            new_cell_source = bot_source
            split_cell_source = top_source

        if split_cell_type is None:
            split_cell_type = CellType(split_cell.cell_type)
        if split_cell_type == CellType.code:
            new_cell = nbformat.v4.new_code_cell(source=new_cell_source)
        elif split_cell_type == CellType.markdown:
            new_cell = nbformat.v4.new_markdown_cell(source=new_cell_source)
        elif split_cell_type == CellType.raw:
            new_cell = nbformat.v4.new_raw_cell(source=new_cell_source)
        else:
            new_cell = nbformat.v4.new_code_cell(source=new_cell_source)

        split_cell.source = split_cell_source

        if new_cell_index >= len(notebook.node.cells):
            notebook.node.cells.append(new_cell)
        else:
            notebook.node.cells.insert(new_cell_index, new_cell)

        # Make sure the new cell has a uuid and positions are renumbered
        self.validator.validate(notebook.node)

        signal(CELL_UPDATE).send(
            cells=notebook.node.cells, notebook_id=notebook_id
        )

        kwargs = {
            "notebook_id": notebook_id,
            "cell_id": cell_id,
            "above": above,
            "insert_new_line": remove_new_line,
        }
        notebook.umanager.add_action(
            self.merge_cells, kwargs=kwargs, name="Split Cells"
        )

    async def handle_import_error(
        self, name: str, notebook_id: UUID, cell_id: Optional[UUID]
    ):
        missing_dependencies = await self.check_dependencies(
            notebook_id, cell_id=cell_id
        )

        signal(IMPORT_ERROR).send(
            notebook_id=notebook_id,
            cell_id=cell_id,
            missing_dependencies=sorted(missing_dependencies, key=str.lower),
        )

    def execute_d1_command(
        self, command: str, notebook_id: UUID, cell_id: Optional[UUID]
    ) -> Optional[Tuple[Callable, List[Any], Dict[str, Any]]]:
        """
        Attempts to parse command, and either executes it or returns a tuple of
        a Callable, args list, and kwargs dict to be executed later (i.e.
        when the invoking execution reaches an idle state)
        """
        try:
            command_dict = json.loads(command)
            command_type = D1CommandType(command_dict.get("command_type"))
            if command_type == D1CommandType.NOTIFY:
                execute_d1_notify(
                    command_dict["title"], command_dict["message"]
                )
            elif command_type == D1CommandType.HANDLE_IMPORT_ERROR:
                return (
                    self.handle_import_error,
                    [command_dict["name"], notebook_id, cell_id],
                    {},
                )
            elif command_type == D1CommandType.CLIENT_COMMAND_URL:
                url = command_dict.get("url", None)
                if url is not None:
                    signal(CLIENT_COMMAND).send(
                        notebook_id=notebook_id,
                        url=url,
                    )

        except Exception as e:
            logger.error(f"Error parsing d1 command {e}")
        return None

    def extract_d1_commands(
        self,
        output: NotebookNode,
        notebook_id: UUID,
        cell_id: Optional[UUID],
        notebook_command: NotebookCommand,
    ) -> NotebookNode:
        splits = output.text.split(D1_COMMAND_DELIMITER)
        split_len = len(splits)
        if split_len > 2:
            if split_len % 2 == 0:
                new_text = "".join(splits[::2] + [splits[-1]])
                commands = splits[1:-1:2]
            else:
                new_text = "".join(splits[::2])
                commands = splits[1::2]
            output.text = new_text
            for command in commands:
                future_command = self.execute_d1_command(
                    command, notebook_id=notebook_id, cell_id=cell_id
                )
                if future_command is not None:
                    notebook_command.post_execution.append(future_command)
        return output

    def create_and_send_cell_patch(
        self, original_cell, new_cell, cell_uuid, notebook_uuid
    ) -> List[JSONType]:
        patch = jsonpatch.make_patch(original_cell, new_cell)
        if len(patch.patch) > 0:
            signal(CELL_UPDATE_PATCH).send(
                patch=patch.patch, cell_id=cell_uuid, notebook_id=notebook_uuid
            )
        return patch.patch

    async def receive_channel_message(
        self, sender, msg, kernel_id, channel, **kwargs
    ):
        if kernel_id not in self.notebooks.keys():
            return
        logger.debug("nb_manager received channel message")
        if settings.LOG_KERNEL_MSGS:
            logger.debug(pprint.pformat(msg))
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

        command = self.msg_to_command.get(parent_id)
        if command is None:
            logger.debug(f"Msg ({parent_id}) not found in msg_to_command:")
            logger.debug(f"    {self.msg_to_command}")
            return

        nb_id = command.notebook_id
        cell_id = command.extras.get("cell_id", None)
        if command.type == CommandType.CELL_EXECUTION:
            cell = self.find_cell(command.notebook_id, cell_id)

        if msg_type == "execute_reply" and content is not None:
            if command.type == CommandType.CELL_EXECUTION:
                command.execution_count = content.get("execution_count", None)
                logger.debug(
                    f"nb_manager posting CELL_EXECUTION_REPLY - execute_reply"
                )
                status = content.get("status", None)
                signal(CELL_EXECUTION_REPLY).send(
                    cell_id=cell_id,
                    execution_count=command.execution_count,
                    status=status,
                    notebook_id=nb_id,
                    parent_id=parent_id,
                )
            if (
                "status" in content
                and content["status"] == "ok"
                and "payload" in content
            ):
                for payload_item in content["payload"]:
                    if payload_item["source"] == "page":
                        signal(PAYLOAD_PAGE).send(
                            msg_id=parent_id,
                            notebook_id=nb_id,
                            data=payload_item["data"],
                            start=payload_item.get(
                                "start",
                                payload_item.get("start_line_number", None),
                            ),
                        )
        elif msg_type == "execute_input":
            command.execution_count = content.get("execution_count", None)
            if command.type == CommandType.CELL_EXECUTION:
                signal(CELL_EXECUTION_INPUT).send(
                    notebook_id=nb_id,
                    parent_id=parent_id,
                    content=content,
                )
        elif (
            msg_type == "complete_reply"
            and command.type == CommandType.COMPLETE_REQUEST
            and content is not None
            and content.get("status") == "ok"
        ):
            logger.debug(f"nb_manager posting COMPLETE_REPLY - {msg_type}")
            signal(COMPLETE_REPLY).send(
                msg_id=parent_id,
                notebook_id=nb_id,
                matches=content["matches"],
                cursor_start=content["cursor_start"],
                cursor_end=content["cursor_end"],
                connection_id=command.connection_id,
                command_id=command.command_id,
            )
        elif msg_type == "history_reply" and content is not None:
            logger.debug(f"nb_manager posting HISTORY_REPLY - {msg_type}")
            signal(HISTORY_REPLY).send(
                msg_id=parent_id, notebook_id=nb_id, history=content["history"]
            )
        elif msg_type in ("execute_result", "error", "stream", "display_data"):
            output = nbformat.v4.output_from_msg(msg)
            if msg_type == "stream":
                # Suppress the stream output for internal commands
                suppress_stream_commands = [
                    CommandType.UPDATE_WORKDIR_REQUEST,
                    CommandType.VARS_REQUEST,
                    CommandType.VAR_DETAIL_REQUEST,
                    CommandType.UPDATE_WORKDIR_REQUEST,
                    CommandType.CHECK_DEPENDENCIES,
                ]
                if command.type not in suppress_stream_commands:
                    output = self.extract_d1_commands(
                        output,
                        notebook_id=nb_id,
                        cell_id=cell_id,
                        notebook_command=command,
                    )
            if command.type == CommandType.CELL_EXECUTION:
                original_cell = None
                if settings.CELL_UPDATE_PATCHES:
                    original_cell = deepcopy(cell)

                needs_update = self.append_cell_output(cell, output, command)
                if "execution_count" in output:
                    command.execution_count = output.execution_count
                    cell.execution_count = command.execution_count
                    needs_update = True

                if needs_update:
                    if settings.CELL_UPDATE_PATCHES:
                        self.create_and_send_cell_patch(
                            original_cell, cell, cell_id, nb_id
                        )
                    else:
                        logger.debug(
                            f"nb_manager posting CELL_UPDATE - {msg_type}"
                        )
                        signal(CELL_UPDATE).send(
                            cells=[cell], notebook_id=nb_id
                        )
            elif command.type == CommandType.SCRATCH_EXECUTION:
                logger.debug(f"nb_manager posting SCRATCH_UPDATE - {msg_type}")
                signal(SCRATCH_UPDATE).send(
                    msg_id=parent_id, notebook_id=nb_id, output=output
                )
            elif command.type == CommandType.VARS_REQUEST:
                vars_manager = self.get_vars_manager(nb_id)
                if (
                    output.output_type in ("stream", "display_data")
                    and vars_manager is not None
                ):
                    vars_manager.parse_output(output)
                elif output.output_type == "error":
                    logger.error(f"error during VARS_REQUEST: {output}")
            elif command.type == CommandType.VAR_DETAIL_REQUEST:
                vars_manager = self.get_vars_manager(nb_id)
                if (
                    output.output_type in ("stream", "display_data")
                    and vars_manager is not None
                ):
                    single_var = vars_manager.parse_single_var_response(output)
                    signal(VAR_DETAILS).send(
                        notebook_id=nb_id,
                        parent_msg_id=parent_id,
                        single_var=single_var,
                    )
            elif command.type == CommandType.CHECK_DEPENDENCIES:
                dep_checker = self.get_dependency_checker(nb_id)
                if (
                    output.output_type in ("stream", "display_data")
                    and dep_checker is not None
                ):
                    missing_deps = (
                        dep_checker.parse_check_dependencies_response(output)
                    )
                    signal(CHECK_DEPENDENCIES).send(
                        notebook_id=nb_id,
                        parent_msg_id=parent_id,
                        missing_dependencies=missing_deps,
                    )
                elif output.output_type == "error":
                    logger.error(
                        f"error checking dependencies: {output.ename}, "
                        f"{output.evalue}, {output.traceback}"
                    )
            elif command.type == CommandType.VAR_STATISTICS_REQUEST:
                vars_manager = self.get_vars_manager(nb_id)
                if (
                    output.output_type in ("stream", "display_data")
                    and vars_manager is not None
                ):
                    stats = vars_manager.parse_single_var_stats_response(
                        output
                    )
                    signal(VAR_STATISTICS).send(
                        notebook_id=nb_id,
                        parent_msg_id=parent_id,
                        stats=stats,
                    )
            elif command.type in (
                CommandType.UPDATE_WORKDIR_REQUEST,
                CommandType.CHANGE_WORKDIR_REQUEST,
            ):
                workdir_manager = self.get_workdir_manager(nb_id)
                if (
                    output.output_type in ("stream", "display_data")
                    and workdir_manager is not None
                ):
                    if command.type == CommandType.UPDATE_WORKDIR_REQUEST:
                        workdir_manager.parse_cwd_output(output)
                    elif command.type == CommandType.CHANGE_WORKDIR_REQUEST:
                        workdir_manager.parse_chdir_output(output)

        if msg_type == "status" and content is not None:

            execution_state = content.get(
                "execution_state"
            )  # busy/idle/starting
            if command.type == CommandType.CELL_EXECUTION:
                original_cell = None
                if settings.CELL_UPDATE_PATCHES:
                    original_cell = deepcopy(cell)

                cell.metadata.jupyter_d1["execution_state"] = execution_state
                if (
                    execution_state == ExecutionState.busy
                    and not command.extras["has_run"]
                ):
                    cell.outputs = []
                    # The has_run flag is used so we only reset the cell
                    # output the first time this cell is "busy" as a result of
                    # this particular Command (another "busy" status and a
                    # "shutdown_reply" message are emitted on behalf of this
                    # Command on kernel restart)
                    command.extras["has_run"] = True
                if execution_state == ExecutionState.idle:
                    cell.execution_count = command.execution_count
                if settings.CELL_UPDATE_PATCHES:
                    logger.debug(
                        "nb_manager posting CELL_UPDATE_PATCH - status"
                    )
                    self.create_and_send_cell_patch(
                        original_cell, cell, cell_id, nb_id
                    )
                else:
                    logger.debug("nb_manager posting CELL_UPDATE - status")
                    signal(CELL_UPDATE).send(cells=[cell], notebook_id=nb_id)
                if execution_state == ExecutionState.idle:
                    notebook = self.notebooks.get(nb_id, None)
                    if notebook is not None and notebook.autosave:
                        await self.save_notebook(uuid=nb_id)
            elif command.type == CommandType.SCRATCH_EXECUTION:
                logger.debug("nb_manager posting SCRATCH_UPDATE - status")
                command.extras["execution_state"] = ExecutionState(
                    execution_state
                )
                signal(SCRATCH_UPDATE).send(
                    msg_id=parent_id,
                    notebook_id=nb_id,
                    execution_state=execution_state,
                )
            elif command.type == CommandType.VARS_REQUEST:
                vars_manager = self.get_vars_manager(nb_id)
                if vars_manager is not None:
                    if execution_state == ExecutionState.busy:
                        vars_manager.on_request_start()
                    elif execution_state == ExecutionState.idle:
                        logger.debug(
                            f"nb_manager posting VARS_UPDATE - {msg_type}"
                        )
                        self.msg_to_command.pop(parent_id)
                        vars = vars_manager.on_request_end()
                        signal(VARS_UPDATE).send(notebook_id=nb_id, vars=vars)
                return
            elif command.type == CommandType.VAR_DETAIL_REQUEST:
                if execution_state == ExecutionState.idle:
                    self.msg_to_command.pop(parent_id)
                return
            elif command.type in (
                CommandType.UPDATE_WORKDIR_REQUEST,
                CommandType.CHANGE_WORKDIR_REQUEST,
            ):
                workdir_manager = self.get_workdir_manager(nb_id)
                if workdir_manager is not None:
                    if execution_state == ExecutionState.idle:
                        self.msg_to_command.pop(parent_id)
                        metadata = self.get_notebook_node(nb_id).metadata
                        resolved_workdir = str(
                            Path(workdir_manager.workdir).resolve()
                        )
                        if (
                            metadata.jupyter_d1.working_directory
                            != resolved_workdir
                        ):
                            logger.debug(
                                f"nb_manager posting METADATA_UPDATE - "
                                f"{msg_type}"
                            )
                            metadata.jupyter_d1.working_directory = (
                                resolved_workdir
                            )
                            notebook = self.notebooks.get(nb_id, None)
                            if notebook is not None and notebook.autosave:
                                await self.save_notebook(uuid=nb_id)
                            self.change_dav_workdir(nb_id, resolved_workdir)
                            signal(METADATA_UPDATE).send(
                                notebook_id=nb_id, metadata=metadata
                            )

            if execution_state == ExecutionState.idle:
                # If something just finished running, update last idle
                self.last_idle = datetime.utcnow()

                # Run any post-execution tasks
                while len(command.post_execution) > 0:
                    f, f_args, f_kwargs = command.post_execution.pop(0)
                    result = f(*f_args, **f_kwargs)
                    if inspect.isawaitable(result):
                        asyncio.create_task(result)

                # If it was user code that just finished running,
                # update kernel vars and working directory
                if command.type in (
                    CommandType.CELL_EXECUTION,
                    CommandType.SCRATCH_EXECUTION,
                ):
                    await self.update_kernel_workdir(nb_id)
                    await self.update_kernel_vars(nb_id)

    def is_idle(self):
        for notebook in self.notebooks.values():
            for cell in notebook.node.cells:
                if (
                    "execution_state" in cell.metadata.jupyter_d1
                    and cell.metadata.jupyter_d1.execution_state != "idle"
                ):
                    return False
        for command in self.msg_to_command.values():
            if command.extras.get("execution_state", None) not in (
                ExecutionState.idle,
                None,
            ):
                return False

        return True

    def append_cell_output(
        self, cell, output, command: NotebookCommand
    ) -> bool:
        """Returns false if no new text was written"""
        if "outputs" not in cell:
            cell.outputs = []

        # If the new output isn't a stream type, just append and skip the rest
        if output.output_type != "stream":
            cell.outputs.append(output)
            return True

        # We store stream cursor position on the command object
        cursor_line = 0
        cursor_position = 0
        stream_states = command.extras.get("stream_states", None)
        if stream_states is not None:
            state = stream_states.get(output.name, None)
            if state is not None:
                cursor_line = state.get("cursor_line", 0)
                cursor_position = state.get("cursor_position", 0)
            else:
                stream_states[output.name] = {}
        else:
            command.extras["stream_states"] = {}
            command.extras["stream_states"][output.name] = {}

        last_output = cell.outputs[-1] if len(cell.outputs) > 0 else None

        if last_output is None or last_output.name != output.name:
            # New list or not the same name, so add as new
            # 'normalize' whatever jupyter kernel spit out
            (
                output.text,
                cursor_line,
                cursor_position,
                text_changed,
            ) = self.handle_special_characters(
                "",
                output.text,
                cursor_line=cursor_line,
                cursor_position=cursor_position,
            )
            cell.outputs.append(output)
        else:
            (
                new_multi,
                cursor_line,
                cursor_position,
                text_changed,
            ) = self.handle_special_characters(
                last_output.text,
                output.text,
                cursor_line=cursor_line,
                cursor_position=cursor_position,
            )
            last_output.text = new_multi

        command.extras["stream_states"][output.name][
            "cursor_line"
        ] = cursor_line
        command.extras["stream_states"][output.name][
            "cursor_position"
        ] = cursor_position

        return text_changed

    def handle_special_characters(
        self, existing_text, new_text, cursor_line=0, cursor_position=0
    ):
        """
        Appends new stream text to existing stream text, handling newlines
        and carriage returns (not ANSI codes)
        """
        # Note: Not handling a list of strings that contain newline characters
        # in the "existing_text",
        # they should have been stripped out by previous calls to this method
        if isinstance(existing_text, str):
            lines = existing_text.split("\n")
        else:
            # Strip off newlines, we'll add them back later
            lines = [t[:-1] if t.endswith("\n") else t for t in existing_text]

        if isinstance(new_text, list):
            new_text = "\n".join(new_text)

        str_position = 0
        # Keeps track of whether any actual text was written, because sometimes the
        # cursor just moves around
        text_changed = False
        # Stick a dummy match on the end to append the remaining unmatched text
        for match in chain(re.finditer(pattern, new_text), iter([None])):
            # Write the chunk of text that came before the match first
            if match is None:
                chunk = new_text[str_position:]
            else:
                chunk = new_text[str_position:match.start()]
                str_position = match.end()
            if len(chunk) > 0:
                chunk_len = len(chunk)
                # If cursor_position is out of bounds for some reason,
                # set it to last line
                if cursor_line > len(lines) - 1:
                    cursor_line = len(lines) - 1
                line = lines[cursor_line]

                line_len = len(line)
                new_line = ""

                # If cursor_position is greater than length of line, pad with whitespace
                if cursor_position > line_len:
                    line += " " * (cursor_position - line_len)
                new_line = line[0:cursor_position]
                new_line += chunk
                if line_len > cursor_position + chunk_len:
                    new_line += line[cursor_position + chunk_len:]
                cursor_position += chunk_len
                lines[cursor_line] = new_line

                text_changed = True

            if match is None:
                continue

            groups = match.groups()
            if groups[0] == "\n":
                if cursor_line == len(lines) - 1:
                    lines.append("")
                    text_changed = True
                cursor_line += 1
                cursor_position = 0
            elif groups[0] == "\r":
                cursor_position = 0

        return (
            [line + "\n" for line in lines],
            cursor_line,
            cursor_position,
            text_changed,
        )

    def multiline_to_list(self, blob):
        # If the blob is just a string, promote it to a list of strings,
        # otherwise assume it is already a list of strings
        if isinstance(blob, str):
            blob = [blob]
        return blob

    def append_to_multiline(self, blob, newBlob):
        blob = self.multiline_to_list(blob)
        newBlob = self.multiline_to_list(newBlob)
        blob.extend(newBlob)

        return blob
