import asyncio
import base64
import os
import pathlib
import pprint
import shutil
from datetime import datetime
from typing import Any, Dict, List, Optional
from unittest import TestCase
from unittest.mock import call

# from fastapi.testclient import TestClient
import pytest  # type: ignore
from pytest_mock import MockFixture  # type: ignore

from jupyter_d1.settings import settings

from .D1TestClient import TestClient
from .utils import (
    clear_websocket_queue,
    collect_websocket_messages,
    compare_cells,
    filter_websocket_collection,
    get_superuser_token,
    msg_id_lengths,
    receive_json,
    resolve,
    wait_for_event,
)

# All test coroutines will be treated as marked.
# pytestmark = pytest.mark.asyncio

WEBSOCKET_SLEEP_TIME = 1.1


async def upload_notebook(
    client: TestClient,
    token_headers: Dict[str, str],
    filename: str = "simple.ipynb",
) -> str:
    nb_filename = f"jupyter_d1/tests/notebooks/{filename}"
    nb_json = open(nb_filename).read()
    response = await client.post(
        "/notebooks/upload",
        query_string={"filename": filename},
        data=nb_json,
        headers=token_headers,
    )
    assert response.status_code == 201, response.text
    path = response.json()["path"]

    response = await client.get(
        f"/notebooks/open/?filepath={path}", headers=token_headers
    )
    assert response.status_code == 201, response.text
    resp_json = response.json()["notebook"]
    uuid = resp_json["metadata"]["jupyter_d1"]["uuid"]

    # Give kernel time to fully start, kernel messages can get
    # dropped otherwise
    await asyncio.sleep(2)
    return uuid


def assert_cell_positions(cells: List[Dict[str, Any]]):
    assert [c["metadata"]["jupyter_d1"]["position"] for c in cells] == list(
        range(0, len(cells))
    )


@pytest.mark.usefixtures("clear_notebooks", "clear_notebook_directory")
class TestNotebookWebSocket:
    @pytest.mark.asyncio
    async def test_open_notebook_infer_kernel_from_language(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Open a notebook with a kernelspec in its metadata that does not match
        any local kernels by name, should infer the kernel based on the language
        """
        uuid = await upload_notebook(
            client,
            superuser_token_headers,
            filename="simple_r_language_in_metadata.ipynb",
        )

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        cell = cells[1]
        cell_uuid = cell["metadata"]["jupyter_d1"]["uuid"]

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            await clear_websocket_queue(websocket)

        response = await client.get(
            f"/notebooks/{uuid}", headers=superuser_token_headers
        )
        assert response.status_code == 200
        nb = response.json()["notebook"]
        cells = nb["cells"]
        metadata = nb["metadata"]

        assert cells[1]["outputs"] == []
        assert cells[1]["execution_count"] == 1
        assert cells[1]["metadata"]["jupyter_d1"]["execution_state"] == "idle"
        assert metadata["kernelspec"] == {
            "name": "ir",
            "language": "R",
            "display_name": "R",
        }

    @pytest.mark.asyncio
    async def test_notebook_cell_execute(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        cell = cells[2]
        cell_uuid = cell["metadata"]["jupyter_d1"]["uuid"]

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            # await asyncio.sleep(WEBSOCKET_SLEEP_TIME)
            await asyncio.sleep(3.5)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            msg_id = response.json()["kernel_message"]["message_id"]

            data = await receive_json(websocket, msg_types=["cell_update"])
            assert len(data["cell_update"]) == 1
            cell_data = data["cell_update"][0]
            d1_metadata = cell_data["metadata"]["jupyter_d1"]
            assert d1_metadata["execution_state"] == "pending"
            assert d1_metadata["uuid"] == cell_uuid
            assert cell_data["execution_count"] is None
            assert len(cell_data["outputs"]) == 0

            # second two chunks received should be a execution count update and
            # cell_update with an execution_state of 'busy' when processing
            # starts. Order is variable, so here we handle either order.
            def assert_json_content(data, execution_count=None):
                if "cell_update" in data:
                    cell_data = data["cell_update"][0]
                    d1_metadata = cell_data["metadata"]["jupyter_d1"]
                    assert d1_metadata["execution_state"] == "busy"
                    assert d1_metadata["uuid"] == cell_uuid
                    assert cell_data["execution_count"] == execution_count
                    return None
                elif "cell_execution_reply" in data:
                    assert data["cell_execution_reply"]["execution_count"] == 1
                    assert data["cell_execution_reply"]["cell_id"] == cell_uuid
                    assert data["cell_execution_reply"]["parent_id"] == msg_id
                    return 1
                else:
                    raise AssertionError(f"unexpected cell type: {data}")

            data = await receive_json(
                websocket, msg_types=["cell_update", "cell_execution_reply"]
            )
            exec_count = assert_json_content(data)
            data = await receive_json(
                websocket, msg_types=["cell_update", "cell_execution_reply"]
            )
            assert_json_content(data, exec_count)

            # third chunk received should be a cell_update with
            # the new output, and an execution_state of 'busy'
            # since it is still processing
            data = await receive_json(websocket, msg_types=["cell_update"])
            expected = {
                "cell_update": [
                    {
                        "cell_type": "code",
                        "execution_count": 1,
                        "metadata": {
                            "jupyter_d1": {
                                "position": 2,
                                "uuid": cell_uuid,
                                "notebook_uuid": uuid,
                                "execution_state": "busy",
                            }
                        },
                        "outputs": [
                            {
                                "data": {"text/plain": "7"},
                                "execution_count": 1,
                                "metadata": {},
                                "output_type": "execute_result",
                            }
                        ],
                        "source": "2+5",
                    }
                ]
            }

            # from pprint import pprint
            # print("data")
            # pprint(data)
            # print("expected")
            # pprint(expected)
            assert data == expected

            # third chunk received should be a cell_update with
            # an execution_state of 'idle' becuase it's all done
            data = await receive_json(websocket, msg_types=["cell_update"])
            d1_metadata = data["cell_update"][0]["metadata"]["jupyter_d1"]
            assert d1_metadata["execution_state"] == "idle"

            data = await receive_json(websocket, msg_types=["vars"])
            assert len(data["vars"]) == 14

    @pytest.mark.asyncio
    async def test_notebook_sequential_execute(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        cell_uuid1 = cells[1]["metadata"]["jupyter_d1"]["uuid"]
        cell_uuid2 = cells[2]["metadata"]["jupyter_d1"]["uuid"]
        cell_uuid3 = cells[3]["metadata"]["jupyter_d1"]["uuid"]

        code1 = """import time; time.sleep(1.1); print("checkpoint1")"""
        code2 = """import time; time.sleep(1.2); print("checkpoint2")"""
        code3 = """import time; time.sleep(1.3); print("checkpoint3")"""

        params1 = {"source": code1}
        params2 = {"source": code2}
        params3 = {"source": code3}

        resp1 = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid1}",
            json=params1,
            headers=superuser_token_headers,
        )
        assert resp1.status_code == 200

        resp2 = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid2}",
            json=params2,
            headers=superuser_token_headers,
        )
        assert resp2.status_code == 200

        resp3 = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid3}",
            json=params3,
            headers=superuser_token_headers,
        )
        assert resp3.status_code == 200

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            pass

            # await asyncio.sleep(WEBSOCKET_SLEEP_TIME)
            await asyncio.sleep(3.5)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid1}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid2}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid3}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            # Messages on the web socket can arrive in a slightly different
            # order from run to run.  The 'cell_update' messages arrive arround
            # the same time as some of the cell_execution messages.  It doesn't
            # really matter, but it makes testing tricky.  For a stable test,
            # gather all the responses and split them into two lists, one for
            # cell_update messages and one for all the others.

            # The most important thing for this test is that all the
            # "cell_execution_request" messages arrive first as the cells are
            # queued for execution and the "cell_execution_input",
            # "cell_execution_reply", etc messages show up later as the cells
            # are processed.

            cell_update_msgs = []
            non_cell_update_msgs = []
            for i in range(22):
                data = await receive_json(websocket)
                if "cell_update" in data.keys():
                    cell_update_msgs.append(data)
                else:
                    non_cell_update_msgs.append(data)

            # should get three execution requests
            data = non_cell_update_msgs.pop(0)
            assert "cell_execution_request" in data.keys()
            msg_id1 = data["cell_execution_request"]["message_id"]
            assert len(msg_id1) in msg_id_lengths

            data = non_cell_update_msgs.pop(0)
            assert "cell_execution_request" in data.keys()
            msg_id2 = data["cell_execution_request"]["message_id"]
            assert len(msg_id2) in msg_id_lengths

            data = non_cell_update_msgs.pop(0)
            assert "cell_execution_request" in data.keys()
            msg_id3 = data["cell_execution_request"]["message_id"]
            assert len(msg_id3) in msg_id_lengths

            for cell_uuid in (cell_uuid1, cell_uuid2, cell_uuid3):
                data = cell_update_msgs.pop(0)
                assert len(data["cell_update"]) == 1
                cell_data = data["cell_update"][0]
                d1_metadata = cell_data["metadata"]["jupyter_d1"]
                assert d1_metadata["execution_state"] == "pending"
                assert d1_metadata["uuid"] == cell_uuid
                assert cell_data["execution_count"] is None
                assert len(cell_data["outputs"]) == 0

            # cell update for the first executing cell
            data = cell_update_msgs.pop(0)
            assert "cell_update" in data.keys()
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"]["uuid"]
                == cell_uuid1
            )

            # cell_execution_input for the first cell's code being executed
            data = non_cell_update_msgs.pop(0)
            assert "cell_execution_input" in data
            assert (
                data["cell_execution_input"]["content"]["code"] == code1
            ), f'Failed to find "{code1}" in  data: {data}'
            assert (
                data["cell_execution_input"]["parent_id"] == msg_id1
            ), f"Failed to find expected parent_id"

            # stream output now sends a cell_update
            data = cell_update_msgs.pop(0)
            assert "cell_update" in data.keys()
            assert data["cell_update"][0]["outputs"][0]["text"] == [
                "checkpoint1\n",
                "\n",
            ], f"Failed to find checkpoint1 in cell_update data: {data}"

            # execution_reply for the end of the first cell's execution
            data = non_cell_update_msgs.pop(0)
            assert "cell_execution_reply" in data.keys()
            assert data["cell_execution_reply"]["parent_id"] == msg_id1

            # cell update with the results of the first cell's execution
            data = cell_update_msgs.pop(0)
            assert "cell_update" in data.keys()
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"]["uuid"]
                == cell_uuid1
            )

            # cell update for the begining of the second cell's execution
            data = cell_update_msgs.pop(0)
            assert "cell_update" in data.keys()
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"]["uuid"]
                == cell_uuid2
            )

            # cell_input update with the second cell's code being executed
            data = non_cell_update_msgs.pop(0)
            assert "cell_execution_input" in data
            assert (
                data["cell_execution_input"]["content"]["code"] == code2
            ), f'Failed to find "{code2}" in cell_update data: {data}'
            assert (
                data["cell_execution_input"]["parent_id"] == msg_id2
            ), f"Failed to find expected parent_id"

            # stream output of the second cell's execution
            data = cell_update_msgs.pop(0)
            assert "cell_update" in data.keys()
            assert data["cell_update"][0]["outputs"][0]["text"] == [
                "checkpoint2\n",
                "\n",
            ], f"Failed to find checkpoint2 in cell_update data: {data}"

            # exectuion_reply for the end of the second cell's execution
            data = non_cell_update_msgs.pop(0)
            assert "cell_execution_reply" in data.keys()
            assert data["cell_execution_reply"]["parent_id"] == msg_id2

            # cell_update with the results of the second cell
            data = cell_update_msgs.pop(0)
            assert "cell_update" in data.keys()
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"]["uuid"]
                == cell_uuid2
            )

            # cell_update as the third cell begins execution
            data = cell_update_msgs.pop(0)
            assert "cell_update" in data.keys()
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"]["uuid"]
                == cell_uuid3
            )

            # cell_execution_input with third cell code about to be executed
            data = non_cell_update_msgs.pop(0)
            assert "cell_execution_input" in data
            assert (
                data["cell_execution_input"]["content"]["code"] == code3
            ), f'Failed to find "{code3}" in cell_update data: {data}'
            assert (
                data["cell_execution_input"]["parent_id"] == msg_id3
            ), f"Failed to find expected parent_id"

            # stream output of the third cell
            data = cell_update_msgs.pop(0)
            assert "cell_update" in data.keys()
            assert data["cell_update"][0]["outputs"][0]["text"] == [
                "checkpoint3\n",
                "\n",
            ], f"Failed to find checkpoint3 in cell_update data: {data}"

            # execution reply for finishing the third cell's execution
            data = non_cell_update_msgs.pop(0)
            assert "cell_execution_reply" in data.keys()
            assert data["cell_execution_reply"]["parent_id"] == msg_id3

            # cell_update for cell three with the output
            data = cell_update_msgs.pop(0)
            assert "cell_update" in data.keys()
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"]["uuid"]
                == cell_uuid3
            )

            # var update
            data = non_cell_update_msgs.pop(0)
            assert "vars" in data.keys()

    @pytest.mark.asyncio
    async def test_cell_patch_and_execute(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == 'print("Larry the Llama")'

        cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        params = {"source": "7-9"}
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        response = await client.get(
            f"/notebooks/{uuid}/vars", headers=superuser_token_headers
        )
        assert response.status_code == 200
        assert len(response.json()["vars"]) == 0

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.patch(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                json=params,
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            expected = {
                "cell_update": [
                    {
                        "cell_type": "code",
                        "execution_count": 1,
                        "metadata": {
                            "jupyter_d1": {
                                "position": 1,
                                "uuid": cell_uuid,
                                "notebook_uuid": uuid,
                                "execution_state": "busy",
                            }
                        },
                        "outputs": [
                            {
                                "data": {"text/plain": "-2"},
                                "execution_count": 1,
                                "metadata": {},
                                "output_type": "execute_result",
                            }
                        ],
                        "source": "7-9",
                    }
                ]
            }

            patch_json = response.json()
            # response should contain both the 'cell','kernel_message' wrappers
            assert "cell" in patch_json.keys()
            msg_id = response.json()["kernel_message"]["message_id"]
            assert len(msg_id) in msg_id_lengths

            # 1 update from the cell patch, 1 from execution
            update1 = await receive_json(websocket, msg_types=["cell_update"])
            update2 = await receive_json(websocket, msg_types=["cell_update"])
            for data in (update1, update2):
                assert len(data["cell_update"]) == 1
                cell_data = data["cell_update"][0]
                d1_metadata = cell_data["metadata"]["jupyter_d1"]
                assert d1_metadata["execution_state"] == "pending"
                assert d1_metadata["uuid"] == cell_uuid
                assert cell_data["execution_count"] is None
                assert len(cell_data["outputs"]) == 0

            exec_reply = await receive_json(
                websocket, msg_types=["cell_execution_reply"]
            )
            assert exec_reply["cell_execution_reply"]["cell_id"] == cell_uuid
            assert exec_reply["cell_execution_reply"]["parent_id"] == msg_id

            data = await receive_json(websocket, msg_types=["cell_update"])
            assert data == expected

    @pytest.mark.asyncio
    async def test_cell_patch_and_execute_first_cell_imports_only(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Test for CAL-1048, first cell doesnt show execution count if it only
        contains imports.
        """
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == 'print("Larry the Llama")'

        cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        params = {
            "source": "import matplotlib as mpl\nimport matplotlib.pyplot as plt"
            "\nimport numpy as np"
        }
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        response = await client.get(
            f"/notebooks/{uuid}/vars", headers=superuser_token_headers
        )
        assert response.status_code == 200
        assert len(response.json()["vars"]) == 0

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.patch(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                json=params,
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            patch_json = response.json()
            # response should contain both the 'cell','kernel_message' wrappers
            assert "cell" in patch_json.keys()
            msg_id = response.json()["kernel_message"]["message_id"]
            assert len(msg_id) in msg_id_lengths

            expected = [
                # second cell_update comes from the cell execution starting
                {
                    "cell_update": [
                        {
                            "cell_type": "code",
                            "execution_count": None,
                            "metadata": {
                                "jupyter_d1": {
                                    "position": 1,
                                    "uuid": cell_uuid,
                                    "notebook_uuid": uuid,
                                    "execution_state": "busy",
                                }
                            },
                            "outputs": [],
                            "source": params["source"],
                        }
                    ]
                },
                # third cell_update comes from the cell execution finishing
                {
                    "cell_update": [
                        {
                            "cell_type": "code",
                            "execution_count": 1,
                            "metadata": {
                                "jupyter_d1": {
                                    "position": 1,
                                    "uuid": cell_uuid,
                                    "notebook_uuid": uuid,
                                    "execution_state": "idle",
                                }
                            },
                            "outputs": [],
                            "source": params["source"],
                        }
                    ]
                },
            ]

            # Order of websocket messages can be a bit variable, we make sure the
            # order of cell_updates is what we expect, otherwise we just check that the
            # messages we expect came through at some point
            msgs = await collect_websocket_messages(websocket, limit=7)

            cell_updates = filter_websocket_collection(msgs, "cell_update")
            assert len(cell_updates) == 4

            for data in cell_updates[:2]:
                assert len(data["cell_update"]) == 1
                cell_data = data["cell_update"][0]
                d1_metadata = cell_data["metadata"]["jupyter_d1"]
                assert d1_metadata["execution_state"] == "pending"
                assert d1_metadata["uuid"] == cell_uuid
                assert cell_data["execution_count"] is None
                assert len(cell_data["outputs"]) == 0

            assert cell_updates[2] == expected[0]
            assert cell_updates[3] == expected[1]

            exec_requests = filter_websocket_collection(
                msgs, "cell_execution_request"
            )
            assert len(exec_requests) == 1
            exec_request = exec_requests[0]
            assert (
                exec_request["cell_execution_request"]["cell_id"] == cell_uuid
            )
            assert (
                exec_request["cell_execution_request"]["message_id"] == msg_id
            )

            exec_inputs = filter_websocket_collection(
                msgs, "cell_execution_input"
            )
            assert len(exec_inputs) == 1
            exec_input = exec_inputs[0]
            assert exec_input["cell_execution_input"]["parent_id"] == msg_id
            assert (
                exec_input["cell_execution_input"]["content"]["code"]
                == params["source"]
            )
            assert (
                exec_input["cell_execution_input"]["content"][
                    "execution_count"
                ]
                == 1
            )

            exec_replies = filter_websocket_collection(
                msgs, "cell_execution_reply"
            )
            assert len(exec_replies) == 1
            exec_reply = exec_replies[0]
            assert exec_reply["cell_execution_reply"]["cell_id"] == cell_uuid
            assert exec_reply["cell_execution_reply"]["parent_id"] == msg_id
            assert exec_reply["cell_execution_reply"]["execution_count"] == 1

            # At the end we expect a vars update
            more_msgs = await collect_websocket_messages(websocket)
            assert len(more_msgs) == 1
            assert "vars" in more_msgs[0]

    @pytest.mark.asyncio
    async def test_notebook_cell_add(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)
            params = {
                "cell_type": "markdown",
                "source": "__**Hello Callisto!**__",
            }
            response = await client.post(
                f"/notebooks/{uuid}/cells",
                json=params,
                headers=superuser_token_headers,
            )
            assert response.status_code == 201

            data = await receive_json(websocket, msg_types=["cell_add"])
            cells = data["cell_add"]
            assert len(cells) == 5  # should dump all the cells
            cell = cells[-1]
            cell_uuid = cell["metadata"]["jupyter_d1"]["uuid"]

            expected = {
                "cell_type": "markdown",
                "metadata": {
                    "jupyter_d1": {
                        "position": 4,
                        "uuid": cell_uuid,
                        "notebook_uuid": uuid,
                    }
                },
                "source": "__**Hello Callisto!**__",
            }

            # from pprint import pprint
            # print("data")
            # pprint(data)
            # print("expected")
            # pprint(expected)
            compare_cells(cell, expected)

    @pytest.mark.asyncio
    async def test_notebook_cell_patch(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # get an existing cell
            response = await client.get(
                f"/notebooks/{uuid}/cells", headers=superuser_token_headers
            )
            assert response.status_code == 200
            cells = response.json()["cells"]
            assert cells[1]["source"] == 'print("Larry the Llama")'

            cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]
            params = {"source": "__Banana Rama!__"}
            response = await client.patch(
                f"/notebooks/{uuid}/cells/{cell_uuid}",
                json=params,
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            data = await receive_json(websocket)
            cells = data["cell_update"]
            assert len(cells) == 1
            cell = cells[0]

            expected = {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {
                    "jupyter_d1": {
                        "execution_state": "idle",
                        "position": 1,
                        "notebook_uuid": uuid,
                        "uuid": cell_uuid,
                    }
                },
                "outputs": [
                    {
                        "name": "stdout",
                        "output_type": "stream",
                        "text": "Larry the Llama\n",
                    }
                ],
                "source": "__Banana Rama!__",
            }

            assert cell == expected

    @pytest.mark.asyncio
    async def test_notebook_cell_patch_cell_type(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Patch cell type to code, make sure the resulting cell has outputs
        array since nbformat validation will fail without it
        """
        uuid = await upload_notebook(client, superuser_token_headers)

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # get an existing cell
            response = await client.get(
                f"/notebooks/{uuid}/cells", headers=superuser_token_headers
            )
            assert response.status_code == 200
            cells = response.json()["cells"]
            assert cells[0]["cell_type"] == "markdown"
            assert "outputs" not in cells[0]

            cell_uuid = cells[0]["metadata"]["jupyter_d1"]["uuid"]
            params = {"cell_type": "code"}
            response = await client.patch(
                f"/notebooks/{uuid}/cells/{cell_uuid}",
                json=params,
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            data = await receive_json(websocket)
            cells = data["cell_update"]
            assert len(cells) == 1
            cell = cells[0]

            expected = {
                "cell_type": "code",
                "metadata": {
                    "jupyter_d1": {
                        "execution_state": "idle",
                        "position": 0,
                        "notebook_uuid": uuid,
                        "uuid": cell_uuid,
                    }
                },
                "outputs": [],
                "source": "## Simple Test Notebook",
            }

            assert cell == expected

    @pytest.mark.asyncio
    async def test_notebook_cell_delete(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        cell = cells[2]
        cell_uuid = cell["metadata"]["jupyter_d1"]["uuid"]

        assert cells[3]["metadata"]["jupyter_d1"]["position"] == 3

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.delete(
                f"/notebooks/{uuid}/cells/{cell_uuid}",
                headers=superuser_token_headers,
            )
            assert response.status_code == 204

            data = await receive_json(websocket)

            del cells[2]
            cells[2]["metadata"]["jupyter_d1"]["position"] = 2
            expected = {"cell_delete": cells}

            assert data == expected

    @pytest.mark.asyncio
    async def test_notebook_cell_move(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # get the existing cells
            response = await client.get(
                f"/notebooks/{uuid}/cells", headers=superuser_token_headers
            )
            assert response.status_code == 200
            cells = response.json()["cells"]
            orig_uuids = list(
                map(lambda x: x["metadata"]["jupyter_d1"]["uuid"], cells)
            )

            # move the last cell to before the first cell
            before_uuid = orig_uuids[1]
            move_uuid = orig_uuids[3]

            params = {"before": before_uuid}
            response = await client.get(
                f"/notebooks/{uuid}/cells/{move_uuid}/move",
                query_string=params,
                headers=superuser_token_headers,
            )
            assert response.status_code == 204

            data = await receive_json(websocket)
            cells = data["cell_update"]
            assert len(cells) == 4  # should dump all the cells

            new_uuids = []
            for cell in cells:
                uuid = cell["metadata"]["jupyter_d1"]["uuid"]
                new_uuids.append(uuid)

            expected_uuids = [
                orig_uuids[0],
                orig_uuids[3],
                orig_uuids[1],
                orig_uuids[2],
            ]
            assert new_uuids == expected_uuids

            # Check cell positions
            assert_cell_positions(cells)

    @pytest.mark.asyncio
    async def test_notebook_cells_merge(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # get the existing cells
            response = await client.get(
                f"/notebooks/{uuid}/cells", headers=superuser_token_headers
            )
            assert response.status_code == 200
            cells = response.json()["cells"]
            cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]
            cells[2]["metadata"]["jupyter_d1"]["uuid"]
            next_cell_uuid = cells[3]["metadata"]["jupyter_d1"]["uuid"]
            assert cells[1]["source"] == 'print("Larry the Llama")'
            assert cells[2]["source"] == "2+5"

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/merge",
                query_string={"above": False},
                headers=superuser_token_headers,
            )
            assert response.status_code == 204

            data = await receive_json(websocket)
            cells = data["cell_delete"]
            assert len(cells) == 3
            assert cells[1]["source"] == 'print("Larry the Llama")\n2+5'
            assert cells[1]["metadata"]["jupyter_d1"]["uuid"] == cell_uuid
            assert cells[2]["source"] == ""
            assert cells[2]["metadata"]["jupyter_d1"]["uuid"] == next_cell_uuid
            # Check cell positions
            assert_cell_positions(cells)

    @pytest.mark.asyncio
    async def test_notebook_cell_split(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # get the existing cells
            response = await client.get(
                f"/notebooks/{uuid}/cells", headers=superuser_token_headers
            )
            assert response.status_code == 200
            cells = response.json()["cells"]
            cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]
            next_cell_uuid = cells[2]["metadata"]["jupyter_d1"]["uuid"]
            assert cells[1]["source"] == 'print("Larry the Llama")'

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/split",
                query_string={"split_location": 2},
                headers=superuser_token_headers,
            )
            assert response.status_code == 204

            data = await receive_json(websocket)
            cells = data["cell_update"]
            assert len(cells) == 5
            assert cells[1]["source"] == "pr"
            assert cells[1]["metadata"]["jupyter_d1"]["uuid"] == cell_uuid
            assert cells[2]["source"] == 'int("Larry the Llama")'
            assert cells[2]["metadata"]["jupyter_d1"]["uuid"] is not None
            assert cells[3]["metadata"]["jupyter_d1"]["uuid"] == next_cell_uuid

            # Check cell positions
            assert_cell_positions(cells)

    @pytest.mark.asyncio
    async def test_idle_status(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        permissionless_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
    ):
        async def is_idle_status():
            response = await client.get(
                f"/kernels/idle", headers=superuser_token_headers
            )
            assert response.status_code == 200
            json = response.json()
            return (
                json["idle"],
                datetime.strptime(json["last_idle"], "%Y-%m-%dT%H:%M:%S.%f"),
            )

        # Kernel is idle
        is_idle, last_idle_1 = await is_idle_status()
        assert is_idle is True

        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # Kernel is still idle
        is_idle, last_idle_2 = await is_idle_status()
        assert is_idle is True
        assert last_idle_1 == last_idle_2

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == 'print("Larry the Llama")'

        busy_cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]
        quick_cell_uuid = cells[2]["metadata"]["jupyter_d1"]["uuid"]

        params = {
            "source": "from time import sleep\nwhile True:\n    sleep(5)"
        }
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{busy_cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{quick_cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            data = await receive_json(websocket, msg_types=["vars"])
            assert "vars" in data

            # Need to wait for the UPDATE_WORKDIR_REQUEST to finish
            # (and we won't see it through the websocket)
            await asyncio.sleep(1)

            # Kernel is still idle (no code running)
            is_idle, last_idle_3 = await is_idle_status()
            assert is_idle is True
            assert last_idle_3 > last_idle_2

            response = await client.get(
                f"/notebooks/{uuid}/cells/{busy_cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            data = await wait_for_event(websocket, "cell_update")
            assert len(data["cell_update"]) == 1
            cell_data = data["cell_update"][0]
            d1_metadata = cell_data["metadata"]["jupyter_d1"]
            assert d1_metadata["execution_state"] == "pending"
            assert d1_metadata["uuid"] == busy_cell_uuid
            assert cell_data["execution_count"] is None
            assert len(cell_data["outputs"]) == 0

            # second chunk received should be a cell_update with
            # an execution_state of 'busy' when processing starts
            data = await wait_for_event(websocket, "cell_update")
            d1_metadata = data["cell_update"][0]["metadata"]["jupyter_d1"]
            assert d1_metadata["execution_state"] == "busy"

            # Kernel should not be idle now
            is_idle, last_idle_4 = await is_idle_status()
            assert is_idle is False
            assert last_idle_4 == last_idle_3

    @pytest.mark.asyncio
    async def test_kernel_interrupt(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
    ):
        async def is_idle_status():
            response = await client.get(
                f"/kernels/idle", headers=superuser_token_headers
            )
            assert response.status_code == 200
            json = response.json()
            return (
                json["idle"],
                datetime.strptime(json["last_idle"], "%Y-%m-%dT%H:%M:%S.%f"),
            )

        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # Kernel is idle
        is_idle, last_idle_1 = await is_idle_status()
        assert is_idle is True

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == 'print("Larry the Llama")'

        busy_cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        params = {
            "source": "from time import sleep\nwhile True:\n    sleep(5)"
        }
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{busy_cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{busy_cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            msg_id = response.json()["kernel_message"]["message_id"]

            data = await wait_for_event(websocket, "cell_update")
            assert len(data["cell_update"]) == 1
            cell_data = data["cell_update"][0]
            d1_metadata = cell_data["metadata"]["jupyter_d1"]
            assert d1_metadata["execution_state"] == "pending"
            assert d1_metadata["uuid"] == busy_cell_uuid
            assert cell_data["execution_count"] is None
            assert len(cell_data["outputs"]) == 0

            # first chunk received should be a cell_update with
            # an execution_state of 'busy' when processing starts
            data = await wait_for_event(websocket, "cell_update")
            d1_metadata = data["cell_update"][0]["metadata"]["jupyter_d1"]
            assert d1_metadata["execution_state"] == "busy"
            assert d1_metadata["uuid"] == busy_cell_uuid

            # Kernel should not be idle now
            is_idle, last_idle_2 = await is_idle_status()
            assert is_idle is False
            assert last_idle_2 == last_idle_1

            response = await client.get(
                f"/notebooks/{uuid}/interrupt_kernel",
                headers=superuser_token_headers,
            )
            assert response.status_code == 204

            data = await wait_for_event(websocket, "kernel_interrupted")
            assert data["kernel_interrupted"]["interrupted"] is True

            def assert_json_content(data, execution_count=None):
                if "cell_update" in data:
                    cell_data = data["cell_update"][0]
                    d1_metadata = cell_data["metadata"]["jupyter_d1"]
                    assert d1_metadata["execution_state"] == "idle"
                    assert d1_metadata["uuid"] == busy_cell_uuid
                    assert cell_data["execution_count"] == execution_count
                    return None
                elif "cell_execution_reply" in data:
                    assert data["cell_execution_reply"]["execution_count"] == 1
                    assert (
                        data["cell_execution_reply"]["cell_id"]
                        == busy_cell_uuid
                    )
                    assert (
                        len(data["cell_execution_reply"]["parent_id"])
                        in msg_id_lengths
                    )
                    assert data["cell_execution_reply"]["parent_id"] == msg_id
                    return 1
                else:
                    raise AssertionError(f"unexpected cell type: {data}")

            # Execution count update
            data = await wait_for_event(websocket, "cell_execution_reply")
            assert_json_content(data)

            # Receive cell error output
            data = await wait_for_event(websocket, "cell_update")
            d1_metadata = data["cell_update"][0]["metadata"]["jupyter_d1"]
            assert d1_metadata["execution_state"] == "idle"
            assert data["cell_update"][0]["execution_count"] == 1
            assert d1_metadata["position"] == 1
            assert d1_metadata["uuid"] == busy_cell_uuid
            cell = data["cell_update"][0]
            assert cell["cell_type"] == "code"
            assert len(cell["outputs"]) == 1
            assert cell["outputs"][0]["ename"] == "KeyboardInterrupt"
            assert "KeyboardInterrupt" in cell["outputs"][0]["traceback"][1]

            await clear_websocket_queue(websocket)

            # Kernel should be idle now
            is_idle, last_idle_3 = await is_idle_status()
            assert is_idle is True
            assert last_idle_3 > last_idle_2

    @pytest.mark.asyncio
    async def test_bogus_code_error(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        permissionless_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        params = {"source": "this isnt code"}
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            msg_id = response.json()["kernel_message"]["message_id"]

            data = await wait_for_event(websocket, "cell_update")
            assert len(data["cell_update"]) == 1
            cell_data = data["cell_update"][0]
            d1_metadata = cell_data["metadata"]["jupyter_d1"]
            assert d1_metadata["execution_state"] == "pending"
            assert d1_metadata["uuid"] == cell_uuid
            assert cell_data["execution_count"] is None
            assert len(cell_data["outputs"]) == 0

            # execution_count update and busy status update,
            # in uncertain order
            def assert_json_content(data, execution_count=None):
                if "cell_update" in data:
                    cell_data = data["cell_update"][0]
                    d1_metadata = cell_data["metadata"]["jupyter_d1"]
                    assert d1_metadata["execution_state"] == "busy"
                    assert d1_metadata["uuid"] == cell_uuid
                    assert d1_metadata["position"] == 1
                    assert cell_data["execution_count"] == execution_count
                    cell = data["cell_update"][0]
                    assert cell["cell_type"] == "code"
                    assert len(cell["outputs"]) == 0
                    return None
                elif "cell_execution_reply" in data:
                    assert data["cell_execution_reply"]["execution_count"] == 1
                    assert data["cell_execution_reply"]["cell_id"] == cell_uuid
                    assert (
                        len(data["cell_execution_reply"]["parent_id"])
                        in msg_id_lengths
                    )
                    assert data["cell_execution_reply"]["parent_id"] == msg_id
                    return 1
                else:
                    raise AssertionError(f"unexpected cell type: {data}")

            msg_types = [
                "cell_update",
                "cell_execution_reply",
            ]

            data = await receive_json(websocket, msg_types=msg_types)
            exec_count = assert_json_content(data)
            data = await receive_json(websocket, msg_types=msg_types)
            assert_json_content(data, exec_count)

            # Still busy with output, error output received
            data = await receive_json(websocket, msg_types=["cell_update"])
            d1_metadata = data["cell_update"][0]["metadata"]["jupyter_d1"]
            assert d1_metadata["execution_state"] == "busy"
            assert data["cell_update"][0]["execution_count"] is None
            assert d1_metadata["position"] == 1
            assert d1_metadata["uuid"] == cell_uuid
            cell = data["cell_update"][0]
            assert cell["cell_type"] == "code"
            assert len(cell["outputs"]) == 1
            assert cell["outputs"][0]["ename"] == "SyntaxError"
            assert "SyntaxError" in cell["outputs"][0]["traceback"][0]

            # Kernel vars update
            data = await receive_json(websocket, msg_types=["vars"])
            assert "vars" in data

    @pytest.mark.asyncio
    async def test_scratch_execute(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        permissionless_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.post(
                f"/notebooks/{uuid}/scratch_execute",
                headers=superuser_token_headers,
                json={"code": "4*5"},
            )
            assert response.status_code == 200
            message_id = response.json()["kernel_message"]["message_id"]

            # first chunk received should be a scratch_update with
            # an execution_state of 'busy' when processing starts
            data = await receive_json(websocket, msg_types=["scratch_update"])
            scratch_update = data["scratch_update"]
            assert scratch_update["message_id"] == message_id
            assert scratch_update["execution_state"] == "busy"

            # Receive scratch execution output
            data = await receive_json(websocket, msg_types=["scratch_update"])
            scratch_update = data["scratch_update"]
            expected_output = {
                "data": {"text/plain": "20"},
                "execution_count": 1,
                "metadata": {},
                "output_type": "execute_result",
            }
            assert scratch_update["output"] == expected_output

            # Scratch execution state set to idle
            data = await receive_json(websocket, msg_types=["scratch_update"])
            scratch_update = data["scratch_update"]
            assert scratch_update["message_id"] == message_id
            assert scratch_update["execution_state"] == "idle"

    @pytest.mark.asyncio
    async def test_scratch_code_idle_status(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        async def is_idle_status():
            response = await client.get(
                f"/kernels/idle", headers=superuser_token_headers
            )
            assert response.status_code == 200
            json = response.json()
            return (
                json["idle"],
                datetime.strptime(json["last_idle"], "%Y-%m-%dT%H:%M:%S.%f"),
            )

        # Kernel is idle
        is_idle, last_idle_1 = await is_idle_status()
        assert is_idle is True

        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # Kernel is still idle
        is_idle, last_idle_2 = await is_idle_status()
        assert is_idle is True
        assert last_idle_1 == last_idle_2

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.post(
                f"/notebooks/{uuid}/scratch_execute",
                headers=superuser_token_headers,
                json={"code": "4+9"},
            )
            assert response.status_code == 200
            message_id = response.json()["kernel_message"]["message_id"]

            # Execution state busy
            await receive_json(websocket, msg_types=["scratch_update"])
            # Execution output
            await receive_json(websocket, msg_types=["scratch_update"])
            # Execution state idle
            await receive_json(websocket, msg_types=["scratch_update"])

            # Kernel is still idle (no code running)
            is_idle, last_idle_3 = await is_idle_status()
            assert is_idle is True
            assert last_idle_3 > last_idle_2

            # Kernel vars update
            data = await receive_json(websocket, msg_types=["vars"])
            assert "vars" in data

            response = await client.post(
                f"/notebooks/{uuid}/scratch_execute",
                headers=superuser_token_headers,
                json={
                    "code": "from time import sleep\n"
                    "while True:\n    sleep(1)"
                },
            )
            assert response.status_code == 200
            message_id = response.json()["kernel_message"]["message_id"]

            # first chunk received should be a cell_update with
            # an execution_state of 'busy' when processing starts
            data = await wait_for_event(websocket, "scratch_update")
            scratch_update = data["scratch_update"]
            assert scratch_update["message_id"] == message_id
            assert scratch_update["execution_state"] == "busy"

            # Kernel should not be idle now
            is_idle, last_idle_4 = await is_idle_status()
            assert is_idle is False
            assert last_idle_4 > last_idle_3

    @pytest.mark.asyncio
    async def test_scratch_stream(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        permissionless_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.post(
                f"/notebooks/{uuid}/scratch_execute",
                headers=superuser_token_headers,
                json={
                    "code": "import time\nfor i in ('heres', 'a', "
                    "'streamofdata'):\n    print(i)\n    "
                    "time.sleep(0.3)"
                },
            )
            assert response.status_code == 200
            message_id = response.json()["kernel_message"]["message_id"]

            # first chunk received should be a scratch_update with
            # an execution_state of 'busy' when processing starts
            data = await receive_json(websocket, msg_types=["scratch_update"])
            scratch_update = data["scratch_update"]
            assert scratch_update["message_id"] == message_id
            assert scratch_update["execution_state"] == "busy"

            # Receive scratch execution output
            async def receive_text(text):
                data = await receive_json(
                    websocket, msg_types=["scratch_update"]
                )
                scratch_update = data["scratch_update"]
                expected_output = {
                    "name": "stdout",
                    "text": f"{text}\n",
                    "output_type": "stream",
                }
                assert scratch_update["output"] == expected_output

            await receive_text("heres")
            await receive_text("a")
            await receive_text("streamofdata")

            # Scratch execution state set to idle
            data = await receive_json(websocket, msg_types=["scratch_update"])
            scratch_update = data["scratch_update"]
            assert scratch_update["message_id"] == message_id
            assert scratch_update["execution_state"] == "idle"

    @pytest.mark.asyncio
    async def test_vars_update_cell_execute(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == 'print("Larry the Llama")'

        cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        params = {"source": "x = 7-9"}
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        response = await client.get(
            f"/notebooks/{uuid}/vars", headers=superuser_token_headers
        )
        assert response.status_code == 200
        assert len(response.json()["vars"]) == 0

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            # Kernel vars update
            data = await receive_json(websocket, msg_types=["vars"])
            vars = {
                var["name"]: {
                    "type": var["type"],
                    "value": var["value"],
                    "summary": var["summary"],
                }
                for var in data["vars"]
            }

            assert vars["x"]["type"] == "int"
            assert vars["x"]["value"]["single_value"] == "-2"
            assert vars["x"]["summary"] == "-2"

            response = await client.get(
                f"/notebooks/{uuid}/vars", headers=superuser_token_headers
            )
            assert response.status_code == 200
            current_vars = response.json()["vars"]
            current_vars = filter(
                lambda x: x["name"] != "___d1os", current_vars
            )
            assert list(current_vars) == data["vars"]

    @pytest.mark.asyncio
    async def test_vars_update_scratch_execute(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        response = await client.get(
            f"/notebooks/{uuid}/vars", headers=superuser_token_headers
        )
        assert response.status_code == 200
        assert len(response.json()["vars"]) == 0

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.post(
                f"/notebooks/{uuid}/scratch_execute",
                headers=superuser_token_headers,
                json={"code": "x_u = 27/10"},
            )
            assert response.status_code == 200

            # Kernel vars update
            data = await receive_json(websocket, msg_types=["vars"])
            vars = {
                var["name"]: {
                    "type": var["type"],
                    "value": var["value"],
                    "summary": var["summary"],
                }
                for var in data["vars"]
            }

            assert vars["x_u"]["type"] == "float"
            assert vars["x_u"]["value"]["single_value"] == "2.7"
            assert vars["x_u"]["summary"] == "2.7"

            response = await client.get(
                f"/notebooks/{uuid}/vars", headers=superuser_token_headers
            )
            assert response.status_code == 200
            current_vars = response.json()["vars"]
            current_vars = filter(
                lambda x: x["name"] != "___d1os", current_vars
            )
            assert list(current_vars) == data["vars"]

    @pytest.mark.asyncio
    async def test_notebook_write_permission(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        readonly_token_headers: Dict[str, str],
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        with pytest.raises(AssertionError):
            async with client.websocket_connect(
                f"/notebooks/{uuid}/ws/notebook",
                headers=readonly_token_headers,
            ):
                pass

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ):
            pass

    @pytest.mark.asyncio
    async def test_notebook_stream_permission(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        readonly_token_headers: Dict[str, str],
        permissionless_token_headers: Dict[str, str],
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        with pytest.raises(AssertionError):
            async with client.websocket_connect(
                f"/notebooks/{uuid}/ws/stream",
                headers=permissionless_token_headers,
            ):
                pass

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/stream", headers=readonly_token_headers
        ):
            pass

    @pytest.mark.asyncio
    async def test_vars_update_bash(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        response = await client.post(
            "/notebooks/create",
            query_string={"kspec_name": "bash", "filename": "heyp"},
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()["notebook"]
        uuid = resp_json["metadata"]["jupyter_d1"]["uuid"]

        response = await client.get(
            f"/notebooks/{uuid}/vars", headers=superuser_token_headers
        )
        assert response.status_code == 200
        vars_list = response.json()["vars"]
        assert len(vars_list) == 0

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.post(
                f"/notebooks/{uuid}/scratch_execute",
                headers=superuser_token_headers,
                json={"code": "export D1_VAR_TEST=p903s"},
            )
            assert response.status_code == 200

            data = await receive_json(
                websocket, timeout=60, msg_types=["vars"]
            )
            vars = {
                var["name"]: {
                    "type": var["type"],
                    "value": var["value"],
                    "summary": var["summary"],
                }
                for var in data["vars"]
            }
            assert vars["D1_VAR_TEST"]["type"] is None
            assert vars["D1_VAR_TEST"]["value"]["single_value"] == "p903s"
            assert vars["D1_VAR_TEST"]["summary"] == "p903s"

    @pytest.mark.asyncio
    async def test_vars_update_r_kernel(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        response = await client.post(
            "/notebooks/create",
            query_string={"kspec_name": "ir", "filename": "heyp"},
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()["notebook"]
        uuid = resp_json["metadata"]["jupyter_d1"]["uuid"]

        response = await client.get(
            f"/notebooks/{uuid}/vars", headers=superuser_token_headers
        )
        assert response.status_code == 200
        vars_list = response.json()["vars"]
        assert len(vars_list) == 0

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.post(
                f"/notebooks/{uuid}/scratch_execute",
                headers=superuser_token_headers,
                json={
                    "code": "ffo <- 9\n"
                    'k = data.frame(col1=c("t", 5), '
                    'col2=c("4", 6), col3=c("h", 8))'
                },
            )
            assert response.status_code == 200

            data = await receive_json(
                websocket, timeout=70, msg_types=["vars"], max_retries=50
            )
            vars = {var["name"]: var for var in data["vars"]}
            print(f"vars output: {vars}")

            assert vars["ffo"]["type"] == "numeric"
            assert vars["ffo"]["abbreviated"] is False
            assert vars["ffo"]["has_next_page"] is False
            assert vars["ffo"]["summary"] == "9"
            assert vars["ffo"]["value"]["single_value"] == "9"
            assert vars["k"]["type"] == "data.frame"
            assert vars["k"]["abbreviated"] is False
            assert vars["k"]["has_next_page"] is False
            assert "Size: 2x3 Memory: " in vars["k"]["summary"]
            assert vars["k"]["value"]["multi_value"]["column_count"] == 3
            assert vars["k"]["value"]["multi_value"]["row_count"] == 2
            assert vars["k"]["value"]["multi_value"]["column_names"] is None
            assert vars["k"]["value"]["multi_value"]["row_names"] is None
            assert vars["k"]["value"]["multi_value"]["column_types"] is None
            assert vars["k"]["value"]["multi_value"]["data"] is None

    @pytest.mark.asyncio
    async def test_page_payload(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        response = await client.post(
            "/notebooks/create",
            query_string={"kspec_name": "python", "filename": "heyp"},
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()["notebook"]
        uuid = resp_json["metadata"]["jupyter_d1"]["uuid"]

        response = await client.post(
            f"/notebooks/{uuid}/cells",
            headers=superuser_token_headers,
            json={"cell_type": "code", "source": "?str"},
        )
        cell_uuid = response.json()["cell"]["metadata"]["jupyter_d1"]["uuid"]

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            msg_id = response.json()["kernel_message"]["message_id"]

            data = await receive_json(websocket, msg_types=["payload_page"])
            assert "text/plain" in data["payload_page"]["data"]
            assert data["payload_page"]["message_id"] == msg_id
            assert data["payload_page"]["start"] == 0

    @pytest.mark.asyncio
    async def test_code_completion(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        response = await client.post(
            "/notebooks/create",
            query_string={"kspec_name": "python", "filename": "heyp"},
            headers=superuser_token_headers,
        )
        print(response.content)
        assert response.status_code == 201
        resp_json = response.json()["notebook"]
        uuid = resp_json["metadata"]["jupyter_d1"]["uuid"]

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.post(
                f"/notebooks/{uuid}/complete",
                json={"code": "s"},
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            msg_id = response.json()["kernel_message"]["message_id"]

            data = await receive_json(websocket)
            assert len(data["complete_reply"]["matches"]) > 0
            assert data["complete_reply"]["message_id"] == msg_id
            assert data["complete_reply"]["cursor_start"] == 0
            assert data["complete_reply"]["cursor_end"] == 1

    @pytest.mark.asyncio
    async def test_code_completion_cursor_position(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        response = await client.post(
            "/notebooks/create",
            query_string={"kspec_name": "python", "filename": "heyp"},
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()["notebook"]
        uuid = resp_json["metadata"]["jupyter_d1"]["uuid"]

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.post(
                f"/notebooks/{uuid}/complete",
                json={"code": "5 + prin + 6", "cursor_position": 7},
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            msg_id = response.json()["kernel_message"]["message_id"]

            data = await receive_json(websocket)
            assert data["complete_reply"]["matches"] == ["print"]
            assert data["complete_reply"]["message_id"] == msg_id
            assert data["complete_reply"]["cursor_start"] == 4
            assert data["complete_reply"]["cursor_end"] == 7

    @pytest.mark.asyncio
    async def test_code_completion_websocket(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """Test sending code completion command over websocket"""
        response = await client.post(
            "/notebooks/create",
            query_string={"kspec_name": "python", "filename": "heyp"},
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()["notebook"]
        uuid = resp_json["metadata"]["jupyter_d1"]["uuid"]

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            await websocket.send_json(
                {
                    "command": "complete",
                    "command_id": "32543-rrep-443",
                    "body": {
                        "code": "5 + prin + 6",
                        "cursor_position": 7,
                    },
                }
            )

            data = await receive_json(websocket)
            assert data["complete_reply"]["matches"] == ["print"]
            assert data["complete_reply"]["message_id"] is not None
            assert data["complete_reply"]["command_id"] == "32543-rrep-443"
            assert data["complete_reply"]["cursor_start"] == 4
            assert data["complete_reply"]["cursor_end"] == 7

    @pytest.mark.asyncio
    async def test_history(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        cell = cells[2]
        cell_uuid = cell["metadata"]["jupyter_d1"]["uuid"]

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            await receive_json(websocket)
            await receive_json(websocket)
            await receive_json(websocket)
            await receive_json(websocket)
            await receive_json(websocket)

            response = await client.post(
                f"/notebooks/{uuid}/history", headers=superuser_token_headers
            )
            assert response.status_code == 200
            msg_id = response.json()["kernel_message"]["message_id"]

            data = await wait_for_event(websocket, "history_reply")

            assert data["history_reply"]["message_id"] == msg_id
            history = data["history_reply"]["history"]
            assert history[0]["line_number"] == 0
            assert history[0]["input"] == ""
            assert history[0]["output"] is None
            assert history[1]["line_number"] == 1
            assert history[1]["input"] == "2+5"
            assert history[1]["output"] == "7"

    @pytest.mark.asyncio
    async def test_restart_kernel(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        cell = cells[2]
        cell_uuid = cell["metadata"]["jupyter_d1"]["uuid"]

        response = await client.get(
            f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        await asyncio.sleep(0.5)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        assert cells[2]["outputs"][0]["data"]["text/plain"] == "7"

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/restart_kernel",
                headers=superuser_token_headers,
            )

            assert response.status_code == 204

            data = await wait_for_event(websocket, "kernel_restarted")

            assert data["kernel_restarted"]["run_all_cells"] is False
            cells = data["kernel_restarted"]["cells"]
            assert cells[2]["outputs"][0]["data"]["text/plain"] == "7"
            assert cells[2]["execution_count"] == 1

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        for cell in cells:
            assert cells[2]["outputs"][0]["data"]["text/plain"] == "7"
            assert cells[2]["execution_count"] == 1

    @pytest.mark.asyncio
    async def test_restart_kernel_and_clear_output(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        cell = cells[2]
        cell_uuid = cell["metadata"]["jupyter_d1"]["uuid"]

        response = await client.get(
            f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        await asyncio.sleep(0.5)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        assert cells[2]["outputs"][0]["data"]["text/plain"] == "7"

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/restart_kernel_and_clear_output",
                headers=superuser_token_headers,
            )

            assert response.status_code == 204

            data = await wait_for_event(websocket, "kernel_restarted")

            assert data["kernel_restarted"]["run_all_cells"] is False
            cells = data["kernel_restarted"]["cells"]
            for cell in cells:
                assert (
                    ("outputs" not in cell or len(cell["outputs"]) == 0)
                    and "execution_count" not in cell
                    or cell["execution_count"] is None
                )

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        for cell in cells:
            assert (
                ("outputs" not in cell or len(cell["outputs"]) == 0)
                and "execution_count" not in cell
                or cell["execution_count"] is None
            )

    @pytest.mark.asyncio
    async def test_restart_kernel_and_run_all_cells(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        cell_ids = [c["metadata"]["jupyter_d1"]["uuid"] for c in cells]

        cell = cells[2]
        cell_uuid = cell["metadata"]["jupyter_d1"]["uuid"]

        response = await client.get(
            f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        await asyncio.sleep(0.5)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        assert "outputs" not in cells[0]
        assert cells[1]["outputs"][0]["text"] == "Larry the Llama\n"
        assert cells[2]["outputs"][0]["data"]["text/plain"] == "7"

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # Clear the web socket before we start
            await collect_websocket_messages(websocket, timeout=2)

            response = await client.get(
                f"/notebooks/{uuid}/restart_kernel_and_execute_all",
                headers=superuser_token_headers,
            )

            assert response.status_code == 200

            msgs = await collect_websocket_messages(websocket, timeout=10)
            kernel_restarted_msgs = filter_websocket_collection(
                msgs, "kernel_restarted"
            )
            cell_update_msgs = filter_websocket_collection(msgs, "cell_update")

            data = kernel_restarted_msgs.pop(0)
            assert data["kernel_restarted"]["run_all_cells"] is True
            cells = data["kernel_restarted"]["cells"]
            for cell in cells:
                assert (
                    ("outputs" not in cell or len(cell["outputs"]) == 0)
                    and "execution_count" not in cell
                    or cell["execution_count"] is None
                )

            # These two pop up due to the restart
            data = cell_update_msgs.pop(0)
            cell = data["cell_update"][0]
            assert cell["outputs"][0]["data"]["text/plain"] == "7"
            assert cell["execution_count"] == 1
            assert cell["metadata"]["jupyter_d1"]["execution_state"] == "busy"
            data = cell_update_msgs.pop(0)
            cell = data["cell_update"][0]
            assert cell["outputs"][0]["data"]["text/plain"] == "7"
            assert cell["execution_count"] == 1
            assert cell["metadata"]["jupyter_d1"]["execution_state"] == "idle"

            for cell_id in cell_ids[1:4]:
                data = cell_update_msgs.pop(0)
                assert len(data["cell_update"]) == 1
                cell_data = data["cell_update"][0]
                d1_metadata = cell_data["metadata"]["jupyter_d1"]
                assert d1_metadata["execution_state"] == "pending"
                assert d1_metadata["uuid"] == cell_id
                assert cell_data["execution_count"] is None
                assert len(cell_data["outputs"]) == 0

            data = cell_update_msgs.pop(0)
            cell = data["cell_update"][0]
            assert len(cell["outputs"]) == 0
            assert cell["metadata"]["jupyter_d1"]["execution_state"] == "busy"

            # This used to be a cell_stream msg
            data = cell_update_msgs.pop(0)
            cell = data["cell_update"][0]
            assert cell["outputs"][0]["text"] == ["Larry the Llama\n", "\n"]
            assert cell["metadata"]["jupyter_d1"]["execution_state"] == "busy"

            data = cell_update_msgs.pop(0)
            cell = data["cell_update"][0]
            assert cell["outputs"][0]["text"] == ["Larry the Llama\n", "\n"]
            assert cell["execution_count"] == 1
            assert cell["metadata"]["jupyter_d1"]["execution_state"] == "idle"

            data = cell_update_msgs.pop(0)
            cell = data["cell_update"][0]
            assert len(cell["outputs"]) == 0
            assert cell["metadata"]["jupyter_d1"]["execution_state"] == "busy"

            data = cell_update_msgs.pop(0)
            cell = data["cell_update"][0]
            assert cell["outputs"][0]["data"]["text/plain"] == "7"
            assert cell["execution_count"] == 2
            assert cell["metadata"]["jupyter_d1"]["execution_state"] == "busy"

            data = cell_update_msgs.pop(0)
            cell = data["cell_update"][0]
            assert cell["outputs"][0]["data"]["text/plain"] == "7"
            assert cell["execution_count"] == 2
            assert cell["metadata"]["jupyter_d1"]["execution_state"] == "idle"

    @pytest.mark.asyncio
    async def test_clear_single_cell(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        response = await client.get(
            f"/notebooks/{uuid}/execute_all",
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells", headers=superuser_token_headers
            )
            assert response.status_code == 200
            cells = response.json()["cells"]

            assert cells[1]["execution_count"] == 1
            assert cells[1]["outputs"][0]["text"] == [
                "Larry the Llama\n",
                "\n",
            ]
            assert cells[2]["execution_count"] == 2
            assert cells[2]["outputs"][0]["data"]["text/plain"] == "7"

            # Clear the web socket before we start
            await collect_websocket_messages(websocket, timeout=2)

            # Clear cell 1
            cell_id = cells[1]["metadata"]["jupyter_d1"]["uuid"]
            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_id}/clear",
                headers=superuser_token_headers,
            )
            assert response.status_code == 204

            msgs = await collect_websocket_messages(websocket, timeout=10)
            cell_update_msgs = filter_websocket_collection(msgs, "cell_update")

            assert len(cell_update_msgs) == 1

            data = cell_update_msgs.pop(0)
            cell = data["cell_update"][0]
            assert cell["metadata"]["jupyter_d1"]["uuid"] == (
                cells[1]["metadata"]["jupyter_d1"]["uuid"]
            )
            assert cell["outputs"] == []
            assert cell["execution_count"] is None
            assert cell["metadata"]["jupyter_d1"]["execution_state"] == "idle"

            # Cell 2 still has output
            response = await client.get(
                f"/notebooks/{uuid}/cells", headers=superuser_token_headers
            )
            assert response.status_code == 200
            cells = response.json()["cells"]
            assert cells[1]["execution_count"] is None
            assert cells[1]["outputs"] == []
            assert cells[2]["execution_count"] == 2
            assert cells[2]["outputs"][0]["data"]["text/plain"] == "7"

            # Clear cell 2
            cell_id = cells[2]["metadata"]["jupyter_d1"]["uuid"]
            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_id}/clear",
                headers=superuser_token_headers,
            )
            assert response.status_code == 204

            msgs = await collect_websocket_messages(websocket, timeout=10)
            cell_update_msgs = filter_websocket_collection(msgs, "cell_update")

            assert len(cell_update_msgs) == 1

            data = cell_update_msgs.pop(0)
            cell = data["cell_update"][0]
            assert cell["metadata"]["jupyter_d1"]["uuid"] == (
                cells[2]["metadata"]["jupyter_d1"]["uuid"]
            )
            assert cell["outputs"] == []
            assert cell["execution_count"] is None
            assert cell["metadata"]["jupyter_d1"]["execution_state"] == "idle"

            # Both cells are empty now
            response = await client.get(
                f"/notebooks/{uuid}/cells", headers=superuser_token_headers
            )
            assert response.status_code == 200
            cells = response.json()["cells"]
            assert cells[1]["execution_count"] is None
            assert cells[1]["outputs"] == []
            assert cells[2]["execution_count"] is None
            assert cells[2]["outputs"] == []

    @pytest.mark.asyncio
    async def test_clear_all_cells(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        ututils: TestCase,
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        response = await client.get(
            f"/notebooks/{uuid}/execute_all",
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # Clear the web socket before we start
            await collect_websocket_messages(websocket, timeout=2)

            response = await client.get(
                f"/notebooks/{uuid}/cells", headers=superuser_token_headers
            )
            assert response.status_code == 200
            cells = response.json()["cells"]

            # Cells have output and execution counts
            assert cells[1]["execution_count"] == 1
            assert cells[1]["outputs"][0]["text"] == [
                "Larry the Llama\n",
                "\n",
            ]
            assert cells[2]["execution_count"] == 2
            assert cells[2]["outputs"][0]["data"]["text/plain"] == "7"
            assert cells[3]["execution_count"] == 3
            assert cells[3]["outputs"] == []

            # Clear all
            cells[1]["metadata"]["jupyter_d1"]["uuid"]
            response = await client.get(
                f"/notebooks/{uuid}/clear_all",
                headers=superuser_token_headers,
            )
            assert response.status_code == 204

            msgs = await collect_websocket_messages(websocket, timeout=10)
            cell_update_msgs = filter_websocket_collection(msgs, "cell_update")

            data = cell_update_msgs.pop(0)
            cell = data["cell_update"][0]
            assert cell["metadata"]["jupyter_d1"]["uuid"] == (
                cells[0]["metadata"]["jupyter_d1"]["uuid"]
            )
            assert cell["metadata"]["jupyter_d1"]["execution_state"] == "idle"

            data = cell_update_msgs.pop(0)
            cell = data["cell_update"][0]
            assert cell["metadata"]["jupyter_d1"]["uuid"] == (
                cells[1]["metadata"]["jupyter_d1"]["uuid"]
            )
            assert cell["outputs"] == []
            assert cell["execution_count"] is None
            assert cell["metadata"]["jupyter_d1"]["execution_state"] == "idle"

            data = cell_update_msgs.pop(0)
            cell = data["cell_update"][0]
            assert cell["metadata"]["jupyter_d1"]["uuid"] == (
                cells[2]["metadata"]["jupyter_d1"]["uuid"]
            )
            assert cell["outputs"] == []
            assert cell["execution_count"] is None
            assert cell["metadata"]["jupyter_d1"]["execution_state"] == "idle"

            data = cell_update_msgs.pop(0)
            cell = data["cell_update"][0]
            assert cell["metadata"]["jupyter_d1"]["uuid"] == (
                cells[3]["metadata"]["jupyter_d1"]["uuid"]
            )
            assert cell["outputs"] == []
            assert cell["execution_count"] is None
            assert cell["metadata"]["jupyter_d1"]["execution_state"] == "idle"

            assert len(cell_update_msgs) == 0

            # Both cells are empty now
            response = await client.get(
                f"/notebooks/{uuid}/cells", headers=superuser_token_headers
            )
            assert response.status_code == 200
            cells = response.json()["cells"]
            assert cells[1]["execution_count"] is None
            assert cells[1]["outputs"] == []
            assert cells[2]["execution_count"] is None
            assert cells[2]["outputs"] == []
            assert cells[3]["execution_count"] is None
            assert cells[3]["outputs"] == []

    @pytest.mark.asyncio
    async def test_ipython_kernel_startup_script(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Test that the callisto_startup.py startup script is run when the
        kernel starts.
        """
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == 'print("Larry the Llama")'

        cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        params = {
            "source": "import pandas as pd\n"
            'pd.get_option("display.html.table_schema")'
        }
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        response = await client.get(
            f"/notebooks/{uuid}/vars", headers=superuser_token_headers
        )
        assert response.status_code == 200
        assert len(response.json()["vars"]) == 0

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.patch(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                json=params,
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            expected = {
                "cell_update": [
                    {
                        "cell_type": "code",
                        "execution_count": 1,
                        "metadata": {
                            "jupyter_d1": {
                                "position": 1,
                                "uuid": cell_uuid,
                                "notebook_uuid": uuid,
                                "execution_state": "busy",
                            }
                        },
                        "outputs": [
                            {
                                "data": {"text/plain": "True"},
                                "execution_count": 1,
                                "metadata": {},
                                "output_type": "execute_result",
                            }
                        ],
                        "source": "import pandas as pd\n"
                        'pd.get_option("display.html.table_schema")',
                    }
                ]
            }

            patch_json = response.json()
            # response should contain both the 'cell','kernel_message' wrappers
            assert "cell" in patch_json.keys()
            msg_id = response.json()["kernel_message"]["message_id"]
            assert len(msg_id) in msg_id_lengths

            exec_reply = await receive_json(
                websocket, msg_types=["cell_execution_reply"]
            )
            assert exec_reply["cell_execution_reply"]["cell_id"] == cell_uuid
            assert exec_reply["cell_execution_reply"]["parent_id"] == msg_id

            data = await receive_json(websocket, msg_types=["cell_update"])
            assert data == expected

    @pytest.mark.asyncio
    async def test_cell_stream_print(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "carriage_return_test.ipynb"
        )

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        import_cell_uuid = cells[0]["metadata"]["jupyter_d1"]["uuid"]
        time_loop_cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # Clear the web socket before we start
            await collect_websocket_messages(websocket, timeout=2)

            # execute import cell to prep for others
            response = await client.get(
                f"/notebooks/{uuid}/cells/{import_cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            # Wait for the import to complete by looking for
            # execution_state == 'idle' on the 'import' cell
            try:
                while True:
                    msg = await receive_json(websocket, timeout=15)
                    if "cell_update" in msg.keys():
                        d1_meta = msg["cell_update"][0]["metadata"][
                            "jupyter_d1"
                        ]
                        if (
                            d1_meta["execution_state"] == "idle"
                            and d1_meta["uuid"] == import_cell_uuid
                        ):

                            break
            except TimeoutError:
                pass

            # Clear the web socket before we start
            await collect_websocket_messages(websocket, timeout=2)

            # execute time loop cell to
            response = await client.get(
                f"/notebooks/{uuid}/cells/{time_loop_cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            msgs = await collect_websocket_messages(websocket, timeout=11)
            cell_update_msgs = filter_websocket_collection(msgs, "cell_update")

            data = cell_update_msgs.pop(0)
            assert len(data["cell_update"]) == 1
            cell_data = data["cell_update"][0]
            d1_metadata = cell_data["metadata"]["jupyter_d1"]
            assert d1_metadata["execution_state"] == "pending"
            assert d1_metadata["uuid"] == time_loop_cell_uuid
            assert cell_data["execution_count"] is None
            assert len(cell_data["outputs"]) == 0

            data = cell_update_msgs.pop(0)
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"]["uuid"]
                == time_loop_cell_uuid
            )
            assert data["cell_update"][0]["execution_count"] is None
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"][
                    "execution_state"
                ]
                == "busy"
            )
            assert data["cell_update"][0]["outputs"] == []

            data = cell_update_msgs.pop(0)
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"]["uuid"]
                == time_loop_cell_uuid
            )
            assert data["cell_update"][0]["execution_count"] is None
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"][
                    "execution_state"
                ]
                == "busy"
            )
            assert data["cell_update"][0]["outputs"] == [
                {
                    "name": "stdout",
                    "output_type": "stream",
                    "text": ["Start\n", "\n"],
                }
            ]

            for idx in [0, 1, 2, 3]:
                data = cell_update_msgs.pop(0)
                assert (
                    data["cell_update"][0]["metadata"]["jupyter_d1"]["uuid"]
                    == time_loop_cell_uuid
                )
                assert data["cell_update"][0]["execution_count"] is None
                assert (
                    data["cell_update"][0]["metadata"]["jupyter_d1"][
                        "execution_state"
                    ]
                    == "busy"
                )
                assert data["cell_update"][0]["outputs"] == [
                    {
                        "name": "stdout",
                        "output_type": "stream",
                        "text": ["Start\n", f"{idx}\n"],
                    }
                ]

            data = cell_update_msgs.pop(0)
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"]["uuid"]
                == time_loop_cell_uuid
            )
            assert data["cell_update"][0]["execution_count"] is None
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"][
                    "execution_state"
                ]
                == "busy"
            )
            assert data["cell_update"][0]["outputs"] == [
                {
                    "name": "stdout",
                    "output_type": "stream",
                    "text": ["Start\n", "Done\n", "\n"],
                }
            ]

            # last cell_update has execution_count == 2 and execution_state is 'idle'
            data = cell_update_msgs.pop(0)
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"]["uuid"]
                == time_loop_cell_uuid
            )
            assert data["cell_update"][0]["execution_count"] == 2
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"][
                    "execution_state"
                ]
                == "idle"
            )
            assert data["cell_update"][0]["outputs"] == [
                {
                    "name": "stdout",
                    "output_type": "stream",
                    "text": ["Start\n", "Done\n", "\n"],
                }
            ]

    @pytest.mark.asyncio
    async def test_cell_stream_tqdm(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "carriage_return_test.ipynb"
        )

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        import_cell_uuid = cells[0]["metadata"]["jupyter_d1"]["uuid"]
        tqdm_cell_uuid = cells[3]["metadata"]["jupyter_d1"]["uuid"]

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # Clear the web socket before we start
            await collect_websocket_messages(websocket, timeout=2)

            # execute import cell to prep for others
            response = await client.get(
                f"/notebooks/{uuid}/cells/{import_cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            # Wait for the import to complete by looking for
            # execution_state == 'idle' on the 'import' cell
            try:
                while True:
                    msg = await receive_json(websocket, timeout=15)
                    if "cell_update" in msg.keys():
                        d1_meta = msg["cell_update"][0]["metadata"][
                            "jupyter_d1"
                        ]
                        if (
                            d1_meta["execution_state"] == "idle"
                            and d1_meta["uuid"] == import_cell_uuid
                        ):

                            break
            except TimeoutError:
                pass

            # Clear the web socket before we start
            await collect_websocket_messages(websocket, timeout=2)

            # execute time loop cell to
            response = await client.get(
                f"/notebooks/{uuid}/cells/{tqdm_cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            msgs = await collect_websocket_messages(websocket, timeout=10)
            cell_update_msgs = filter_websocket_collection(msgs, "cell_update")

            data = cell_update_msgs.pop(0)
            assert len(data["cell_update"]) == 1
            cell_data = data["cell_update"][0]
            d1_metadata = cell_data["metadata"]["jupyter_d1"]
            assert d1_metadata["execution_state"] == "pending"
            assert d1_metadata["uuid"] == tqdm_cell_uuid
            assert cell_data["execution_count"] is None
            assert len(cell_data["outputs"]) == 0

            data = cell_update_msgs.pop(0)
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"]["uuid"]
                == tqdm_cell_uuid
            )
            assert data["cell_update"][0]["execution_count"] is None
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"][
                    "execution_state"
                ]
                == "busy"
            )
            assert data["cell_update"][0]["outputs"] == []

            # Updates for each of the 4 chunks, every 25%
            for idx in ["  0", " 25", " 50", " 75", "100"]:
                data = cell_update_msgs.pop(0)
                assert (
                    data["cell_update"][0]["metadata"]["jupyter_d1"]["uuid"]
                    == tqdm_cell_uuid
                )
                assert data["cell_update"][0]["execution_count"] is None
                assert (
                    data["cell_update"][0]["metadata"]["jupyter_d1"][
                        "execution_state"
                    ]
                    == "busy"
                )
                assert data["cell_update"][0]["outputs"][0]["name"] == "stderr"
                assert (
                    data["cell_update"][0]["outputs"][0]["output_type"]
                    == "stream"
                )
                # text = data['cell_update'][0]['outputs'][0]['text'][0]
                # print(">>> text:", text)
                # print(">>> type(text):", type(text))
                assert data["cell_update"][0]["outputs"][0]["text"][
                    0
                ].startswith(f"{idx}%|")
                assert data["cell_update"][0]["outputs"][0]["text"][
                    0
                ].endswith("it/s]\n")
                assert (
                    len(data["cell_update"][0]["outputs"][0]["text"][0]) == 101
                )

            # Then we get this twice. ¯\_(ツ)_/¯  Must be tqdm cleaning up.
            for dummy in range(2):
                data = cell_update_msgs.pop(0)
                assert (
                    data["cell_update"][0]["metadata"]["jupyter_d1"]["uuid"]
                    == tqdm_cell_uuid
                )
                assert data["cell_update"][0]["execution_count"] is None
                assert (
                    data["cell_update"][0]["metadata"]["jupyter_d1"][
                        "execution_state"
                    ]
                    == "busy"
                )
                assert data["cell_update"][0]["outputs"][0]["name"] == "stderr"
                assert (
                    data["cell_update"][0]["outputs"][0]["output_type"]
                    == "stream"
                )
                assert data["cell_update"][0]["outputs"][0]["text"][
                    0
                ].startswith(f"100%|")
                assert data["cell_update"][0]["outputs"][0]["text"][
                    0
                ].endswith("it/s]\n")
                assert (
                    len(data["cell_update"][0]["outputs"][0]["text"][0]) == 101
                )

            # Finally get execution_state == 'idle'
            data = cell_update_msgs.pop(0)
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"]["uuid"]
                == tqdm_cell_uuid
            )
            assert data["cell_update"][0]["execution_count"] == 2
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"][
                    "execution_state"
                ]
                == "idle"
            )
            assert data["cell_update"][0]["outputs"][0]["name"] == "stderr"
            assert (
                data["cell_update"][0]["outputs"][0]["output_type"] == "stream"
            )
            assert data["cell_update"][0]["outputs"][0]["text"][0].startswith(
                f"100%|"
            )
            assert data["cell_update"][0]["outputs"][0]["text"][0].endswith(
                "it/s]\n"
            )
            assert len(data["cell_update"][0]["outputs"][0]["text"][0]) == 101

    @pytest.mark.asyncio
    async def test_cell_stream_tqdm_nested(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Dont strip out ANSI codes (we used to handle \x1b[A which happens
        when tqdm loops are nested)
        """
        uuid = await upload_notebook(
            client, superuser_token_headers, "carriage_return_test.ipynb"
        )

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        nested_tqdm_cell_uuid = cells[4]["metadata"]["jupyter_d1"]["uuid"]

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # Clear the web socket before we start
            await collect_websocket_messages(websocket, timeout=2)

            # execute time loop cell to
            response = await client.get(
                f"/notebooks/{uuid}/cells/{nested_tqdm_cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            msgs = await collect_websocket_messages(websocket, timeout=10)
            cell_update_msgs = filter_websocket_collection(msgs, "cell_update")

            data = cell_update_msgs.pop(0)
            assert len(data["cell_update"]) == 1
            cell_data = data["cell_update"][0]
            d1_metadata = cell_data["metadata"]["jupyter_d1"]
            assert d1_metadata["execution_state"] == "pending"
            assert d1_metadata["uuid"] == nested_tqdm_cell_uuid
            assert cell_data["execution_count"] is None
            assert len(cell_data["outputs"]) == 0

            data = cell_update_msgs.pop(0)
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"]["uuid"]
                == nested_tqdm_cell_uuid
            )
            assert data["cell_update"][0]["execution_count"] is None
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"][
                    "execution_state"
                ]
                == "busy"
            )
            assert data["cell_update"][0]["outputs"] == []

            def check_cell_update(data, lines):
                """
                lines should be a list of tuples of percentage, numerator, and
                denominator for a line of tqdm output, OR just a string
                """
                assert (
                    data["cell_update"][0]["metadata"]["jupyter_d1"]["uuid"]
                    == nested_tqdm_cell_uuid
                )
                assert data["cell_update"][0]["execution_count"] is None
                assert (
                    data["cell_update"][0]["metadata"]["jupyter_d1"][
                        "execution_state"
                    ]
                    == "busy"
                )
                assert data["cell_update"][0]["outputs"][0]["name"] == "stderr"
                assert (
                    data["cell_update"][0]["outputs"][0]["output_type"]
                    == "stream"
                )

                assert len(
                    data["cell_update"][0]["outputs"][0]["text"]
                ) == len(lines)
                for idx, line in enumerate(lines):
                    text = data["cell_update"][0]["outputs"][0]["text"][idx]
                    print(text)
                    if isinstance(line, str):
                        assert text == line
                    else:
                        s = " " * (3 - len(str(line[0]))) + f"{line[0]}%|"
                        assert text.startswith(s)
                        assert f"| {line[1]}/{line[2]}" in text
                        ender = line[3] if len(line) > 3 else ""
                        assert text.endswith(f"it/s]{ender}\n")
                        assert len(text) == 101 + len(ender)

            outputs: List[Any] = [[0, 0, 7]]

            def check_inner_loop():
                outputs.append("\n")
                check_cell_update(cell_update_msgs.pop(0), outputs)
                outputs[-1] = [0, 0, 4]
                check_cell_update(cell_update_msgs.pop(0), outputs)
                outputs[-1].append("\x1b[A")
                check_cell_update(cell_update_msgs.pop(0), outputs)
                outputs.append("\n")
                check_cell_update(cell_update_msgs.pop(0), outputs)
                outputs[-1] = [25, 1, 4]
                check_cell_update(cell_update_msgs.pop(0), outputs)
                outputs[-1].append("\x1b[A")
                check_cell_update(cell_update_msgs.pop(0), outputs)
                outputs.append("\n")
                check_cell_update(cell_update_msgs.pop(0), outputs)
                outputs[-1] = [50, 2, 4]
                check_cell_update(cell_update_msgs.pop(0), outputs)
                outputs[-1].append("\x1b[A")
                check_cell_update(cell_update_msgs.pop(0), outputs)
                outputs.append("\n")
                check_cell_update(cell_update_msgs.pop(0), outputs)
                outputs[-1] = [75, 3, 4]
                check_cell_update(cell_update_msgs.pop(0), outputs)
                outputs[-1].append("\x1b[A")
                check_cell_update(cell_update_msgs.pop(0), outputs)
                outputs.append("\n")
                check_cell_update(cell_update_msgs.pop(0), outputs)
                outputs[-1] = [100, 4, 4]
                check_cell_update(cell_update_msgs.pop(0), outputs)
                outputs[-1].append("\x1b[A")
                check_cell_update(cell_update_msgs.pop(0), outputs)
                check_cell_update(cell_update_msgs.pop(0), outputs)

            check_cell_update(cell_update_msgs.pop(0), outputs)

            check_inner_loop()

            outputs.append("\n")
            check_cell_update(cell_update_msgs.pop(0), outputs)
            outputs[-1] = [14, 1, 7]
            check_cell_update(cell_update_msgs.pop(0), outputs)
            outputs[-1] = [29, 2, 7]
            check_cell_update(cell_update_msgs.pop(0), outputs)
            outputs[-1] = [43, 3, 7]
            check_cell_update(cell_update_msgs.pop(0), outputs)

            check_inner_loop()

            outputs.append("\n")
            check_cell_update(cell_update_msgs.pop(0), outputs)
            outputs[-1] = [57, 4, 7]
            check_cell_update(cell_update_msgs.pop(0), outputs)
            outputs[-1] = [71, 5, 7]
            check_cell_update(cell_update_msgs.pop(0), outputs)
            outputs[-1] = [86, 6, 7]
            check_cell_update(cell_update_msgs.pop(0), outputs)

            check_inner_loop()

            outputs.append("\n")
            check_cell_update(cell_update_msgs.pop(0), outputs)
            outputs[-1] = [100, 7, 7]
            check_cell_update(cell_update_msgs.pop(0), outputs)
            check_cell_update(cell_update_msgs.pop(0), outputs)
            outputs.append("\n")
            check_cell_update(cell_update_msgs.pop(0), outputs)

            # Finally get execution_state == 'idle'
            data = cell_update_msgs.pop(0)
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"]["uuid"]
                == nested_tqdm_cell_uuid
            )
            assert data["cell_update"][0]["execution_count"] == 1
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"][
                    "execution_state"
                ]
                == "idle"
            )
            assert data["cell_update"][0]["outputs"][0]["name"] == "stderr"
            assert (
                data["cell_update"][0]["outputs"][0]["output_type"] == "stream"
            )
            assert data["cell_update"][0]["outputs"][0]["text"][0].startswith(
                f"  0%|"
            )
            assert data["cell_update"][0]["outputs"][0]["text"][0].endswith(
                "it/s]\n"
            )
            assert len(data["cell_update"][0]["outputs"][0]["text"][0]) == 101

    @pytest.mark.asyncio
    async def test_cell_stream_ansi_code(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Test the ANSI codes, with some prints (dont strip them out or handle them)
        """
        uuid = await upload_notebook(
            client, superuser_token_headers, "carriage_return_test.ipynb"
        )

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        cell_uuid = cells[5]["metadata"]["jupyter_d1"]["uuid"]

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # Clear the web socket before we start
            await collect_websocket_messages(websocket, timeout=2)

            # execute time loop cell to
            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            msgs = await collect_websocket_messages(websocket, timeout=10)
            print(msgs)
            cell_update_msgs = filter_websocket_collection(msgs, "cell_update")

            data = cell_update_msgs.pop(0)
            assert len(data["cell_update"]) == 1
            cell_data = data["cell_update"][0]
            d1_metadata = cell_data["metadata"]["jupyter_d1"]
            assert d1_metadata["execution_state"] == "pending"
            assert d1_metadata["uuid"] == cell_uuid
            assert cell_data["execution_count"] is None
            assert len(cell_data["outputs"]) == 0

            data = cell_update_msgs.pop(0)
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"]["uuid"]
                == cell_uuid
            )
            assert data["cell_update"][0]["execution_count"] is None
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"][
                    "execution_state"
                ]
                == "busy"
            )
            assert data["cell_update"][0]["outputs"] == []

            def check_cell_update(data, lines):
                assert (
                    data["cell_update"][0]["metadata"]["jupyter_d1"]["uuid"]
                    == cell_uuid
                )
                assert data["cell_update"][0]["execution_count"] is None
                assert (
                    data["cell_update"][0]["metadata"]["jupyter_d1"][
                        "execution_state"
                    ]
                    == "busy"
                )
                assert data["cell_update"][0]["outputs"][0]["name"] == "stdout"
                assert (
                    data["cell_update"][0]["outputs"][0]["output_type"]
                    == "stream"
                )
                assert len(
                    data["cell_update"][0]["outputs"][0]["text"]
                ) == len(lines)

                for idx, line in enumerate(lines):
                    text = data["cell_update"][0]["outputs"][0]["text"][idx]
                    assert text == line

            check_cell_update(cell_update_msgs.pop(0), ["line1\n"])
            check_cell_update(cell_update_msgs.pop(0), ["thoe1\n", "\n"])
            check_cell_update(
                cell_update_msgs.pop(0), ["thoe1\n", "next\n", "\n"]
            )
            check_cell_update(
                cell_update_msgs.pop(0),
                ["thoe1\n", "next\n", "\x1b[38;5;34myoutweeed\n"],
            )
            check_cell_update(
                cell_update_msgs.pop(0),
                ["thoe1\n", "next\n", "\x1b[38;5;34myoutweeed\x1b[A\n"],
            )

            check_cell_update(
                cell_update_msgs.pop(0),
                [
                    "thoe1\n",
                    "next\n",
                    "\x1b[38;5;34myoutweeed\x1b[Aoil\n",
                    "\n",
                ],
            )

            # Finally get execution_state == 'idle'
            data = cell_update_msgs.pop(0)
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"]["uuid"]
                == cell_uuid
            )
            assert data["cell_update"][0]["execution_count"] == 1
            assert (
                data["cell_update"][0]["metadata"]["jupyter_d1"][
                    "execution_state"
                ]
                == "idle"
            )
            assert data["cell_update"][0]["outputs"][0]["name"] == "stdout"
            assert (
                data["cell_update"][0]["outputs"][0]["output_type"] == "stream"
            )
            assert data["cell_update"][0]["outputs"][0]["text"] == [
                "thoe1\n",
                "next\n",
                "\x1b[38;5;34myoutweeed\x1b[Aoil\n",
                "\n",
            ]

    @pytest.mark.asyncio
    async def test_run_all_cells(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        ututils: TestCase,
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        cell_uuid1 = cells[1]["metadata"]["jupyter_d1"]["uuid"]
        cell_uuid2 = cells[2]["metadata"]["jupyter_d1"]["uuid"]
        cell_uuid3 = cells[3]["metadata"]["jupyter_d1"]["uuid"]

        response = await client.get(
            f"/notebooks/{uuid}/cells/{cell_uuid2}/execute",
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        await asyncio.sleep(0.5)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        assert "outputs" not in cells[0]
        assert cells[1]["outputs"][0]["text"] == "Larry the Llama\n"
        assert cells[2]["outputs"][0]["data"]["text/plain"] == "7"

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # Clear the web socket before we start
            await collect_websocket_messages(websocket, timeout=2)

            response = await client.get(
                f"/notebooks/{uuid}/execute_all",
                headers=superuser_token_headers,
            )

            assert response.status_code == 200

            msgs = await collect_websocket_messages(websocket, timeout=10)
            cell_update_msgs = filter_websocket_collection(
                msgs, ["cell_update"]
            )

            for cell_uuid in (cell_uuid1, cell_uuid2, cell_uuid3):
                data = cell_update_msgs.pop(0)
                assert len(data["cell_update"]) == 1
                cell_data = data["cell_update"][0]
                d1_metadata = cell_data["metadata"]["jupyter_d1"]
                assert d1_metadata["execution_state"] == "pending"
                assert d1_metadata["uuid"] == cell_uuid
                assert cell_data["execution_count"] is None
                assert len(cell_data["outputs"]) == 0

            # Cell 1
            data = cell_update_msgs.pop(0)
            cell_update = data["cell_update"]
            ututils.assertCountEqual(
                cell_update,
                [
                    {
                        "cell_type": "code",
                        "execution_count": None,
                        "metadata": {
                            "jupyter_d1": {
                                "notebook_uuid": uuid,
                                "position": 1,
                                "uuid": cell_uuid1,
                                "execution_state": "busy",
                            }
                        },
                        "outputs": [],
                        "source": 'print("Larry the Llama")',
                    }
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_update = data["cell_update"]
            ututils.assertCountEqual(
                cell_update,
                [
                    {
                        "cell_type": "code",
                        "execution_count": None,
                        "metadata": {
                            "jupyter_d1": {
                                "notebook_uuid": uuid,
                                "position": 1,
                                "uuid": cell_uuid1,
                                "execution_state": "busy",
                            }
                        },
                        "outputs": [
                            {
                                "output_type": "stream",
                                "name": "stdout",
                                "text": ["Larry the Llama\n", "\n"],
                            }
                        ],
                        "source": 'print("Larry the Llama")',
                    }
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_update = data["cell_update"]
            ututils.assertCountEqual(
                cell_update,
                [
                    {
                        "cell_type": "code",
                        "execution_count": 2,
                        "metadata": {
                            "jupyter_d1": {
                                "notebook_uuid": uuid,
                                "position": 1,
                                "uuid": cell_uuid1,
                                "execution_state": "idle",
                            }
                        },
                        "outputs": [
                            {
                                "output_type": "stream",
                                "name": "stdout",
                                "text": ["Larry the Llama\n", "\n"],
                            }
                        ],
                        "source": 'print("Larry the Llama")',
                    }
                ],
            )

            # Cell 2
            data = cell_update_msgs.pop(0)
            cell_update = data["cell_update"]
            ututils.assertCountEqual(
                cell_update,
                [
                    {
                        "cell_type": "code",
                        "execution_count": None,
                        "metadata": {
                            "jupyter_d1": {
                                "notebook_uuid": uuid,
                                "position": 2,
                                "uuid": cell_uuid2,
                                "execution_state": "busy",
                            }
                        },
                        "outputs": [],
                        "source": "2+5",
                    }
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_update = data["cell_update"]
            ututils.assertCountEqual(
                cell_update,
                [
                    {
                        "cell_type": "code",
                        "execution_count": 3,
                        "metadata": {
                            "jupyter_d1": {
                                "notebook_uuid": uuid,
                                "position": 2,
                                "uuid": cell_uuid2,
                                "execution_state": "busy",
                            }
                        },
                        "outputs": [
                            {
                                "output_type": "execute_result",
                                "metadata": {},
                                "data": {"text/plain": "7"},
                                "execution_count": 3,
                            }
                        ],
                        "source": "2+5",
                    }
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_update = data["cell_update"]
            ututils.assertCountEqual(
                cell_update,
                [
                    {
                        "cell_type": "code",
                        "execution_count": 3,
                        "metadata": {
                            "jupyter_d1": {
                                "notebook_uuid": uuid,
                                "position": 2,
                                "uuid": cell_uuid2,
                                "execution_state": "idle",
                            }
                        },
                        "outputs": [
                            {
                                "output_type": "execute_result",
                                "metadata": {},
                                "data": {"text/plain": "7"},
                                "execution_count": 3,
                            }
                        ],
                        "source": "2+5",
                    }
                ],
            )

            # Cell 3
            data = cell_update_msgs.pop(0)
            cell_update = data["cell_update"]
            ututils.assertCountEqual(
                cell_update,
                [
                    {
                        "cell_type": "code",
                        "execution_count": None,
                        "metadata": {
                            "jupyter_d1": {
                                "notebook_uuid": uuid,
                                "position": 3,
                                "uuid": cell_uuid3,
                                "execution_state": "busy",
                            }
                        },
                        "outputs": [],
                        "source": "",
                    }
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_update = data["cell_update"]
            ututils.assertCountEqual(
                cell_update,
                [
                    {
                        "cell_type": "code",
                        "execution_count": 4,
                        "metadata": {
                            "jupyter_d1": {
                                "notebook_uuid": uuid,
                                "position": 3,
                                "uuid": cell_uuid3,
                                "execution_state": "idle",
                            }
                        },
                        "outputs": [],
                        "source": "",
                    }
                ],
            )

            assert len(cell_update_msgs) == 0

    @pytest.mark.asyncio
    async def test_run_cells_above(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        ututils: TestCase,
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        cell_uuid1 = cells[1]["metadata"]["jupyter_d1"]["uuid"]
        cell_uuid2 = cells[2]["metadata"]["jupyter_d1"]["uuid"]
        cells[3]["metadata"]["jupyter_d1"]["uuid"]

        response = await client.get(
            f"/notebooks/{uuid}/cells/{cell_uuid2}/execute",
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        await asyncio.sleep(0.5)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        assert "outputs" not in cells[0]
        assert cells[1]["outputs"][0]["text"] == "Larry the Llama\n"
        assert cells[2]["outputs"][0]["data"]["text/plain"] == "7"

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # Clear the web socket before we start
            await collect_websocket_messages(websocket, timeout=2)

            response = await client.get(
                f"/notebooks/{uuid}/execute_all",
                headers=superuser_token_headers,
                params={"above_position": 3},
            )

            assert response.status_code == 200

            msgs = await collect_websocket_messages(websocket, timeout=10)
            cell_update_msgs = filter_websocket_collection(
                msgs, ["cell_update"]
            )

            for cell_uuid in (cell_uuid1, cell_uuid2):
                data = cell_update_msgs.pop(0)
                assert len(data["cell_update"]) == 1
                cell_data = data["cell_update"][0]
                d1_metadata = cell_data["metadata"]["jupyter_d1"]
                assert d1_metadata["execution_state"] == "pending"
                assert d1_metadata["uuid"] == cell_uuid
                assert cell_data["execution_count"] is None
                assert len(cell_data["outputs"]) == 0

            # Cell 1
            data = cell_update_msgs.pop(0)
            cell_update = data["cell_update"]
            ututils.assertCountEqual(
                cell_update,
                [
                    {
                        "cell_type": "code",
                        "execution_count": None,
                        "metadata": {
                            "jupyter_d1": {
                                "notebook_uuid": uuid,
                                "position": 1,
                                "uuid": cell_uuid1,
                                "execution_state": "busy",
                            }
                        },
                        "outputs": [],
                        "source": 'print("Larry the Llama")',
                    }
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_update = data["cell_update"]
            ututils.assertCountEqual(
                cell_update,
                [
                    {
                        "cell_type": "code",
                        "execution_count": None,
                        "metadata": {
                            "jupyter_d1": {
                                "notebook_uuid": uuid,
                                "position": 1,
                                "uuid": cell_uuid1,
                                "execution_state": "busy",
                            }
                        },
                        "outputs": [
                            {
                                "output_type": "stream",
                                "name": "stdout",
                                "text": ["Larry the Llama\n", "\n"],
                            }
                        ],
                        "source": 'print("Larry the Llama")',
                    }
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_update = data["cell_update"]
            ututils.assertCountEqual(
                cell_update,
                [
                    {
                        "cell_type": "code",
                        "execution_count": 2,
                        "metadata": {
                            "jupyter_d1": {
                                "notebook_uuid": uuid,
                                "position": 1,
                                "uuid": cell_uuid1,
                                "execution_state": "idle",
                            }
                        },
                        "outputs": [
                            {
                                "output_type": "stream",
                                "name": "stdout",
                                "text": ["Larry the Llama\n", "\n"],
                            }
                        ],
                        "source": 'print("Larry the Llama")',
                    }
                ],
            )

            # Cell 2
            data = cell_update_msgs.pop(0)
            cell_update = data["cell_update"]
            ututils.assertCountEqual(
                cell_update,
                [
                    {
                        "cell_type": "code",
                        "execution_count": None,
                        "metadata": {
                            "jupyter_d1": {
                                "notebook_uuid": uuid,
                                "position": 2,
                                "uuid": cell_uuid2,
                                "execution_state": "busy",
                            }
                        },
                        "outputs": [],
                        "source": "2+5",
                    }
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_update = data["cell_update"]
            ututils.assertCountEqual(
                cell_update,
                [
                    {
                        "cell_type": "code",
                        "execution_count": 3,
                        "metadata": {
                            "jupyter_d1": {
                                "notebook_uuid": uuid,
                                "position": 2,
                                "uuid": cell_uuid2,
                                "execution_state": "busy",
                            }
                        },
                        "outputs": [
                            {
                                "output_type": "execute_result",
                                "metadata": {},
                                "data": {"text/plain": "7"},
                                "execution_count": 3,
                            }
                        ],
                        "source": "2+5",
                    }
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_update = data["cell_update"]
            ututils.assertCountEqual(
                cell_update,
                [
                    {
                        "cell_type": "code",
                        "execution_count": 3,
                        "metadata": {
                            "jupyter_d1": {
                                "notebook_uuid": uuid,
                                "position": 2,
                                "uuid": cell_uuid2,
                                "execution_state": "idle",
                            }
                        },
                        "outputs": [
                            {
                                "output_type": "execute_result",
                                "metadata": {},
                                "data": {"text/plain": "7"},
                                "execution_count": 3,
                            }
                        ],
                        "source": "2+5",
                    }
                ],
            )

            assert len(cell_update_msgs) == 0

    @pytest.mark.asyncio
    async def test_run_cells_below(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        ututils: TestCase,
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        cells[1]["metadata"]["jupyter_d1"]["uuid"]
        cell_uuid2 = cells[2]["metadata"]["jupyter_d1"]["uuid"]
        cell_uuid3 = cells[3]["metadata"]["jupyter_d1"]["uuid"]

        response = await client.get(
            f"/notebooks/{uuid}/cells/{cell_uuid2}/execute",
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        await asyncio.sleep(0.5)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        assert "outputs" not in cells[0]
        assert cells[1]["outputs"][0]["text"] == "Larry the Llama\n"
        assert cells[2]["outputs"][0]["data"]["text/plain"] == "7"

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # Clear the web socket before we start
            await collect_websocket_messages(websocket, timeout=2)

            response = await client.get(
                f"/notebooks/{uuid}/execute_all",
                headers=superuser_token_headers,
                params={"below_position": 1},
            )

            assert response.status_code == 200

            msgs = await collect_websocket_messages(websocket, timeout=10)
            cell_update_msgs = filter_websocket_collection(
                msgs, ["cell_update"]
            )

            for cell_uuid in (cell_uuid2, cell_uuid3):
                data = cell_update_msgs.pop(0)
                assert len(data["cell_update"]) == 1
                cell_data = data["cell_update"][0]
                d1_metadata = cell_data["metadata"]["jupyter_d1"]
                assert d1_metadata["execution_state"] == "pending"
                assert d1_metadata["uuid"] == cell_uuid
                assert cell_data["execution_count"] is None
                assert len(cell_data["outputs"]) == 0

            # Cell 2
            data = cell_update_msgs.pop(0)
            cell_update = data["cell_update"]
            ututils.assertCountEqual(
                cell_update,
                [
                    {
                        "cell_type": "code",
                        "execution_count": None,
                        "metadata": {
                            "jupyter_d1": {
                                "notebook_uuid": uuid,
                                "position": 2,
                                "uuid": cell_uuid2,
                                "execution_state": "busy",
                            }
                        },
                        "outputs": [],
                        "source": "2+5",
                    }
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_update = data["cell_update"]
            ututils.assertCountEqual(
                cell_update,
                [
                    {
                        "cell_type": "code",
                        "execution_count": 2,
                        "metadata": {
                            "jupyter_d1": {
                                "notebook_uuid": uuid,
                                "position": 2,
                                "uuid": cell_uuid2,
                                "execution_state": "busy",
                            }
                        },
                        "outputs": [
                            {
                                "output_type": "execute_result",
                                "metadata": {},
                                "data": {"text/plain": "7"},
                                "execution_count": 2,
                            }
                        ],
                        "source": "2+5",
                    }
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_update = data["cell_update"]
            ututils.assertCountEqual(
                cell_update,
                [
                    {
                        "cell_type": "code",
                        "execution_count": 2,
                        "metadata": {
                            "jupyter_d1": {
                                "notebook_uuid": uuid,
                                "position": 2,
                                "uuid": cell_uuid2,
                                "execution_state": "idle",
                            }
                        },
                        "outputs": [
                            {
                                "output_type": "execute_result",
                                "metadata": {},
                                "data": {"text/plain": "7"},
                                "execution_count": 2,
                            }
                        ],
                        "source": "2+5",
                    }
                ],
            )

            # Cell 3
            data = cell_update_msgs.pop(0)
            cell_update = data["cell_update"]
            ututils.assertCountEqual(
                cell_update,
                [
                    {
                        "cell_type": "code",
                        "execution_count": None,
                        "metadata": {
                            "jupyter_d1": {
                                "notebook_uuid": uuid,
                                "position": 3,
                                "uuid": cell_uuid3,
                                "execution_state": "busy",
                            }
                        },
                        "outputs": [],
                        "source": "",
                    }
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_update = data["cell_update"]
            ututils.assertCountEqual(
                cell_update,
                [
                    {
                        "cell_type": "code",
                        "execution_count": 3,
                        "metadata": {
                            "jupyter_d1": {
                                "notebook_uuid": uuid,
                                "position": 3,
                                "uuid": cell_uuid3,
                                "execution_state": "idle",
                            }
                        },
                        "outputs": [],
                        "source": "",
                    }
                ],
            )

            assert len(cell_update_msgs) == 0

    @pytest.mark.asyncio
    async def test_run_all_cells_exception_early(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        ututils: TestCase,
    ):
        """Run all cells but a cell fails, cells queued up after should update."""
        uuid = await upload_notebook(client, superuser_token_headers)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        cell_uuid1 = cells[1]["metadata"]["jupyter_d1"]["uuid"]
        cell_uuid2 = cells[2]["metadata"]["jupyter_d1"]["uuid"]
        cell_uuid3 = cells[3]["metadata"]["jupyter_d1"]["uuid"]

        params = {"source": "print(heeth)"}
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid1}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # Clear the web socket before we start
            await collect_websocket_messages(websocket, timeout=2)

            response = await client.get(
                f"/notebooks/{uuid}/execute_all",
                headers=superuser_token_headers,
            )

            assert response.status_code == 200

            msgs = await collect_websocket_messages(websocket, timeout=10)

            cell_update_msgs = filter_websocket_collection(
                msgs, ["cell_update"]
            )
            execute_reply_msgs = filter_websocket_collection(
                msgs, ["cell_execution_reply"]
            )

            for cell_uuid in (cell_uuid1, cell_uuid2, cell_uuid3):
                data = cell_update_msgs.pop(0)
                assert len(data["cell_update"]) == 1
                cell_data = data["cell_update"][0]
                d1_metadata = cell_data["metadata"]["jupyter_d1"]
                assert d1_metadata["execution_state"] == "pending"
                assert d1_metadata["uuid"] == cell_uuid
                assert cell_data["execution_count"] is None
                assert len(cell_data["outputs"]) == 0

            # Cell 1
            data = cell_update_msgs.pop(0)
            cell_update = data["cell_update"]
            ututils.assertCountEqual(
                cell_update,
                [
                    {
                        "cell_type": "code",
                        "execution_count": None,
                        "metadata": {
                            "jupyter_d1": {
                                "notebook_uuid": uuid,
                                "position": 1,
                                "uuid": cell_uuid1,
                                "execution_state": "busy",
                            }
                        },
                        "outputs": [],
                        "source": "print(heeth)",
                    }
                ],
            )

            cell: Any = {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {
                    "jupyter_d1": {
                        "notebook_uuid": uuid,
                        "position": 1,
                        "uuid": cell_uuid1,
                        "execution_state": "busy",
                    }
                },
                "outputs": [
                    {
                        "output_type": "error",
                        "ename": "NameError",
                        "evalue": "name 'heeth' is not defined",
                        "traceback": [
                            "\x1b[0;31m---------------------------------------"
                            "------------------------------------\x1b[0m",
                            "\x1b[0;31mNameError\x1b[0m                       "
                            "          Traceback (most recent call last)",
                            "Cell \x1b[0;32mIn[1], line 1\x1b[0m\n\x1b[0;32m--"
                            "--> 1\x1b[0m \x1b[38;5;28mprint\x1b[39m(\x1b[43mh"
                            "eeth\x1b[49m)\n",
                            "\x1b[0;31mNameError\x1b[0m: name 'heeth' is not defined",
                        ],
                    }
                ],
                "source": "print(heeth)",
            }

            data = cell_update_msgs.pop(0)
            cell_update = data["cell_update"]
            ututils.assertCountEqual(
                cell_update,
                [cell],
            )

            data = cell_update_msgs.pop(0)
            cell_update = data["cell_update"]
            cell["metadata"]["jupyter_d1"]["execution_state"] = "idle"
            cell["execution_count"] = 1
            ututils.assertCountEqual(
                cell_update,
                [cell],
            )

            data = execute_reply_msgs.pop(0)
            exec_reply = data["cell_execution_reply"]
            assert exec_reply["cell_id"] == cell_uuid1
            assert exec_reply["status"] == "error"
            assert exec_reply["execution_count"] == 1

            # Cell 2
            data = cell_update_msgs.pop(0)
            cell_update = data["cell_update"]
            ututils.assertCountEqual(
                cell_update,
                [
                    {
                        "cell_type": "code",
                        "execution_count": None,
                        "metadata": {
                            "jupyter_d1": {
                                "notebook_uuid": uuid,
                                "position": 2,
                                "uuid": cell_uuid2,
                                "execution_state": "busy",
                            }
                        },
                        "outputs": [],
                        "source": "2+5",
                    }
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_update = data["cell_update"]
            ututils.assertCountEqual(
                cell_update,
                [
                    {
                        "cell_type": "code",
                        "execution_count": None,
                        "metadata": {
                            "jupyter_d1": {
                                "notebook_uuid": uuid,
                                "position": 2,
                                "uuid": cell_uuid2,
                                "execution_state": "idle",
                            }
                        },
                        "outputs": [],
                        "source": "2+5",
                    }
                ],
            )

            data = execute_reply_msgs.pop(0)
            exec_reply = data["cell_execution_reply"]
            assert exec_reply["cell_id"] == cell_uuid2
            assert exec_reply["status"] == "aborted"
            assert exec_reply["execution_count"] is None

            # Cell 3
            data = cell_update_msgs.pop(0)
            cell_update = data["cell_update"]
            ututils.assertCountEqual(
                cell_update,
                [
                    {
                        "cell_type": "code",
                        "execution_count": None,
                        "metadata": {
                            "jupyter_d1": {
                                "notebook_uuid": uuid,
                                "position": 3,
                                "uuid": cell_uuid3,
                                "execution_state": "busy",
                            }
                        },
                        "outputs": [],
                        "source": "",
                    }
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_update = data["cell_update"]
            ututils.assertCountEqual(
                cell_update,
                [
                    {
                        "cell_type": "code",
                        "execution_count": None,
                        "metadata": {
                            "jupyter_d1": {
                                "notebook_uuid": uuid,
                                "position": 3,
                                "uuid": cell_uuid3,
                                "execution_state": "idle",
                            }
                        },
                        "outputs": [],
                        "source": "",
                    }
                ],
            )

            data = execute_reply_msgs.pop(0)
            exec_reply = data["cell_execution_reply"]
            assert exec_reply["cell_id"] == cell_uuid3
            assert exec_reply["status"] == "aborted"
            assert exec_reply["execution_count"] is None

            assert len(cell_update_msgs) == 0
            assert len(execute_reply_msgs) == 0

    @pytest.mark.asyncio
    async def test_import_error_handling(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        ututils: TestCase,
    ):
        """
        Import error due to a dependency not being installed should send
        import_error message on webhook
        """
        uuid = await upload_notebook(client, superuser_token_headers)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        params = {
            "source": "print('yo')\nfrom pandas.truf import anythie"
            "\nfrom requests import bigstuffo\nimport funkykong\nimport abdeefer"
        }
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            msgs = await collect_websocket_messages(websocket)
            pprint.pprint(msgs)

            import_error = filter_websocket_collection(msgs, ["import_error"])

            assert len(import_error) == 1
            assert import_error[0]["import_error"]["cell_id"] == cell_uuid
            assert import_error[0]["import_error"]["missing_dependencies"] == [
                "abdeefer",
                "funkykong",
            ]


@pytest.mark.usefixtures(
    "clear_notebooks", "clear_notebook_directory", "enable_cell_update_patches"
)
class TestCellUpdatePatches:
    """
    Test the cell patches feature, turned on by setting the
    CELL_UPDATE_PATCHES flag to true.

    Most of these test scenarios are the tests that fail in the
    TestNotebooksWebsocket class above when the CELL_UPDATE_PATCHES
    flag is True. When CELL_UPDATE_PATCHES is eventually default True,
    replace the corresponding tests in TestNotebookWebsocket with these tests
    """

    @pytest.mark.asyncio
    async def test_notebook_cell_execute(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        ututils: TestCase,
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        cell = cells[2]
        cell_uuid = cell["metadata"]["jupyter_d1"]["uuid"]

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            msg_id = response.json()["kernel_message"]["message_id"]

            data = await receive_json(
                websocket, msg_types=["cell_update_patch"]
            )
            assert data["cell_update_patch"]["cell_id"] == cell_uuid
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "pending",
                    },
                    {
                        "op": "remove",
                        "path": "/outputs/0",
                    },
                ],
            )

            # first two chunks received should be a execution count update and
            # cell_update_patch with an execution_state of 'busy' when processing
            # starts. Order is variable, so here we handle either order.
            def assert_json_content(data, execution_count=None):
                if "cell_update_patch" in data:
                    assert data["cell_update_patch"]["cell_id"] == cell_uuid
                    ututils.assertCountEqual(
                        data["cell_update_patch"]["patch"],
                        [
                            {
                                "op": "replace",
                                "path": "/metadata/jupyter_d1/execution_state",
                                "value": "busy",
                            },
                        ],
                    )
                    return None
                elif "cell_execution_reply" in data:
                    assert data["cell_execution_reply"]["execution_count"] == 1
                    assert data["cell_execution_reply"]["cell_id"] == cell_uuid
                    assert data["cell_execution_reply"]["parent_id"] == msg_id
                    return 1
                else:
                    raise AssertionError(f"unexpected cell type: {data}")

            data = await receive_json(
                websocket,
                msg_types=["cell_update_patch", "cell_execution_reply"],
            )
            exec_count = assert_json_content(data)
            data = await receive_json(
                websocket,
                msg_types=["cell_update_patch", "cell_execution_reply"],
            )
            assert_json_content(data, exec_count)

            # third chunk received should be a cell_update_patch with
            # the new output
            data = await receive_json(
                websocket, msg_types=["cell_update_patch"]
            )
            expected = {
                "cell_update_patch": {
                    "cell_id": cell_uuid,
                    "patch": [
                        {
                            "op": "add",
                            "path": "/outputs/0",
                            "value": {
                                "data": {"text/plain": "7"},
                                "execution_count": 1,
                                "metadata": {},
                                "output_type": "execute_result",
                            },
                        },
                        {
                            "op": "replace",
                            "path": "/execution_count",
                            "value": 1,
                        },
                    ],
                }
            }
            assert (
                data["cell_update_patch"]["cell_id"]
                == expected["cell_update_patch"]["cell_id"]
            )
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"],
                expected["cell_update_patch"]["patch"],
            )

            # third chunk received should be a cell_update with
            # an execution_state of 'idle' becuase it's all done
            data = await receive_json(
                websocket, msg_types=["cell_update_patch"]
            )
            assert "cell_update_patch" in data.keys()
            assert data["cell_update_patch"]["cell_id"] == cell_uuid
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "idle",
                    },
                ],
            )

            data = await receive_json(websocket, msg_types=["vars"])
            assert len(data["vars"]) == 14

    @pytest.mark.asyncio
    async def test_notebook_sequential_execute(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        ututils: TestCase,
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        cell_uuid1 = cells[1]["metadata"]["jupyter_d1"]["uuid"]
        cell_uuid2 = cells[2]["metadata"]["jupyter_d1"]["uuid"]
        cell_uuid3 = cells[3]["metadata"]["jupyter_d1"]["uuid"]

        code1 = """import time; time.sleep(1.1); print("checkpoint1")"""
        code2 = """import time; time.sleep(1.2); print("checkpoint2")"""
        code3 = """import time; time.sleep(1.3); print("checkpoint3")"""

        params1 = {"source": code1}
        params2 = {"source": code2}
        params3 = {"source": code3}

        resp1 = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid1}",
            json=params1,
            headers=superuser_token_headers,
        )
        assert resp1.status_code == 200

        resp2 = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid2}",
            json=params2,
            headers=superuser_token_headers,
        )
        assert resp2.status_code == 200

        resp3 = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid3}",
            json=params3,
            headers=superuser_token_headers,
        )
        assert resp3.status_code == 200

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            # await asyncio.sleep(WEBSOCKET_SLEEP_TIME)
            await asyncio.sleep(3.5)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid1}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid2}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid3}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            # Messages on the web socket can arrive in a slightly different
            # order from run to run.  The 'cell_update' messages arrive arround
            # the same time as some of the cell_execution messages.  It doesn't
            # really matter, but it makes testing tricky.  For a stable test,
            # gather all the responses and split them into two lists, one for
            # cell_update messages and one for all the others.

            # The most important thing for this test is that all the
            # "cell_execution_request" messages arrive first as the cells are
            # queued for execution and the "cell_execution_input",
            # "cell_execution_reply", etc messages show up later as the cells
            # are processed.

            cell_update_msgs = []
            non_cell_update_msgs = []
            for i in range(22):
                data = await receive_json(websocket)
                if (
                    "cell_update" in data.keys()
                    or "cell_update_patch" in data.keys()
                ):
                    cell_update_msgs.append(data)
                else:
                    non_cell_update_msgs.append(data)

            # should get three execution requests
            data = non_cell_update_msgs.pop(0)
            assert "cell_execution_request" in data.keys()
            msg_id1 = data["cell_execution_request"]["message_id"]
            assert len(msg_id1) in msg_id_lengths

            data = non_cell_update_msgs.pop(0)
            assert "cell_execution_request" in data.keys()
            msg_id2 = data["cell_execution_request"]["message_id"]
            assert len(msg_id2) in msg_id_lengths

            data = non_cell_update_msgs.pop(0)
            assert "cell_execution_request" in data.keys()
            msg_id3 = data["cell_execution_request"]["message_id"]
            assert len(msg_id3) in msg_id_lengths

            for cell_uuid in (cell_uuid1, cell_uuid2, cell_uuid3):
                data = cell_update_msgs.pop(0)
                assert data["cell_update_patch"]["cell_id"] == cell_uuid
                patches = [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "pending",
                    },
                ]
                if cell_uuid in (cell_uuid1, cell_uuid2):
                    patches.append(
                        {
                            "op": "remove",
                            "path": "/outputs/0",
                        }
                    )
                ututils.assertCountEqual(
                    data["cell_update_patch"]["patch"], patches
                )

            # cell update for the first executing cell
            data = cell_update_msgs.pop(0)
            assert "cell_update_patch" in data.keys()
            assert data["cell_update_patch"]["cell_id"] == cell_uuid1
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "busy",
                    },
                ],
            )

            # cell_execution_input for the first cell's code being executed
            data = non_cell_update_msgs.pop(0)
            assert "cell_execution_input" in data
            assert (
                data["cell_execution_input"]["content"]["code"] == code1
            ), f'Failed to find "{code1}" in  data: {data}'
            assert (
                data["cell_execution_input"]["parent_id"] == msg_id1
            ), f"Failed to find expected parent_id"

            # stream output now sends a cell_update_patch
            data = cell_update_msgs.pop(0)
            assert "cell_update_patch" in data.keys()
            assert data["cell_update_patch"]["cell_id"] == cell_uuid1
            assert data["cell_update_patch"]["patch"] == [
                {
                    "op": "add",
                    "path": "/outputs/0",
                    "value": {
                        "name": "stdout",
                        "output_type": "stream",
                        "text": ["checkpoint1\n", "\n"],
                    },
                }
            ]

            # execution_reply for the end of the first cell's execution
            data = non_cell_update_msgs.pop(0)
            assert "cell_execution_reply" in data.keys()
            assert data["cell_execution_reply"]["parent_id"] == msg_id1

            # cell update with the results of the first cell's execution
            data = cell_update_msgs.pop(0)
            assert "cell_update_patch" in data.keys()
            assert data["cell_update_patch"]["cell_id"] == cell_uuid1
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "idle",
                    },
                    {
                        "op": "replace",
                        "path": "/execution_count",
                        "value": 1,
                    },
                ],
            )

            # cell update for the begining of the second cell's execution
            data = cell_update_msgs.pop(0)
            assert "cell_update_patch" in data.keys()
            assert data["cell_update_patch"]["cell_id"] == cell_uuid2
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "busy",
                    },
                ],
            )

            # cell_input update with the second cell's code being executed
            data = non_cell_update_msgs.pop(0)
            assert "cell_execution_input" in data
            assert (
                data["cell_execution_input"]["content"]["code"] == code2
            ), f'Failed to find "{code2}" in cell_update data: {data}'
            assert (
                data["cell_execution_input"]["parent_id"] == msg_id2
            ), f"Failed to find expected parent_id"

            # stream output of the second cell's execution
            data = cell_update_msgs.pop(0)
            assert "cell_update_patch" in data.keys()
            assert data["cell_update_patch"]["cell_id"] == cell_uuid2
            assert data["cell_update_patch"]["patch"] == [
                {
                    "op": "add",
                    "path": "/outputs/0",
                    "value": {
                        "name": "stdout",
                        "output_type": "stream",
                        "text": ["checkpoint2\n", "\n"],
                    },
                }
            ]

            # exectuion_reply for the end of the second cell's execution
            data = non_cell_update_msgs.pop(0)
            assert "cell_execution_reply" in data.keys()
            assert data["cell_execution_reply"]["parent_id"] == msg_id2

            # cell_update with the results of the second cell
            data = cell_update_msgs.pop(0)
            assert "cell_update_patch" in data.keys()
            assert data["cell_update_patch"]["cell_id"] == cell_uuid2
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "idle",
                    },
                    {
                        "op": "replace",
                        "path": "/execution_count",
                        "value": 2,
                    },
                ],
            )

            # cell_update as the third cell begins execution
            data = cell_update_msgs.pop(0)
            assert "cell_update_patch" in data.keys()
            assert data["cell_update_patch"]["cell_id"] == cell_uuid3
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "busy",
                    },
                ],
            )

            # cell_execution_input with third cell code about to be executed
            data = non_cell_update_msgs.pop(0)
            assert "cell_execution_input" in data
            assert (
                data["cell_execution_input"]["content"]["code"] == code3
            ), f'Failed to find "{code3}" in cell_update data: {data}'
            assert (
                data["cell_execution_input"]["parent_id"] == msg_id3
            ), f"Failed to find expected parent_id"

            # stream output of the third cell
            data = cell_update_msgs.pop(0)
            assert "cell_update_patch" in data.keys()
            assert data["cell_update_patch"]["cell_id"] == cell_uuid3
            assert data["cell_update_patch"]["patch"] == [
                {
                    "op": "add",
                    "path": "/outputs/0",
                    "value": {
                        "name": "stdout",
                        "output_type": "stream",
                        "text": ["checkpoint3\n", "\n"],
                    },
                }
            ]

            # execution reply for finishing the third cell's execution
            data = non_cell_update_msgs.pop(0)
            assert "cell_execution_reply" in data.keys()
            assert data["cell_execution_reply"]["parent_id"] == msg_id3

            # cell_update for cell three with the output
            data = cell_update_msgs.pop(0)
            assert "cell_update_patch" in data.keys()
            assert data["cell_update_patch"]["cell_id"] == cell_uuid3
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "idle",
                    },
                    {
                        "op": "replace",
                        "path": "/execution_count",
                        "value": 3,
                    },
                ],
            )

            # var update
            data = non_cell_update_msgs.pop(0)
            assert "vars" in data.keys()

    @pytest.mark.asyncio
    async def test_cell_patch_and_execute(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        ututils: TestCase,
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == 'print("Larry the Llama")'

        cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        params = {"source": "7-9"}
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        response = await client.get(
            f"/notebooks/{uuid}/vars", headers=superuser_token_headers
        )
        assert response.status_code == 200
        assert len(response.json()["vars"]) == 0

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.patch(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                json=params,
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            data = await receive_json(
                websocket, msg_types=["cell_update_patch"]
            )
            assert data["cell_update_patch"]["cell_id"] == cell_uuid
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "pending",
                    },
                    {
                        "op": "remove",
                        "path": "/outputs/0",
                    },
                ],
            )

            expected = [
                {
                    "op": "replace",
                    "path": "/execution_count",
                    "value": 1,
                },
                {
                    "op": "add",
                    "path": "/outputs/0",
                    "value": {
                        "data": {"text/plain": "-2"},
                        "execution_count": 1,
                        "metadata": {},
                        "output_type": "execute_result",
                    },
                },
            ]

            patch_json = response.json()
            # response should contain a None 'cell', empty list 'patch', and
            # 'kernel_message' wrapper
            assert "cell" in patch_json.keys()
            assert patch_json["cell"] is None
            assert patch_json["patch"] == []
            msg_id = patch_json["kernel_message"]["message_id"]
            assert len(msg_id) in msg_id_lengths

            exec_reply = await receive_json(
                websocket, msg_types=["cell_execution_reply"]
            )
            assert exec_reply["cell_execution_reply"]["cell_id"] == cell_uuid
            assert exec_reply["cell_execution_reply"]["parent_id"] == msg_id

            data = await receive_json(
                websocket, msg_types=["cell_update_patch"]
            )
            assert data["cell_update_patch"]["cell_id"] == cell_uuid
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"], expected
            )

    @pytest.mark.asyncio
    async def test_cell_patch_and_execute_first_cell_imports_only(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        ututils: TestCase,
    ):
        """
        Test for CAL-1048, first cell doesnt show execution count if it only
        contains imports.
        """
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == 'print("Larry the Llama")'

        cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        params = {
            "source": "import matplotlib as mpl\nimport matplotlib.pyplot as plt"
            "\nimport numpy as np"
        }
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200
        patch_json = response.json()
        assert patch_json["cell"] is None
        assert patch_json["patch"] == [
            {
                "op": "replace",
                "path": "/source",
                "value": "import matplotlib as mpl\nimport matplotlib.pyplot as plt"
                "\nimport numpy as np",
            }
        ]

        response = await client.get(
            f"/notebooks/{uuid}/vars", headers=superuser_token_headers
        )
        assert response.status_code == 200
        assert len(response.json()["vars"]) == 0

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.patch(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                json=params,
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            patch_json = response.json()
            # response should contain None 'cell', empty list 'patch',
            # and 'kernel_message' wrappers
            assert "cell" in patch_json.keys()
            assert patch_json["cell"] is None
            assert patch_json["patch"] == []
            msg_id = patch_json["kernel_message"]["message_id"]
            assert len(msg_id) in msg_id_lengths

            data = await receive_json(
                websocket, msg_types=["cell_update_patch"]
            )
            assert data["cell_update_patch"]["cell_id"] == cell_uuid
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "pending",
                    },
                    {
                        "op": "remove",
                        "path": "/outputs/0",
                    },
                ],
            )

            expected = [
                # first cell_update comes from the cell execution starting
                {
                    "cell_update_patch": {
                        "cell_id": cell_uuid,
                        "patch": [
                            {
                                "op": "replace",
                                "path": "/metadata/jupyter_d1/execution_state",
                                "value": "busy",
                            }
                        ],
                    }
                },
                # second cell_update comes from the cell execution finishing
                {
                    "cell_update_patch": {
                        "cell_id": cell_uuid,
                        "patch": [
                            {
                                "op": "replace",
                                "path": "/metadata/jupyter_d1/execution_state",
                                "value": "idle",
                            },
                            {
                                "op": "replace",
                                "path": "/execution_count",
                                "value": 1,
                            },
                        ],
                    }
                },
            ]

            # Order of websocket messages can be a bit variable, we make sure the
            # order of cell_updates is what we expect, otherwise we just check that the
            # messages we expect came through at some point
            msgs = await collect_websocket_messages(websocket, limit=5)

            cell_updates = filter_websocket_collection(
                msgs, ["cell_update", "cell_update_patch"]
            )
            assert len(cell_updates) == 2
            assert cell_updates[0]["cell_update_patch"]["cell_id"] == cell_uuid
            ututils.assertCountEqual(
                cell_updates[0]["cell_update_patch"]["patch"],
                expected[0]["cell_update_patch"]["patch"],
            )
            assert cell_updates[1]["cell_update_patch"]["cell_id"] == cell_uuid
            ututils.assertCountEqual(
                cell_updates[1]["cell_update_patch"]["patch"],
                expected[1]["cell_update_patch"]["patch"],
            )

            exec_requests = filter_websocket_collection(
                msgs, "cell_execution_request"
            )
            assert len(exec_requests) == 1
            exec_request = exec_requests[0]
            assert (
                exec_request["cell_execution_request"]["cell_id"] == cell_uuid
            )
            assert (
                exec_request["cell_execution_request"]["message_id"] == msg_id
            )

            exec_inputs = filter_websocket_collection(
                msgs, "cell_execution_input"
            )
            assert len(exec_inputs) == 1
            exec_input = exec_inputs[0]
            assert exec_input["cell_execution_input"]["parent_id"] == msg_id
            assert (
                exec_input["cell_execution_input"]["content"]["code"]
                == params["source"]
            )
            assert (
                exec_input["cell_execution_input"]["content"][
                    "execution_count"
                ]
                == 1
            )

            exec_replies = filter_websocket_collection(
                msgs, "cell_execution_reply"
            )
            assert len(exec_replies) == 1
            exec_reply = exec_replies[0]
            assert exec_reply["cell_execution_reply"]["cell_id"] == cell_uuid
            assert exec_reply["cell_execution_reply"]["parent_id"] == msg_id
            assert exec_reply["cell_execution_reply"]["execution_count"] == 1

            # At the end we expect a vars update
            more_msgs = await collect_websocket_messages(websocket)
            assert len(more_msgs) == 1
            assert "vars" in more_msgs[0]

    @pytest.mark.asyncio
    async def test_notebook_cell_patch(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # get an existing cell
            response = await client.get(
                f"/notebooks/{uuid}/cells", headers=superuser_token_headers
            )
            assert response.status_code == 200
            cells = response.json()["cells"]
            assert cells[1]["source"] == 'print("Larry the Llama")'

            cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]
            params = {"source": "__Banana Rama!__"}
            response = await client.patch(
                f"/notebooks/{uuid}/cells/{cell_uuid}",
                json=params,
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            data = await receive_json(websocket)
            cell_patch = data["cell_update_patch"]
            assert cell_patch["cell_id"] == cell_uuid
            assert cell_patch["patch"] == [
                {
                    "op": "replace",
                    "path": "/source",
                    "value": "__Banana Rama!__",
                }
            ]

    @pytest.mark.asyncio
    async def test_notebook_cell_patch_cell_type(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        ututils: TestCase,
    ):
        """
        Patch cell type to code, make sure the resulting cell has outputs
        array since nbformat validation will fail without it
        """
        uuid = await upload_notebook(client, superuser_token_headers)

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # get an existing cell
            response = await client.get(
                f"/notebooks/{uuid}/cells", headers=superuser_token_headers
            )
            assert response.status_code == 200
            cells = response.json()["cells"]
            assert cells[0]["source"] == "## Simple Test Notebook"

            cell_uuid = cells[0]["metadata"]["jupyter_d1"]["uuid"]
            params = {"cell_type": "code"}
            response = await client.patch(
                f"/notebooks/{uuid}/cells/{cell_uuid}",
                json=params,
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            data = await receive_json(websocket)
            cell_patch = data["cell_update_patch"]
            assert cell_patch["cell_id"] == cell_uuid
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/cell_type",
                        "value": "code",
                    },
                    {
                        "op": "add",
                        "path": "/outputs",
                        "value": [],
                    },
                ],
            )

    @pytest.mark.asyncio
    async def test_idle_status(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        permissionless_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
        ututils: TestCase,
    ):
        async def is_idle_status():
            response = await client.get(
                f"/kernels/idle", headers=superuser_token_headers
            )
            assert response.status_code == 200
            json = response.json()
            return (
                json["idle"],
                datetime.strptime(json["last_idle"], "%Y-%m-%dT%H:%M:%S.%f"),
            )

        # Kernel is idle
        is_idle, last_idle_1 = await is_idle_status()
        assert is_idle is True

        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # Kernel is still idle
        is_idle, last_idle_2 = await is_idle_status()
        assert is_idle is True
        assert last_idle_1 == last_idle_2

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == 'print("Larry the Llama")'

        busy_cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]
        quick_cell_uuid = cells[2]["metadata"]["jupyter_d1"]["uuid"]

        params = {
            "source": "from time import sleep\nwhile True:\n    sleep(5)"
        }
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{busy_cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook",
            headers=superuser_token_headers,
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{quick_cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            data = await receive_json(websocket, msg_types=["vars"])
            assert "vars" in data

            # Need to wait for the UPDATE_WORKDIR_REQUEST to finish
            # (and we won't see it through the websocket)
            await asyncio.sleep(1)

            # Kernel is still idle (no code running)
            is_idle, last_idle_3 = await is_idle_status()
            assert is_idle is True
            assert last_idle_3 > last_idle_2

            response = await client.get(
                f"/notebooks/{uuid}/cells/{busy_cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            data = await receive_json(
                websocket, msg_types=["cell_update_patch"]
            )
            assert data["cell_update_patch"]["cell_id"] == busy_cell_uuid
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "pending",
                    },
                    {
                        "op": "remove",
                        "path": "/outputs/0",
                    },
                ],
            )

            # first chunk received should be a cell_update with
            # an execution_state of 'busy' when processing starts
            data = await wait_for_event(websocket, "cell_update_patch")
            assert data["cell_update_patch"]["cell_id"] == busy_cell_uuid
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "busy",
                    }
                ],
            )

            # Kernel should not be idle now
            is_idle, last_idle_4 = await is_idle_status()
            assert is_idle is False
            assert last_idle_4 == last_idle_3

    @pytest.mark.asyncio
    async def test_kernel_interrupt(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        ututils: TestCase,
    ):
        async def is_idle_status():
            response = await client.get(
                f"/kernels/idle", headers=superuser_token_headers
            )
            assert response.status_code == 200
            json = response.json()
            return (
                json["idle"],
                datetime.strptime(json["last_idle"], "%Y-%m-%dT%H:%M:%S.%f"),
            )

        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # Kernel is idle
        is_idle, last_idle_1 = await is_idle_status()
        assert is_idle is True

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == 'print("Larry the Llama")'

        busy_cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        params = {
            "source": "from time import sleep\nwhile True:\n    sleep(5)"
        }
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{busy_cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{busy_cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            msg_id = response.json()["kernel_message"]["message_id"]

            data = await receive_json(
                websocket, msg_types=["cell_update_patch"]
            )
            assert data["cell_update_patch"]["cell_id"] == busy_cell_uuid
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "pending",
                    },
                    {
                        "op": "remove",
                        "path": "/outputs/0",
                    },
                ],
            )

            # second chunk received should be a cell_update with
            # an execution_state of 'busy' when processing starts
            data = await wait_for_event(websocket, "cell_update_patch")
            cell_patch = data["cell_update_patch"]
            assert cell_patch["cell_id"] == busy_cell_uuid
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "busy",
                    },
                ],
            )

            # Kernel should not be idle now
            is_idle, last_idle_2 = await is_idle_status()
            assert is_idle is False
            assert last_idle_2 == last_idle_1

            response = await client.get(
                f"/notebooks/{uuid}/interrupt_kernel",
                headers=superuser_token_headers,
            )
            assert response.status_code == 204

            data = await wait_for_event(websocket, "kernel_interrupted")
            assert data["kernel_interrupted"]["interrupted"] is True

            # Receive cell error output
            data = await wait_for_event(websocket, "cell_update_patch")
            cell_patch = data["cell_update_patch"]
            assert cell_patch["cell_id"] == busy_cell_uuid
            assert len(cell_patch["patch"]) == 1
            assert cell_patch["patch"][0]["op"] == "add"
            assert cell_patch["patch"][0]["path"] == "/outputs/0"
            assert (
                cell_patch["patch"][0]["value"]["ename"] == "KeyboardInterrupt"
            )
            assert (
                "KeyboardInterrupt"
                in cell_patch["patch"][0]["value"]["traceback"][1]
            )

            def assert_json_content(data, execution_count=None):
                if "cell_update_patch" in data:
                    cell_patch = data["cell_update_patch"]
                    assert cell_patch["cell_id"] == busy_cell_uuid
                    ututils.assertCountEqual(
                        cell_patch["patch"],
                        [
                            {
                                "op": "replace",
                                "path": "/metadata/jupyter_d1/execution_state",
                                "value": "idle",
                            },
                            {
                                "op": "replace",
                                "path": "/execution_count",
                                "value": 1,
                            },
                        ],
                    )
                    return None
                elif "cell_execution_reply" in data:
                    assert data["cell_execution_reply"]["execution_count"] == 1
                    assert (
                        data["cell_execution_reply"]["cell_id"]
                        == busy_cell_uuid
                    )
                    assert (
                        len(data["cell_execution_reply"]["parent_id"])
                        in msg_id_lengths
                    )
                    assert data["cell_execution_reply"]["parent_id"] == msg_id
                    return 1
                else:
                    raise AssertionError(f"unexpected cell type: {data}")

            # Execution count update
            data = await wait_for_event(websocket, "cell_execution_reply")
            exec_count = assert_json_content(data)
            data = await wait_for_event(websocket, "cell_update_patch")
            assert_json_content(data, exec_count)

            await clear_websocket_queue(websocket)

            # Kernel should be idle now
            is_idle, last_idle_3 = await is_idle_status()
            assert is_idle is True
            assert last_idle_3 > last_idle_2

    @pytest.mark.asyncio
    async def test_bogus_code_error(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        permissionless_token_headers: Dict[str, str],
        superuser_token_headers: Dict[str, str],
        ututils: TestCase,
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        params = {"source": "this isnt code"}
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            msg_id = response.json()["kernel_message"]["message_id"]

            data = await receive_json(
                websocket, msg_types=["cell_update_patch"]
            )
            assert data["cell_update_patch"]["cell_id"] == cell_uuid
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "pending",
                    },
                    {
                        "op": "remove",
                        "path": "/outputs/0",
                    },
                ],
            )

            # execution_count update and busy status update,
            # in uncertain order
            def assert_json_content(data, execution_count=None):
                if "cell_update_patch" in data:
                    cell_patch = data["cell_update_patch"]
                    assert cell_patch["cell_id"] == cell_uuid
                    ututils.assertCountEqual(
                        cell_patch["patch"],
                        [
                            {
                                "op": "replace",
                                "path": "/metadata/jupyter_d1/execution_state",
                                "value": "busy",
                            }
                        ],
                    )
                    return None
                elif "cell_execution_reply" in data:
                    assert data["cell_execution_reply"]["execution_count"] == 1
                    assert data["cell_execution_reply"]["cell_id"] == cell_uuid
                    assert (
                        len(data["cell_execution_reply"]["parent_id"])
                        in msg_id_lengths
                    )
                    assert data["cell_execution_reply"]["parent_id"] == msg_id
                    return 1
                else:
                    raise AssertionError(f"unexpected cell type: {data}")

            msg_types = [
                "cell_update_patch",
                "cell_execution_reply",
            ]

            data = await receive_json(websocket, msg_types=msg_types)
            exec_count = assert_json_content(data)
            data = await receive_json(websocket, msg_types=msg_types)
            assert_json_content(data, exec_count)

            # Still busy with output, error output received
            data = await receive_json(
                websocket, msg_types=["cell_update_patch"]
            )
            cell_patch = data["cell_update_patch"]
            assert cell_patch["cell_id"] == cell_uuid
            assert len(cell_patch["patch"]) == 1
            assert cell_patch["patch"][0]["op"] == "add"
            assert cell_patch["patch"][0]["path"] == "/outputs/0"
            assert cell_patch["patch"][0]["value"]["ename"] == "SyntaxError"
            assert (
                "SyntaxError"
                in cell_patch["patch"][0]["value"]["traceback"][0]
            )

            data = await receive_json(
                websocket, msg_types=["cell_update_patch"]
            )
            cell_patch = data["cell_update_patch"]
            assert cell_patch["cell_id"] == cell_uuid
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "idle",
                    },
                    {"op": "replace", "path": "/execution_count", "value": 1},
                ],
            )

            # Kernel vars update
            data = await receive_json(websocket, msg_types=["vars"])
            assert "vars" in data

    @pytest.mark.asyncio
    async def test_restart_kernel_and_run_all_cells(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        ututils: TestCase,
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        cell = cells[2]
        cell_uuid = cell["metadata"]["jupyter_d1"]["uuid"]

        response = await client.get(
            f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        await asyncio.sleep(0.5)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        assert "outputs" not in cells[0]
        assert cells[1]["outputs"][0]["text"] == "Larry the Llama\n"
        assert cells[2]["outputs"][0]["data"]["text/plain"] == "7"

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # Clear the web socket before we start
            await collect_websocket_messages(websocket, timeout=2)

            response = await client.get(
                f"/notebooks/{uuid}/restart_kernel_and_execute_all",
                headers=superuser_token_headers,
            )

            assert response.status_code == 200

            msgs = await collect_websocket_messages(websocket, timeout=10)
            kernel_restarted_msgs = filter_websocket_collection(
                msgs, "kernel_restarted"
            )
            cell_update_msgs = filter_websocket_collection(
                msgs, ["cell_update", "cell_update_patch"]
            )

            data = kernel_restarted_msgs.pop(0)
            assert data["kernel_restarted"]["run_all_cells"] is True
            cells = data["kernel_restarted"]["cells"]
            cell_ids = []
            for cell in cells:
                cell_ids.append(cell["metadata"]["jupyter_d1"]["uuid"])
                assert (
                    "outputs" not in cell or len(cell["outputs"]) == 0
                ) and (
                    "execution_count" not in cell
                    or cell["execution_count"] is None
                )

            # These two pop up due to the restart
            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert cell_patch["cell_id"] == cell_uuid
            assert cell_patch["patch"] == [
                {
                    "op": "replace",
                    "path": "/metadata/jupyter_d1/execution_state",
                    "value": "busy",
                }
            ]
            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert cell_patch["cell_id"] == cell_uuid
            assert cell_patch["patch"] == [
                {
                    "op": "replace",
                    "path": "/metadata/jupyter_d1/execution_state",
                    "value": "idle",
                }
            ]

            data = cell_update_msgs.pop(0)
            assert data["cell_update_patch"]["cell_id"] == cell_ids[1]
            patches: Any = [
                {
                    "op": "replace",
                    "path": "/metadata/jupyter_d1/execution_state",
                    "value": "pending",
                },
                {
                    "op": "remove",
                    "path": "/outputs/0",
                },
            ]
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"], patches
            )

            data = cell_update_msgs.pop(0)
            assert data["cell_update_patch"]["cell_id"] == cell_ids[2]
            patches = [
                {
                    "op": "replace",
                    "path": "/metadata/jupyter_d1/execution_state",
                    "value": "pending",
                },
                {
                    "op": "remove",
                    "path": "/outputs/0",
                },
                {
                    "op": "replace",
                    "path": "/execution_count",
                    "value": None,
                },
            ]
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"], patches
            )

            data = cell_update_msgs.pop(0)
            assert data["cell_update_patch"]["cell_id"] == cell_ids[3]
            patches = [
                {
                    "op": "replace",
                    "path": "/metadata/jupyter_d1/execution_state",
                    "value": "pending",
                }
            ]
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"], patches
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert cell_patch["cell_id"] == cell_ids[1]
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "busy",
                    }
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert cell_patch["cell_id"] == cell_ids[1]
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "add",
                        "path": "/outputs/0",
                        "value": {
                            "name": "stdout",
                            "output_type": "stream",
                            "text": ["Larry the Llama\n", "\n"],
                        },
                    },
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert cell_patch["cell_id"] == cell_ids[1]
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "idle",
                    },
                    {"op": "replace", "path": "/execution_count", "value": 1},
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert cell_patch["cell_id"] == cell_ids[2]
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "busy",
                    }
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert cell_patch["cell_id"] == cell_ids[2]
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "add",
                        "path": "/outputs/0",
                        "value": {
                            "data": {"text/plain": "7"},
                            "execution_count": 2,
                            "metadata": {},
                            "output_type": "execute_result",
                        },
                    },
                    {"op": "replace", "path": "/execution_count", "value": 2},
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert cell_patch["cell_id"] == cell_ids[2]
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "idle",
                    },
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert cell_patch["cell_id"] == cell_ids[3]
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "busy",
                    }
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert cell_patch["cell_id"] == cell_ids[3]
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "idle",
                    },
                    {"op": "replace", "path": "/execution_count", "value": 3},
                ],
            )

            assert len(cell_update_msgs) == 0

    @pytest.mark.asyncio
    async def test_run_all_cells(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        ututils: TestCase,
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        cell_ids = [c["metadata"]["jupyter_d1"]["uuid"] for c in cells]

        cell = cells[2]
        cell_uuid = cell["metadata"]["jupyter_d1"]["uuid"]

        response = await client.get(
            f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        await asyncio.sleep(0.5)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        assert "outputs" not in cells[0]
        assert cells[1]["outputs"][0]["text"] == "Larry the Llama\n"
        assert cells[2]["outputs"][0]["data"]["text/plain"] == "7"

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # Clear the web socket before we start
            await collect_websocket_messages(websocket, timeout=2)

            response = await client.get(
                f"/notebooks/{uuid}/execute_all",
                headers=superuser_token_headers,
            )

            assert response.status_code == 200

            msgs = await collect_websocket_messages(websocket, timeout=10)
            cell_update_msgs = filter_websocket_collection(
                msgs, ["cell_update", "cell_update_patch"]
            )

            data = cell_update_msgs.pop(0)
            assert data["cell_update_patch"]["cell_id"] == cell_ids[1]
            patches: Any = [
                {
                    "op": "replace",
                    "path": "/metadata/jupyter_d1/execution_state",
                    "value": "pending",
                },
                {
                    "op": "remove",
                    "path": "/outputs/0",
                },
            ]
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"], patches
            )

            data = cell_update_msgs.pop(0)
            assert data["cell_update_patch"]["cell_id"] == cell_ids[2]
            patches = [
                {
                    "op": "replace",
                    "path": "/metadata/jupyter_d1/execution_state",
                    "value": "pending",
                },
                {
                    "op": "remove",
                    "path": "/outputs/0",
                },
                {
                    "op": "replace",
                    "path": "/execution_count",
                    "value": None,
                },
            ]
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"], patches
            )

            data = cell_update_msgs.pop(0)
            assert data["cell_update_patch"]["cell_id"] == cell_ids[3]
            patches = [
                {
                    "op": "replace",
                    "path": "/metadata/jupyter_d1/execution_state",
                    "value": "pending",
                }
            ]
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"], patches
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert (
                cell_patch["cell_id"]
                == cells[1]["metadata"]["jupyter_d1"]["uuid"]
            )
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "busy",
                    },
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert (
                cell_patch["cell_id"]
                == cells[1]["metadata"]["jupyter_d1"]["uuid"]
            )
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "add",
                        "path": "/outputs/0",
                        "value": {
                            "output_type": "stream",
                            "name": "stdout",
                            "text": ["Larry the Llama\n", "\n"],
                        },
                    }
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert (
                cell_patch["cell_id"]
                == cells[1]["metadata"]["jupyter_d1"]["uuid"]
            )
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {"op": "replace", "path": "/execution_count", "value": 2},
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "idle",
                    },
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert (
                cell_patch["cell_id"]
                == cells[2]["metadata"]["jupyter_d1"]["uuid"]
            )
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "busy",
                    },
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert (
                cell_patch["cell_id"]
                == cells[2]["metadata"]["jupyter_d1"]["uuid"]
            )
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {"op": "replace", "path": "/execution_count", "value": 3},
                    {
                        "op": "add",
                        "path": "/outputs/0",
                        "value": {
                            "output_type": "execute_result",
                            "metadata": {},
                            "data": {"text/plain": "7"},
                            "execution_count": 3,
                        },
                    },
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert (
                cell_patch["cell_id"]
                == cells[2]["metadata"]["jupyter_d1"]["uuid"]
            )
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "idle",
                    }
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert (
                cell_patch["cell_id"]
                == cells[3]["metadata"]["jupyter_d1"]["uuid"]
            )
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "busy",
                    }
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert (
                cell_patch["cell_id"]
                == cells[3]["metadata"]["jupyter_d1"]["uuid"]
            )
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {"op": "replace", "path": "/execution_count", "value": 4},
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "idle",
                    },
                ],
            )

            assert len(cell_update_msgs) == 0

    @pytest.mark.asyncio
    async def test_run_cells_above(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        ututils: TestCase,
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        cell_ids = [c["metadata"]["jupyter_d1"]["uuid"] for c in cells]

        cell = cells[2]
        cell_uuid = cell["metadata"]["jupyter_d1"]["uuid"]

        response = await client.get(
            f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        await asyncio.sleep(0.5)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        assert "outputs" not in cells[0]
        assert cells[1]["outputs"][0]["text"] == "Larry the Llama\n"
        assert cells[2]["outputs"][0]["data"]["text/plain"] == "7"

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # Clear the web socket before we start
            await collect_websocket_messages(websocket, timeout=2)

            response = await client.get(
                f"/notebooks/{uuid}/execute_all",
                headers=superuser_token_headers,
                params={"above_position": 3},
            )

            assert response.status_code == 200

            msgs = await collect_websocket_messages(websocket, timeout=10)
            cell_update_msgs = filter_websocket_collection(
                msgs, ["cell_update", "cell_update_patch"]
            )

            data = cell_update_msgs.pop(0)
            assert data["cell_update_patch"]["cell_id"] == cell_ids[1]
            patches: Any = [
                {
                    "op": "replace",
                    "path": "/metadata/jupyter_d1/execution_state",
                    "value": "pending",
                },
                {
                    "op": "remove",
                    "path": "/outputs/0",
                },
            ]
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"], patches
            )

            data = cell_update_msgs.pop(0)
            assert data["cell_update_patch"]["cell_id"] == cell_ids[2]
            patches = [
                {
                    "op": "replace",
                    "path": "/metadata/jupyter_d1/execution_state",
                    "value": "pending",
                },
                {
                    "op": "remove",
                    "path": "/outputs/0",
                },
                {
                    "op": "replace",
                    "path": "/execution_count",
                    "value": None,
                },
            ]
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"], patches
            )

            data = cell_update_msgs.pop(0)
            assert data["cell_update_patch"]["cell_id"] == cell_ids[1]
            patches = [
                {
                    "op": "replace",
                    "path": "/metadata/jupyter_d1/execution_state",
                    "value": "busy",
                },
            ]
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"], patches
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert (
                cell_patch["cell_id"]
                == cells[1]["metadata"]["jupyter_d1"]["uuid"]
            )
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "add",
                        "path": "/outputs/0",
                        "value": {
                            "output_type": "stream",
                            "name": "stdout",
                            "text": ["Larry the Llama\n", "\n"],
                        },
                    }
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert (
                cell_patch["cell_id"]
                == cells[1]["metadata"]["jupyter_d1"]["uuid"]
            )
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {"op": "replace", "path": "/execution_count", "value": 2},
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "idle",
                    },
                ],
            )

            data = cell_update_msgs.pop(0)
            assert data["cell_update_patch"]["cell_id"] == cell_ids[2]
            patches = [
                {
                    "op": "replace",
                    "path": "/metadata/jupyter_d1/execution_state",
                    "value": "busy",
                },
            ]
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"], patches
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert (
                cell_patch["cell_id"]
                == cells[2]["metadata"]["jupyter_d1"]["uuid"]
            )
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {"op": "replace", "path": "/execution_count", "value": 3},
                    {
                        "op": "add",
                        "path": "/outputs/0",
                        "value": {
                            "output_type": "execute_result",
                            "metadata": {},
                            "data": {"text/plain": "7"},
                            "execution_count": 3,
                        },
                    },
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert (
                cell_patch["cell_id"]
                == cells[2]["metadata"]["jupyter_d1"]["uuid"]
            )
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "idle",
                    }
                ],
            )

            assert len(cell_update_msgs) == 0

    @pytest.mark.asyncio
    async def test_run_cells_below(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        ututils: TestCase,
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        cell_ids = [c["metadata"]["jupyter_d1"]["uuid"] for c in cells]

        cell = cells[2]
        cell_uuid = cell["metadata"]["jupyter_d1"]["uuid"]

        response = await client.get(
            f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        await asyncio.sleep(0.5)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        assert "outputs" not in cells[0]
        assert cells[1]["outputs"][0]["text"] == "Larry the Llama\n"
        assert cells[2]["outputs"][0]["data"]["text/plain"] == "7"

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # Clear the web socket before we start
            await collect_websocket_messages(websocket, timeout=2)

            response = await client.get(
                f"/notebooks/{uuid}/execute_all",
                headers=superuser_token_headers,
                params={"below_position": 1},
            )

            assert response.status_code == 200

            msgs = await collect_websocket_messages(websocket, timeout=10)
            cell_update_msgs = filter_websocket_collection(
                msgs, ["cell_update", "cell_update_patch"]
            )

            data = cell_update_msgs.pop(0)
            assert data["cell_update_patch"]["cell_id"] == cell_ids[2]
            patches = [
                {
                    "op": "replace",
                    "path": "/metadata/jupyter_d1/execution_state",
                    "value": "pending",
                },
                {
                    "op": "remove",
                    "path": "/outputs/0",
                },
                {
                    "op": "replace",
                    "path": "/execution_count",
                    "value": None,
                },
            ]
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"], patches
            )

            data = cell_update_msgs.pop(0)
            assert data["cell_update_patch"]["cell_id"] == cell_ids[3]
            patches = [
                {
                    "op": "replace",
                    "path": "/metadata/jupyter_d1/execution_state",
                    "value": "pending",
                }
            ]
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"], patches
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert (
                cell_patch["cell_id"]
                == cells[2]["metadata"]["jupyter_d1"]["uuid"]
            )
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "busy",
                    }
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert (
                cell_patch["cell_id"]
                == cells[2]["metadata"]["jupyter_d1"]["uuid"]
            )
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {"op": "replace", "path": "/execution_count", "value": 2},
                    {
                        "op": "add",
                        "path": "/outputs/0",
                        "value": {
                            "output_type": "execute_result",
                            "metadata": {},
                            "data": {"text/plain": "7"},
                            "execution_count": 2,
                        },
                    },
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert (
                cell_patch["cell_id"]
                == cells[2]["metadata"]["jupyter_d1"]["uuid"]
            )
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "idle",
                    }
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert (
                cell_patch["cell_id"]
                == cells[3]["metadata"]["jupyter_d1"]["uuid"]
            )
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "busy",
                    }
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert (
                cell_patch["cell_id"]
                == cells[3]["metadata"]["jupyter_d1"]["uuid"]
            )
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {"op": "replace", "path": "/execution_count", "value": 3},
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "idle",
                    },
                ],
            )

            assert len(cell_update_msgs) == 0

    @pytest.mark.asyncio
    async def test_run_all_cells_exception_early(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        ututils: TestCase,
    ):
        """Run all cells but a cell fails, cells queued up after should update."""
        uuid = await upload_notebook(client, superuser_token_headers)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        cell_ids = [c["metadata"]["jupyter_d1"]["uuid"] for c in cells]

        params = {"source": "print(heeth)"}
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_ids[1]}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # Clear the web socket before we start
            await collect_websocket_messages(websocket, timeout=2)

            response = await client.get(
                f"/notebooks/{uuid}/execute_all",
                headers=superuser_token_headers,
            )

            assert response.status_code == 200

            msgs = await collect_websocket_messages(websocket, timeout=10)

            cell_update_msgs = filter_websocket_collection(
                msgs, ["cell_update", "cell_update_patch"]
            )
            execute_reply_msgs = filter_websocket_collection(
                msgs, ["cell_execution_reply"]
            )

            data = cell_update_msgs.pop(0)
            assert data["cell_update_patch"]["cell_id"] == cell_ids[1]
            patches = [
                {
                    "op": "replace",
                    "path": "/metadata/jupyter_d1/execution_state",
                    "value": "pending",
                },
                {
                    "op": "remove",
                    "path": "/outputs/0",
                },
            ]
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"], patches
            )

            data = cell_update_msgs.pop(0)
            assert data["cell_update_patch"]["cell_id"] == cell_ids[2]
            patches = [
                {
                    "op": "replace",
                    "path": "/metadata/jupyter_d1/execution_state",
                    "value": "pending",
                },
                {
                    "op": "remove",
                    "path": "/outputs/0",
                },
            ]
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"], patches
            )

            data = cell_update_msgs.pop(0)
            assert data["cell_update_patch"]["cell_id"] == cell_ids[3]
            patches = [
                {
                    "op": "replace",
                    "path": "/metadata/jupyter_d1/execution_state",
                    "value": "pending",
                }
            ]
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"], patches
            )

            # Cell 1
            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert (
                cell_patch["cell_id"]
                == cells[1]["metadata"]["jupyter_d1"]["uuid"]
            )
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "busy",
                    }
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert cell_patch["cell_id"] == cell_ids[1]
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "add",
                        "path": "/outputs/0",
                        "value": {
                            "output_type": "error",
                            "ename": "NameError",
                            "evalue": "name 'heeth' is not defined",
                            "traceback": [
                                "\x1b[0;31m-----------------------------------"
                                "----------------------------------------\x1b[0m",
                                "\x1b[0;31mNameError\x1b[0m                   "
                                "              Traceback (most recent call last)",
                                "Cell \x1b[0;32mIn[1], line 1\x1b[0m\n\x1b[0;32m"
                                "----> 1\x1b[0m \x1b[38;5;28mprint\x1b[39m(\x1b["
                                "43mheeth\x1b[49m)\n",
                                "\x1b[0;31mNameError\x1b[0m: name 'heeth' is not"
                                " defined",
                            ],
                        },
                    },
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert cell_patch["cell_id"] == cell_ids[1]
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {"op": "replace", "path": "/execution_count", "value": 1},
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "idle",
                    },
                ],
            )

            data = execute_reply_msgs.pop(0)
            exec_reply = data["cell_execution_reply"]
            assert exec_reply["cell_id"] == cell_ids[1]
            assert exec_reply["status"] == "error"
            assert exec_reply["execution_count"] == 1

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert cell_patch["cell_id"] == cell_ids[2]
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "busy",
                    },
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert cell_patch["cell_id"] == cell_ids[2]
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "idle",
                    },
                ],
            )

            data = execute_reply_msgs.pop(0)
            exec_reply = data["cell_execution_reply"]
            assert exec_reply["cell_id"] == cell_ids[2]
            assert exec_reply["status"] == "aborted"
            assert exec_reply["execution_count"] is None

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert cell_patch["cell_id"] == cell_ids[3]
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "busy",
                    },
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert cell_patch["cell_id"] == cell_ids[3]
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "idle",
                    },
                ],
            )

            data = execute_reply_msgs.pop(0)
            exec_reply = data["cell_execution_reply"]
            assert exec_reply["cell_id"] == cell_ids[3]
            assert exec_reply["status"] == "aborted"
            assert exec_reply["execution_count"] is None

            assert len(cell_update_msgs) == 0
            assert len(execute_reply_msgs) == 0

    @pytest.mark.asyncio
    async def test_ipython_kernel_startup_script(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        ututils: TestCase,
    ):
        """
        Test that the callisto_startup.py startup script is run when the
        kernel starts.
        """
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == 'print("Larry the Llama")'

        cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        params = {
            "source": "import pandas as pd\n"
            'pd.get_option("display.html.table_schema")'
        }
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        response = await client.get(
            f"/notebooks/{uuid}/vars", headers=superuser_token_headers
        )
        assert response.status_code == 200
        assert len(response.json()["vars"]) == 0

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.patch(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                json=params,
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            msgs = await collect_websocket_messages(websocket, timeout=3)

            patch_json = response.json()
            # response should contain both 'cell', 'patch, and 'kernel_message' wrappers
            assert patch_json["cell"] is None
            assert patch_json["patch"] == []
            msg_id = response.json()["kernel_message"]["message_id"]
            assert len(msg_id) in msg_id_lengths

            cell_exec_replies = filter_websocket_collection(
                msgs, "cell_execution_reply"
            )

            assert len(cell_exec_replies) == 1
            exec_reply = cell_exec_replies[0]
            assert exec_reply["cell_execution_reply"]["cell_id"] == cell_uuid
            assert exec_reply["cell_execution_reply"]["parent_id"] == msg_id

            cell_update_patches = filter_websocket_collection(
                msgs, "cell_update_patch"
            )

            assert len(cell_update_patches) == 4

            data = cell_update_patches.pop(0)
            assert data["cell_update_patch"]["cell_id"] == cell_uuid
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "pending",
                    },
                    {"op": "remove", "path": "/outputs/0"},
                ],
            )

            data = cell_update_patches.pop(0)
            assert data["cell_update_patch"]["cell_id"] == cell_uuid
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "busy",
                    },
                ],
            )
            data = cell_update_patches.pop(0)
            assert data["cell_update_patch"]["cell_id"] == cell_uuid
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"],
                [
                    {
                        "op": "add",
                        "path": "/outputs/0",
                        "value": {
                            "data": {"text/plain": "True"},
                            "execution_count": 1,
                            "metadata": {},
                            "output_type": "execute_result",
                        },
                    },
                    {
                        "op": "replace",
                        "path": "/execution_count",
                        "value": 1,
                    },
                ],
            )
            data = cell_update_patches.pop(0)
            assert data["cell_update_patch"]["cell_id"] == cell_uuid
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "idle",
                    },
                ],
            )

    @pytest.mark.asyncio
    async def test_cell_stream_print(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        ututils: TestCase,
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "carriage_return_test.ipynb"
        )

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        import_cell_uuid = cells[0]["metadata"]["jupyter_d1"]["uuid"]
        time_loop_cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # Clear the web socket before we start
            await collect_websocket_messages(websocket, timeout=2)

            # execute import cell to prep for others
            response = await client.get(
                f"/notebooks/{uuid}/cells/{import_cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            # Wait for the import to complete by looking for
            # execution_state == 'idle' on the 'import' cell
            try:
                while True:
                    msg = await receive_json(websocket, timeout=15)
                    if "cell_update_patch" in msg.keys():
                        patches = list(
                            filter(
                                lambda x: (
                                    x["path"]
                                    == "/metadata/jupyter_d1/execution_state"
                                    and "value" in x
                                    and x["value"] == "idle"
                                ),
                                msg["cell_update_patch"]["patch"],
                            )
                        )
                        if (
                            len(patches) > 0
                            and msg["cell_update_patch"]["cell_id"]
                            == import_cell_uuid
                        ):

                            break
            except TimeoutError:
                pass

            # Clear the web socket before we start
            await collect_websocket_messages(websocket, timeout=2)

            # execute time loop cell to
            response = await client.get(
                f"/notebooks/{uuid}/cells/{time_loop_cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            msgs = await collect_websocket_messages(websocket, timeout=10)
            cell_update_msgs = filter_websocket_collection(
                msgs, ["cell_update", "cell_update_patch"]
            )

            data = cell_update_msgs.pop(0)
            assert data["cell_update_patch"]["cell_id"] == time_loop_cell_uuid
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "pending",
                    },
                    {"op": "remove", "path": "/outputs/0"},
                ],
            )

            data = cell_update_msgs.pop(0)
            assert data["cell_update_patch"]["cell_id"] == time_loop_cell_uuid
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "busy",
                    },
                ],
            )

            data = cell_update_msgs.pop(0)
            assert data["cell_update_patch"]["cell_id"] == time_loop_cell_uuid
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"],
                [
                    {
                        "op": "add",
                        "path": "/outputs/0",
                        "value": {
                            "name": "stdout",
                            "output_type": "stream",
                            "text": ["Start\n", "\n"],
                        },
                    },
                ],
            )

            for idx in [0, 1, 2, 3]:
                data = cell_update_msgs.pop(0)
                assert (
                    data["cell_update_patch"]["cell_id"] == time_loop_cell_uuid
                )
                ututils.assertCountEqual(
                    data["cell_update_patch"]["patch"],
                    [
                        {
                            "op": "replace",
                            "path": "/outputs/0/text/1",
                            "value": f"{idx}\n",
                        },
                    ],
                )

            data = cell_update_msgs.pop(0)
            assert data["cell_update_patch"]["cell_id"] == time_loop_cell_uuid
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/outputs/0/text/1",
                        "value": "Done\n",
                    },
                    {"op": "add", "path": "/outputs/0/text/2", "value": "\n"},
                ],
            )

            # last cell_update_patch has execution_count == 2 and
            # execution_state is 'idle'
            data = cell_update_msgs.pop(0)
            assert data["cell_update_patch"]["cell_id"] == time_loop_cell_uuid
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "idle",
                    },
                    {"op": "replace", "path": "/execution_count", "value": 2},
                ],
            )

            assert len(cell_update_msgs) == 0

    @pytest.mark.asyncio
    async def test_cell_stream_tqdm(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        ututils: TestCase,
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "carriage_return_test.ipynb"
        )

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        import_cell_uuid = cells[0]["metadata"]["jupyter_d1"]["uuid"]
        tqdm_cell_uuid = cells[3]["metadata"]["jupyter_d1"]["uuid"]

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # Clear the web socket before we start
            await collect_websocket_messages(websocket, timeout=2)

            # execute import cell to prep for others
            response = await client.get(
                f"/notebooks/{uuid}/cells/{import_cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            # Wait for the import to complete by looking for
            # execution_state == 'idle' on the 'import' cell
            try:
                while True:
                    msg = await receive_json(websocket, timeout=15)
                    if "cell_update_patch" in msg.keys():
                        patches = list(
                            filter(
                                lambda x: (
                                    x["path"]
                                    == "/metadata/jupyter_d1/execution_state"
                                    and "value" in x
                                    and x["value"] == "idle"
                                ),
                                msg["cell_update_patch"]["patch"],
                            )
                        )
                        if (
                            len(patches) > 0
                            and msg["cell_update_patch"]["cell_id"]
                            == import_cell_uuid
                        ):

                            break
            except TimeoutError:
                pass

            # Clear the web socket before we start
            await collect_websocket_messages(websocket, timeout=2)

            # execute time loop cell to
            response = await client.get(
                f"/notebooks/{uuid}/cells/{tqdm_cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            msgs = await collect_websocket_messages(websocket, timeout=10)
            print(msgs)
            cell_update_msgs = filter_websocket_collection(
                msgs, ["cell_update", "cell_update_patch"]
            )

            data = cell_update_msgs.pop(0)
            assert data["cell_update_patch"]["cell_id"] == tqdm_cell_uuid
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "pending",
                    },
                    {"op": "remove", "path": "/outputs/0"},
                ],
            )

            data = cell_update_msgs.pop(0)
            assert data["cell_update_patch"]["cell_id"] == tqdm_cell_uuid
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "busy",
                    },
                ],
            )

            # Updates for each of the 4 chunks, every 25%
            for idx in ["  0", " 25", " 50", " 75", "100", "100"]:
                data = cell_update_msgs.pop(0)
                assert data["cell_update_patch"]["cell_id"] == tqdm_cell_uuid
                assert len(data["cell_update_patch"]["patch"]) == 1
                patch = data["cell_update_patch"]["patch"][0]
                if idx == "  0":
                    assert patch["op"] == "add"
                    assert patch["path"] == "/outputs/0"
                    assert patch["value"]["name"] == "stderr"
                    assert patch["value"]["output_type"] == "stream"
                    patch_text = patch["value"]["text"][0]
                else:
                    assert patch["op"] == "replace"
                    assert patch["path"] == "/outputs/0/text/0"
                    patch_text = patch["value"]
                assert patch_text.startswith(f"{idx}%|")
                assert patch_text.endswith("it/s]\n")
                assert len(patch_text) == 101

            data = cell_update_msgs.pop(0)
            assert data["cell_update_patch"]["cell_id"] == tqdm_cell_uuid
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"],
                [
                    {"op": "add", "path": "/outputs/0/text/1", "value": "\n"},
                ],
            )

            # Finally get execution_state == 'idle'
            data = cell_update_msgs.pop(0)
            assert data["cell_update_patch"]["cell_id"] == tqdm_cell_uuid
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "idle",
                    },
                    {"op": "replace", "path": "/execution_count", "value": 2},
                ],
            )

            assert len(cell_update_msgs) == 0

    @pytest.mark.asyncio
    async def test_websocket_invalid_command_error(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Test sending an invalid command over websocket,
        should receive an error message over the websocket
        """
        response = await client.post(
            "/notebooks/create",
            query_string={"kspec_name": "python", "filename": "heyp"},
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()["notebook"]
        uuid = resp_json["metadata"]["jupyter_d1"]["uuid"]

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            await websocket.send_json(
                {
                    "command": "nothing",
                    "command_id": "32543-rrep-443",
                    "body": {
                        "code": "5 + prin + 6",
                        "cursor_position": 7,
                    },
                }
            )

            data = await receive_json(websocket)
            assert (
                data["error"]["message"]
                == "Command 'nothing' is not supported"
            )
            assert data["error"]["command_id"] == "32543-rrep-443"

    @pytest.mark.asyncio
    async def test_websocket_invalid_command_payload_error(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Test sending an invalid command payload over websocket,
        should receive an error message over the websocket
        """
        response = await client.post(
            "/notebooks/create",
            query_string={"kspec_name": "python", "filename": "heyp"},
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()["notebook"]
        uuid = resp_json["metadata"]["jupyter_d1"]["uuid"]

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            await websocket.send_json(
                {
                    "command": "complete",
                    "command_id": "32543-rrep-443",
                    "body": {
                        "cursor_position": 7,
                    },
                }
            )

            data = await receive_json(websocket)
            assert (
                data["error"]["message"]
                == "Error processing incoming command, invalid body"
            )
            assert data["error"]["detail"] == [
                {
                    "loc": ["code"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
            assert data["error"]["command_id"] == "32543-rrep-443"

    @pytest.mark.asyncio
    async def test_clear_single_cell(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        ututils: TestCase,
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        response = await client.get(
            f"/notebooks/{uuid}/execute_all",
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells", headers=superuser_token_headers
            )
            assert response.status_code == 200
            cells = response.json()["cells"]

            assert cells[1]["execution_count"] == 1
            assert cells[1]["outputs"][0]["text"] == [
                "Larry the Llama\n",
                "\n",
            ]
            assert cells[2]["execution_count"] == 2
            assert cells[2]["outputs"][0]["data"]["text/plain"] == "7"

            # Clear the web socket before we start
            await collect_websocket_messages(websocket, timeout=2)

            # Clear cell 1
            cell_id = cells[1]["metadata"]["jupyter_d1"]["uuid"]
            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_id}/clear",
                headers=superuser_token_headers,
            )
            assert response.status_code == 204

            msgs = await collect_websocket_messages(websocket, timeout=10)
            cell_update_msgs = filter_websocket_collection(
                msgs, ["cell_update", "cell_update_patch"]
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert (
                cell_patch["cell_id"]
                == cells[1]["metadata"]["jupyter_d1"]["uuid"]
            )
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/execution_count",
                        "value": None,
                    },
                    {"op": "remove", "path": "/outputs/0"},
                ],
            )

            assert len(cell_update_msgs) == 0

            # Cell 2 still has output
            response = await client.get(
                f"/notebooks/{uuid}/cells", headers=superuser_token_headers
            )
            assert response.status_code == 200
            cells = response.json()["cells"]
            assert cells[1]["execution_count"] is None
            assert cells[1]["outputs"] == []
            assert cells[2]["execution_count"] == 2
            assert cells[2]["outputs"][0]["data"]["text/plain"] == "7"

            # Clear cell 2
            cell_id = cells[2]["metadata"]["jupyter_d1"]["uuid"]
            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_id}/clear",
                headers=superuser_token_headers,
            )
            assert response.status_code == 204

            msgs = await collect_websocket_messages(websocket, timeout=10)
            cell_update_msgs = filter_websocket_collection(
                msgs, ["cell_update", "cell_update_patch"]
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert (
                cell_patch["cell_id"]
                == cells[2]["metadata"]["jupyter_d1"]["uuid"]
            )
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/execution_count",
                        "value": None,
                    },
                    {"op": "remove", "path": "/outputs/0"},
                ],
            )

            assert len(cell_update_msgs) == 0

            # Both cells are empty now
            response = await client.get(
                f"/notebooks/{uuid}/cells", headers=superuser_token_headers
            )
            assert response.status_code == 200
            cells = response.json()["cells"]
            assert cells[1]["execution_count"] is None
            assert cells[1]["outputs"] == []
            assert cells[2]["execution_count"] is None
            assert cells[2]["outputs"] == []

    @pytest.mark.asyncio
    async def test_clear_all_cells(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        ututils: TestCase,
    ):
        uuid = await upload_notebook(client, superuser_token_headers)

        response = await client.get(
            f"/notebooks/{uuid}/execute_all",
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # Clear the web socket before we start
            await collect_websocket_messages(websocket, timeout=2)

            response = await client.get(
                f"/notebooks/{uuid}/cells", headers=superuser_token_headers
            )
            assert response.status_code == 200
            cells = response.json()["cells"]

            # Cells have output and execution counts
            assert cells[1]["execution_count"] == 1
            assert cells[1]["outputs"][0]["text"] == [
                "Larry the Llama\n",
                "\n",
            ]
            assert cells[2]["execution_count"] == 2
            assert cells[2]["outputs"][0]["data"]["text/plain"] == "7"
            assert cells[3]["execution_count"] == 3
            assert cells[3]["outputs"] == []

            # Clear all
            cells[1]["metadata"]["jupyter_d1"]["uuid"]
            response = await client.get(
                f"/notebooks/{uuid}/clear_all",
                headers=superuser_token_headers,
            )
            assert response.status_code == 204

            msgs = await collect_websocket_messages(websocket, timeout=10)
            cell_update_msgs = filter_websocket_collection(
                msgs, ["cell_update", "cell_update_patch"]
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert (
                cell_patch["cell_id"]
                == cells[1]["metadata"]["jupyter_d1"]["uuid"]
            )
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/execution_count",
                        "value": None,
                    },
                    {"op": "remove", "path": "/outputs/0"},
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert (
                cell_patch["cell_id"]
                == cells[2]["metadata"]["jupyter_d1"]["uuid"]
            )
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/execution_count",
                        "value": None,
                    },
                    {"op": "remove", "path": "/outputs/0"},
                ],
            )

            data = cell_update_msgs.pop(0)
            cell_patch = data["cell_update_patch"]
            assert (
                cell_patch["cell_id"]
                == cells[3]["metadata"]["jupyter_d1"]["uuid"]
            )
            ututils.assertCountEqual(
                cell_patch["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/execution_count",
                        "value": None,
                    },
                ],
            )

            assert len(cell_update_msgs) == 0

            # Both cells are empty now
            response = await client.get(
                f"/notebooks/{uuid}/cells", headers=superuser_token_headers
            )
            assert response.status_code == 200
            cells = response.json()["cells"]
            assert cells[1]["execution_count"] is None
            assert cells[1]["outputs"] == []
            assert cells[2]["execution_count"] is None
            assert cells[2]["outputs"] == []
            assert cells[3]["execution_count"] is None
            assert cells[3]["outputs"] == []


@pytest.mark.usefixtures("clear_notebooks", "clear_notebook_directory")
class TestKernelVarsManager:
    @pytest.mark.asyncio
    async def test_get_single_var_detail(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Large dataframe is abbreviated in summary, not in variable
        details request.
        """
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == 'print("Larry the Llama")'

        cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        params = {
            "source": "import pandas as pd\ndf3 = "
            "pd.DataFrame([{str(i): i + j for i in range(5)} for j in "
            "range(150)])"
        }
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        response = await client.get(
            f"/notebooks/{uuid}/vars", headers=superuser_token_headers
        )
        assert response.status_code == 200
        assert len(response.json()["vars"]) == 0

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            # Kernel vars update
            data = await receive_json(websocket, msg_types=["vars"])
            vars = {
                var["name"]: {
                    "type": var["type"],
                    "value": var["value"],
                    "summary": var["summary"],
                    "abbreviated": var["abbreviated"],
                    "has_next_page": var["has_next_page"],
                }
                for var in data["vars"]
            }

            assert vars["df3"]["type"] == "DataFrame"
            assert vars["df3"]["value"] == {
                "multi_value": {
                    "row_count": 150,
                    "column_count": 5,
                    "column_names": None,
                    "data": None,
                    "row_names": None,
                    "column_types": None,
                }
            }
            assert vars["df3"]["summary"] == "Size: 150x5"
            assert vars["df3"]["abbreviated"] is False
            assert vars["df3"]["has_next_page"] is False

            response = await client.get(
                f"/notebooks/{uuid}/vars", headers=superuser_token_headers
            )
            assert response.status_code == 200
            current_vars = response.json()["vars"]
            current_vars = filter(
                lambda x: x["name"] != "___d1os", current_vars
            )
            assert list(current_vars) == data["vars"]

            response = await client.get(
                f"/notebooks/{uuid}/vars/df3", headers=superuser_token_headers
            )
            assert response.status_code == 200
            single_var = response.json()["single_var"]
            assert single_var["name"] == "df3"
            assert single_var["type"] == "DataFrame"
            assert single_var["value"]["multi_value"]["column_count"] == 5
            assert single_var["value"]["multi_value"]["row_count"] == 150
            assert single_var["value"]["multi_value"]["column_names"] == [
                str(i) for i in range(5)
            ]
            assert single_var["value"]["multi_value"]["column_types"] == [
                "integer",
                "integer",
                "integer",
                "integer",
                "integer",
            ]
            assert single_var["value"]["multi_value"]["data"] == [
                [str(i + j) for i in range(5)]
                for j in range(settings.VAR_DEFAULT_PAGE_SIZE)
            ]
            assert single_var["summary"] == "Size: 150x5"
            assert single_var["abbreviated"] is True
            assert single_var["has_next_page"] is True

            # Shouldn't have changed anything in the current vars
            response = await client.get(
                f"/notebooks/{uuid}/vars", headers=superuser_token_headers
            )
            assert response.status_code == 200
            current_vars = response.json()["vars"]
            current_vars = filter(
                lambda x: x["name"] != "___d1os", current_vars
            )
            assert list(current_vars) == data["vars"]

            # Var that doesn't exist
            response = await client.get(
                f"/notebooks/{uuid}/vars/df2", headers=superuser_token_headers
            )
            assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_single_var_detail_pagination(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Large dataframe is abbreviated in summary, not in variable
        details request.
        """
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == 'print("Larry the Llama")'

        cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        params = {
            "source": "import pandas as pd\ndf3 = "
            "pd.DataFrame([{str(i): i + j for i in range(5)} for j in "
            "range(150)])"
        }
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        response = await client.get(
            f"/notebooks/{uuid}/vars", headers=superuser_token_headers
        )
        assert response.status_code == 200
        assert len(response.json()["vars"]) == 0

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            # Kernel vars update
            data = await receive_json(websocket, msg_types=["vars"])
            vars = {
                var["name"]: {
                    "type": var["type"],
                    "value": var["value"],
                    "summary": var["summary"],
                    "abbreviated": var["abbreviated"],
                    "has_next_page": var["has_next_page"],
                }
                for var in data["vars"]
            }

            assert vars["df3"]["type"] == "DataFrame"
            assert vars["df3"]["value"] == {
                "multi_value": {
                    "row_count": 150,
                    "column_count": 5,
                    "column_names": None,
                    "data": None,
                    "row_names": None,
                    "column_types": None,
                }
            }
            assert vars["df3"]["summary"] == "Size: 150x5"
            assert vars["df3"]["abbreviated"] is False

            # First page
            response = await client.get(
                f"/notebooks/{uuid}/vars/df3",
                query_string={"page_size": 11, "page": 0},
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            single_var = response.json()["single_var"]
            assert single_var["name"] == "df3"
            assert single_var["type"] == "DataFrame"
            assert single_var["value"]["multi_value"]["column_count"] == 5
            assert single_var["value"]["multi_value"]["row_count"] == 150
            assert single_var["value"]["multi_value"]["column_names"] == [
                str(i) for i in range(5)
            ]
            assert single_var["value"]["multi_value"]["column_types"] == [
                "integer",
                "integer",
                "integer",
                "integer",
                "integer",
            ]
            assert single_var["value"]["multi_value"]["data"] == [
                [str(i + j) for i in range(5)] for j in range(11)
            ]
            assert single_var["summary"] == "Size: 150x5"
            assert single_var["abbreviated"] is True
            assert single_var["has_next_page"] is True

            # Second page
            response = await client.get(
                f"/notebooks/{uuid}/vars/df3",
                query_string={"page_size": 11, "page": 1},
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            single_var = response.json()["single_var"]
            assert single_var["name"] == "df3"
            assert single_var["type"] == "DataFrame"
            assert single_var["value"]["multi_value"]["column_count"] == 5
            assert single_var["value"]["multi_value"]["row_count"] == 150
            assert single_var["value"]["multi_value"]["column_names"] == [
                str(i) for i in range(5)
            ]
            assert single_var["value"]["multi_value"]["column_types"] == [
                "integer",
                "integer",
                "integer",
                "integer",
                "integer",
            ]
            assert single_var["value"]["multi_value"]["data"] == [
                [str(i + j) for i in range(5)] for j in range(11, 22)
            ]
            assert single_var["summary"] == "Size: 150x5"
            assert single_var["abbreviated"] is True
            assert single_var["has_next_page"] is True

            # Final page
            response = await client.get(
                f"/notebooks/{uuid}/vars/df3",
                query_string={"page_size": 11, "page": 13},
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            single_var = response.json()["single_var"]
            assert single_var["name"] == "df3"
            assert single_var["type"] == "DataFrame"
            assert single_var["value"]["multi_value"]["column_count"] == 5
            assert single_var["value"]["multi_value"]["row_count"] == 150
            assert single_var["value"]["multi_value"]["column_names"] == [
                str(i) for i in range(5)
            ]
            assert single_var["value"]["multi_value"]["column_types"] == [
                "integer",
                "integer",
                "integer",
                "integer",
                "integer",
            ]
            assert single_var["value"]["multi_value"]["data"] == [
                [str(i + j) for i in range(5)] for j in range(143, 150)
            ]
            assert single_var["summary"] == "Size: 150x5"
            assert single_var["abbreviated"] is False
            assert single_var["has_next_page"] is False

            # Out of range
            response = await client.get(
                f"/notebooks/{uuid}/vars/df3",
                query_string={"page_size": 11, "page": 14},
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            single_var = response.json()["single_var"]
            assert single_var["name"] == "df3"
            assert single_var["type"] == "DataFrame"
            assert single_var["value"]["multi_value"]["column_count"] == 5
            assert single_var["value"]["multi_value"]["row_count"] == 150
            assert single_var["value"]["multi_value"]["column_names"] == [
                str(i) for i in range(5)
            ]
            assert single_var["value"]["multi_value"]["column_types"] == [
                "integer",
                "integer",
                "integer",
                "integer",
                "integer",
            ]
            assert single_var["value"]["multi_value"]["data"] == []
            assert single_var["summary"] == "Size: 150x5"
            assert single_var["abbreviated"] is False
            assert single_var["has_next_page"] is False

            # Shouldn't have changed anything in the current vars
            response = await client.get(
                f"/notebooks/{uuid}/vars", headers=superuser_token_headers
            )
            assert response.status_code == 200
            current_vars = response.json()["vars"]
            current_vars = filter(
                lambda x: x["name"] != "___d1os", current_vars
            )
            assert list(current_vars) == data["vars"]

            # Var that doesn't exist
            response = await client.get(
                f"/notebooks/{uuid}/vars/df2", headers=superuser_token_headers
            )
            assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_single_var_detail_sorting(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Able to sort columns in dataframe
        """
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == 'print("Larry the Llama")'

        cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        params = {
            "source": "import pandas as pd\ndf3 = "
            "pd.DataFrame(data={'col1': [3, 2, 1, 4, 5, 6], "
            "'col2': [5, 5, 5, 2, 2, 2], "
            "'col3': ['a', 'a', 'b', 'd', 'c', 'a']})"
        }
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        response = await client.get(
            f"/notebooks/{uuid}/vars", headers=superuser_token_headers
        )
        assert response.status_code == 200
        assert len(response.json()["vars"]) == 0

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            # Kernel vars update
            data = await receive_json(websocket, msg_types=["vars"])

            # Sort by a single column
            response = await client.post(
                f"/notebooks/{uuid}/vars/df3",
                json={"page_size": 10, "page": 0, "sort_by": ["col1"]},
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            single_var = response.json()["single_var"]
            assert single_var["name"] == "df3"
            assert single_var["type"] == "DataFrame"
            assert single_var["value"]["multi_value"]["column_count"] == 3
            assert single_var["value"]["multi_value"]["row_count"] == 6
            assert single_var["value"]["multi_value"]["column_names"] == [
                "col1",
                "col2",
                "col3",
            ]
            assert single_var["value"]["multi_value"]["column_types"] == [
                "integer",
                "integer",
                "string",
            ]
            assert single_var["value"]["multi_value"]["data"] == [
                ["1", "5", "b"],
                ["2", "5", "a"],
                ["3", "5", "a"],
                ["4", "2", "d"],
                ["5", "2", "c"],
                ["6", "2", "a"],
            ]
            assert single_var["summary"] == "Size: 6x3"
            assert single_var["abbreviated"] is False
            assert single_var["has_next_page"] is False

            # Sort by multiple columns
            response = await client.post(
                f"/notebooks/{uuid}/vars/df3",
                json={
                    "page_size": 10,
                    "page": 0,
                    "sort_by": ["col2", "col3"],
                    "ascending": [False, True],
                },
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            single_var = response.json()["single_var"]
            assert single_var["name"] == "df3"
            assert single_var["type"] == "DataFrame"
            assert single_var["value"]["multi_value"]["column_count"] == 3
            assert single_var["value"]["multi_value"]["row_count"] == 6
            assert single_var["value"]["multi_value"]["column_names"] == [
                "col1",
                "col2",
                "col3",
            ]
            assert single_var["value"]["multi_value"]["column_types"] == [
                "integer",
                "integer",
                "string",
            ]
            assert single_var["value"]["multi_value"]["data"] == [
                ["3", "5", "a"],
                ["2", "5", "a"],
                ["1", "5", "b"],
                ["6", "2", "a"],
                ["5", "2", "c"],
                ["4", "2", "d"],
            ]
            assert single_var["summary"] == "Size: 6x3"
            assert single_var["abbreviated"] is False
            assert single_var["has_next_page"] is False

            # Filter
            response = await client.post(
                f"/notebooks/{uuid}/vars/df3",
                json={
                    "page_size": 10,
                    "page": 0,
                    "sort_by": ["col3", "col1"],
                    "ascending": [True, True],
                    "filters": [
                        {
                            "col": "col2",
                            "search": "5",
                        }
                    ],
                },
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            single_var = response.json()["single_var"]
            assert single_var["name"] == "df3"
            assert single_var["type"] == "DataFrame"
            assert single_var["value"]["multi_value"]["column_count"] == 3
            assert single_var["value"]["multi_value"]["row_count"] == 3
            assert single_var["value"]["multi_value"]["column_names"] == [
                "col1",
                "col2",
                "col3",
            ]
            assert single_var["value"]["multi_value"]["column_types"] == [
                "integer",
                "integer",
                "string",
            ]
            assert single_var["value"]["multi_value"]["data"] == [
                ["2", "5", "a"],
                ["3", "5", "a"],
                ["1", "5", "b"],
            ]
            assert single_var["summary"] == "Size: 6x3"
            assert single_var["abbreviated"] is False
            assert single_var["has_next_page"] is False

            # Multiple Filters
            response = await client.post(
                f"/notebooks/{uuid}/vars/df3",
                json={
                    "page_size": 10,
                    "page": 0,
                    "sort_by": ["col3", "col1"],
                    "ascending": [True, True],
                    "filters": [
                        {
                            "col": "col2",
                            "search": "5",
                        },
                        {"col": "col1", "min": 2},
                    ],
                },
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            single_var = response.json()["single_var"]
            assert single_var["name"] == "df3"
            assert single_var["type"] == "DataFrame"
            assert single_var["value"]["multi_value"]["column_count"] == 3
            assert single_var["value"]["multi_value"]["row_count"] == 2
            assert single_var["value"]["multi_value"]["column_names"] == [
                "col1",
                "col2",
                "col3",
            ]
            assert single_var["value"]["multi_value"]["column_types"] == [
                "integer",
                "integer",
                "string",
            ]
            assert single_var["value"]["multi_value"]["data"] == [
                ["2", "5", "a"],
                ["3", "5", "a"],
            ]
            assert single_var["summary"] == "Size: 6x3"
            assert single_var["abbreviated"] is False
            assert single_var["has_next_page"] is False

            # Shouldn't have changed anything in the current vars
            response = await client.get(
                f"/notebooks/{uuid}/vars", headers=superuser_token_headers
            )
            assert response.status_code == 200
            current_vars = response.json()["vars"]
            current_vars = filter(
                lambda x: x["name"] != "___d1os", current_vars
            )
            assert list(current_vars) == data["vars"]

            # Var that doesn't exist
            response = await client.get(
                f"/notebooks/{uuid}/vars/df2", headers=superuser_token_headers
            )
            assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_single_var_statistical_summary(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Able to get a statistical summary for a variable
        """
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == 'print("Larry the Llama")'

        cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        params = {
            "source": "import pandas as pd\nfrom datetime import datetime\n"
            "df3 = pd.DataFrame(data={"
            "'col1': [4, 5, 1, 7, 10],"
            "'col2': [datetime(2021,2,10),datetime(2021,5,23),datetime(2020,1,30),"
            "datetime(2020,10,20),datetime(2020,6,5)],"
            "'col3': [5.5, -2.3, 5.5, 191.3, 5.5],"
            "'col4': ['hello', '😎', '😎', 'hello', 'hi'],"
            "'col5': [4, 5.5, pd.NA, 'hello', 10]"
            "})"
        }
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        response = await client.get(
            f"/notebooks/{uuid}/vars/df3/stats",
            headers=superuser_token_headers,
        )
        assert response.status_code == 404

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            # Kernel vars update
            data = await receive_json(websocket, msg_types=["vars"])
            vars = {var["name"]: var for var in data["vars"]}
            assert vars["df3"]["type"] == "DataFrame"

            # Get df3 stats
            response = await client.get(
                f"/notebooks/{uuid}/vars/df3/stats",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            stats = response.json()

            assert len(stats["stats"]) == 5

            assert stats["stats"]["col1"] == {
                "min": 1,
                "max": 10,
                "mean": 5.4,
                "type": "numeric",
                "na_count": 0,
                "top_values": None,
                "unique_count": None,
            }

            assert stats["stats"]["col2"] == {
                "min": "2020-01-30 00:00:00",
                "max": "2021-05-23 00:00:00",
                "mean": None,
                "type": "date",
                "na_count": 0,
                "top_values": None,
                "unique_count": 5,
            }

            assert stats["stats"]["col3"] == {
                "min": -2.3,
                "max": 191.3,
                "mean": 41.1,
                "type": "numeric",
                "na_count": 0,
                "top_values": None,
                "unique_count": None,
            }

            assert stats["stats"]["col4"] == {
                "min": None,
                "max": None,
                "mean": None,
                "type": "category",
                "na_count": 0,
                "top_values": {"hello": 2, "hi": 1, "😎": 2},
                "unique_count": 3,
            }

            assert stats["stats"]["col5"] == {
                "min": None,
                "max": None,
                "mean": None,
                "type": "misc",
                "na_count": 1,
                "top_values": None,
                "unique_count": 4,
            }

    @pytest.mark.asyncio
    async def test_get_single_var_statistical_summary_single_column(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Able to get a statistical summary for a specific column in a variable
        """
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == 'print("Larry the Llama")'

        cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        params = {
            "source": "import pandas as pd\nfrom datetime import datetime\n"
            "df3 = pd.DataFrame(data={"
            "'col1': [4, 5, 1, 7, 10],"
            "'col2': [datetime(2021,2,10),datetime(2021,5,23),datetime(2020,1,30),"
            "datetime(2020,10,20),datetime(2020,6,5)],"
            "'β🥦': [5.5, -2.3, 5.5, 191.3, 5.5],"
            "'col4': ['hello', '😎', '😎', 'hello', 'hi'],"
            "'col5': [4, 5.5, pd.NA, 'hello', 10]"
            "})"
        }
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        response = await client.get(
            f"/notebooks/{uuid}/vars/df3/stats/col1",
            headers=superuser_token_headers,
        )
        assert response.status_code == 404

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            # Kernel vars update
            data = await receive_json(websocket, msg_types=["vars"])
            vars = {var["name"]: var for var in data["vars"]}
            assert vars["df3"]["type"] == "DataFrame"

            # Get col1 stats
            response = await client.get(
                f"/notebooks/{uuid}/vars/df3/stats/col1",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            stats = response.json()

            assert len(stats["stats"]) == 1

            assert stats["stats"]["col1"] == {
                "min": 1,
                "max": 10,
                "mean": 5.4,
                "type": "numeric",
                "na_count": 0,
                "top_values": None,
                "unique_count": None,
            }

            # Get β🥦 stats
            response = await client.get(
                f"/notebooks/{uuid}/vars/df3/stats/β🥦",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            stats = response.json()

            assert len(stats["stats"]) == 1

            assert stats["stats"]["β🥦"] == {
                "min": -2.3,
                "max": 191.3,
                "mean": 41.1,
                "type": "numeric",
                "na_count": 0,
                "top_values": None,
                "unique_count": None,
            }

    @pytest.mark.asyncio
    async def test_get_single_var_detail_sorting_numpy(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Able to sort columns in dataframe
        """
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == 'print("Larry the Llama")'

        cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        params = {
            "source": "import numpy as np\narray1 = "
            "np.array([['c', 'd', '5', 'Cool'],"
            "['b', 'd', '5', 'cool'],"
            "['c', 'l', '3', 'Kool'],"
            "['b', 'e', '3', 'Koolaid'],"
            "['a', 'f', '2', 'Coffee']])"
        }
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        response = await client.get(
            f"/notebooks/{uuid}/vars", headers=superuser_token_headers
        )
        assert response.status_code == 200
        assert len(response.json()["vars"]) == 0

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            # Kernel vars update
            data = await receive_json(websocket, msg_types=["vars"])

            # Sort by 2 columns
            response = await client.post(
                f"/notebooks/{uuid}/vars/array1",
                json={
                    "page_size": 10,
                    "page": 0,
                    "sort_by": [0, 2],
                    "ascending": [True],
                },
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            single_var = response.json()["single_var"]
            assert single_var["name"] == "array1"
            assert single_var["type"] == "ndarray"
            assert single_var["value"]["multi_value"]["column_count"] == 4
            assert single_var["value"]["multi_value"]["row_count"] == 5
            assert single_var["value"]["multi_value"]["column_names"] == [
                "0",
                "1",
                "2",
                "3",
            ]
            assert single_var["value"]["multi_value"]["column_types"] == [
                "string",
                "string",
                "string",
                "string",
            ]
            assert single_var["value"]["multi_value"]["data"] == [
                ["a", "f", "2", "Coffee"],
                ["b", "e", "3", "Koolaid"],
                ["b", "d", "5", "cool"],
                ["c", "l", "3", "Kool"],
                ["c", "d", "5", "Cool"],
            ]
            assert single_var["summary"] == "Size: 5x4 Memory: 560.0 Bytes"
            assert single_var["abbreviated"] is False
            assert single_var["has_next_page"] is False

            # Shouldn't have changed anything in the current vars
            response = await client.get(
                f"/notebooks/{uuid}/vars", headers=superuser_token_headers
            )
            assert response.status_code == 200
            current_vars = response.json()["vars"]
            current_vars = filter(
                lambda x: x["name"] != "___d1os", current_vars
            )
            assert list(current_vars) == data["vars"]

            # Var that doesn't exist
            response = await client.get(
                f"/notebooks/{uuid}/vars/df2", headers=superuser_token_headers
            )
            assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_single_var_detail_sorting_weird_characters(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Make sure weird characters don't break sorting
        """
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == 'print("Larry the Llama")'

        cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        weird_chars = [
            " ",
            ",",
            "'",
            '"',
            "`",
            "%",
            "$",
            "+",
            "<",
            ";",
            "*",
            "(",
            "🥸",
            "⻆",
        ]
        params = {
            "source": """
            import pandas as pd
            df3 = pd.DataFrame()
            for x in {}:
                df3[x] = [3, 5, 2, 4, 1, 6]
            """.format(
                weird_chars
            )
        }
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        response = await client.get(
            f"/notebooks/{uuid}/vars", headers=superuser_token_headers
        )
        assert response.status_code == 200
        assert len(response.json()["vars"]) == 0

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            # Kernel vars update
            data = await receive_json(websocket, msg_types=["vars"])

            for x in weird_chars:

                # Sort by single column
                response = await client.post(
                    f"/notebooks/{uuid}/vars/df3",
                    json={"page_size": 10, "page": 0, "sort_by": [x]},
                    headers=superuser_token_headers,
                )
                assert response.status_code == 200
                single_var = response.json()["single_var"]
                assert (
                    single_var["value"]["multi_value"]["column_names"]
                    == weird_chars
                )
                assert single_var["name"] == "df3"
                assert single_var["type"] == "DataFrame"
                assert single_var["value"]["multi_value"]["row_count"] == 6
                assert single_var["value"]["multi_value"]["row_names"] == [
                    "4",
                    "2",
                    "0",
                    "3",
                    "1",
                    "5",
                ]
                assert single_var["value"]["multi_value"]["column_types"] == [
                    "integer" for i in weird_chars
                ]
                assert single_var["abbreviated"] is False
                assert single_var["has_next_page"] is False

                # Filter a column
                response = await client.post(
                    f"/notebooks/{uuid}/vars/df3",
                    json={
                        "page_size": 10,
                        "page": 0,
                        "filters": [{"col": x, "min": 4}],
                    },
                    headers=superuser_token_headers,
                )
                assert response.status_code == 200
                single_var = response.json()["single_var"]
                assert (
                    single_var["value"]["multi_value"]["column_names"]
                    == weird_chars
                )
                assert single_var["name"] == "df3"
                assert single_var["type"] == "DataFrame"
                assert single_var["value"]["multi_value"]["row_count"] == 3
                assert single_var["value"]["multi_value"]["row_names"] == [
                    "1",
                    "3",
                    "5",
                ]
                assert single_var["value"]["multi_value"]["column_types"] == [
                    "integer" for i in weird_chars
                ]
                assert single_var["abbreviated"] is False
                assert single_var["has_next_page"] is False

            # Shouldn't have changed anything in the current vars
            response = await client.get(
                f"/notebooks/{uuid}/vars", headers=superuser_token_headers
            )
            assert response.status_code == 200
            current_vars = response.json()["vars"]
            current_vars = filter(
                lambda x: x["name"] != "___d1os", current_vars
            )
            assert list(current_vars) == data["vars"]

            # Var that doesn't exist
            response = await client.get(
                f"/notebooks/{uuid}/vars/df2", headers=superuser_token_headers
            )
            assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_single_var_detail_r_kernel(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        R Kernel large dataframe returns data in detail request, not in summary
        """
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple_r.ipynb"
        )

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == "f <- 543"

        cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        params = {"source": "kool = data.frame(col1=c(1:150), col2=c(150:1))"}
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        response = await client.get(
            f"/notebooks/{uuid}/vars", headers=superuser_token_headers
        )
        assert response.status_code == 200
        assert len(response.json()["vars"]) == 0

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            # Kernel vars update
            data = await receive_json(
                websocket, msg_types=["vars"], timeout=90, max_retries=50
            )
            vars = {var["name"]: var for var in data["vars"]}

            assert vars["kool"]["type"] == "data.frame"
            assert vars["kool"]["value"]["multi_value"]["column_count"] == 2
            assert vars["kool"]["value"]["multi_value"]["row_count"] == 150
            assert vars["kool"]["value"]["multi_value"]["column_names"] is None
            assert vars["kool"]["value"]["multi_value"]["data"] is None
            assert vars["kool"]["value"]["multi_value"]["column_types"] is None
            assert "Size: 150x2 Memory:" in vars["kool"]["summary"]
            assert vars["kool"]["abbreviated"] is False
            assert vars["kool"]["has_next_page"] is False

            response = await client.get(
                f"/notebooks/{uuid}/vars", headers=superuser_token_headers
            )
            assert response.status_code == 200
            current_vars = response.json()["vars"]
            assert list(current_vars) == data["vars"]

            response = await client.get(
                f"/notebooks/{uuid}/vars/kool", headers=superuser_token_headers
            )
            assert response.status_code == 200
            single_var = response.json()["single_var"]
            assert single_var["name"] == "kool"
            assert single_var["type"] == "data.frame"
            assert single_var["value"]["multi_value"]["column_count"] == 2
            assert single_var["value"]["multi_value"]["row_count"] == 150
            assert single_var["value"]["multi_value"]["column_names"] == [
                "col1 (integer)",
                "col2 (integer)",
            ]
            assert single_var["value"]["multi_value"]["column_types"] == [
                "integer",
                "integer",
            ]
            assert single_var["value"]["multi_value"]["data"] == [
                [str(i + 1), str(150 - i)] for i in range(50)
            ]
            assert "Size: 150x2 Memory:" in single_var["summary"]
            assert single_var["abbreviated"] is True
            assert single_var["has_next_page"] is True

            # Shouldn't have changed anything in the current vars
            response = await client.get(
                f"/notebooks/{uuid}/vars", headers=superuser_token_headers
            )
            assert response.status_code == 200
            current_vars = response.json()["vars"]
            assert list(current_vars) == data["vars"]

            # Var that doesn't exist
            response = await client.get(
                f"/notebooks/{uuid}/vars/df2", headers=superuser_token_headers
            )
            assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_single_var_detail_r_kernel_pagination(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        R Kernel dataframe is paginated in details request
        """
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple_r.ipynb"
        )

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == "f <- 543"

        cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        params = {"source": "kool = data.frame(col1=c(1:150), col2=c(150:1))"}
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        response = await client.get(
            f"/notebooks/{uuid}/vars", headers=superuser_token_headers
        )
        assert response.status_code == 200
        assert len(response.json()["vars"]) == 0

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            # Kernel vars update
            data = await receive_json(
                websocket, msg_types=["vars"], timeout=90, max_retries=50
            )
            vars = {var["name"]: var for var in data["vars"]}
            assert vars["kool"]["type"] == "data.frame"

            # First Page
            response = await client.get(
                f"/notebooks/{uuid}/vars/kool",
                query_string={"page_size": 11, "page": 0},
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            single_var = response.json()["single_var"]
            assert single_var["name"] == "kool"
            assert single_var["type"] == "data.frame"
            assert single_var["value"]["multi_value"]["column_count"] == 2
            assert single_var["value"]["multi_value"]["row_count"] == 150
            assert single_var["value"]["multi_value"]["column_names"] == [
                "col1 (integer)",
                "col2 (integer)",
            ]
            assert single_var["value"]["multi_value"]["column_types"] == [
                "integer",
                "integer",
            ]
            assert single_var["value"]["multi_value"]["data"] == [
                [str(i + 1), str(150 - i)] for i in range(11)
            ]
            assert "Size: 150x2 Memory:" in single_var["summary"]
            assert single_var["abbreviated"] is True
            assert single_var["has_next_page"] is True

            # Second Page
            response = await client.get(
                f"/notebooks/{uuid}/vars/kool",
                query_string={"page_size": 11, "page": 1},
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            single_var = response.json()["single_var"]
            assert single_var["name"] == "kool"
            assert single_var["type"] == "data.frame"
            assert single_var["value"]["multi_value"]["column_count"] == 2
            assert single_var["value"]["multi_value"]["row_count"] == 150
            assert single_var["value"]["multi_value"]["column_names"] == [
                "col1 (integer)",
                "col2 (integer)",
            ]
            assert single_var["value"]["multi_value"]["column_types"] == [
                "integer",
                "integer",
            ]
            assert single_var["value"]["multi_value"]["data"] == [
                [str(i + 1), str(150 - i)] for i in range(11, 22)
            ]
            assert "Size: 150x2 Memory:" in single_var["summary"]
            assert single_var["abbreviated"] is True
            assert single_var["has_next_page"] is True

            # Final Page
            response = await client.get(
                f"/notebooks/{uuid}/vars/kool",
                query_string={"page_size": 11, "page": 13},
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            single_var = response.json()["single_var"]
            assert single_var["name"] == "kool"
            assert single_var["type"] == "data.frame"
            assert single_var["value"]["multi_value"]["column_count"] == 2
            assert single_var["value"]["multi_value"]["row_count"] == 150
            assert single_var["value"]["multi_value"]["column_names"] == [
                "col1 (integer)",
                "col2 (integer)",
            ]
            assert single_var["value"]["multi_value"]["column_types"] == [
                "integer",
                "integer",
            ]
            assert single_var["value"]["multi_value"]["data"] == [
                [str(i + 1), str(150 - i)] for i in range(143, 150)
            ]
            assert "Size: 150x2 Memory:" in single_var["summary"]
            assert single_var["abbreviated"] is False
            assert single_var["has_next_page"] is False

            # Shouldn't have changed anything in the current vars
            response = await client.get(
                f"/notebooks/{uuid}/vars", headers=superuser_token_headers
            )
            assert response.status_code == 200
            current_vars = response.json()["vars"]
            assert list(current_vars) == data["vars"]

            # Var that doesn't exist
            response = await client.get(
                f"/notebooks/{uuid}/vars/df2", headers=superuser_token_headers
            )
            assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_single_var_statistical_summary_r_kernel(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        R Kernel returns statistical summary for dataframes
        """
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple_r.ipynb"
        )

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == "f <- 543"

        cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        params = {
            "source": (
                "kool <- data.frame(col1=c(4, 5, 1, 7, 10),"
                + "col2=c(as.Date('2021-01-10'),as.Date('2021-05-23'),"
                + "as.Date('2020-01-30'),as.Date('2020-10-20'),as.Date('2020-06-05')),"
                + "col3=c(5.5, -2.3, 5.5, 0191.3, 5.5),"
                + "col4=factor(c('hello', '😎', '😎', 'hello', 'hi')),"
                + "col5=c(4, 5.5, NA, 'hello', 10))"
            )
        }
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        response = await client.get(
            f"/notebooks/{uuid}/vars/kool/stats",
            headers=superuser_token_headers,
        )
        assert response.status_code == 404

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            # Kernel vars update
            data = await receive_json(websocket, msg_types=["vars"])
            vars = {var["name"]: var for var in data["vars"]}
            assert vars["kool"]["type"] == "data.frame"

            # Get kool stats
            response = await client.get(
                f"/notebooks/{uuid}/vars/kool/stats",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            stats = response.json()

            assert len(stats["stats"]) == 5
            assert stats["stats"]["col1"] == {
                "min": 1,
                "max": 10,
                "mean": 5.4,
                "type": "numeric",
                "na_count": 0,
                "top_values": None,
                "unique_count": None,
            }

            assert stats["stats"]["col2"] == {
                "min": "2020-01-30",
                "max": "2021-05-23",
                "mean": None,
                "type": "date",
                "na_count": 0,
                "top_values": None,
                "unique_count": 5,
            }

            assert stats["stats"]["col3"] == {
                "min": -2.3,
                "max": 191.3,
                "mean": 41.1,
                "type": "numeric",
                "na_count": 0,
                "top_values": None,
                "unique_count": None,
            }

            assert stats["stats"]["col4"] == {
                "min": None,
                "max": None,
                "mean": None,
                "type": "category",
                "na_count": 0,
                "top_values": {"hello": 2, "😎": 2},
                "unique_count": 2,
            }

            assert stats["stats"]["col5"] == {
                "min": None,
                "max": None,
                "mean": None,
                "type": "misc",
                "na_count": 1,
                "top_values": None,
                "unique_count": 4,
            }

    @pytest.mark.asyncio
    async def test_get_single_var_statistical_summary_r_kernel_single_column(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        R Kernel - able to get a statistical summary for a specific column
        """
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple_r.ipynb"
        )

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == "f <- 543"

        cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        params = {
            "source": (
                "kool <- data.frame(col1=c(4, 5, 1, 7, 10),"
                + "col2=c(as.Date('2021-01-10'),as.Date('2021-05-23'),"
                + "as.Date('2020-01-30'),as.Date('2020-10-20'),as.Date('2020-06-05')),"
                + "col3=c(5.5, -2.3, 5.5, 0191.3, 5.5),"
                + "col4=factor(c('hello', '😎', '😎', 'hello', 'hi')),"
                + "col5=c(4, 5.5, NA, 'hello', 10))"
            )
        }
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        response = await client.get(
            f"/notebooks/{uuid}/vars/kool/stats",
            headers=superuser_token_headers,
        )
        assert response.status_code == 404

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            # Kernel vars update
            data = await receive_json(
                websocket, msg_types=["vars"], max_retries=50
            )
            print(data)
            vars = {var["name"]: var for var in data["vars"]}
            assert vars["kool"]["type"] == "data.frame"

            # Get col1 stats
            response = await client.get(
                f"/notebooks/{uuid}/vars/kool/stats/col1",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            stats = response.json()

            assert len(stats["stats"]) == 1
            assert stats["stats"]["col1"] == {
                "min": 1,
                "max": 10,
                "mean": 5.4,
                "type": "numeric",
                "na_count": 0,
                "top_values": None,
                "unique_count": None,
            }

            # Get col3 stats
            response = await client.get(
                f"/notebooks/{uuid}/vars/kool/stats/col3",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            stats = response.json()

            assert len(stats["stats"]) == 1
            assert stats["stats"]["col3"] == {
                "min": -2.3,
                "max": 191.3,
                "mean": 41.1,
                "type": "numeric",
                "na_count": 0,
                "top_values": None,
                "unique_count": None,
            }

    @pytest.mark.asyncio
    async def test_post_single_detail_r_kernel_sorting(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        R Kernel sorting and filtering params
        """
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple_r.ipynb"
        )

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == "f <- 543"

        cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]

        params = {
            "source": """
                kool = dataframe1 <- data.frame(
                    Name = c('Jon', 'Bill', 'Maria', 'Ben', 'Tina'),
                    Age = c(23, 41, 32, 58, 26),
                    Employed = c(TRUE, FALSE, TRUE, TRUE, FALSE)
                )
            """
        }
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=params,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        response = await client.get(
            f"/notebooks/{uuid}/vars", headers=superuser_token_headers
        )
        assert response.status_code == 200
        assert len(response.json()["vars"]) == 0

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            # Kernel vars update
            data = await receive_json(
                websocket, msg_types=["vars"], timeout=90, max_retries=50
            )
            vars = {var["name"]: var for var in data["vars"]}

            assert vars["kool"]["type"] == "data.frame"

            # Sort by Name column
            response = await client.post(
                f"/notebooks/{uuid}/vars/kool",
                headers=superuser_token_headers,
                json={"sort_by": ["Name"]},
            )
            assert response.status_code == 200
            single_var = response.json()["single_var"]
            assert single_var["name"] == "kool"
            assert single_var["type"] == "data.frame"
            assert single_var["value"]["multi_value"]["column_count"] == 3
            assert single_var["value"]["multi_value"]["row_count"] == 5
            assert single_var["value"]["multi_value"]["column_names"] == [
                "Name (character)",
                "Age (numeric)",
                "Employed (logical)",
            ]
            assert single_var["value"]["multi_value"]["column_types"] == [
                "string",
                "number",
                "boolean",
            ]
            assert single_var["value"]["multi_value"]["data"] == [
                ["Ben", "58", "TRUE"],
                ["Bill", "41", "FALSE"],
                ["Jon", "23", "TRUE"],
                ["Maria", "32", "TRUE"],
                ["Tina", "26", "FALSE"],
            ]
            assert "Size: 5x3 Memory:" in single_var["summary"]
            assert single_var["abbreviated"] is False
            assert single_var["has_next_page"] is False

            # Sort by Age and Name columns
            response = await client.post(
                f"/notebooks/{uuid}/vars/kool",
                headers=superuser_token_headers,
                json={"sort_by": ["Age", "Name"], "ascending": [False, True]},
            )
            assert response.status_code == 200
            single_var = response.json()["single_var"]
            assert single_var["name"] == "kool"
            assert single_var["type"] == "data.frame"
            assert single_var["value"]["multi_value"]["column_count"] == 3
            assert single_var["value"]["multi_value"]["row_count"] == 5
            assert single_var["value"]["multi_value"]["column_names"] == [
                "Name (character)",
                "Age (numeric)",
                "Employed (logical)",
            ]
            assert single_var["value"]["multi_value"]["column_types"] == [
                "string",
                "number",
                "boolean",
            ]
            assert single_var["value"]["multi_value"]["data"] == [
                ["Ben", "58", "TRUE"],
                ["Bill", "41", "FALSE"],
                ["Maria", "32", "TRUE"],
                ["Tina", "26", "FALSE"],
                ["Jon", "23", "TRUE"],
            ]
            assert "Size: 5x3 Memory:" in single_var["summary"]
            assert single_var["abbreviated"] is False
            assert single_var["has_next_page"] is False

            # Search a single column
            response = await client.post(
                f"/notebooks/{uuid}/vars/kool",
                headers=superuser_token_headers,
                json={
                    "filters": [
                        {
                            "col": "Age",
                            "search": "2",
                        },
                    ]
                },
            )
            assert response.status_code == 200
            single_var = response.json()["single_var"]
            assert single_var["name"] == "kool"
            assert single_var["type"] == "data.frame"
            assert single_var["value"]["multi_value"]["column_count"] == 3
            assert single_var["value"]["multi_value"]["row_count"] == 3
            assert single_var["value"]["multi_value"]["column_names"] == [
                "Name (character)",
                "Age (numeric)",
                "Employed (logical)",
            ]
            assert single_var["value"]["multi_value"]["column_types"] == [
                "string",
                "number",
                "boolean",
            ]
            assert single_var["value"]["multi_value"]["data"] == [
                ["Jon", "23", "TRUE"],
                ["Maria", "32", "TRUE"],
                ["Tina", "26", "FALSE"],
            ]
            assert "Size: 5x3 Memory:" in single_var["summary"]
            assert single_var["abbreviated"] is False
            assert single_var["has_next_page"] is False

            # Filter by min/max
            response = await client.post(
                f"/notebooks/{uuid}/vars/kool",
                headers=superuser_token_headers,
                json={
                    "sort_by": ["Age"],
                    "ascending": [True],
                    "filters": [
                        {
                            "col": "Age",
                            "min": 32,
                            "max": 70,
                        },
                    ],
                },
            )
            assert response.status_code == 200
            single_var = response.json()["single_var"]
            assert single_var["name"] == "kool"
            assert single_var["type"] == "data.frame"
            assert single_var["value"]["multi_value"]["column_count"] == 3
            assert single_var["value"]["multi_value"]["row_count"] == 3
            assert single_var["value"]["multi_value"]["column_names"] == [
                "Name (character)",
                "Age (numeric)",
                "Employed (logical)",
            ]
            assert single_var["value"]["multi_value"]["column_types"] == [
                "string",
                "number",
                "boolean",
            ]
            assert single_var["value"]["multi_value"]["data"] == [
                ["Maria", "32", "TRUE"],
                ["Bill", "41", "FALSE"],
                ["Ben", "58", "TRUE"],
            ]
            assert "Size: 5x3 Memory:" in single_var["summary"]
            assert single_var["abbreviated"] is False
            assert single_var["has_next_page"] is False

            # Shouldn't have changed anything in the current vars
            response = await client.get(
                f"/notebooks/{uuid}/vars", headers=superuser_token_headers
            )
            assert response.status_code == 200
            current_vars = response.json()["vars"]
            assert list(current_vars) == data["vars"]


@pytest.mark.usefixtures("clear_notebooks", "clear_notebook_directory")
class TestWorkingDirectory:
    async def assert_python_working_directory(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        open_path: str,
        working_directory: str,
        query_string: Optional[Dict[str, Any]] = None,
    ):
        """Test that python kernel is started in correct directory."""
        if query_string is None:
            query_string = {}
        query_string["filepath"] = open_path
        response = await client.get(
            f"/notebooks/open/",
            headers=superuser_token_headers,
            query_string=query_string,
        )
        assert response.status_code == 201
        resp_json = response.json()["notebook"]
        uuid = resp_json["metadata"]["jupyter_d1"]["uuid"]

        # /tmp symlinks to /private/tmp on mac, so we resolve
        resolved_work_dir = str(pathlib.Path(working_directory).resolve())

        assert (
            resp_json["metadata"]["jupyter_d1"]["working_directory"]
            == resolved_work_dir
        )

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.post(
                f"/notebooks/{uuid}/scratch_execute",
                headers=superuser_token_headers,
                json={"code": "import os\nos.getcwd()"},
            )
            assert response.status_code == 200
            message_id = response.json()["kernel_message"]["message_id"]

            # first chunk received should be a scratch_update with
            # an execution_state of 'busy' when processing starts
            data = await receive_json(websocket, msg_types=["scratch_update"])
            scratch_update = data["scratch_update"]
            assert scratch_update["message_id"] == message_id
            assert scratch_update["execution_state"] == "busy"

            # Receive scratch execution output
            data = await receive_json(websocket, msg_types=["scratch_update"])
            scratch_update = data["scratch_update"]

            expected_output = {
                "data": {"text/plain": f"'{resolved_work_dir}'"},
                "execution_count": 1,
                "metadata": {},
                "output_type": "execute_result",
            }
            assert scratch_update["output"] == expected_output

            # Scratch execution state set to idle
            data = await receive_json(websocket, msg_types=["scratch_update"])
            scratch_update = data["scratch_update"]
            assert scratch_update["message_id"] == message_id
            assert scratch_update["execution_state"] == "idle"

            token = get_superuser_token()
            auth = base64.b64encode(f"{token}:".encode("utf-8"))
            response = await client.get(
                f"/dav{resolved_work_dir}",
                headers={"Authorization": f"Basic {auth.decode('utf-8')}"},
            )
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_working_directory_passed_in(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        If notebook is opened with working directory specified, make sure
        the kernel is running in that directory.
        """
        filename = "simple.ipynb"
        nb_filename = f"jupyter_d1/tests/notebooks/{filename}"
        nb_json = open(nb_filename).read()
        response = await client.post(
            "/notebooks/upload",
            query_string={"filename": filename},
            data=nb_json,
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        await self.assert_python_working_directory(
            client,
            superuser_token_headers,
            open_path=filename,
            working_directory=f"{os.getcwd()}/jupyter_d1/tests/notebooks",
            query_string={
                "working_directory": f"{os.getcwd()}/jupyter_d1"
                "/tests/notebooks"
            },
        )

    @pytest.mark.asyncio
    async def test_file_in_different_working_directory(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        If notebook in a different directory is opened, make sure
        the kernel is running in that directory.
        """
        shutil.copyfile(
            "jupyter_d1/tests/notebooks/simple.ipynb",
            "jupyter_d1/tests/notebooks/simple_copy.ipynb",
        )
        await self.assert_python_working_directory(
            client,
            superuser_token_headers,
            open_path=f"{os.getcwd()}/jupyter_d1/tests/"
            "notebooks/simple_copy.ipynb",
            working_directory=f"{os.getcwd()}/jupyter_d1/tests/notebooks",
        )
        os.remove("jupyter_d1/tests/notebooks/simple_copy.ipynb")

    @pytest.mark.asyncio
    async def test_file_in_parent_directory_of_working_directory(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        If notebook in the parent directory of the server's working directory
        is opened, make sure the kernel is running in that parent directory.
        """
        shutil.copyfile(
            "jupyter_d1/tests/notebooks/simple.ipynb",
            f"/tmp/simple_copy.ipynb",
        )
        await self.assert_python_working_directory(
            client,
            superuser_token_headers,
            open_path=f"/tmp/simple_copy.ipynb",
            working_directory=f"/tmp",
        )
        os.remove("/tmp/simple_copy.ipynb")

    @pytest.mark.asyncio
    async def test_file_in_sub_directory_of_working_directory(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        If notebook in a sub directory of the server's working directory
        is opened, make sure the kernel is running in that sub directory.
        """
        pathlib.Path(f"{settings.ROOT_DIR}/some_nbs").mkdir(exist_ok=True)
        shutil.copyfile(
            "jupyter_d1/tests/notebooks/simple.ipynb",
            f"{settings.ROOT_DIR}/some_nbs/simple_copy.ipynb",
        )
        await self.assert_python_working_directory(
            client,
            superuser_token_headers,
            open_path=f"{settings.ROOT_DIR}/some_nbs/simple_copy.ipynb",
            working_directory=f"{settings.ROOT_DIR}/some_nbs",
        )
        shutil.rmtree(f"{settings.ROOT_DIR}/some_nbs")

    @pytest.mark.asyncio
    async def test_r_kernel_working_directory_passed_in(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        working_directory = "/tmp"
        response = await client.post(
            "/notebooks/create",
            query_string={
                "kspec_name": "ir",
                "filename": "heyp",
                "working_directory": working_directory,
            },
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()["notebook"]
        uuid = resp_json["metadata"]["jupyter_d1"]["uuid"]

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.post(
                f"/notebooks/{uuid}/scratch_execute",
                headers=superuser_token_headers,
                json={"code": "getwd()"},
            )
            assert response.status_code == 200
            message_id = response.json()["kernel_message"]["message_id"]

            # first chunk received should be a scratch_update with
            # an execution_state of 'busy' when processing starts
            data = await receive_json(websocket, msg_types=["scratch_update"])
            scratch_update = data["scratch_update"]
            assert scratch_update["message_id"] == message_id
            assert scratch_update["execution_state"] == "busy"

            # Receive scratch execution output
            data = await receive_json(websocket, msg_types=["scratch_update"])
            scratch_update = data["scratch_update"]
            # /tmp symlinks to /private/tmp on mac, so we resolve
            resolved_work_dir = pathlib.Path(working_directory).resolve()
            expected_output = {
                "data": {
                    "text/html": f"'{resolved_work_dir}'",
                    "text/latex": f"'{resolved_work_dir}'",
                    "text/markdown": f"'{resolved_work_dir}'",
                    "text/plain": f'[1] "{resolved_work_dir}"',
                },
                "metadata": {},
                "output_type": "display_data",
            }
            assert scratch_update["output"] == expected_output

            # Scratch execution state set to idle
            data = await receive_json(websocket, msg_types=["scratch_update"])
            scratch_update = data["scratch_update"]
            assert scratch_update["message_id"] == message_id
            assert scratch_update["execution_state"] == "idle"

            token = get_superuser_token()
            auth = base64.b64encode(f"{token}:".encode("utf-8"))
            response = await client.get(
                f"/dav{resolved_work_dir}",
                headers={"Authorization": f"Basic {auth.decode('utf-8')}"},
            )
            assert response.status_code == 200


@pytest.mark.usefixtures("clear_notebooks", "clear_notebook_directory")
class TestChangeWorkingDirectory:
    async def do_test_change_working_directory(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        kspec_name: str,
    ):
        working_directory = "/tmp"
        resolved_work_dir = str(pathlib.Path(working_directory).resolve())
        response = await client.post(
            "/notebooks/create",
            query_string={
                "kspec_name": kspec_name,
                "filename": "heyp",
                "working_directory": working_directory,
            },
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()["notebook"]
        uuid = resp_json["metadata"]["jupyter_d1"]["uuid"]

        token = get_superuser_token()
        auth = base64.b64encode(f"{token}:".encode("utf-8"))
        response = await client.get(
            f"/dav{resolved_work_dir}",
            headers={"Authorization": f"Basic {auth.decode('utf-8')}"},
        )
        assert response.status_code == 200

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            new_workdir = f"{os.getcwd()}/jupyter_d1/tests/notebooks"
            response = await client.patch(
                f"/notebooks/{uuid}/change_working_directory",
                headers=superuser_token_headers,
                query_string={"directory": new_workdir},
            )
            assert response.status_code == 200

            data = await receive_json(websocket, msg_types=["metadata"])

            metadata = data["metadata"]
            assert metadata["jupyter_d1"]["working_directory"] == new_workdir

            response = await client.get(
                f"/dav{new_workdir}",
                headers={"Authorization": f"Basic {auth.decode('utf-8')}"},
            )
            assert response.status_code == 200

            response = await client.get(
                f"/dav{resolved_work_dir}",
                headers={"Authorization": f"Basic {auth.decode('utf-8')}"},
            )
            assert response.status_code == 404

        response = await client.get(
            f"/notebooks/{uuid}", headers=superuser_token_headers
        )
        resp_json = response.json()["notebook"]
        assert (
            resp_json["metadata"]["jupyter_d1"]["working_directory"]
            == new_workdir
        )

    async def do_test_change_working_directory_in_code(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        kspec_name: str,
        chdir_code: str,
    ):
        working_directory = "/tmp"
        resolved_work_dir = str(pathlib.Path(working_directory).resolve())
        response = await client.post(
            "/notebooks/create",
            query_string={
                "kspec_name": kspec_name,
                "filename": "heyp",
                "working_directory": working_directory,
            },
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()["notebook"]
        uuid = resp_json["metadata"]["jupyter_d1"]["uuid"]

        token = get_superuser_token()
        auth = base64.b64encode(f"{token}:".encode("utf-8"))
        response = await client.get(
            f"/dav{resolved_work_dir}",
            headers={"Authorization": f"Basic {auth.decode('utf-8')}"},
        )
        assert response.status_code == 200

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            new_workdir = f"{os.getcwd()}/jupyter_d1/tests/notebooks"
            response = await client.post(
                f"/notebooks/{uuid}/scratch_execute",
                headers=superuser_token_headers,
                json={"code": chdir_code.format(new_workdir=new_workdir)},
            )
            assert response.status_code == 200

            data = await wait_for_event(websocket, "metadata", timeout=10)

            metadata = data["metadata"]
            assert metadata["jupyter_d1"]["working_directory"] == new_workdir

            response = await client.get(
                f"/dav{new_workdir}",
                headers={"Authorization": f"Basic {auth.decode('utf-8')}"},
            )
            assert response.status_code == 200

            response = await client.get(
                f"/dav{resolved_work_dir}",
                headers={"Authorization": f"Basic {auth.decode('utf-8')}"},
            )
            assert response.status_code == 404

        response = await client.get(
            f"/notebooks/{uuid}", headers=superuser_token_headers
        )
        resp_json = response.json()["notebook"]
        assert (
            resp_json["metadata"]["jupyter_d1"]["working_directory"]
            == new_workdir
        )

    @pytest.mark.asyncio
    async def test_python_change_working_directory_endpoint(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        await self.do_test_change_working_directory(
            client, superuser_token_headers, "python"
        )

    @pytest.mark.asyncio
    async def test_python_change_working_directory_in_code(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        await self.do_test_change_working_directory_in_code(
            client,
            superuser_token_headers,
            "python",
            'import os\nos.chdir("{new_workdir}")',
        )

    @pytest.mark.asyncio
    async def test_r_change_working_directory_endpoint(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        await self.do_test_change_working_directory(
            client, superuser_token_headers, "ir"
        )

    @pytest.mark.asyncio
    async def test_r_change_working_directory_in_code(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        await self.do_test_change_working_directory_in_code(
            client, superuser_token_headers, "ir", 'setwd("{new_workdir}")'
        )

    @pytest.mark.asyncio
    async def test_bash_change_working_directory_endpoint(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        await self.do_test_change_working_directory(
            client, superuser_token_headers, "bash"
        )

    @pytest.mark.asyncio
    async def test_bash_change_working_directory_in_code(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        await self.do_test_change_working_directory_in_code(
            client, superuser_token_headers, "bash", "cd {new_workdir}"
        )

    @pytest.mark.asyncio
    async def test_change_working_directory_fail_invalid_directory(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        working_directory = "/tmp"
        resolved_work_dir = str(pathlib.Path(working_directory).resolve())
        response = await client.post(
            "/notebooks/create",
            query_string={
                "kspec_name": "python",
                "filename": "heyp",
                "working_directory": working_directory,
            },
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()["notebook"]
        uuid = resp_json["metadata"]["jupyter_d1"]["uuid"]

        token = get_superuser_token()
        auth = base64.b64encode(f"{token}:".encode("utf-8"))
        response = await client.get(
            f"/dav{resolved_work_dir}",
            headers={"Authorization": f"Basic {auth.decode('utf-8')}"},
        )
        assert response.status_code == 200

        await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

        new_workdir = f"{os.getcwd()}/tests/notrealdir"
        response = await client.patch(
            f"/notebooks/{uuid}/change_working_directory",
            headers=superuser_token_headers,
            query_string={"directory": new_workdir},
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Directory does not exist"

        await asyncio.sleep(2)

        response = await client.get(
            f"/dav{new_workdir}",
            headers={"Authorization": f"Basic {auth.decode('utf-8')}"},
        )
        assert response.status_code == 404

        response = await client.get(
            f"/dav{resolved_work_dir}",
            headers={"Authorization": f"Basic {auth.decode('utf-8')}"},
        )
        assert response.status_code == 200

        response = await client.get(
            f"/notebooks/{uuid}", headers=superuser_token_headers
        )
        resp_json = response.json()["notebook"]
        assert (
            resp_json["metadata"]["jupyter_d1"]["working_directory"]
            == resolved_work_dir
        )

    @pytest.mark.asyncio
    async def test_restart_kernel_preserves_last_set_workdir(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Set the working directory via the change_working_directory endpoint,
        then restart the kernel, working directory should be preserved
        """
        uuid = await upload_notebook(client, superuser_token_headers)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        cell = cells[2]
        cell_uuid = cell["metadata"]["jupyter_d1"]["uuid"]

        response = await client.get(
            f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        await asyncio.sleep(0.5)

        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        assert cells[2]["outputs"][0]["data"]["text/plain"] == "7"

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            new_workdir = "/tmp"
            resolved_work_dir = str(pathlib.Path(new_workdir).resolve())
            response = await client.patch(
                f"/notebooks/{uuid}/change_working_directory",
                headers=superuser_token_headers,
                query_string={"directory": resolved_work_dir},
            )
            assert response.status_code == 200

            data = await receive_json(websocket, msg_types=["metadata"])

            metadata = data["metadata"]
            assert (
                metadata["jupyter_d1"]["working_directory"]
                == resolved_work_dir
            )

            response = await client.get(
                f"/notebooks/{uuid}/restart_kernel",
                headers=superuser_token_headers,
            )

            assert response.status_code == 204

            data = await wait_for_event(websocket, "kernel_restarted")

            assert data["kernel_restarted"]["run_all_cells"] is False
            cells = data["kernel_restarted"]["cells"]
            assert cells[2]["outputs"][0]["data"]["text/plain"] == "7"
            assert cells[2]["execution_count"] == 1

            data = await receive_json(websocket, msg_types=["metadata"])

            metadata = data["metadata"]
            assert (
                metadata["jupyter_d1"]["working_directory"]
                == resolved_work_dir
            )

            response = await client.get(
                f"/notebooks/{uuid}", headers=superuser_token_headers
            )
            assert response.status_code == 200
            notebook = response.json()["notebook"]
            assert (
                notebook["metadata"]["jupyter_d1"]["working_directory"]
                == resolved_work_dir
            )

            response = await client.post(
                f"/notebooks/{uuid}/scratch_execute",
                headers=superuser_token_headers,
                json={"code": "pwd"},
            )
            assert response.status_code == 200
            message_id = response.json()["kernel_message"]["message_id"]

            # first chunk received should be a scratch_update with
            # an execution_state of 'busy' when processing starts
            data = await receive_json(websocket, msg_types=["scratch_update"])
            scratch_update = data["scratch_update"]
            assert scratch_update["message_id"] == message_id
            assert scratch_update["execution_state"] == "busy"

            # Receive scratch execution output
            data = await receive_json(websocket, msg_types=["scratch_update"])
            scratch_update = data["scratch_update"]
            expected_output = {
                "data": {"text/plain": f"'{resolved_work_dir}'"},
                "execution_count": 1,
                "metadata": {},
                "output_type": "execute_result",
            }
            assert scratch_update["output"] == expected_output

    @pytest.mark.asyncio
    async def test_restart_and_run_all_cells_preserves_last_set_workdir(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        other_notebook_directory: str,
    ):
        """
        Set the working directory via the change_working_directory endpoint,
        run cell to os.chdir, then restart the kernel and run all cells,
        working directory should be reset to the last one set via
        change_working_directory
        """
        resolved_other_dir = str(
            pathlib.Path(other_notebook_directory).resolve()
        )

        working_directory = "/tmp"
        resolved_work_dir = str(pathlib.Path(working_directory).resolve())
        response = await client.post(
            "/notebooks/create",
            query_string={
                "kspec_name": "python",
                "filename": "oschdirnb",
                "working_directory": working_directory,
            },
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        resp_json = response.json()["notebook"]
        uuid = resp_json["metadata"]["jupyter_d1"]["uuid"]

        assert (
            resp_json["metadata"]["jupyter_d1"]["working_directory"]
            == resolved_work_dir
        )

        # Create a file to be read from notebook
        with open(f"{other_notebook_directory}/somedata.txt", "w") as f:
            f.write("phosh5 buwl74")

        new_workdir = f"{os.getcwd()}/jupyter_d1/tests/notebooks"
        response = await client.post(
            f"/notebooks/{uuid}/cells",
            json={"source": f'import os\nos.chdir("{new_workdir}")'},
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        cell = response.json()["cell"]
        cell_uuid = cell["metadata"]["jupyter_d1"]["uuid"]

        response = await client.post(
            f"/notebooks/{uuid}/cells",
            json={
                "source": f'with open("somedata.txt", "r") as f:\n'
                "   print(f.read())"
            },
            headers=superuser_token_headers,
        )
        assert response.status_code == 201
        cell2 = response.json()["cell"]
        cell_uuid2 = cell2["metadata"]["jupyter_d1"]["uuid"]

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # Change directory with endpoint first
            response = await client.patch(
                f"/notebooks/{uuid}/change_working_directory",
                headers=superuser_token_headers,
                query_string={"directory": other_notebook_directory},
            )
            assert response.status_code == 200

            data = await receive_json(websocket, msg_types=["metadata"])

            metadata = data["metadata"]
            assert (
                metadata["jupyter_d1"]["working_directory"]
                == resolved_other_dir
            )

            # Execute code to change working directory second
            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            data = await wait_for_event(websocket, "metadata", timeout=10)

            metadata = data["metadata"]
            assert metadata["jupyter_d1"]["working_directory"] == new_workdir

            # Remove code that changed directory so it doesn't get run on restart
            response = await client.delete(
                f"/notebooks/{uuid}/cells/{cell_uuid}",
                headers=superuser_token_headers,
            )
            assert response.status_code == 204

            response = await client.get(
                f"/notebooks/{uuid}/restart_kernel_and_execute_all",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            data = await wait_for_event(websocket, "kernel_restarted")

            assert data["kernel_restarted"]["run_all_cells"] is True
            cells = data["kernel_restarted"]["cells"]
            assert len(cells[0]["outputs"]) == 0
            assert cells[0]["execution_count"] is None

            # Directory should get set on restart
            data = await receive_json(websocket, msg_types=["metadata"])
            metadata = data["metadata"]
            assert (
                metadata["jupyter_d1"]["working_directory"]
                == resolved_other_dir
            )

            data = await receive_json(websocket, msg_types=["cell_update"])
            assert len(data["cell_update"]) == 1
            metadata = data["cell_update"][0]["metadata"]["jupyter_d1"]
            assert metadata["execution_state"] == "busy"
            assert "execution_count" not in metadata
            assert metadata["uuid"] == cell_uuid2

            # Make sure notebook cell ran successfully, which can only happen
            # if the kernel has the right working directory
            data = await receive_json(websocket, msg_types=["cell_update"])
            assert len(data["cell_update"]) == 1
            metadata = data["cell_update"][0]["metadata"]["jupyter_d1"]
            assert metadata["execution_state"] == "busy"
            assert "execution_count" not in metadata
            assert metadata["uuid"] == cell_uuid2
            assert data["cell_update"][0]["outputs"] == [
                {
                    "name": "stdout",
                    "output_type": "stream",
                    "text": ["phosh5 buwl74\n", "\n"],
                }
            ]

            response = await client.get(
                f"/notebooks/{uuid}", headers=superuser_token_headers
            )
            assert response.status_code == 200
            notebook = response.json()["notebook"]
            assert (
                notebook["metadata"]["jupyter_d1"]["working_directory"]
                == resolved_other_dir
            )

            response = await client.post(
                f"/notebooks/{uuid}/scratch_execute",
                headers=superuser_token_headers,
                json={"code": "pwd"},
            )
            assert response.status_code == 200
            message_id = response.json()["kernel_message"]["message_id"]

            # first chunk received should be a scratch_update with
            # an execution_state of 'busy' when processing starts
            data = await receive_json(websocket, msg_types=["scratch_update"])
            scratch_update = data["scratch_update"]
            assert scratch_update["message_id"] == message_id
            assert scratch_update["execution_state"] == "busy"

            # Receive scratch execution output
            data = await receive_json(websocket, msg_types=["scratch_update"])
            scratch_update = data["scratch_update"]
            expected_output = {
                "data": {"text/plain": f"'{resolved_other_dir}'"},
                "execution_count": 2,
                "metadata": {},
                "output_type": "execute_result",
            }
            assert scratch_update["output"] == expected_output


@pytest.mark.usefixtures("clear_notebooks", "clear_notebook_directory")
class TestSaveAs:
    @pytest.mark.asyncio
    async def test_rename(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, filename="simple.ipynb"
        )

        assert os.path.exists(f"{settings.ROOT_DIR}/simple.ipynb")
        assert not os.path.exists(f"{settings.ROOT_DIR}/awholenewname.ipynb")

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            response = await client.patch(
                f"/notebooks/{uuid}/rename",
                query_string={"filename": "awholenewname"},
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            assert (
                response.json()["path"]
                == f"{settings.ROOT_DIR}/awholenewname.ipynb"
            )

            data = await receive_json(websocket, msg_types=["metadata"])
            metadata = data["metadata"]
            assert (
                metadata["jupyter_d1"]["path"]
                == f"{settings.ROOT_DIR}/awholenewname.ipynb"
            )
            assert metadata["jupyter_d1"]["name"] == "awholenewname"

            assert os.path.exists(f"{settings.ROOT_DIR}/awholenewname.ipynb")
            assert not os.path.exists(f"{settings.ROOT_DIR}/simple.ipynb")

    @pytest.mark.asyncio
    async def test_rename_different_directory(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        other_notebook_directory: str,
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, filename="simple.ipynb"
        )

        assert os.path.exists(f"{settings.ROOT_DIR}/simple.ipynb")
        assert not os.path.exists(
            f"{other_notebook_directory}/awholenewname.ipynb"
        )

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            response = await client.patch(
                f"/notebooks/{uuid}/rename",
                query_string={
                    "filename": "awholenewname",
                    "directory": other_notebook_directory,
                },
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            assert (
                response.json()["path"]
                == f"{other_notebook_directory}/awholenewname.ipynb"
            )

            data = await receive_json(websocket, msg_types=["metadata"])
            metadata = data["metadata"]
            assert resolve(metadata["jupyter_d1"]["path"]) == resolve(
                f"{other_notebook_directory}/awholenewname.ipynb"
            )
            assert metadata["jupyter_d1"]["name"] == "awholenewname"

            assert os.path.exists(
                f"{other_notebook_directory}/awholenewname.ipynb"
            )
            assert not os.path.exists(f"{settings.ROOT_DIR}/simple.ipynb")

    @pytest.mark.asyncio
    async def test_rename_file_exists(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        other_notebook_directory: str,
    ):
        """Fail if file exists unless overwrite param is set to true"""
        uuid = await upload_notebook(
            client, superuser_token_headers, filename="simple.ipynb"
        )

        with open(f"{other_notebook_directory}/awholenewname.ipynb", "w") as f:
            f.write("some text here")

        assert os.path.exists(f"{settings.ROOT_DIR}/simple.ipynb")
        assert os.path.exists(
            f"{other_notebook_directory}/awholenewname.ipynb"
        )

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            response = await client.patch(
                f"/notebooks/{uuid}/rename",
                query_string={
                    "filename": "awholenewname",
                    "directory": other_notebook_directory,
                },
                headers=superuser_token_headers,
            )
            assert response.status_code == 400
            assert response.json()["detail"] == f"File already exists"

            response = await client.patch(
                f"/notebooks/{uuid}/rename",
                query_string={
                    "filename": "awholenewname",
                    "directory": other_notebook_directory,
                    "overwrite": True,
                },
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            assert (
                response.json()["path"]
                == f"{other_notebook_directory}/awholenewname.ipynb"
            )

            data = await receive_json(websocket, msg_types=["metadata"])
            metadata = data["metadata"]
            assert resolve(metadata["jupyter_d1"]["path"]) == resolve(
                f"{other_notebook_directory}/awholenewname.ipynb"
            )
            assert metadata["jupyter_d1"]["name"] == "awholenewname"

            assert os.path.exists(
                f"{other_notebook_directory}/awholenewname.ipynb"
            )
            assert not os.path.exists(f"{settings.ROOT_DIR}/simple.ipynb")

        with open(f"{other_notebook_directory}/awholenewname.ipynb", "r") as f:
            assert f.read() != "some text here"

    @pytest.mark.asyncio
    async def test_rename_just_metadata(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        other_notebook_directory: str,
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, filename="simple.ipynb"
        )

        assert os.path.exists(f"{settings.ROOT_DIR}/simple.ipynb")
        assert not os.path.exists(
            f"{other_notebook_directory}/awholenewname.ipynb"
        )

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            response = await client.patch(
                f"/notebooks/{uuid}/rename",
                query_string={
                    "filename": "awholenewname",
                    "directory": other_notebook_directory,
                    "just_metadata": True,
                },
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            assert (
                response.json()["path"]
                == f"{other_notebook_directory}/awholenewname.ipynb"
            )

            data = await receive_json(websocket, msg_types=["metadata"])
            metadata = data["metadata"]
            assert resolve(metadata["jupyter_d1"]["path"]) == resolve(
                f"{other_notebook_directory}/awholenewname.ipynb"
            )
            assert metadata["jupyter_d1"]["name"] == "awholenewname"

            assert not os.path.exists(
                f"{other_notebook_directory}/awholenewname.ipynb"
            )
            assert os.path.exists(f"{settings.ROOT_DIR}/simple.ipynb")

    @pytest.mark.asyncio
    async def test_save_as(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, filename="simple.ipynb"
        )

        assert os.path.exists(f"{settings.ROOT_DIR}/simple.ipynb")
        assert not os.path.exists(f"{settings.ROOT_DIR}/awholenewname.ipynb")

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            response = await client.patch(
                f"/notebooks/{uuid}/save_as",
                query_string={"filename": "awholenewname"},
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            assert (
                response.json()["path"]
                == f"{settings.ROOT_DIR}/awholenewname.ipynb"
            )

            data = await receive_json(websocket, msg_types=["metadata"])
            metadata = data["metadata"]
            assert (
                metadata["jupyter_d1"]["path"]
                == f"{settings.ROOT_DIR}/awholenewname.ipynb"
            )
            assert metadata["jupyter_d1"]["name"] == "awholenewname"
            assert metadata["jupyter_d1"]["uuid"] == uuid

            assert os.path.exists(f"{settings.ROOT_DIR}/awholenewname.ipynb")
            assert os.path.exists(f"{settings.ROOT_DIR}/simple.ipynb")

            response = await client.get(
                f"/notebooks/{uuid}", headers=superuser_token_headers
            )
            resp_json = response.json()["notebook"]
            assert (
                resp_json["metadata"]["jupyter_d1"]["name"] == "awholenewname"
            )
            assert resp_json["metadata"]["jupyter_d1"]["uuid"] == uuid

    @pytest.mark.asyncio
    async def test_save_as_different_directory(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        other_notebook_directory: str,
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, filename="simple.ipynb"
        )

        assert os.path.exists(f"{settings.ROOT_DIR}/simple.ipynb")
        assert not os.path.exists(
            f"{other_notebook_directory}/awholenewname.ipynb"
        )

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            response = await client.patch(
                f"/notebooks/{uuid}/save_as",
                query_string={
                    "filename": "awholenewname",
                    "directory": other_notebook_directory,
                },
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            assert (
                response.json()["path"]
                == f"{other_notebook_directory}/awholenewname.ipynb"
            )

            data = await receive_json(websocket, msg_types=["metadata"])
            metadata = data["metadata"]
            assert resolve(metadata["jupyter_d1"]["path"]) == resolve(
                f"{other_notebook_directory}/awholenewname.ipynb"
            )
            assert metadata["jupyter_d1"]["name"] == "awholenewname"

            assert os.path.exists(
                f"{other_notebook_directory}/awholenewname.ipynb"
            )
            assert os.path.exists(f"{settings.ROOT_DIR}/simple.ipynb")

    @pytest.mark.asyncio
    async def test_save_as_file_exists(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        other_notebook_directory: str,
    ):
        """Fail if file exists unless overwrite param is set to true"""
        uuid = await upload_notebook(
            client, superuser_token_headers, filename="simple.ipynb"
        )

        with open(f"{other_notebook_directory}/awholenewname.ipynb", "w") as f:
            f.write("some text here")

        assert os.path.exists(f"{settings.ROOT_DIR}/simple.ipynb")
        assert os.path.exists(
            f"{other_notebook_directory}/awholenewname.ipynb"
        )

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            response = await client.patch(
                f"/notebooks/{uuid}/save_as",
                query_string={
                    "filename": "awholenewname",
                    "directory": other_notebook_directory,
                },
                headers=superuser_token_headers,
            )
            assert response.status_code == 400
            assert response.json()["detail"] == f"File already exists"

            response = await client.patch(
                f"/notebooks/{uuid}/save_as",
                query_string={
                    "filename": "awholenewname",
                    "directory": other_notebook_directory,
                    "overwrite": True,
                },
                headers=superuser_token_headers,
            )
            assert response.status_code == 200
            assert (
                response.json()["path"]
                == f"{other_notebook_directory}/awholenewname.ipynb"
            )

            data = await receive_json(websocket, msg_types=["metadata"])
            metadata = data["metadata"]
            assert resolve(metadata["jupyter_d1"]["path"]) == resolve(
                f"{other_notebook_directory}/awholenewname.ipynb"
            )
            assert metadata["jupyter_d1"]["name"] == "awholenewname"

            assert os.path.exists(
                f"{other_notebook_directory}/awholenewname.ipynb"
            )
            assert os.path.exists(f"{settings.ROOT_DIR}/simple.ipynb")

        with open(f"{other_notebook_directory}/awholenewname.ipynb", "r") as f:
            assert f.read() != "some text here"


@pytest.mark.usefixtures("clear_notebooks", "clear_notebook_directory")
class TestD1Commands:
    async def do_test_d1_notify(
        self,
        cell_content: str,
        notifications: List[Dict[str, str]],
        remaining_stdout: str,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        mocker: MockFixture,
        msg_count=4,
        update_count=2,
    ):
        execute_d1_notify = mocker.patch(
            "jupyter_d1.storage.notebook_manager.execute_d1_notify"
        )

        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == 'print("Larry the Llama")'

        cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]
        assert cells[1]["execution_count"] is None

        body = {"source": cell_content}
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=body,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            data = await receive_json(websocket, msg_types=["cell_update"])
            assert len(data["cell_update"]) == 1
            cell_data = data["cell_update"][0]
            d1_metadata = cell_data["metadata"]["jupyter_d1"]
            assert d1_metadata["execution_state"] == "pending"
            assert d1_metadata["uuid"] == cell_uuid
            assert cell_data["execution_count"] is None
            assert len(cell_data["outputs"]) == 0

            received_info = {
                "received_cell_update_count": 0,
                "received_cell_execution": False,
                "received_vars": False,
            }

            async def receive_cell_update(data):
                cell_update = data["cell_update"]
                assert len(cell_update) == 1
                cell_d1_data = cell_update[0]["metadata"]["jupyter_d1"]
                assert cell_d1_data["uuid"] == cell_uuid
                if received_info["received_cell_update_count"] == 0:
                    assert cell_d1_data["execution_state"] == "busy"
                    assert (
                        cell_update[0]["execution_count"] is None
                        or cell_update[0]["execution_count"] == 1
                    )
                else:
                    # If execution_count is None, then this should be the
                    # equivalent of the old cell_stream message where the
                    # exec_state is still busy.
                    # Once the execution_count updates, the cell should be
                    # idle.
                    if cell_update[0]["execution_count"] is not None:
                        assert cell_update[0]["execution_count"] == 1
                        assert cell_d1_data["execution_state"] == "idle"
                    else:
                        assert cell_d1_data["execution_state"] == "busy"
                received_info["received_cell_update_count"] += 1

            async def receive_cell_execution(data):
                cell_exec = data["cell_execution_reply"]
                assert cell_exec["cell_id"] == cell_uuid
                assert cell_exec["execution_count"] == 1
                assert len(cell_exec["parent_id"]) in msg_id_lengths
                received_info["received_cell_execution"] = True

            msg_types = [
                "cell_update",
                "cell_execution_reply",
                "vars",
            ]
            for i in range(msg_count):
                data = await receive_json(websocket, 20, msg_types=msg_types)
                if "cell_update" in data:
                    await receive_cell_update(data)
                if "cell_execution_reply" in data:
                    await receive_cell_execution(data)
                if "vars" in data:
                    received_info["received_vars"] = True

            assert received_info["received_cell_update_count"] == update_count
            assert received_info["received_cell_execution"]
            assert received_info["received_vars"]

            execute_d1_notify.assert_has_calls(
                [
                    call(note["title"], note["message"])
                    for note in notifications
                ]
            )

    @pytest.mark.asyncio
    async def test_d1_notify(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        mocker: MockFixture,
    ):
        cell_content = (
            'print("___callisto_d1_command___{'
            '\\"command_type\\":\\"notify\\",'
            '\\"title\\":\\"atitle\\",'
            '\\"message\\":\\"test6e4\\"}___callisto_d1_command___", '
            ' end="")'
        )
        notifications = [{"title": "atitle", "message": "test6e4"}]
        await self.do_test_d1_notify(
            cell_content,
            notifications,
            "",
            client,
            superuser_token_headers,
            mocker,
        )

    @pytest.mark.asyncio
    async def test_d1_notify_incomplete(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        mocker: MockFixture,
    ):
        cell_content = (
            'print("ruh___callisto_d1_command___{'
            '\\"command_type\\":\\"notify\\",'
            '\\"title\\":\\"atitle\\",'
            '\\"message\\":\\"test6e4\\"}___callisto_d1_command___mori'
            '___callisto_d1_command___jjuo", '
            ' end="")'
        )
        notifications = [{"title": "atitle", "message": "test6e4"}]
        await self.do_test_d1_notify(
            cell_content,
            notifications,
            "ruhmorijjuo",
            client,
            superuser_token_headers,
            mocker,
            msg_count=5,
            update_count=3,
        )

    @pytest.mark.asyncio
    async def test_d1_notify_invalid_command(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        mocker: MockFixture,
    ):
        cell_content = (
            'print("___callisto_d1_command___{'
            '\\"command_type\\":\\"notify\\",'
            '\\"title\\":\\"atitle\\",'
            '\\"message\\":\\"test6e4\\"}___callisto_d1_command___mori'
            "___callisto_d1_command___{jjuo}___callisto_d1_command___"
            'whey", '
            ' end="")'
        )
        notifications = [{"title": "atitle", "message": "test6e4"}]
        await self.do_test_d1_notify(
            cell_content,
            notifications,
            "moriwhey",
            client,
            superuser_token_headers,
            mocker,
            msg_count=5,
            update_count=3,
        )


@pytest.mark.usefixtures(
    "clear_notebooks", "clear_notebook_directory", "enable_cell_update_patches"
)
class TestD1CommandsCellUpdatePatches:
    """
    Test the cell patches feature, turned on by setting the
    CELL_UPDATE_PATCHES flag to true.

    Most of these test scenarios are the tests that fail in the
    TestD1Commands class above when the CELL_UPDATE_PATCHES
    flag is True. When CELL_UPDATE_PATCHES is eventually default True,
    replace the corresponding tests in TestD1Commands with these tests
    """

    async def do_test_d1_notify(
        self,
        cell_content: str,
        notifications: List[Dict[str, str]],
        remaining_stdout: str,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        mocker: MockFixture,
        ututils: TestCase,
    ):
        execute_d1_notify = mocker.patch(
            "jupyter_d1.storage.notebook_manager.execute_d1_notify"
        )

        uuid = await upload_notebook(
            client, superuser_token_headers, "simple.ipynb"
        )

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]
        assert cells[1]["source"] == 'print("Larry the Llama")'

        cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]
        assert cells[1]["execution_count"] is None

        body = {"source": cell_content}
        response = await client.patch(
            f"/notebooks/{uuid}/cells/{cell_uuid}",
            json=body,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            msgs = await collect_websocket_messages(websocket, timeout=10)

            cell_exec_replies = filter_websocket_collection(
                msgs, "cell_execution_reply"
            )
            cell_update_patches = filter_websocket_collection(
                msgs, "cell_update_patch"
            )
            vars_msgs = filter_websocket_collection(msgs, "vars")

            data = cell_exec_replies.pop(0)
            cell_exec = data["cell_execution_reply"]
            assert cell_exec["cell_id"] == cell_uuid
            assert cell_exec["execution_count"] == 1
            assert len(cell_exec["parent_id"]) in msg_id_lengths

            data = cell_update_patches.pop(0)
            assert data["cell_update_patch"]["cell_id"] == cell_uuid
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "pending",
                    },
                    {"op": "remove", "path": "/outputs/0"},
                ],
            )

            data = cell_update_patches.pop(0)
            assert data["cell_update_patch"]["cell_id"] == cell_uuid
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "busy",
                    },
                ],
            )

            if len(remaining_stdout) > 0:
                data = cell_update_patches.pop(0)
                assert data["cell_update_patch"]["cell_id"] == cell_uuid
                ututils.assertCountEqual(
                    data["cell_update_patch"]["patch"],
                    [
                        {
                            "op": "add",
                            "path": "/outputs/0",
                            "value": {
                                "output_type": "stream",
                                "name": "stdout",
                                "text": [remaining_stdout],
                            },
                        },
                    ],
                )
            data = cell_update_patches.pop(0)
            assert data["cell_update_patch"]["cell_id"] == cell_uuid
            ututils.assertCountEqual(
                data["cell_update_patch"]["patch"],
                [
                    {
                        "op": "replace",
                        "path": "/metadata/jupyter_d1/execution_state",
                        "value": "idle",
                    },
                    {"op": "replace", "path": "/execution_count", "value": 1},
                ],
            )
            assert len(cell_update_patches) == 0

            assert len(vars_msgs) == 1

            execute_d1_notify.assert_has_calls(
                [
                    call(note["title"], note["message"])
                    for note in notifications
                ]
            )

    @pytest.mark.asyncio
    async def test_d1_notify(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        mocker: MockFixture,
        ututils: TestCase,
    ):
        cell_content = (
            'print("___callisto_d1_command___{'
            '\\"command_type\\":\\"notify\\",'
            '\\"title\\":\\"atitle\\",'
            '\\"message\\":\\"test6e4\\"}___callisto_d1_command___", '
            ' end="")'
        )
        notifications = [{"title": "atitle", "message": "test6e4"}]
        await self.do_test_d1_notify(
            cell_content,
            notifications,
            "",
            client,
            superuser_token_headers,
            mocker,
            ututils,
        )

    @pytest.mark.asyncio
    async def test_d1_notify_incomplete(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        mocker: MockFixture,
        ututils: TestCase,
    ):
        cell_content = (
            'print("ruh___callisto_d1_command___{'
            '\\"command_type\\":\\"notify\\",'
            '\\"title\\":\\"atitle\\",'
            '\\"message\\":\\"test6e4\\"}___callisto_d1_command___mori'
            '___callisto_d1_command___jjuo", '
            ' end="")'
        )
        notifications = [{"title": "atitle", "message": "test6e4"}]
        await self.do_test_d1_notify(
            cell_content,
            notifications,
            "ruhmorijjuo\n",
            client,
            superuser_token_headers,
            mocker,
            ututils,
        )

    @pytest.mark.asyncio
    async def test_d1_notify_invalid_command(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
        mocker: MockFixture,
        ututils: TestCase,
    ):
        cell_content = (
            'print("___callisto_d1_command___{'
            '\\"command_type\\":\\"notify\\",'
            '\\"title\\":\\"atitle\\",'
            '\\"message\\":\\"test6e4\\"}___callisto_d1_command___mori'
            "___callisto_d1_command___{jjuo}___callisto_d1_command___"
            'whey", '
            ' end="")'
        )
        notifications = [{"title": "atitle", "message": "test6e4"}]
        await self.do_test_d1_notify(
            cell_content,
            notifications,
            "moriwhey\n",
            client,
            superuser_token_headers,
            mocker,
            ututils,
        )


@pytest.mark.usefixtures("clear_notebooks", "clear_notebook_directory")
class TestNotebooksWebSocket:
    async def get_notebooks_event(self, websocket):
        for i in range(5):
            data = await receive_json(websocket)
            if "notebooks" in data:
                break
        return data

    @pytest.mark.asyncio
    async def test_notebooks_updates(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):

        async with client.websocket_connect(
            f"/server/ws", headers=superuser_token_headers
        ) as websocket:

            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            uuid = await upload_notebook(client, superuser_token_headers)

            data = await wait_for_event(websocket, "notebooks", tries=100)
            assert len(data["notebooks"]) == 1
            assert data["notebooks"][0]["uuid"] == uuid
            assert data["notebooks"][0]["name"] == "simple"

            uuid2 = await upload_notebook(
                client,
                superuser_token_headers,
                filename="stateful_simple.ipynb",
            )
            data = await wait_for_event(websocket, "notebooks", tries=100)
            assert len(data["notebooks"]) == 2
            assert data["notebooks"][0]["uuid"] == uuid
            assert data["notebooks"][0]["name"] == "simple"
            assert data["notebooks"][1]["uuid"] == uuid2
            assert data["notebooks"][1]["name"] == "stateful_simple"

            response = await client.delete(
                f"/notebooks/{uuid}", headers=superuser_token_headers
            )
            assert response.status_code == 204
            data = await wait_for_event(websocket, "notebooks", tries=100)
            assert len(data["notebooks"]) == 1
            assert data["notebooks"][0]["uuid"] == uuid2
            assert data["notebooks"][0]["name"] == "stateful_simple"

            response = await client.delete(
                "/notebooks", headers=superuser_token_headers
            )
            assert response.status_code == 204
            data = await wait_for_event(websocket, "notebooks", tries=100)
            assert len(data["notebooks"]) == 0


class TestClientCommands:
    @pytest.mark.asyncio
    async def test_client_commands(
        self,
        client: TestClient,
        superuser_token_headers: Dict[str, str],
    ):
        """
        Send client commands on stdout
        These should get forwarded through the websocket
        """

        uuid = await upload_notebook(
            client, superuser_token_headers, "client_commands.ipynb"
        )

        # get an existing cell
        response = await client.get(
            f"/notebooks/{uuid}/cells", headers=superuser_token_headers
        )
        assert response.status_code == 200
        cells = response.json()["cells"]

        async with client.websocket_connect(
            f"/notebooks/{uuid}/ws/notebook", headers=superuser_token_headers
        ) as websocket:
            await asyncio.sleep(WEBSOCKET_SLEEP_TIME)

            # Execute first cell
            cell_uuid = cells[1]["metadata"]["jupyter_d1"]["uuid"]
            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            msgs = await collect_websocket_messages(websocket, timeout=10)

            commands = filter_websocket_collection(msgs, "client_command_url")
            assert len(commands) == 1
            assert commands[0] == {
                "client_command_url": {
                    "command": "com.callistoapp.callisto://ui/data-explorer"
                }
            }

            # Execute second cell
            cell_uuid = cells[2]["metadata"]["jupyter_d1"]["uuid"]
            response = await client.get(
                f"/notebooks/{uuid}/cells/{cell_uuid}/execute",
                headers=superuser_token_headers,
            )
            assert response.status_code == 200

            msgs = await collect_websocket_messages(websocket, timeout=10)

            commands = filter_websocket_collection(msgs, "client_command_url")
            assert len(commands) == 1
            assert commands[0] == {"client_command_url": {"command": "🐌±🦖⋍🎩"}}
