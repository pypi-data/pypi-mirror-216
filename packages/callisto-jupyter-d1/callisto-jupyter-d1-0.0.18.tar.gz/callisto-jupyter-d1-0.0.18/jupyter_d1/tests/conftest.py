import logging
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import AsyncGenerator, Dict, Generator

import pytest  # type: ignore
import pytest_asyncio
from pytest_mock import MockFixture  # type: ignore

from jupyter_d1 import app
from jupyter_d1.settings import settings

from ..logger import logger
from .D1TestClient import TestClient
from .utils import (
    get_permissionless_token_headers,
    get_readonly_token_headers,
    get_superuser_token_headers,
)

enable_logger_output = False
# enable_logger_output = True


@pytest_asyncio.fixture()
async def client() -> AsyncGenerator:
    async with TestClient(app) as c:
        yield c


@pytest_asyncio.fixture()
async def superuser_token_headers(client: TestClient) -> Dict[str, str]:
    return await get_superuser_token_headers(client)


@pytest.fixture()
def readonly_token_headers(client: TestClient) -> Dict[str, str]:
    return get_readonly_token_headers()


@pytest.fixture()
def permissionless_token_headers(client: TestClient) -> Dict[str, str]:
    return get_permissionless_token_headers()


@pytest_asyncio.fixture(scope="function")
async def clear_notebooks(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> AsyncGenerator:
    yield
    response = await client.delete(
        "/notebooks", headers=superuser_token_headers
    )
    assert response.status_code == 204
    response = await client.get("/notebooks", headers=superuser_token_headers)
    assert response.status_code == 200


@pytest.fixture(scope="function")
def clear_notebook_directory(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> Generator:
    root_path = Path(settings.ROOT_DIR)
    root_path.mkdir(parents=True, exist_ok=True)
    yield
    if "/tmp" in str(root_path.absolute()):
        for filename in os.listdir(root_path):
            file_path = os.path.join(root_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print("Failed to delete %s. Reason: %s" % (file_path, e))


@pytest.fixture(scope="function")
def other_notebook_directory() -> Generator:
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname


@pytest_asyncio.fixture(scope="function")
async def clear_bg_kernel_runner() -> AsyncGenerator:
    yield
    import jupyter_d1.storage as storage
    import jupyter_d1.dependency as dependency

    dependency.dependency_managers = {}
    await storage.bg_kernel_runner.clear()
    await storage.kmanager.shutdown_all()
    storage.kmanager.shutdown_warmups()


@pytest_asyncio.fixture
async def websocket_client() -> AsyncGenerator:
    async with TestClient(app) as c:
        yield c


@pytest.fixture()
def ututils() -> unittest.TestCase:
    """Unittest TestCase so we can use useful things like assertCountEquals"""
    return unittest.TestCase()


@pytest.fixture()
def enable_cell_update_patches(mocker: MockFixture):
    mock_setting = mocker.patch(
        "jupyter_d1.storage.notebook_manager.settings.CELL_UPDATE_PATCHES"
    )
    mock_setting.return_value = True
    mock_setting2 = mocker.patch(
        "jupyter_d1.routers.notebooks.settings.CELL_UPDATE_PATCHES",
    )
    mock_setting2.return_value = True


def pytest_sessionstart(session):

    if enable_logger_output:
        # Print out logging (visible with `pytest -s`)
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        ch.setFormatter(formatter)
        logger.addHandler(ch)
