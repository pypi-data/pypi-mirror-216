import asyncio
from typing import Dict
from uuid import uuid4

import pytest  # type: ignore

from .D1TestClient import TestClient
from .test_notebooks_websocket import upload_notebook
# from .async_fixtures import client, superuser_token_headers
from .utils import collect_websocket_messages, receive_json

WEBSOCKET_RECEIVE_TIMEOUT = 7


@pytest.mark.usefixtures("clear_bg_kernel_runner")
class TestPipDependenciesWebSocket:
    @pytest.mark.asyncio
    async def test_pip_list(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        async with client.websocket_connect(
            f"/dependencies/ws", headers=superuser_token_headers
        ) as websocket:
            request_id = str(uuid4())
            msg = {
                "command": "pip",
                "subcommand": "list",
                "args": [],
                "request_id": str(request_id),
            }
            await websocket.send_json(msg)

            data = await receive_json(websocket)
            assert data["status"] == "update"
            assert data["request_id"] == request_id
            assert data["stdout"] == (
                '\n%%sh -s "$python_executable"\n$1 -m pip list'
                + " --disable-pip-version-check --format json\n"
            )

            data = await receive_json(websocket)
            assert data["status"] == "received"
            assert data["request_id"] == request_id

            data = await receive_json(websocket)
            assert data["status"] == "complete", data
            assert data["request_id"] == request_id
            assert (
                len(
                    [
                        dep
                        for dep in data["payload"]["data"]
                        if dep["name"] == "fastapi"
                    ]
                )
                > 0
            )
            assert (
                len(
                    [
                        dep
                        for dep in data["payload"]["data"]
                        if dep["name"] == "jupyter-client"
                    ]
                )
                > 0
            )

            # Not expecting any more messages
            assert len(await collect_websocket_messages(websocket)) == 0

        # await asyncio.sleep(65)

        # from ..storage import bg_kernel_runner
        # from ..dependency import dependency_managers
        # assert len(bg_kernel_runner.kernels.items()) == 0
        # assert len(bg_kernel_runner.kernel_connections) == 0
        # assert len(dependency_managers.items()) == 1

    @pytest.mark.asyncio
    async def test_pip_list_fail(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        async with client.websocket_connect(
            f"/dependencies/ws", headers=superuser_token_headers
        ) as websocket:
            request_id = str(uuid4())
            msg = {
                "command": "pip",
                "subcommand": "list",
                "args": ["--hocups"],
                "request_id": str(request_id),
            }
            await websocket.send_json(msg)

            msgs = await collect_websocket_messages(
                websocket, WEBSOCKET_RECEIVE_TIMEOUT
            )

            assert len(msgs) > 4

            assert msgs[0]["status"] == "update"
            assert msgs[0]["request_id"] == request_id
            assert msgs[0]["stdout"] == (
                '\n%%sh -s "$python_executable"\n$1 -m pip list'
                + " --disable-pip-version-check --format json --hocups\n"
            )

            assert msgs[1]["status"] == "received"
            assert msgs[1]["request_id"] == request_id

            for i in range(2, len(msgs) - 2):
                assert msgs[i]["status"] == "update"
                assert msgs[i]["request_id"] == request_id
                assert msgs[i]["stderr"] is not None
                assert msgs[i]["stdout"] is None

            assert msgs[-1]["status"] == "failed"
            assert msgs[-1]["request_id"] == request_id
            assert msgs[-1]["info"] is not None

    @pytest.mark.asyncio
    async def test_pip_install(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        async with client.websocket_connect(
            f"/dependencies/ws", headers=superuser_token_headers
        ) as websocket:
            request_id = str(uuid4())
            msg = {
                "command": "pip",
                "subcommand": "install",
                "args": ["jupyter_d1/tests/dummy_pip_package"],
                "request_id": str(request_id),
            }
            await websocket.send_json(msg)

            msgs = await collect_websocket_messages(
                websocket, WEBSOCKET_RECEIVE_TIMEOUT
            )

            assert len(msgs) > 3

            assert msgs[0]["status"] == "update"
            assert msgs[0]["request_id"] == request_id
            assert msgs[0]["stdout"] == (
                '\n%%sh -s "$python_executable"\n$1 -m pip install'
                + " jupyter_d1/tests/dummy_pip_package\n"
            )

            assert msgs[1]["status"] == "received"
            assert msgs[1]["request_id"] == request_id

            for i in range(2, len(msgs) - 2):
                assert msgs[i]["status"] == "update"
                assert msgs[i]["request_id"] == request_id
                assert msgs[i]["stderr"] is None
                assert msgs[i]["stdout"] is not None

            assert msgs[-1]["status"] == "complete"
            assert msgs[-1]["request_id"] == request_id
            assert msgs[-1]["payload"] is None

    @pytest.mark.asyncio
    async def test_pip_install_error(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        async with client.websocket_connect(
            f"/dependencies/ws", headers=superuser_token_headers
        ) as websocket:
            request_id = str(uuid4())
            msg = {
                "command": "pip",
                "subcommand": "install",
                "args": ["jupyter_d1/tests/doesntexist"],
                "request_id": str(request_id),
            }
            await websocket.send_json(msg)

            msgs = await collect_websocket_messages(
                websocket, WEBSOCKET_RECEIVE_TIMEOUT
            )

            assert len(msgs) > 3

            assert msgs[0]["status"] == "update"
            assert msgs[0]["request_id"] == request_id
            assert msgs[0]["stdout"] == (
                '\n%%sh -s "$python_executable"\n$1 -m pip install'
                + " jupyter_d1/tests/doesntexist\n"
            )

            assert msgs[1]["status"] == "received"
            assert msgs[1]["request_id"] == request_id

            for i in range(2, len(msgs) - 2):
                assert msgs[i]["status"] == "update"
                assert msgs[i]["request_id"] == request_id
                assert msgs[i]["stderr"] is not None
                assert msgs[i]["stdout"] is None

            assert msgs[-1]["status"] == "failed"
            assert msgs[-1]["request_id"] == request_id
            assert msgs[-1]["info"] is not None

    @pytest.mark.asyncio
    async def test_pip_uninstall(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        async with client.websocket_connect(
            f"/dependencies/ws", headers=superuser_token_headers
        ) as websocket:
            await self.test_pip_install(client, superuser_token_headers)

            request_id = str(uuid4())
            msg = {
                "command": "pip",
                "subcommand": "uninstall",
                "args": ["dummy_test"],
                "request_id": str(request_id),
            }
            await websocket.send_json(msg)

            msgs = await collect_websocket_messages(
                websocket, WEBSOCKET_RECEIVE_TIMEOUT
            )

            assert len(msgs) > 4

            assert msgs[0]["status"] == "update"
            assert msgs[0]["request_id"] == request_id
            assert (
                msgs[0]["stdout"]
                == '\n%%sh -s "$python_executable"\n$1 -m pip uninstall -y dummy_test\n'
            )

            assert msgs[1]["status"] == "received"
            assert msgs[1]["request_id"] == request_id

            for i in range(2, len(msgs) - 2):
                assert msgs[i]["status"] == "update"
                assert msgs[i]["request_id"] == request_id
                assert msgs[i]["stderr"] is None
                if i == len(msgs) - 2:
                    assert "Successfully uninstalled" in msgs[i]["stdout"]
                else:
                    assert msgs[i]["stdout"] is not None

            assert msgs[-1]["status"] == "complete"
            assert msgs[-1]["request_id"] == request_id
            assert msgs[-1]["payload"] is None

    @pytest.mark.asyncio
    async def test_unknown_command(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        async with client.websocket_connect(
            f"/dependencies/ws", headers=superuser_token_headers
        ) as websocket:
            await self.test_pip_install(client, superuser_token_headers)

            request_id = str(uuid4())
            msg = {
                "command": "pip",
                "subcommand": "--version",
                "args": [],
                "request_id": str(request_id),
            }
            await websocket.send_json(msg)

            msgs = await collect_websocket_messages(
                websocket, WEBSOCKET_RECEIVE_TIMEOUT
            )

            assert len(msgs) == 4

            assert msgs[0]["status"] == "update"
            assert msgs[0]["request_id"] == request_id
            assert (
                msgs[0]["stdout"]
                == '\n%%sh -s "$python_executable"\n$1 -m pip --version\n'
            )

            assert msgs[1]["status"] == "received"
            assert msgs[1]["request_id"] == request_id

            assert msgs[2]["status"] == "update"
            assert msgs[2]["request_id"] == request_id
            assert msgs[2]["stderr"] is None
            assert "pip" in msgs[2]["stdout"]

            assert msgs[3]["status"] == "complete"
            assert msgs[3]["request_id"] == request_id
            assert msgs[3]["payload"] is None

    @pytest.mark.asyncio
    async def test_multiple_connections(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        """
        Two separate connections should use the same kernel and receive
        responses for only their requests
        """
        async with client.websocket_connect(
            f"/dependencies/ws", headers=superuser_token_headers
        ) as websocket:
            async with client.websocket_connect(
                f"/dependencies/ws", headers=superuser_token_headers
            ) as websocket2:
                from ..dependency import dependency_managers
                from ..storage import bg_kernel_runner

                assert len(bg_kernel_runner.kernels.items()) == 1
                assert len(bg_kernel_runner.kernel_connections) == 1
                assert (
                    len(list(bg_kernel_runner.kernel_connections.values())[0])
                    == 2
                )
                assert len(dependency_managers.items()) == 1

                request_id = str(uuid4())
                request_id2 = str(uuid4())
                msg = {
                    "command": "pip",
                    "subcommand": "list",
                    "args": [],
                    "request_id": str(request_id),
                }
                msg2 = {
                    "command": "pip",
                    "subcommand": "install",
                    "args": ["jupyter_d1/tests/dummy_pip_package"],
                    "request_id": str(request_id2),
                }
                await websocket.send_json(msg)
                await websocket2.send_json(msg2)

                msgs, msgs2 = await asyncio.gather(
                    collect_websocket_messages(
                        websocket, WEBSOCKET_RECEIVE_TIMEOUT
                    ),
                    collect_websocket_messages(
                        websocket2, WEBSOCKET_RECEIVE_TIMEOUT
                    ),
                )

                assert len(msgs) == 3
                assert len(msgs2) > 4

                assert msgs[0]["status"] == "update"
                assert msgs[0]["request_id"] == request_id
                assert msgs[0]["stdout"] == (
                    '\n%%sh -s "$python_executable"\n$1 -m pip list'
                    + " --disable-pip-version-check --format json\n"
                )

                assert msgs[1]["status"] == "received"
                assert msgs[1]["request_id"] == request_id

                assert msgs[2]["status"] == "complete"
                assert msgs[2]["request_id"] == request_id
                assert (
                    len(
                        [
                            dep
                            for dep in msgs[2]["payload"]["data"]
                            if dep["name"] == "fastapi"
                        ]
                    )
                    > 0
                )
                assert (
                    len(
                        [
                            dep
                            for dep in msgs[2]["payload"]["data"]
                            if dep["name"] == "jupyter-client"
                        ]
                    )
                    > 0
                )

                assert msgs2[0]["status"] == "update"
                assert msgs2[0]["request_id"] == request_id2
                assert msgs2[0]["stdout"] == (
                    '\n%%sh -s "$python_executable"\n$1 -m pip install'
                    + " jupyter_d1/tests/dummy_pip_package\n"
                )

                assert msgs2[1]["status"] == "received"
                assert msgs2[1]["request_id"] == request_id2

                for i in range(2, len(msgs2) - 2):
                    assert msgs2[i]["status"] == "update"
                    assert msgs2[i]["request_id"] == request_id2
                    assert msgs2[i]["stderr"] is None
                    assert msgs2[i]["stdout"] is not None

                assert msgs2[-1]["status"] == "complete"
                assert msgs2[-1]["request_id"] == request_id2
                assert msgs2[-1]["payload"] is None


@pytest.mark.usefixtures(
    "clear_notebooks", "clear_notebook_directory", "clear_bg_kernel_runner"
)
class TestRDependenciesWebSocket:
    @pytest.mark.asyncio
    async def test_rip_list(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple_r.ipynb"
        )

        async with client.websocket_connect(
            f"/dependencies/ws?notebook_uuid={uuid}",
            headers=superuser_token_headers,
        ) as websocket:
            request_id = str(uuid4())
            msg = {
                "command": "rip",
                "subcommand": "list",
                "args": [],
                "request_id": str(request_id),
            }
            await websocket.send_json(msg)

            data = await receive_json(websocket)
            assert data["status"] == "update"
            assert data["request_id"] == request_id
            print(data["stdout"])
            assert (
                data["stdout"]
                == "\n    my_packages <- as.data.frame(installed.packages()[ , "
                + 'c(1, 3:4)])\n\n    json <- "["\n    for(i in 1:nrow(my_packages))'
                + " {       # for-loop over rows\n      row <- my_packages[i,]\n      "
                + 'line <- sprintf("{\\"name\\": \\"%s\\", \\"version\\": \\"%s\\"}",'
                + " row[[1]], row[[2]])\n      json <- paste(json, line)\n      "
                + 'if (i != nrow(my_packages)) {\n        json <- paste(json, ",")\n'
                + '      }\n      json <- paste(json, "\\n")\n    }\n    json <- '
                + 'paste(json, "]\\n")\n\n    cat(json)\n    \n'
            )

            data = await receive_json(websocket)
            assert data["status"] == "received"
            assert data["request_id"] == request_id

            data = await receive_json(
                websocket, timeout=WEBSOCKET_RECEIVE_TIMEOUT * 2
            )

            assert data["status"] == "complete", data
            assert data["request_id"] == request_id
            assert (
                len(
                    [
                        dep
                        for dep in data["payload"]["data"]
                        if dep["name"] == "jsonlite"
                    ]
                )
                > 0
            )
            assert (
                len(
                    [
                        dep
                        for dep in data["payload"]["data"]
                        if dep["name"] == "IRkernel"
                    ]
                )
                > 0
            )

            # Not expecting any more messages
            assert len(await collect_websocket_messages(websocket)) == 0

        # await asyncio.sleep(65)

        # from ..storage import bg_kernel_runner
        # from ..dependency import dependency_managers
        # assert len(bg_kernel_runner.kernels.items()) == 0
        # assert len(bg_kernel_runner.kernel_connections) == 0
        # assert len(dependency_managers.items()) == 1

    # async def test_rip_list_fail(
    # async def test_rip_install_error(
    # WJL -- Can't test either of these failure modes b/c they don't really fail
    # The list method ignores arguments, so it can't really screw up
    # at least from the client side.
    # And the install never fails. If you give it a bogus package, it just
    # says it's not availble for this version

    @pytest.mark.asyncio
    async def test_rip_install_uninstall(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple_r.ipynb"
        )

        async with client.websocket_connect(
            f"/dependencies/ws?notebook_uuid={uuid}",
            headers=superuser_token_headers,
        ) as websocket:
            request_id = str(uuid4())
            msg = {
                "command": "rip",
                "subcommand": "install",
                "args": ["jupyter_d1/tests/D1Dummy", "--local"],
                "request_id": str(request_id),
            }
            await websocket.send_json(msg)

            msgs = await collect_websocket_messages(
                websocket, WEBSOCKET_RECEIVE_TIMEOUT
            )

            assert len(msgs) == 3

            assert msgs[0]["status"] == "update"
            assert msgs[0]["request_id"] == request_id
            assert msgs[0]["stdout"] == (
                '\n    install.packages(c("jupyter_d1/tests/D1Dummy"), repos=NULL,'
                + " type='source')\n    \n"
            )

            assert msgs[1]["status"] == "received"
            assert msgs[1]["request_id"] == request_id

            assert msgs[2]["status"] == "complete"
            assert msgs[2]["request_id"] == request_id
            assert msgs[2]["payload"] is None

            request_id = str(uuid4())
            msg = {
                "command": "rip",
                "subcommand": "uninstall",
                "args": ["D1Dummy"],
                "request_id": str(request_id),
            }
            await websocket.send_json(msg)

            msgs = await collect_websocket_messages(
                websocket, WEBSOCKET_RECEIVE_TIMEOUT
            )

            assert len(msgs) > 3

            assert msgs[0]["status"] == "update"
            assert msgs[0]["request_id"] == request_id
            assert msgs[0]["stdout"] == (
                '\n    remove.packages(c("D1Dummy"))\n    \n'
            )

            assert msgs[1]["status"] == "received"
            assert msgs[1]["request_id"] == request_id

            assert msgs[-1]["status"] == "complete"
            assert msgs[-1]["request_id"] == request_id
            assert msgs[-1]["payload"] is None

    @pytest.mark.asyncio
    async def test_rip_unknown_command(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        uuid = await upload_notebook(
            client, superuser_token_headers, "simple_r.ipynb"
        )

        async with client.websocket_connect(
            f"/dependencies/ws?notebook_uuid={uuid}",
            headers=superuser_token_headers,
        ) as websocket:

            request_id = str(uuid4())
            msg = {
                "command": "rip",
                "subcommand": "hello_world",
                "args": [],
                "request_id": str(request_id),
            }
            await websocket.send_json(msg)

            msgs = await collect_websocket_messages(
                websocket, WEBSOCKET_RECEIVE_TIMEOUT * 3
            )

            assert len(msgs) == 4

            assert msgs[0]["status"] == "update"
            assert msgs[0]["request_id"] == request_id
            assert msgs[0]["stdout"] == (
                "warning('unknown command: rip hello_world []')\n"
            )

            assert msgs[1]["status"] == "received"
            assert msgs[1]["request_id"] == request_id

            assert msgs[2]["status"] == "update"
            assert msgs[2]["request_id"] == request_id
            assert msgs[2]["stdout"] is None
            assert "unknown command: rip hello_world" in msgs[2]["stderr"]

            assert msgs[3]["status"] == "complete"
            assert msgs[3]["request_id"] == request_id
            assert msgs[3]["payload"] is None
