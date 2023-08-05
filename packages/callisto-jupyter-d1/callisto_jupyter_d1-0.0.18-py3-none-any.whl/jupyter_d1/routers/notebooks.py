import asyncio
import json
from os import path
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from uuid import UUID, uuid4

import jsonschema
from asyncblink import signal  # type: ignore
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Body,
    Depends,
    HTTPException,
    Query,
    Request,
    Response,
    WebSocket,
    status,
)
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from jupyter_d1.signals import (
    CELL_ADDED,
    CELL_DELETED,
    CELL_EXECUTION_INPUT,
    CELL_EXECUTION_REPLY,
    CELL_EXECUTION_REQUEST,
    CELL_UPDATE,
    CELL_UPDATE_PATCH,
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
    PAYLOAD_PAGE,
    SCRATCH_UPDATE,
    SHELL_CHANNEL,
    STDIN_CHANNEL,
    VARS_UPDATE,
)

from ..d1_response import D1Encoder, D1Response
from ..deps import read_access_websocket, write_access, write_access_websocket
from ..logger import logger
from ..models.cell import (
    CellAdd,
    CellKernelMessageWrapper,
    CellsWrapper,
    CellUpdate,
    CellWrapper,
)
from ..models.code_complete import CodeComplete
from ..models.dependency import MissingDependenciesWrapper
from ..models.kernel_message import (
    KernelMessage,
    KernelMessagesWrapper,
    KernelMessageWrapper,
)
from ..models.kernel_variable import (
    KernelVariable,
    KernelVariableStats,
    KernelVariablesWrapper,
    KernelVariableWrapper,
)
from ..models.notebook import (
    Filter,
    MetadataWrapper,
    NotebookPath,
    NotebooksWrapper,
    NotebookWrapper,
)
from ..models.scratch import ScratchCode
from ..settings import settings
from ..storage import manager
from ..utils import (
    NotebookNode,
    add_to_dict_metadata,
    websocket_poll,
    websocket_send_and_receive,
)

router = APIRouter(default_response_class=D1Response)


@router.get("", response_model=NotebooksWrapper)
async def get_notebooks():
    notebooks = manager.get_notebooks_dicts()
    return NotebooksWrapper(notebooks=notebooks)


@router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(write_access)],
)
async def delete_notebooks():
    await manager.delete_notebooks()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{uuid}", response_model=NotebookWrapper)
async def get_notebook(uuid: UUID):
    notebook = manager.get_notebook_dict(uuid)
    return NotebookWrapper(notebook=notebook)


@router.delete(
    "/{uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(write_access)],
)
async def delete_notebook(uuid: UUID):
    await manager.delete_notebook(uuid)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{uuid}/cells", response_model=CellsWrapper)
async def get_notebook_cells(uuid: UUID):
    node = manager.get_notebook_node(uuid)
    if node is not None:
        cells = node.cells
    else:
        raise HTTPException(
            status_code=404, detail=f"Notebook not found for id {uuid}"
        )
    return CellsWrapper(cells=cells)


def schedule_notebook_save(background_tasks: BackgroundTasks, uuid: UUID):
    if manager.get_notebook(uuid).autosave:
        background_tasks.add_task(manager.save_notebook, uuid=uuid)


@router.post(
    "/{uuid}/cells",
    status_code=status.HTTP_201_CREATED,
    response_model=CellWrapper,
    dependencies=[Depends(write_access)],
)
async def create_notebook_cell(
    uuid: UUID, cell_add: Optional[CellAdd], background_tasks: BackgroundTasks
) -> Any:
    """Create a new cell with type `cell_type` and source code of `source`.

    The `before` parameter is the uuid of the cell will be inserted
    before.
    If `before`
    is omitted, the cell will be added as the last cell.
    """
    if cell_add is None:
        cell_add = CellAdd()
    new_cell = manager.create_cell(
        notebook_id=uuid,
        cell_type=cell_add.cell_type,
        source=cell_add.source,
        before=cell_add.before,
    )
    schedule_notebook_save(background_tasks, uuid=uuid)
    return CellWrapper(cell=new_cell)


@router.get(
    "/{uuid}/cells/{cell_uuid}/move",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(write_access)],
)
async def move_notebook_cell(
    uuid: UUID,
    cell_uuid: UUID,
    background_tasks: BackgroundTasks,
    before: Optional[UUID] = None,
):
    """Move an existing cell with uuid `cell_uuid` to the slot before
    the cell with uuid `before`.
    If `before`
    is omitted, the cell will be moved to the end of the cell list.
    """
    manager.move_cell(notebook_id=uuid, cell_id=cell_uuid, before=before)
    schedule_notebook_save(background_tasks, uuid=uuid)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{uuid}/cells/{cell_uuid}/merge",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(write_access)],
)
async def merge_notebook_cells(
    uuid: UUID,
    cell_uuid: UUID,
    background_tasks: BackgroundTasks,
    above: bool = False,
):
    """Merge a cell with the cell above or below it."""
    manager.merge_cells(notebook_id=uuid, cell_id=cell_uuid, above=above)
    schedule_notebook_save(background_tasks, uuid=uuid)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{uuid}/cells/{cell_uuid}/split",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(write_access)],
)
async def split_notebook_cell(
    uuid: UUID,
    cell_uuid: UUID,
    background_tasks: BackgroundTasks,
    split_location: int,
):
    """Split a cell at the location specified by split_location."""
    manager.split_cell(
        notebook_id=uuid, cell_id=cell_uuid, split_location=split_location
    )
    schedule_notebook_save(background_tasks, uuid=uuid)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{uuid}/cells/{cell_id}/clear",
    dependencies=[Depends(write_access)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def clear_single_cell(uuid: UUID, cell_id: UUID):
    cell = manager.find_cell(uuid, cell_id)
    manager.clear_single_cell(uuid, cell)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{uuid}/undo",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(write_access)],
)
async def undo_notebook_operation(
    uuid: UUID, background_tasks: BackgroundTasks
):
    "Undo the last operaton on the notebook with given UUID."
    manager.undo(uuid)
    schedule_notebook_save(background_tasks, uuid=uuid)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{uuid}/redo",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(write_access)],
)
async def redo_notebook_operation(
    uuid: UUID, background_tasks: BackgroundTasks
):
    "Redo the last operaton on the notebook with given UUID."
    manager.redo(uuid)
    schedule_notebook_save(background_tasks, uuid=uuid)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/{uuid}/cells/{cell_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(write_access)],
)
async def delete_notebook_cell(
    uuid: UUID, cell_uuid: UUID, background_tasks: BackgroundTasks
):
    manager.delete_cell(uuid, cell_uuid)
    schedule_notebook_save(background_tasks, uuid=uuid)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{uuid}/cells/{cell_uuid}", response_model=CellWrapper)
async def get_notebook_cell(uuid: UUID, cell_uuid: UUID) -> Any:
    cell = manager.find_cell(uuid, cell_uuid)
    return CellWrapper(cell=cell)


@router.get(
    "/{uuid}/cells/{cell_uuid}/execute",
    dependencies=[Depends(write_access)],
    response_model=KernelMessageWrapper,
)
async def execute_notebook_cell(uuid: UUID, cell_uuid: UUID):
    msg_id = await manager.execute(uuid, cell_uuid)
    return KernelMessageWrapper(
        kernel_message=KernelMessage(message_id=msg_id)
    )


@router.get(
    "/{uuid}/interrupt_kernel",
    dependencies=[Depends(write_access)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def interrupt_kernel(uuid: UUID):
    await manager.interrupt_kernel(uuid)


@router.get(
    "/{uuid}/restart_kernel",
    dependencies=[Depends(write_access)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def restart_kernel(uuid: UUID):
    await manager.restart_kernel(uuid)


@router.get(
    "/{uuid}/restart_kernel_and_clear_output",
    dependencies=[Depends(write_access)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def restart_kernel_and_clear_output(uuid: UUID):
    await manager.restart_kernel(uuid, clear_output=True)


@router.get(
    "/{uuid}/restart_kernel_and_execute_all",
    dependencies=[Depends(write_access)],
    response_model=KernelMessagesWrapper,
)
async def restart_kernel_and_execute_all(uuid: UUID):
    msg_ids = await manager.restart_kernel_and_run_all_cells(uuid)
    return KernelMessagesWrapper(
        kernel_messages=[
            KernelMessage(message_id=msg_id) for msg_id in msg_ids
        ]
    )


@router.get(
    "/{uuid}/execute_all",
    dependencies=[Depends(write_access)],
    response_model=KernelMessagesWrapper,
)
async def execute_all(
    uuid: UUID,
    above_position: Optional[int] = None,
    below_position: Optional[int] = None,
):
    msg_ids = await manager.execute_all(uuid, above_position, below_position)
    return KernelMessagesWrapper(
        kernel_messages=[
            KernelMessage(message_id=msg_id) for msg_id in msg_ids
        ]
    )


@router.get(
    "/{uuid}/clear_all",
    dependencies=[Depends(write_access)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def clear_all_cells(uuid: UUID):
    notebook = manager.get_notebook(uuid)
    manager.clear_multiple_cells(notebook, uuid)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/{uuid}/scratch_execute",
    dependencies=[Depends(write_access)],
    response_model=KernelMessageWrapper,
)
async def execute_notebook_scratch(uuid: UUID, scratch_code: ScratchCode):
    msg_id = await manager.execute_scratch(uuid, scratch_code.code)
    return KernelMessageWrapper(
        kernel_message=KernelMessage(message_id=msg_id)
    )


@router.post(
    "/{uuid}/complete",
    dependencies=[Depends(write_access)],
    response_model=KernelMessageWrapper,
)
async def notebook_code_completion(uuid: UUID, code: CodeComplete):
    msg_id = await manager.complete(uuid, code.code, code.cursor_position)
    return KernelMessageWrapper(
        kernel_message=KernelMessage(message_id=msg_id)
    )


@router.post("/{uuid}/history", response_model=KernelMessageWrapper)
async def notebook_history(uuid: UUID):
    msg_id = await manager.history(uuid)
    return KernelMessageWrapper(
        kernel_message=KernelMessage(message_id=msg_id)
    )


@router.get(
    "/{uuid}/vars",
    dependencies=[Depends(write_access)],
    response_model=KernelVariablesWrapper,
)
async def get_notebook_vars(uuid: UUID):
    """Get a list of vars defined in the kernel."""
    vars = await manager.get_vars(uuid)
    return KernelVariablesWrapper(vars=vars)


@router.get(
    "/{uuid}/vars/{var_name}",
    dependencies=[Depends(write_access)],
    response_model=KernelVariableWrapper,
)
async def get_notebook_single_var(
    uuid: UUID, var_name: str, page_size: Optional[int] = -1, page: int = 0
):
    """Get details on a single var defined in the kernel."""
    if page_size is None or page_size == 0:
        page_size = None
    elif page_size < 0:
        page_size = settings.VAR_DEFAULT_PAGE_SIZE
    single_var = await manager.get_kernel_var_details(
        uuid, var_name, page_size=page_size, page=page
    )
    if single_var is None:
        raise HTTPException(404, f"Variable {var_name} not found")
    return KernelVariableWrapper(single_var=single_var)


@router.post(
    "/{uuid}/vars/{var_name}",
    dependencies=[Depends(write_access)],
    response_model=KernelVariableWrapper,
)
async def get_notebook_single_var_sorted(
    uuid: UUID,
    var_name: str,
    page_size: Optional[int] = -1,
    page: int = 0,
    sort_by: Optional[List[Union[str, int]]] = Body(default=None),
    ascending: Optional[List[bool]] = Body(default=None),
    filters: Optional[List[Filter]] = Body(default=None),
):
    """Get details on a single var defined in the kernel, with sorting/filtering."""
    if page_size is None or page_size == 0:
        page_size = None
    elif page_size < 0:
        page_size = settings.VAR_DEFAULT_PAGE_SIZE
    single_var = await manager.get_kernel_var_details(
        uuid,
        var_name,
        page_size=page_size,
        page=page,
        sort_by=sort_by,
        ascending=ascending,
        filters=filters,
    )
    if single_var is None:
        raise HTTPException(404, f"Variable {var_name} not found")
    return KernelVariableWrapper(single_var=single_var)


@router.get(
    "/{uuid}/check_dependencies",
    dependencies=[Depends(write_access)],
    response_model=MissingDependenciesWrapper,
)
async def check_dependencies(uuid: UUID):
    """Check dependencies in a notebook."""
    missing_dependencies = await manager.check_dependencies(uuid)
    return MissingDependenciesWrapper(
        missing_dependencies=sorted(missing_dependencies, key=str.lower)
    )


@router.get(
    "/{uuid}/vars/{var_name}/stats",
    dependencies=[Depends(write_access)],
    response_model=KernelVariableStats,
)
async def get_notebook_var_stats(uuid: UUID, var_name: str):
    """Get statistical summary for a variable"""
    stats = await manager.get_kernel_var_statistics(uuid, var_name)
    if stats is None:
        raise HTTPException(
            404, f"Unable to get statistical data for {var_name}"
        )
    return stats


@router.get(
    "/{uuid}/vars/{var_name}/stats/{column}",
    dependencies=[Depends(write_access)],
    response_model=KernelVariableStats,
)
async def get_notebook_var_stats_single_column(
    uuid: UUID, var_name: str, column: str
):
    """Get statistical summary for a variable"""
    stats = await manager.get_kernel_var_statistics(uuid, var_name, column)
    if stats is None:
        raise HTTPException(
            404,
            f"Unable to get statistical data for {var_name}, column={column}",
        )
    return stats


@router.patch(
    "/{uuid}/cells/{cell_uuid}",
    response_model=CellWrapper,
    dependencies=[Depends(write_access)],
)
async def patch_notebook_cell(
    uuid: UUID,
    cell_uuid: UUID,
    cell_update: CellUpdate,
    background_tasks: BackgroundTasks,
) -> Any:
    cell = manager.update_cell(uuid, cell_uuid, cell_update)
    schedule_notebook_save(background_tasks, uuid=uuid)
    return CellWrapper(
        cell=cell if not settings.CELL_UPDATE_PATCHES else None,
        patch=cell if settings.CELL_UPDATE_PATCHES else None,
    )


@router.patch(
    "/{uuid}/cells/{cell_uuid}/execute",
    dependencies=[Depends(write_access)],
    response_model=CellKernelMessageWrapper,
)
async def patch_and_execute_notebook_cell(
    uuid: UUID,
    cell_uuid: UUID,
    cell_update: CellUpdate,
    background_tasks: BackgroundTasks,
):
    cell = manager.update_cell(uuid, cell_uuid, cell_update)
    msg_id = await manager.execute(uuid, cell_uuid)
    schedule_notebook_save(background_tasks, uuid=uuid)
    return CellKernelMessageWrapper(
        cell=cell if not settings.CELL_UPDATE_PATCHES else None,
        patch=cell if settings.CELL_UPDATE_PATCHES else None,
        kernel_message=KernelMessage(message_id=msg_id),
    )


@router.patch(
    "/{uuid}/change_working_directory",
    dependencies=[Depends(write_access)],
    response_model=KernelMessageWrapper,
)
async def change_working_directory(uuid: UUID, directory: str):
    if not path.exists(directory):
        raise HTTPException(404, "Directory does not exist")
    msg_id = await manager.change_kernel_workdir(uuid, directory=directory)
    return KernelMessageWrapper(
        kernel_message=KernelMessage(message_id=msg_id)
    )


def format_file_path(
    directory: Optional[str],
    filename: str,
    allow_exists: bool = False,
) -> Dict[str, str]:
    """
    Gets absolute path for file, filename with extension, checks that directory
    exists, and makes sure file doesn't already exist.
    """
    filedir = Path(settings.ROOT_DIR)
    file_path_obj = Path(filename).with_suffix(".ipynb")
    relative_path = file_path_obj
    if directory is not None:
        directory_path = Path(directory)
        if directory_path.is_absolute():
            filedir = directory_path
        else:
            filedir = filedir / directory_path
        relative_path = directory_path / relative_path
    if not filedir.exists():
        raise HTTPException(
            status_code=404, detail=f"Directory does not exist {str(filedir)}"
        )
    filepath = filedir / file_path_obj
    if not allow_exists and filepath.exists():
        raise HTTPException(status_code=400, detail=f"File already exists")
    return {
        "directory": str(filedir),
        "filename": file_path_obj.stem,
        "relative_path": str(relative_path),
        "absolute_path": str(filepath),
    }


@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(write_access)],
    response_model=NotebookPath,
)
async def upload_notebook(
    request: Request, filename: str, directory: Optional[str] = None
) -> Any:
    body = await request.body()
    path_info = format_file_path(directory, filename)
    try:
        await manager.upload_notebook(
            body, path_info["directory"], path_info["filename"]
        )
    except (jsonschema.exceptions.ValidationError, AttributeError) as e:
        raise HTTPException(400, f"Failed to parse notebook: {type(e)} {e}")
    return NotebookPath(path=path_info["relative_path"])


@router.post(
    "/upload_and_open",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(write_access)],
    response_model=NotebookWrapper,
)
async def upload_and_open_notebook(
    request: Request,
    filename: Optional[str] = None,
    directory: Optional[str] = None,
    kspec_name: Optional[str] = None,
    working_directory: Optional[str] = None,
    autosave: bool = True,
) -> Any:
    body = await request.body()

    if filename is not None:
        # If not autosaving allow the file to exists
        path_info = format_file_path(
            directory, filename, allow_exists=not autosave
        )
        directory = path_info["directory"]
        filename = path_info["filename"]
    if directory is None:
        directory = settings.ROOT_DIR
    try:
        nb_uuid = await manager.add_notebook_json(
            body,
            kspec_name=kspec_name,
            directory=directory,
            filename=filename,
            working_directory=working_directory,
            autosave=autosave,
        )

        nb = manager.get_notebook_node(nb_uuid)
        return NotebookWrapper(notebook=nb.dict())
    except (jsonschema.exceptions.ValidationError, AttributeError) as e:
        raise HTTPException(400, f"Failed to parse notebook: {type(e)} {e}")


@router.get(
    "/open/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(write_access)],
    response_model=NotebookWrapper,
)
async def open_notebook(
    filepath: str,
    kspec_name: Optional[str] = None,
    working_directory: Optional[str] = None,
):
    abs_path = (
        f"{settings.ROOT_DIR}/{filepath}"
        if not filepath.startswith("/")
        else filepath
    )
    if not path.exists(abs_path):
        raise HTTPException(status_code=404, detail=f"File not found")
    try:
        nb_uuid = await manager.open_notebook(
            abs_path,
            kspec_name=kspec_name,
            working_directory=working_directory,
        )

        nb = manager.get_notebook_node(nb_uuid)
        return NotebookWrapper(notebook=nb.dict())

    except (jsonschema.exceptions.ValidationError, AttributeError) as e:
        raise HTTPException(400, f"Failed to parse notebook: {type(e)} {e}")


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(write_access)],
    response_model=NotebookWrapper,
)
async def create_notebook(
    request: Request,
    filename: str,
    directory: Optional[str] = None,
    kspec_name: Optional[str] = None,
    working_directory: Optional[str] = None,
):
    path_info = format_file_path(directory, filename)
    nb = await manager.create_notebook(
        kspec_name=kspec_name,
        directory=path_info["directory"],
        filename=path_info["filename"],
        working_directory=working_directory,
    )
    return NotebookWrapper(notebook=nb.dict())


@router.get(
    "/metadata/",
    status_code=status.HTTP_200_OK,
    response_model=MetadataWrapper,
)
async def get_metadata(
    filepath: str,
):
    abs_path = (
        f"{settings.ROOT_DIR}/{filepath}"
        if not filepath.startswith("/")
        else filepath
    )
    if not path.exists(abs_path):
        raise HTTPException(status_code=404, detail=f"File not found")
    try:
        metadata = manager.get_metadata(abs_path)
        return MetadataWrapper(metadata=metadata.dict())
    except (jsonschema.exceptions.ValidationError, AttributeError) as e:
        raise HTTPException(400, f"Failed to parse notebook: {type(e)} {e}")


@router.patch(
    "/{uuid}/save_as",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(write_access)],
    response_model=NotebookPath,
)
async def save_notebook_as(
    uuid: UUID,
    filename: str,
    directory: Optional[str] = None,
    overwrite: bool = False,
):
    path_info = format_file_path(directory, filename, overwrite)
    await manager.save_notebook_as(
        uuid, path_info["directory"], path_info["filename"]
    )
    return NotebookPath(path=path_info["absolute_path"])


@router.patch(
    "/{uuid}/rename",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(write_access)],
    response_model=NotebookPath,
)
async def rename_notebook(
    uuid: UUID,
    filename: str,
    directory: Optional[str] = None,
    overwrite: bool = False,
    just_metadata: bool = Query(
        False,
        description="Just update the in-memory"
        " notebook's metadata, dont save or delete any files. Used by the local "
        "environment on Callisto Mac/iPad, where file operations are handled in "
        "swift",
    ),
):
    """
    Rename a notebook, save it, and update it's name and path in its metadata
    """
    path_info = format_file_path(
        directory, filename, overwrite or just_metadata
    )
    await manager.save_notebook_as(
        uuid,
        path_info["directory"],
        path_info["filename"],
        delete_old=not just_metadata,
        just_metadata=just_metadata,
    )
    return NotebookPath(path=path_info["absolute_path"])


@router.websocket("/{uuid}/ws/stream")
async def websocket_stream(
    uuid: UUID,
    websocket: WebSocket,
    read_access: bool = Depends(read_access_websocket),
):
    await websocket.accept()
    msgs = []

    async def receive_channel_message(
        sender, msg, kernel_id, channel, **kwargs
    ):
        if kernel_id == uuid:
            # Add the 'channel' attribute since we're multiplex all of this
            # on one websocket (like the jupyter-kernel-gateway)
            msg["channel"] = channel

            # add the cell id to the metadata if avaiable
            parent_id = None
            if msg.get("parent_header") is not None:
                parent_id = msg["parent_header"].get("msg_id")
            if parent_id is not None:
                id_tuple = manager.notebook_cell_id_for_message_id(parent_id)
                if id_tuple is not None:
                    (nb_id, cell_id) = id_tuple
                    add_to_dict_metadata(msg, cell_uuid=cell_id)

            json_string = json.dumps(msg, cls=D1Encoder)
            msgs.append(json_string)

    signal(IOPUB_CHANNEL).connect(receive_channel_message)
    signal(SHELL_CHANNEL).connect(receive_channel_message)
    signal(STDIN_CHANNEL).connect(receive_channel_message)
    signal(HB_CHANNEL).connect(receive_channel_message)
    signal(CONTROL_CHANNEL).connect(receive_channel_message)

    await websocket_poll(websocket, msgs)


class UnsupportedWebsocketCommand(Exception):
    pass


@router.websocket("/{uuid}/ws/notebook")
async def websocket_cells(
    uuid: UUID,
    websocket: WebSocket,
    write_access: bool = Depends(write_access_websocket),
):
    await websocket.accept()
    msg_queue: asyncio.queues.Queue = asyncio.queues.Queue()
    ws_connection_id = uuid4()

    async def receive_cell_update(sender, cells, notebook_id, **kwargs):
        logger.debug("receiving CELL_UPDATE")
        if notebook_id == uuid:
            wrapper_dict = {"cell_update": cells}
            msg_queue.put_nowait(wrapper_dict)

    signal(CELL_UPDATE).connect(receive_cell_update)

    async def receive_cell_update_patch(
        sender, patch, cell_id, notebook_id, **kwargs
    ):
        logger.debug("receiving CELL_UPDATE_PATCH")
        if notebook_id == uuid:
            wrapper_dict = {
                "cell_update_patch": {
                    "cell_id": cell_id,
                    "patch": patch,
                }
            }
            msg_queue.put_nowait(wrapper_dict)

    signal(CELL_UPDATE_PATCH).connect(receive_cell_update_patch)

    async def receive_cell_added(sender, cells, notebook_id, **kwargs):
        logger.debug("receiving CELL_ADDED")
        if notebook_id == uuid:
            wrapper_dict = {"cell_add": cells}
            msg_queue.put_nowait(wrapper_dict)

    signal(CELL_ADDED).connect(receive_cell_added)

    async def receive_cell_deleted(sender, cells, notebook_id, **kwargs):
        logger.debug("receiving CELL_DELETED")
        if notebook_id == uuid:
            wrapper_dict = {"cell_delete": cells}
            msg_queue.put_nowait(wrapper_dict)

    signal(CELL_DELETED).connect(receive_cell_deleted)

    async def receive_cell_execution_reply(
        sender,
        execution_count,
        status,
        notebook_id,
        cell_id,
        parent_id,
        **kwargs,
    ):
        logger.debug("receiving CELL_EXECUTION_REPLY")
        if notebook_id == uuid:
            wrapper_dict = {
                "cell_execution_reply": {
                    "cell_id": cell_id,
                    "execution_count": execution_count,
                    "status": status,
                    "parent_id": parent_id,
                }
            }
            msg_queue.put_nowait(wrapper_dict)

    signal(CELL_EXECUTION_REPLY).connect(receive_cell_execution_reply)

    async def receive_cell_execution_input(
        sender, notebook_id, parent_id, content, **kwargs
    ):
        logger.debug("receiving CELL_EXECUTION_INPUT")
        if notebook_id == uuid:
            wrapper_dict = {
                "cell_execution_input": {
                    "content": content,
                    "parent_id": parent_id,
                }
            }
            msg_queue.put_nowait(wrapper_dict)

    signal(CELL_EXECUTION_INPUT).connect(receive_cell_execution_input)

    async def receive_cell_execution_request(
        sender, notebook_id, cell_id, msg_id, **kwargs
    ):
        logger.debug("receiving CELL_EXECUTION_REQUEST")
        if notebook_id == uuid:
            wrapper_dict = {
                "cell_execution_request": {
                    "cell_id": cell_id,
                    "message_id": msg_id,
                }
            }
            msg_queue.put_nowait(wrapper_dict)

    signal(CELL_EXECUTION_REQUEST).connect(receive_cell_execution_request)

    async def receive_scratch_update(
        sender: Any,
        msg_id: UUID,
        notebook_id: UUID,
        output: Optional[NotebookNode] = None,
        execution_state: Optional[str] = None,
        **kwargs,
    ):
        logger.debug("receiving SCRATCH_UPDATE")
        if notebook_id == uuid:
            scratch_update: Dict[str, Any] = {"message_id": msg_id}
            if output is not None:
                scratch_update["output"] = output
            if execution_state is not None:
                scratch_update["execution_state"] = execution_state
            wrapper_dict = {"scratch_update": scratch_update}
            msg_queue.put_nowait(wrapper_dict)

    signal(SCRATCH_UPDATE).connect(receive_scratch_update)

    async def receive_vars_update(
        sender: Any, notebook_id: UUID, vars: List[KernelVariable], **kwargs
    ):
        logger.debug("receiving VARS_UPDATE")
        if notebook_id == uuid:
            wrapper_dict = {"vars": jsonable_encoder(vars)}
            msg_queue.put_nowait(wrapper_dict)

    signal(VARS_UPDATE).connect(receive_vars_update)

    async def receive_import_error(
        sender: Any,
        notebook_id: UUID,
        cell_id: UUID,
        missing_dependencies: List[str],
        **kwargs,
    ):
        logger.debug("receiving IMPORT_ERROR")
        if notebook_id == uuid:
            wrapper_dict = {
                "import_error": {
                    "cell_id": cell_id,
                    "missing_dependencies": missing_dependencies,
                }
            }
            msg_queue.put_nowait(wrapper_dict)

    signal(IMPORT_ERROR).connect(receive_import_error)

    async def receive_page_payload(
        sender: Any,
        msg_id: UUID,
        notebook_id: UUID,
        data: Dict[str, Any],
        start: Optional[int],
        connection_id: Optional[UUID] = None,
        **kwargs,
    ):
        logger.debug("receiving PAYLOAD_PAGE")
        if notebook_id == uuid and (
            connection_id is None or connection_id == ws_connection_id
        ):
            wrapper_dict = {
                "payload_page": {
                    "data": data,
                    "start": start,
                    "message_id": msg_id,
                }
            }
            msg_queue.put_nowait(wrapper_dict)

    signal(PAYLOAD_PAGE).connect(receive_page_payload)

    async def receive_code_complete_reply(
        sender: Any,
        msg_id: UUID,
        notebook_id: UUID,
        matches: List[str],
        cursor_start: int,
        cursor_end: int,
        connection_id: Optional[UUID] = None,
        command_id: Optional[str] = None,
        **kwargs,
    ):
        logger.debug("receiving COMPLETE_REPLY")
        if notebook_id == uuid and (
            connection_id is None or connection_id == ws_connection_id
        ):
            wrapper_dict = {
                "complete_reply": {
                    "matches": matches,
                    "cursor_start": cursor_start,
                    "cursor_end": cursor_end,
                    "message_id": msg_id,
                    "command_id": command_id,
                }
            }
            msg_queue.put_nowait(wrapper_dict)

    signal(COMPLETE_REPLY).connect(receive_code_complete_reply)

    async def receive_history_reply(
        sender: Any,
        msg_id: UUID,
        notebook_id: UUID,
        history: List[Any],
        connection_id: Optional[UUID] = None,
        **kwargs,
    ):
        logger.debug("receiving HISTORY_REPLY")
        if notebook_id == uuid and (
            connection_id is None or connection_id == ws_connection_id
        ):
            wrapper_dict = {
                "history_reply": {
                    "history": [
                        {
                            "line_number": item[1],
                            "input": item[2][0],
                            "output": item[2][1],
                        }
                        for item in history
                    ],
                    "message_id": msg_id,
                }
            }
            msg_queue.put_nowait(wrapper_dict)

    signal(HISTORY_REPLY).connect(receive_history_reply)

    async def receive_metadata_update_reply(
        sender: Any, notebook_id: UUID, metadata: NotebookNode, **kwargs
    ):
        logger.debug("receiving METADATA_UPDATE")
        if notebook_id == uuid:
            wrapper_dict = {"metadata": metadata}
            msg_queue.put_nowait(wrapper_dict)

    signal(METADATA_UPDATE).connect(receive_metadata_update_reply)

    async def receive_kernel_restarted(
        sender: Any,
        cells: List[NotebookNode],
        notebook_id: UUID,
        run_all_cells: bool,
        **kwargs,
    ):
        logger.debug("receiving KERNEL_RESTARTED")
        if notebook_id == uuid:
            wrapper_dict = {
                "kernel_restarted": {
                    "run_all_cells": run_all_cells,
                    "cells": cells,
                }
            }
            msg_queue.put_nowait(wrapper_dict)

    signal(KERNEL_RESTARTED).connect(receive_kernel_restarted)

    async def receive_kernel_interrupted(
        sender: Any,
        notebook_id: UUID,
        **kwargs,
    ):
        logger.debug("receiving KERNEL_INTERRUPTED")
        if notebook_id == uuid:
            wrapper_dict = {"kernel_interrupted": {"interrupted": True}}
            msg_queue.put_nowait(wrapper_dict)

    signal(KERNEL_INTERRUPTED).connect(receive_kernel_interrupted)

    async def on_receive(data: Dict[str, Any]):
        command = data.get("command", None)
        payload = data.get("body", None)
        command_id = data.get("command_id", None)
        try:
            if command == "complete":
                code_complete = CodeComplete.parse_obj(payload)
                await manager.complete(
                    uuid,
                    code_complete.code,
                    code_complete.cursor_position,
                    connection_id=ws_connection_id,
                    command_id=command_id,
                )
            else:
                raise UnsupportedWebsocketCommand()
        except Exception as e:
            logger.error(f"failed to parse: {e}")
            wrapper_dict = {
                "error": {
                    "message": "Error processing incoming command",
                    "command_id": command_id,
                }
            }
            if isinstance(e, ValidationError):
                wrapper_dict["error"][
                    "message"
                ] = "Error processing incoming command, invalid body"
                wrapper_dict["error"]["detail"] = jsonable_encoder(e.errors())
            elif isinstance(e, UnsupportedWebsocketCommand):
                wrapper_dict["error"][
                    "message"
                ] = f"Command '{command}' is not supported"

            msg_queue.put_nowait(wrapper_dict)

    async def receive_client_command(
        sender: Any,
        notebook_id: UUID,
        url: str,
        **kwargs,
    ):
        logger.debug(f"receiving Client Command with url: '{url}'")
        if notebook_id == uuid:
            wrapper_dict = {"client_command_url": {"command": url}}
            msg_queue.put_nowait(wrapper_dict)

    signal(CLIENT_COMMAND).connect(receive_client_command)

    await websocket_send_and_receive(websocket, msg_queue, on_receive)
