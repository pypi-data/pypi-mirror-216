import json
import os
import pathlib
from typing import Dict, Tuple

import pytest  # type: ignore

from jupyter_d1.settings import settings

from .D1TestClient import TestClient
from .utils import msg_id_lengths

pytestmark = pytest.mark.asyncio


async def upload_notebook(
    client: TestClient,
    token_headers: Dict[str, str],
    filename: str = "simple.ipynb",
    open_nb: bool = True,
) -> str:
    nb_filename = f"jupyter_d1/tests/notebooks/{filename}"
    nb_json = open(nb_filename).read()
    response = await client.post(
        "/notebooks/upload",
        params={"filename": filename},
        data=nb_json,
        headers=token_headers,
    )
    assert response.status_code == 201
    path = response.json()["path"]

    if not open_nb:
        return ""

    response = await client.get(
        f"/notebooks/open/?filepath={path}", headers=token_headers
    )
    assert response.status_code == 201
    resp_json = response.json()["notebook"]
    uuid = resp_json["metadata"]["jupyter_d1"]["uuid"]
    return uuid


@pytest.mark.usefixtures("clear_notebooks", "clear_notebook_directory")
class TestNotebook:
    async def test_notebook(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(client, superuser_token_headers)
        response = await client.get(
            f"/notebooks/{uuid}", headers=superuser_token_headers
        )
        assert response.status_code == 200
        nb = response.json()["notebook"]
        assert "cells" in nb.keys()
        assert "metadata" in nb.keys()
        assert "nbformat" in nb.keys()
        assert "nbformat_minor" in nb.keys()
        assert nb["metadata"]["jupyter_d1"]["uuid"] == uuid

    async def test_notebooks(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )
        uuid2 = await upload_notebook(
            client, superuser_token_headers, "other_simple.ipynb"
        )
        response = await client.get(
            "/notebooks", headers=superuser_token_headers
        )
        assert response.status_code == 200
        resp_json = response.json()
        notebooks = resp_json["notebooks"]
        assert len(notebooks) == 2

        ret_uuid = notebooks[0]["metadata"]["jupyter_d1"]["uuid"]
        ret_uuid2 = notebooks[1]["metadata"]["jupyter_d1"]["uuid"]
        assert uuid != uuid2
        assert set([uuid, uuid2]) == set([ret_uuid, ret_uuid2])

    async def test_delete_notebooks(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        await upload_notebook(client, superuser_token_headers, "simple.ipynb")
        await upload_notebook(
            client, superuser_token_headers, "other_simple.ipynb"
        )
        response = await client.get(
            "/notebooks", headers=superuser_token_headers
        )
        assert response.status_code == 200
        resp_json = response.json()["notebooks"]
        assert len(resp_json) == 2

        response = await client.delete(
            "/notebooks", headers=superuser_token_headers
        )
        assert response.status_code == 204

        response = await client.get(
            "/notebooks", headers=superuser_token_headers
        )
        assert response.status_code == 200
        resp_json = response.json()["notebooks"]
        assert len(resp_json) == 0

    async def test_delete_notebook(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )
        uuid2 = await upload_notebook(
            client, superuser_token_headers, "other_simple.ipynb"
        )
        response = await client.get(
            "/notebooks", headers=superuser_token_headers
        )
        assert response.status_code == 200
        resp_json = response.json()["notebooks"]
        assert len(resp_json) == 2
        ret_uuid = resp_json[0]["metadata"]["jupyter_d1"]["uuid"]
        ret_uuid2 = resp_json[1]["metadata"]["jupyter_d1"]["uuid"]
        assert set([uuid, uuid2]) == set([ret_uuid, ret_uuid2])

        # delete the first one
        response = await client.delete(
            f"/notebooks/{uuid}", headers=superuser_token_headers
        )
        assert response.status_code == 204

        response = await client.get(
            "/notebooks", headers=superuser_token_headers
        )
        assert response.status_code == 200
        resp_json = response.json()["notebooks"]
        assert len(resp_json) == 1
        # remaining notebook should have uuid2
        assert resp_json[0]["metadata"]["jupyter_d1"]["uuid"] == uuid2

    async def test_cells(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert len(cells) == 4

        for cell in cells:
            uuid = cell["metadata"]["jupyter_d1"]["uuid"]
            assert len(uuid) == 36
            uuid = cell["metadata"]["jupyter_d1"]["notebook_uuid"] == uuid

        cell0 = cells[0]
        assert cell0["cell_type"] == "markdown"
        assert cell0["source"] == "## Simple Test Notebook"

        cell1 = cells[1]
        assert cell1["cell_type"] == "code"
        assert cell1["source"] == 'print("Larry the Llama")'

    async def test_one_cell(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        cell1 = cells[1]
        cell1_uuid = cell1["metadata"]["jupyter_d1"]["uuid"]

        response = await client.get(
            f"/notebooks/{uuid}/cells/{cell1_uuid}",
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        cell = response.json()["cell"]
        uuid = cell["metadata"]["jupyter_d1"]["uuid"]
        assert uuid == cell1_uuid
        assert cell["cell_type"] == "code"
        assert cell["source"] == 'print("Larry the Llama")'

    async def test_patch_cell(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        cell1 = cells[1]
        cell1_uuid = cell1["metadata"]["jupyter_d1"]["uuid"]

        new_source = 'hello = "world"'
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell1_uuid}",
            headers=superuser_token_headers,
            json={"source": new_source},
        )
        assert response.status_code == 200
        # check that the returned cell has the new source
        cell = response.json()["cell"]
        assert cell["source"] == new_source

        # Assert that change was written to disk
        with open(f"{settings.ROOT_DIR}/simple.ipynb") as f:
            file_nb = json.loads(f.read())
        assert (
            file_nb["cells"][1]["metadata"]["jupyter_d1"]["uuid"]
            == cell["metadata"]["jupyter_d1"]["uuid"]
        )
        assert file_nb["cells"][1]["source"][0] == new_source

        # check that retrieving the cell has has the new source
        response = await client.get(
            f"/notebooks/{uuid}/cells/{cell1_uuid}",
            headers=superuser_token_headers,
        )
        assert response.status_code == 200
        cell = response.json()["cell"]
        assert cell["source"] == new_source

    async def test_create_cell(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # get the existing cells
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        orig_uuids = list(
            map(lambda x: x["metadata"]["jupyter_d1"]["uuid"], cells)
        )

        assert len(orig_uuids) == 4
        before_uuid = orig_uuids[1]  # place the new cell before position 1

        # add a new cell before index 1
        src = "__**Hello Callist**__"
        params = {
            "before": before_uuid,
            "cell_type": "markdown",
            "source": src,
        }
        response = await client.post(
            f"/notebooks/{uuid}/cells",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        new_cell = response.json()["cell"]
        assert new_cell["cell_type"] == "markdown"
        assert new_cell["source"] == src

        new_cell_uuid = new_cell["metadata"]["jupyter_d1"]["uuid"]
        assert len(new_cell_uuid) == 36

        # insert the new uuid into the original list
        orig_uuids.insert(1, new_cell_uuid)

        # Assert that change was written to disk
        with open(f"{settings.ROOT_DIR}/simple.ipynb") as f:
            file_nb = json.loads(f.read())
        assert (
            file_nb["cells"][1]["metadata"]["jupyter_d1"]["uuid"]
            == new_cell["metadata"]["jupyter_d1"]["uuid"]
        )

        # get the new list of cells
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        new_cells = response.json()["cells"]
        new_uuids = list(
            map(lambda x: x["metadata"]["jupyter_d1"]["uuid"], new_cells)
        )
        assert len(new_uuids) == 5

        # assert the new list of uuids is the old list with the new uuid
        assert new_uuids == orig_uuids

        # add a new cell at the end (omit position parameter)
        response = await client.post(
            f"/notebooks/{uuid}/cells",
            json={},
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        new_cell = response.json()["cell"]

        new_cell_uuid = new_cell["metadata"]["jupyter_d1"]["uuid"]
        assert len(new_cell_uuid) == 36

        # insert the new uuid into the original list
        orig_uuids.append(new_cell_uuid)

        # get the new list of cells
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        new_cells = response.json()["cells"]
        new_uuids = list(
            map(lambda x: x["metadata"]["jupyter_d1"]["uuid"], new_cells)
        )

        # assert the new list of uuids is the old list with the new uuid
        assert new_uuids == orig_uuids

    async def test_move_cell(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # get the existing cells
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        orig_uuids = list(
            map(lambda x: x["metadata"]["jupyter_d1"]["uuid"], cells)
        )

        assert len(orig_uuids) == 4
        # move the third cell 'before' the second cell (swap positions)
        move_uuid = orig_uuids[2]  # place the new cell before position 1
        before_uuid = orig_uuids[1]  # place the new cell before position 1

        params = {"before": before_uuid}
        response = await client.get(
            f"/notebooks/{uuid}/cells/{move_uuid}/move",
            params=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 204

        # This is the expected reordering
        reordered_uuids = [
            orig_uuids[0],
            orig_uuids[2],  # swap indecies 1, 2
            orig_uuids[1],
            orig_uuids[3],
        ]

        # Assert that change was written to disk
        with open(f"{settings.ROOT_DIR}/simple.ipynb") as f:
            file_nb = json.loads(f.read())
        file_uuids = list(
            map(
                lambda x: x["metadata"]["jupyter_d1"]["uuid"], file_nb["cells"]
            )
        )
        assert file_uuids == reordered_uuids

        # get the new list of cells
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        new_cells = response.json()["cells"]
        new_uuids = list(
            map(lambda x: x["metadata"]["jupyter_d1"]["uuid"], new_cells)
        )
        assert len(new_uuids) == 4

        # assert the new list of uuids is the old list with the new uuid
        assert new_uuids == reordered_uuids

        move_uuid = reordered_uuids[0]
        # move the first cell to the end (omit position parameter)
        response = await client.get(
            f"/notebooks/{uuid}/cells/{move_uuid}/move",
            headers=superuser_token_headers,
        )
        assert response.status_code == 204

        # final list just has the first cell moved to the end
        final_uuids = [
            reordered_uuids[1],
            reordered_uuids[2],
            reordered_uuids[3],
            reordered_uuids[0],
        ]

        # get the new list of cells
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        new_cells = response.json()["cells"]
        new_uuids = list(
            map(lambda x: x["metadata"]["jupyter_d1"]["uuid"], new_cells)
        )

        # assert the new list of uuids is the old list with the new uuid
        assert new_uuids == final_uuids

    async def _test_merge_cells(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        uuid: str,
        position: int,
        above: bool,
        cell_types: Tuple[str, str],
    ):
        if above:
            position_1 = position - 1
            position_2 = position
        else:
            position_1 = position
            position_2 = position + 1

        # get the existing cells
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert len(cells) == 4
        cell_uuid = cells[position]["metadata"]["jupyter_d1"]["uuid"]
        cell_1_source = cells[position_1]["source"]
        assert cells[position_1]["cell_type"] == cell_types[0]
        cell_2_source = cells[position_2]["source"]
        assert cells[position_2]["cell_type"] == cell_types[1]

        params = {}
        if above:
            params["above"] = True
        response = await client.get(
            f"/notebooks/{uuid}/cells/{cell_uuid}/merge",
            params=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 204

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert len(cells) == 3
        cell = cells[position_1]
        assert cell["source"] == f"{cell_1_source}\n{cell_2_source}"
        assert cell["cell_type"] == cell_types[1 if above else 0]
        assert cell["metadata"]["jupyter_d1"]["uuid"] == cell_uuid

        response = await client.get(
            f"/notebooks/{uuid}/undo", headers=superuser_token_headers
        )
        assert response.status_code == 204

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert len(cells) == 4
        assert cells[position]["metadata"]["jupyter_d1"]["uuid"] == cell_uuid
        assert cells[position_1]["source"] == cell_1_source
        assert cells[position_1]["cell_type"] == cell_types[0]
        assert cells[position_2]["source"] == cell_2_source
        assert cells[position_2]["cell_type"] == cell_types[1]

        response = await client.get(
            f"/notebooks/{uuid}/redo", headers=superuser_token_headers
        )
        assert response.status_code == 204

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert len(cells) == 3
        cell = cells[position_1]
        assert cell["source"] == f"{cell_1_source}\n{cell_2_source}"
        assert cell["cell_type"] == cell_types[1 if above else 0]
        assert cell["metadata"]["jupyter_d1"]["uuid"] == cell_uuid

    async def test_merge_cells(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )
        await self._test_merge_cells(
            client,
            superuser_token_headers,
            uuid=uuid,
            position=1,
            above=False,
            cell_types=("code", "code"),
        )

    async def test_merge_cells_above(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )
        await self._test_merge_cells(
            client,
            superuser_token_headers,
            uuid=uuid,
            position=1,
            above=True,
            cell_types=("markdown", "code"),
        )

    async def test_merge_first_2_cells(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )
        await self._test_merge_cells(
            client,
            superuser_token_headers,
            uuid=uuid,
            position=0,
            above=False,
            cell_types=("markdown", "code"),
        )

    async def test_merge_last_2_cells(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )
        await self._test_merge_cells(
            client,
            superuser_token_headers,
            uuid=uuid,
            position=3,
            above=True,
            cell_types=("code", "code"),
        )

    async def _test_split_cell(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        uuid: str,
        position: int,
        split_location: int,
        expected_sources: Tuple[str, str],
        cell_type: str,
    ):
        # get the existing cells
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert len(cells) == 4
        cell_uuid = cells[position]["metadata"]["jupyter_d1"]["uuid"]
        original_source = cells[position]["source"]
        assert cells[position]["cell_type"] == cell_type

        response = await client.get(
            f"/notebooks/{uuid}/cells/{cell_uuid}/split",
            params={"split_location": split_location},
            headers=superuser_token_headers,
        )
        assert response.status_code == 204

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert len(cells) == 5
        assert cells[position]["source"] == expected_sources[0]
        assert cells[position]["cell_type"] == cell_type
        assert cells[position + 1]["source"] == expected_sources[1]
        assert cells[position + 1]["cell_type"] == cell_type
        assert cells[position]["metadata"]["jupyter_d1"]["uuid"] == cell_uuid

        response = await client.get(
            f"/notebooks/{uuid}/undo", headers=superuser_token_headers
        )
        assert response.status_code == 204

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert len(cells) == 4
        assert cells[position]["metadata"]["jupyter_d1"]["uuid"] == cell_uuid
        assert cells[position]["source"] == original_source
        assert cells[position]["cell_type"] == cell_type

        response = await client.get(
            f"/notebooks/{uuid}/redo", headers=superuser_token_headers
        )
        assert response.status_code == 204

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert len(cells) == 5
        assert cells[position]["source"] == expected_sources[0]
        assert cells[position]["cell_type"] == cell_type
        assert cells[position + 1]["source"] == expected_sources[1]
        assert cells[position + 1]["cell_type"] == cell_type
        assert cells[position]["metadata"]["jupyter_d1"]["uuid"] == cell_uuid

    async def test_split_cell(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )
        await self._test_split_cell(
            client,
            superuser_token_headers,
            uuid=uuid,
            position=2,
            split_location=2,
            expected_sources=("2+", "5"),
            cell_type="code",
        )

    async def test_split_first_cell(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )
        await self._test_split_cell(
            client,
            superuser_token_headers,
            uuid=uuid,
            position=0,
            split_location=11,
            expected_sources=("## Simple T", "est Notebook"),
            cell_type="markdown",
        )

    async def test_split_last_cell(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )
        await self._test_split_cell(
            client,
            superuser_token_headers,
            uuid=uuid,
            position=3,
            split_location=0,
            expected_sources=("", ""),
            cell_type="code",
        )

    async def test_round_trip(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Check that when a notebook is uploaded, it gets a UUID.
        Then when it is download, uploaded and downloaded again,
        the UUID is different.
        """
        # initial upload
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # download the notebook, now with uuid
        response = await client.get(
            f"/notebooks/{uuid}", headers=superuser_token_headers
        )
        assert response.status_code == 200
        notebook = response.json()["notebook"]
        data = json.dumps(notebook)
        dl1_uuid = notebook["metadata"]["jupyter_d1"]["uuid"]
        assert uuid == dl1_uuid
        assert (
            notebook["metadata"]["jupyter_d1"]["path"]
            == f"{settings.ROOT_DIR}/simple.ipynb"
        )
        assert notebook["metadata"]["jupyter_d1"]["name"] == "simple"

        # delete the notebook on the server
        response = await client.delete(
            f"/notebooks/{uuid}", headers=superuser_token_headers
        )
        assert response.status_code == 204

        # upload the downloaded notebook, fail because file exists
        response = await client.post(
            "/notebooks/upload",
            params={"filename": "simple.ipynb"},
            data=data,
            headers=superuser_token_headers,
        )
        assert response.status_code == 400
        path = response.json()["detail"] == "File alreaady exists"

        # upload the downloaded notebook with different name,
        # complete with uuid
        response = await client.post(
            "/notebooks/upload",
            params={"filename": "isimple.ipynb"},
            data=data,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        path = response.json()["path"]

        # Check that remote file has a different uuid after upload
        with open(f"{settings.ROOT_DIR}/{path}", "r") as f:
            nb = json.loads(f.read())
        file_uuid = nb["metadata"]["jupyter_d1"]["uuid"]
        assert uuid != file_uuid
        assert (
            nb["metadata"]["jupyter_d1"]["path"]
            == f"{settings.ROOT_DIR}/isimple.ipynb"
        )
        assert nb["metadata"]["jupyter_d1"]["name"] == "isimple"

        # Open notebook, check that uuid changes again
        response = await client.get(
            f"/notebooks/open/?filepath={path}",
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        notebook = response.json()["notebook"]
        open_uuid = notebook["metadata"]["jupyter_d1"]["uuid"]
        assert uuid != open_uuid
        assert file_uuid != open_uuid
        assert (
            notebook["metadata"]["jupyter_d1"]["path"]
            == f"{settings.ROOT_DIR}/isimple.ipynb"
        )
        assert notebook["metadata"]["jupyter_d1"]["name"] == "isimple"

        # Check that new uuid was written to disk after opening the notebook
        with open(f"{settings.ROOT_DIR}/{path}", "r") as f:
            nb = json.loads(f.read())
        new_file_uuid = nb["metadata"]["jupyter_d1"]["uuid"]
        assert new_file_uuid == open_uuid
        assert (
            nb["metadata"]["jupyter_d1"]["path"]
            == f"{settings.ROOT_DIR}/isimple.ipynb"
        )
        assert nb["metadata"]["jupyter_d1"]["name"] == "isimple"

        # finally, get the notebook again and make sure the
        # uuid is the same as when opened
        response = await client.get(
            f"/notebooks/{open_uuid}", headers=superuser_token_headers
        )
        assert response.status_code == 200
        notebook = response.json()["notebook"]
        dl2_uuid = notebook["metadata"]["jupyter_d1"]["uuid"]
        assert open_uuid == dl2_uuid

    async def test_cell_state_reset(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Check that when a notebook is uploaded, cells states get reset to
        idle and execution counts are reset
        """
        # initial upload
        uuid = await upload_notebook(
            client, superuser_token_headers, "stateful_simple.ipynb"
        )

        # download the notebook
        response = await client.get(
            f"/notebooks/{uuid}", headers=superuser_token_headers
        )
        assert response.status_code == 200
        notebook = response.json()["notebook"]
        dl1_uuid = notebook["metadata"]["jupyter_d1"]["uuid"]
        assert uuid == dl1_uuid
        assert (
            notebook["metadata"]["jupyter_d1"]["path"]
            == f"{settings.ROOT_DIR}/stateful_simple.ipynb"
        )
        assert notebook["metadata"]["jupyter_d1"]["name"] == "stateful_simple"

        for cell in notebook["cells"]:
            if "jupyter_d1" in cell["metadata"]:
                d1_data = cell["metadata"]["jupyter_d1"]
                if "execution_state" in d1_data:
                    assert d1_data["execution_state"] == "idle"
            if "execution_count" in cell:
                assert cell["execution_count"] is None

    async def test_get_bogus_notebook(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        "Test error condition when downloading an non-existent notebook."
        from uuid import uuid4

        uuid = uuid4()
        response = await client.get(
            f"/notebooks/{uuid}", headers=superuser_token_headers
        )
        assert response.status_code == 404
        resp_json = response.json()
        assert resp_json["error"] == "NOTEBOOK_NOT_FOUND"
        assert resp_json["reason"] == f"Notebook not found with uuid: {uuid}"
        assert resp_json["detail"] is None

    async def test_get_bogus_cell(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        "Test error condition when downloading an non-existent cell."
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )
        from uuid import uuid4

        cell_uuid = uuid4()
        response = await client.get(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            headers=superuser_token_headers,
        )
        assert response.status_code == 404
        resp_json = response.json()
        assert resp_json["error"] == "CELL_NOT_FOUND"
        assert resp_json["reason"] == f"Cell not found with uuid: {cell_uuid}"
        assert resp_json["detail"] is None

    async def test_bogus_kernel(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        "Test notebook upload that has an unsupported kernel."
        await upload_notebook(
            client, superuser_token_headers, "weird_kernel.ipynb"
        )

    async def test_upload_to_directory(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        os.mkdir(f"{settings.ROOT_DIR}/aproject")
        with open(f"jupyter_d1/tests/notebooks/simple.ipynb", "r") as f:
            nb_raw = f.read()
        response = await client.post(
            "/notebooks/upload",
            params={"directory": "aproject", "filename": "koy"},
            data=nb_raw,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        path = response.json()["path"]
        assert path == f"aproject/koy.ipynb"

        with open(f"{settings.ROOT_DIR}/{path}", "r") as f:
            nb = json.loads(f.read())
        file_uuid = nb["metadata"]["jupyter_d1"]["uuid"]
        assert file_uuid is not None
        assert (
            nb["metadata"]["jupyter_d1"]["path"]
            == f"{settings.ROOT_DIR}/{path}"
        )
        assert nb["metadata"]["jupyter_d1"]["name"] == "koy"

        response = await client.get(
            f"/notebooks/open/?filepath={path}",
            headers=superuser_token_headers,
        )

        assert response.status_code == 201
        nb = response.json()["notebook"]
        uuid = nb["metadata"]["jupyter_d1"]["uuid"]
        assert uuid != file_uuid
        assert (
            nb["metadata"]["jupyter_d1"]["path"]
            == f"{settings.ROOT_DIR}/{path}"
        )
        assert nb["metadata"]["jupyter_d1"]["name"] == "koy"

    async def test_upload_to_directory_fail(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        with open(f"jupyter_d1/tests/notebooks/simple.ipynb", "r") as f:
            nb = json.loads(f.read())
        response = await client.post(
            "/notebooks/upload",
            params={"directory": "aproject", "filename": "koy"},
            data=nb,
            headers=superuser_token_headers,
        )
        assert response.status_code == 404
        assert (
            response.json()["detail"]
            == f"Directory does not exist {settings.ROOT_DIR}/aproject"
        )

    async def test_working_directory(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        nb_filename = f"jupyter_d1/tests/notebooks/simple.ipynb"
        nb_json = open(nb_filename).read()
        response = await client.post(
            "/notebooks/upload",
            params={"filename": "name.ipynb"},
            data=nb_json,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        assert response.json()["path"] == "name.ipynb"
        response = await client.get(
            "/notebooks/open/?filepath=name.ipynb",
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()
        assert (
            resp_json["notebook"]["metadata"]["jupyter_d1"][
                "working_directory"
            ]
            == settings.ROOT_DIR
        )
        uuid = resp_json["notebook"]["metadata"]["jupyter_d1"]["uuid"]
        response = await client.delete(
            f"/notebooks/{uuid}", data=nb_json, headers=superuser_token_headers
        )
        assert response.status_code == 204

        response = await client.get(
            "/notebooks/open/",
            headers=superuser_token_headers,
            params={
                "filepath": "name.ipynb",
                "working_directory": "/tmp",
            },
        )
        assert response.json()["notebook"]["metadata"]["jupyter_d1"][
            "working_directory"
        ] == str(pathlib.Path("/tmp").resolve())

    async def test_upload_and_open_in_memory_no_working_dir_specified(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Working directory should default to root dir,
        notebook should not be saved on disk.
        """
        nb_filename = f"jupyter_d1/tests/notebooks/simple.ipynb"
        nb_json = open(nb_filename).read()
        response = await client.post(
            "/notebooks/upload_and_open",
            params={"filename": "name.ipynb", "autosave": "False"},
            data=nb_json,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()
        assert (
            resp_json["notebook"]["metadata"]["jupyter_d1"][
                "working_directory"
            ]
            == settings.ROOT_DIR
        )
        uuid = resp_json["notebook"]["metadata"]["jupyter_d1"]["uuid"]

        # Do an action that would save the notebook if autosave was true
        cell1_uuid = resp_json["notebook"]["cells"][1]["metadata"][
            "jupyter_d1"
        ]["uuid"]
        new_source = 'hello = "world"'
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell1_uuid}",
            headers=superuser_token_headers,
            json={"source": new_source},
        )
        assert response.status_code == 200

        assert not os.path.exists(f"{settings.ROOT_DIR}/name.ipynb")

        response = await client.get(
            "/notebooks", headers=superuser_token_headers
        )
        assert response.status_code == 200
        resp_json = response.json()
        notebooks = resp_json["notebooks"]
        assert len(notebooks) == 1
        assert notebooks[0]["metadata"]["jupyter_d1"]["uuid"] == uuid
        assert (
            notebooks[0]["metadata"]["jupyter_d1"]["working_directory"]
            == settings.ROOT_DIR
        )

    async def test_upload_and_open_in_memory_file_exists_but_its_fine(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Opening notebook in memory when file exists should work fine.
        """
        nb_filename = f"jupyter_d1/tests/notebooks/simple.ipynb"
        nb_json = open(nb_filename).read()
        with open(f"{settings.ROOT_DIR}/name.ipynb", "w") as f:
            f.write(nb_json)
        response = await client.post(
            "/notebooks/upload_and_open",
            params={"filename": "name.ipynb", "autosave": "False"},
            data=nb_json,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()
        assert (
            resp_json["notebook"]["metadata"]["jupyter_d1"][
                "working_directory"
            ]
            == settings.ROOT_DIR
        )
        uuid = resp_json["notebook"]["metadata"]["jupyter_d1"]["uuid"]

        assert os.path.exists(f"{settings.ROOT_DIR}/name.ipynb")

        response = await client.get(
            "/notebooks", headers=superuser_token_headers
        )
        assert response.status_code == 200
        resp_json = response.json()
        notebooks = resp_json["notebooks"]
        assert len(notebooks) == 1
        assert notebooks[0]["metadata"]["jupyter_d1"]["uuid"] == uuid
        assert (
            notebooks[0]["metadata"]["jupyter_d1"]["working_directory"]
            == settings.ROOT_DIR
        )

    async def test_upload_and_open_in_memory_working_dir_specified(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Working directory should be set to specified directory,
        notebook should not be saved on disk.
        """
        nb_filename = f"jupyter_d1/tests/notebooks/simple.ipynb"
        nb_json = open(nb_filename).read()
        response = await client.post(
            "/notebooks/upload_and_open",
            params={
                "filename": "name.ipynb",
                "autosave": "False",
                "working_directory": f"{os.getcwd()}/jupyter_d1"
                "/tests/notebooks",
            },
            data=nb_json,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()
        assert (
            resp_json["notebook"]["metadata"]["jupyter_d1"][
                "working_directory"
            ]
            == f"{os.getcwd()}/jupyter_d1/tests/notebooks"
        )
        uuid = resp_json["notebook"]["metadata"]["jupyter_d1"]["uuid"]

        assert not os.path.exists(f"{settings.ROOT_DIR}/name.ipynb")
        # This should be impossible, but might as well check it
        assert not os.path.exists(
            f"{os.getcwd()}/jupyter_d1/tests/notebooks/name.ipynb"
        )

        response = await client.get(
            "/notebooks", headers=superuser_token_headers
        )
        assert response.status_code == 200
        resp_json = response.json()
        notebooks = resp_json["notebooks"]
        assert len(notebooks) == 1
        assert notebooks[0]["metadata"]["jupyter_d1"]["uuid"] == uuid
        assert (
            notebooks[0]["metadata"]["jupyter_d1"]["working_directory"]
            == f"{os.getcwd()}/jupyter_d1/tests/notebooks"
        )

    async def test_upload_and_open_no_working_dir_specified(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Working directory should default to root dir,
        notebook should be saved on disk.
        """
        nb_filename = f"jupyter_d1/tests/notebooks/simple.ipynb"
        nb_json = open(nb_filename).read()
        response = await client.post(
            "/notebooks/upload_and_open",
            params={"filename": "name.ipynb"},
            data=nb_json,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()
        assert (
            resp_json["notebook"]["metadata"]["jupyter_d1"][
                "working_directory"
            ]
            == settings.ROOT_DIR
        )
        uuid = resp_json["notebook"]["metadata"]["jupyter_d1"]["uuid"]

        assert os.path.exists(f"{settings.ROOT_DIR}/name.ipynb")

        response = await client.get(
            "/notebooks", headers=superuser_token_headers
        )
        assert response.status_code == 200
        resp_json = response.json()
        notebooks = resp_json["notebooks"]
        assert len(notebooks) == 1
        assert notebooks[0]["metadata"]["jupyter_d1"]["uuid"] == uuid
        assert (
            notebooks[0]["metadata"]["jupyter_d1"]["working_directory"]
            == settings.ROOT_DIR
        )

    async def test_upload_and_open_working_dir_defaults_to_root_dir(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Working directory should default to root dir,
        notebook should be saved on disk.
        """
        try:
            os.remove(f"{os.getcwd()}/jupyter_d1/tests/notebooks/name.ipynb")
        except Exception:
            pass
        nb_filename = f"jupyter_d1/tests/notebooks/simple.ipynb"
        nb_json = open(nb_filename).read()
        response = await client.post(
            "/notebooks/upload_and_open",
            params={
                "filename": "name.ipynb",
                "directory": f"{os.getcwd()}/jupyter_d1/tests/notebooks",
            },
            data=nb_json,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()
        assert (
            resp_json["notebook"]["metadata"]["jupyter_d1"][
                "working_directory"
            ]
            == f"{os.getcwd()}/jupyter_d1/tests/notebooks"
        )
        uuid = resp_json["notebook"]["metadata"]["jupyter_d1"]["uuid"]

        assert os.path.exists(
            f"{os.getcwd()}/jupyter_d1/tests/notebooks/name.ipynb"
        )

        response = await client.get(
            "/notebooks", headers=superuser_token_headers
        )
        assert response.status_code == 200
        resp_json = response.json()
        notebooks = resp_json["notebooks"]
        assert len(notebooks) == 1
        assert notebooks[0]["metadata"]["jupyter_d1"]["uuid"] == uuid
        assert (
            notebooks[0]["metadata"]["jupyter_d1"]["working_directory"]
            == f"{os.getcwd()}/jupyter_d1/tests/notebooks"
        )
        os.remove(f"{os.getcwd()}/jupyter_d1/tests/notebooks/name.ipynb")

    async def test_upload_and_open_working_dir_defaults_to_dir(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Working directory should default to directory provided (where notebook
        is also saved), notebook should be saved on disk.
        """
        try:
            os.remove(f"{os.getcwd()}/jupyter_d1/tests/notebooks/name.ipynb")
        except Exception:
            pass
        nb_filename = f"jupyter_d1/tests/notebooks/simple.ipynb"
        nb_json = open(nb_filename).read()
        response = await client.post(
            "/notebooks/upload_and_open",
            params={
                "filename": "name.ipynb",
                "directory": f"{os.getcwd()}/jupyter_d1/tests/notebooks",
            },
            data=nb_json,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()
        assert (
            resp_json["notebook"]["metadata"]["jupyter_d1"][
                "working_directory"
            ]
            == f"{os.getcwd()}/jupyter_d1/tests/notebooks"
        )
        uuid = resp_json["notebook"]["metadata"]["jupyter_d1"]["uuid"]

        assert os.path.exists(
            f"{os.getcwd()}/jupyter_d1/tests/notebooks/name.ipynb"
        )

        response = await client.get(
            "/notebooks", headers=superuser_token_headers
        )
        assert response.status_code == 200
        resp_json = response.json()
        notebooks = resp_json["notebooks"]
        assert len(notebooks) == 1
        assert notebooks[0]["metadata"]["jupyter_d1"]["uuid"] == uuid
        assert (
            notebooks[0]["metadata"]["jupyter_d1"]["working_directory"]
            == f"{os.getcwd()}/jupyter_d1/tests/notebooks"
        )
        os.remove(f"{os.getcwd()}/jupyter_d1/tests/notebooks/name.ipynb")

    async def test_upload_and_open_working_directory_specified(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Working directory should be set to provided working dir,
        notebook should be saved on disk.
        """
        try:
            os.remove(f"{os.getcwd()}/jupyter_d1/tests/notebooks/name.ipynb")
        except Exception:
            pass
        nb_filename = f"jupyter_d1/tests/notebooks/simple.ipynb"
        nb_json = open(nb_filename).read()
        response = await client.post(
            "/notebooks/upload_and_open",
            params={
                "filename": "name.ipynb",
                "directory": f"{os.getcwd()}/jupyter_d1/tests/notebooks",
                "working_directory": "/tmp",
            },
            data=nb_json,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()
        assert resp_json["notebook"]["metadata"]["jupyter_d1"][
            "working_directory"
        ] == str(pathlib.Path("/tmp").resolve())
        uuid = resp_json["notebook"]["metadata"]["jupyter_d1"]["uuid"]

        assert os.path.exists(
            f"{os.getcwd()}/jupyter_d1/tests/notebooks/name.ipynb"
        )

        response = await client.get(
            "/notebooks", headers=superuser_token_headers
        )
        assert response.status_code == 200
        resp_json = response.json()
        notebooks = resp_json["notebooks"]
        assert len(notebooks) == 1
        assert notebooks[0]["metadata"]["jupyter_d1"]["uuid"] == uuid
        assert notebooks[0]["metadata"]["jupyter_d1"][
            "working_directory"
        ] == str(pathlib.Path("/tmp").resolve())
        os.remove(f"{os.getcwd()}/jupyter_d1/tests/notebooks/name.ipynb")

    async def test_open_notebook_file_twice_returns_same_notebook(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """Opening a notebook twice returns an error"""
        nb_filename = f"jupyter_d1/tests/notebooks/simple.ipynb"
        nb_json = open(nb_filename).read()
        response = await client.post(
            "/notebooks/upload",
            params={"filename": "name.ipynb"},
            data=nb_json,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        assert response.json()["path"] == "name.ipynb"
        response = await client.get(
            "/notebooks/open/?filepath=name.ipynb",
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        metadata = response.json()["notebook"]["metadata"]["jupyter_d1"]
        assert metadata["working_directory"] == settings.ROOT_DIR
        uuid = metadata["uuid"]

        response = await client.get(
            "/notebooks/open/",
            headers=superuser_token_headers,
            params={
                "filepath": "name.ipynb",
                "working_directory": "/tmp",
            },
        )
        assert response.status_code == 201
        metadata = response.json()["notebook"]["metadata"]["jupyter_d1"]
        assert metadata["working_directory"] == settings.ROOT_DIR
        assert metadata["uuid"] == uuid

        response = await client.get(
            "/notebooks", headers=superuser_token_headers
        )
        assert response.status_code == 200
        resp_json = response.json()
        notebooks = resp_json["notebooks"]
        assert len(notebooks) == 1
        assert notebooks[0]["metadata"]["jupyter_d1"]["uuid"] == uuid
        assert (
            notebooks[0]["metadata"]["jupyter_d1"]["working_directory"]
            == settings.ROOT_DIR
        )

    async def test_upload_and_open_notebook_twice_returns_same_notebook(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        nb_filename = f"jupyter_d1/tests/notebooks/simple.ipynb"
        nb_json = open(nb_filename).read()
        response = await client.post(
            "/notebooks/upload_and_open",
            params={"autosave": "False"},
            data=nb_json,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()
        assert (
            resp_json["notebook"]["metadata"]["jupyter_d1"][
                "working_directory"
            ]
            == settings.ROOT_DIR
        )
        uuid = resp_json["notebook"]["metadata"]["jupyter_d1"]["uuid"]

        assert not os.path.exists(f"{settings.ROOT_DIR}/name.ipynb")

        response = await client.post(
            "/notebooks/upload_and_open",
            params={"autosave": "False", "working_directory": "/tmp"},
            data=json.dumps(resp_json["notebook"]),
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()
        assert (
            resp_json["notebook"]["metadata"]["jupyter_d1"][
                "working_directory"
            ]
            == settings.ROOT_DIR
        )
        assert resp_json["notebook"]["metadata"]["jupyter_d1"]["uuid"] == uuid

        response = await client.get(
            "/notebooks", headers=superuser_token_headers
        )
        assert response.status_code == 200
        resp_json = response.json()
        notebooks = resp_json["notebooks"]
        assert len(notebooks) == 1
        assert notebooks[0]["metadata"]["jupyter_d1"]["uuid"] == uuid
        assert (
            notebooks[0]["metadata"]["jupyter_d1"]["working_directory"]
            == settings.ROOT_DIR
        )

    async def test_upload_invalid_notebook(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Invalid notebook should return 400, and not cause a 500
        """
        response = await client.post(
            "/notebooks/upload",
            params={"filename": "name.ipynb", "autosave": "False"},
            data="{}",
            headers=superuser_token_headers,
        )
        assert response.status_code == 400
        assert (
            response.json()["detail"] == "Failed to parse notebook: "
            "<class 'jsonschema.exceptions.ValidationError'> Notebook could"
            " not be converted from version 1 to version 2 because it's"
            " missing a key: cells"
        )

    async def test_open_invalid_notebook(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Invalid notebook should return 400, and not cause a 500
        """
        with open(f"{settings.ROOT_DIR}/name1l.ipynb", "w") as f:
            f.write("{}")

        response = await client.get(
            "/notebooks/open/",
            params={"filepath": "name1l.ipynb"},
            data="{}",
            headers=superuser_token_headers,
        )
        assert response.status_code == 400
        assert (
            response.json()["detail"] == "Failed to parse notebook: "
            "<class 'jsonschema.exceptions.ValidationError'> Notebook could"
            " not be converted from version 1 to version 2 because it's"
            " missing a key: cells"
        )

    async def test_upload_and_open_invalid_notebook(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Invalid notebook should return 400, and not cause a 500
        """
        response = await client.post(
            "/notebooks/upload_and_open",
            params={"filename": "name.ipynb", "autosave": "False"},
            data="{}",
            headers=superuser_token_headers,
        )
        assert response.status_code == 400
        assert (
            response.json()["detail"] == "Failed to parse notebook: "
            "<class 'jsonschema.exceptions.ValidationError'> Notebook could"
            " not be converted from version 1 to version 2 because it's"
            " missing a key: cells"
        )

    async def test_get_metadata(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        await upload_notebook(client, superuser_token_headers, "simple.ipynb")
        await upload_notebook(
            client,
            superuser_token_headers,
            "other_simple.ipynb",
            open_nb=False,
        )

        async def assert_open_notebooks():
            response = await client.get(
                "/notebooks", headers=superuser_token_headers
            )
            assert response.status_code == 200
            resp_json = response.json()
            notebooks = resp_json["notebooks"]
            assert len(notebooks) == 1
            assert notebooks[0]["metadata"]["jupyter_d1"]["name"] == "simple"

        await assert_open_notebooks()

        # Metadata for a notebook that is currently open
        response = await client.get(
            "/notebooks/metadata/",
            params={"filepath": "simple.ipynb"},
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        metadata = response.json()["metadata"]
        assert metadata["kernelspec"]["name"] == "python3"
        assert metadata["jupyter_d1"]["name"] == "simple"
        assert metadata["jupyter_d1"]["path"].endswith("/simple.ipynb")

        # Try with full path
        response = await client.get(
            "/notebooks/metadata/",
            params={"filepath": metadata["jupyter_d1"]["path"]},
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        assert response.json()["metadata"] == metadata

        # Metadata for a notebook that is not open
        response = await client.get(
            "/notebooks/metadata/",
            params={"filepath": "other_simple.ipynb"},
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        metadata = response.json()["metadata"]
        assert metadata["kernelspec"]["name"] == "python3"
        assert metadata["jupyter_d1"]["name"] == "other_simple"
        assert metadata["jupyter_d1"]["path"].endswith("/other_simple.ipynb")

        # Make sure "simple" is still the only open notebook
        await assert_open_notebooks()

        # Try with full path
        response = await client.get(
            "/notebooks/metadata/",
            params={"filepath": metadata["jupyter_d1"]["path"]},
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        assert response.json()["metadata"] == metadata

        await assert_open_notebooks()

    async def test_get_metadata_invalid_path(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        await upload_notebook(client, superuser_token_headers, "simple.ipynb")
        await upload_notebook(
            client,
            superuser_token_headers,
            "other_simple.ipynb",
            open_nb=False,
        )

        response = await client.get(
            "/notebooks/metadata/",
            params={"filepath": "bogus.ipynb"},
            headers=superuser_token_headers,
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "File not found"

    async def test_get_metadata_invalid_notebook(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        with open(f"{settings.ROOT_DIR}/name1l.ipynb", "w") as f:
            f.write("{}")

        response = await client.get(
            "/notebooks/metadata/",
            params={"filepath": "name1l.ipynb"},
            headers=superuser_token_headers,
        )
        assert response.status_code == 400
        assert response.status_code == 400
        assert (
            response.json()["detail"] == "Failed to parse notebook: "
            "<class 'jsonschema.exceptions.ValidationError'> Notebook could"
            " not be converted from version 1 to version 2 because it's"
            " missing a key: cells"
        )


@pytest.mark.usefixtures("clear_notebooks", "clear_notebook_directory")
class TestNotebookPermissions:
    async def test_notebooks(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        readonly_token_headers: Dict[str, str],
        permissionless_token_headers: Dict[str, str],
    ):
        await upload_notebook(client, superuser_token_headers, "simple.ipynb")
        await upload_notebook(
            client, superuser_token_headers, "other_simple.ipynb"
        )
        response = await client.get(
            "/notebooks", headers=permissionless_token_headers
        )
        assert response.status_code == 403
        response = await client.get(
            "/notebooks", headers=readonly_token_headers
        )
        assert response.status_code == 200

    async def test_notebook(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        permissionless_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
    ):
        uuid = await upload_notebook(client, superuser_token_headers)
        response = await client.get(
            f"/notebooks/{uuid}", headers=permissionless_token_headers
        )
        assert response.status_code == 403
        response = await client.get(
            f"/notebooks/{uuid}", headers=readonly_token_headers
        )
        assert response.status_code == 200

    async def test_delete_notebooks(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
    ):
        await upload_notebook(client, superuser_token_headers, "simple.ipynb")
        await upload_notebook(
            client, superuser_token_headers, "other_simple.ipynb"
        )
        response = await client.delete(
            "/notebooks", headers=readonly_token_headers
        )
        assert response.status_code == 403
        response = await client.delete(
            "/notebooks", headers=superuser_token_headers
        )
        assert response.status_code == 204

    async def test_delete_notebook(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )
        response = await client.delete(
            f"/notebooks/{uuid}", headers=readonly_token_headers
        )
        assert response.status_code == 403
        response = await client.delete(
            f"/notebooks/{uuid}", headers=superuser_token_headers
        )
        assert response.status_code == 204

    async def test_cells(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        permissionless_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=permissionless_token_headers
        )
        assert response.status_code == 403
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=readonly_token_headers
        )
        assert response.status_code == 200

    async def test_one_cell(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        permissionless_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=readonly_token_headers
        )
        assert response.status_code == 200
        cell1_uuid = response.json()["cells"][1]["metadata"]["jupyter_d1"][
            "uuid"
        ]

        response = await client.get(
            f"/notebooks/{uuid}/cells/{cell1_uuid}",
            headers=permissionless_token_headers,
        )
        assert response.status_code == 403
        response = await client.get(
            f"/notebooks/{uuid}/cells/{cell1_uuid}",
            headers=readonly_token_headers,
        )
        assert response.status_code == 200

    async def test_patch_cell(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cell1_uuid = response.json()["cells"][1]["metadata"]["jupyter_d1"][
            "uuid"
        ]

        new_source = 'hello = "world"'
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell1_uuid}",
            headers=readonly_token_headers,
            json={"source": new_source},
        )
        assert response.status_code == 403
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell1_uuid}",
            headers=superuser_token_headers,
            json={"source": new_source},
        )
        assert response.status_code == 200

    async def test_patch_and_execute_cell(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cell1_uuid = response.json()["cells"][1]["metadata"]["jupyter_d1"][
            "uuid"
        ]

        new_source = 'hello = "world"'
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell1_uuid}/execute",
            headers=readonly_token_headers,
            json={"source": new_source},
        )
        assert response.status_code == 403
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell1_uuid}/execute",
            headers=superuser_token_headers,
            json={"source": new_source},
        )
        assert response.status_code == 200

        uuid = response.json()["cell"]["metadata"]["jupyter_d1"]["uuid"]
        assert len(uuid) == 36
        message_id = response.json()["kernel_message"]["message_id"]
        assert len(message_id) in msg_id_lengths

    async def test_create_cell(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # add a new cell
        src = "__**Hello Callist**__"
        params = {"cell_type": "markdown", "source": src}
        response = await client.post(
            f"/notebooks/{uuid}/cells",
            json=params,
            headers=readonly_token_headers,
        )
        assert response.status_code == 403
        response = await client.post(
            f"/notebooks/{uuid}/cells",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201

    async def test_move_cell(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # get the existing cells
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        move_uuid = response.json()["cells"][2]["metadata"]["jupyter_d1"][
            "uuid"
        ]

        response = await client.get(
            f"/notebooks/{uuid}/cells/{move_uuid}/move",
            headers=readonly_token_headers,
        )
        assert response.status_code == 403
        response = await client.get(
            f"/notebooks/{uuid}/cells/{move_uuid}/move",
            headers=superuser_token_headers,
        )
        assert response.status_code == 204

    async def test_upload_notebook(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
    ):
        nb_filename = f"jupyter_d1/tests/notebooks/simple.ipynb"
        nb_json = open(nb_filename).read()
        response = await client.post(
            "/notebooks/upload", data=nb_json, headers=readonly_token_headers
        )
        assert response.status_code == 403
        response = await client.post(
            "/notebooks/upload",
            params={"filename": "name.ipynb"},
            data=nb_json,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        assert response.json()["path"] == "name.ipynb"
        response = await client.get(
            "/notebooks/open/?filepath=name.ipynb",
            headers=superuser_token_headers,
        )
        assert response.status_code == 201


@pytest.mark.usefixtures("clear_notebooks", "clear_notebook_directory")
class TestDependencyChecker:
    async def test_check_dependencies(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "outside_imports.ipynb"
        )

        response = await client.get(
            f"/notebooks/{uuid}/check_dependencies",
            headers=superuser_token_headers,
        )

        assert response.json()["missing_dependencies"] == [
            "Faker",
            "Flask",
            "tensorflow",
        ]
