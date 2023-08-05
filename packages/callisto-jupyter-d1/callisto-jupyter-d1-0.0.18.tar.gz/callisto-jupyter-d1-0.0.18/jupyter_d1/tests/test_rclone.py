from datetime import datetime, timedelta
from typing import Dict

import pytest  # type: ignore
from pytest_mock import MockFixture  # type: ignore

from jupyter_d1.settings import settings

from .D1TestClient import TestClient
from .utils import resolve, wait_for_event

pytestmark = pytest.mark.asyncio


async def test_rclone(
    client: TestClient,
    superuser_token_headers: Dict[str, str],
    mocker: MockFixture,
):
    mock_requests = mocker.patch("jupyter_d1.routers.rclone.requests")
    mock_requests.post().json.return_value = {"pldefe": "fj39499"}
    response = await client.post(
        "/rclone/config/dump", headers=superuser_token_headers
    )
    assert response.status_code == 200
    # print(response.json())
    assert response.json() == {"pldefe": "fj39499"}
    assert (
        mock_requests.post.call_args[0][0]
        == "http://127.0.0.1:5572/config/dump"
    )


async def test_rclone_query_params(
    client: TestClient,
    superuser_token_headers: Dict[str, str],
    mocker: MockFixture,
):
    mock_requests = mocker.patch("jupyter_d1.routers.rclone.requests")
    mock_requests.post().json.return_value = {"gg": "754d"}
    response = await client.post(
        "/rclone/config/get",
        headers=superuser_token_headers,
        params={"name": "gdrive"},
    )
    assert response.status_code == 200
    # print(response.json())
    assert response.json() == {"gg": "754d"}
    assert (
        mock_requests.post.call_args[0][0]
        == "http://127.0.0.1:5572/config/get"
    )
    assert dict(mock_requests.post.call_args[1]["params"]) == {
        "name": "gdrive"
    }


async def test_rclone_post_data(
    client: TestClient,
    superuser_token_headers: Dict[str, str],
    mocker: MockFixture,
):
    mock_requests = mocker.patch("jupyter_d1.routers.rclone.requests")
    mock_requests.post().json.return_value = {"polnd": "logkj"}
    superuser_token_headers["Content-Type"] = "application/json"
    response = await client.post(
        "/rclone/options/set",
        headers=superuser_token_headers,
        data='{"vfs": {"CacheMaxSize": 100}}',
    )
    assert response.status_code == 200
    # print(response.json())
    assert response.json() == {"polnd": "logkj"}
    # mock_requests.post.assert_called_once()
    # print(mock_requests.post.calls)
    assert (
        mock_requests.post.call_args[0][0]
        == "http://127.0.0.1:5572/options/set"
    )
    assert (
        mock_requests.post.call_args[1]["data"]
        == b'{"vfs": {"CacheMaxSize": 100}}'
    )


async def test_rclone_websocket(
    websocket_client: TestClient,
    superuser_token_headers: Dict[str, str],
    mocker: MockFixture,
):
    mock_requests = mocker.patch("jupyter_d1.routers.rclone.requests")
    mock_requests.post().json.return_value = {"polnd": "logkj"}

    async with websocket_client.websocket_connect(
        f"/server/ws", headers=superuser_token_headers
    ) as websocket:
        time = datetime.now()

        async def assert_stats():
            resp = await wait_for_event(websocket, "rclone_stats")
            assert resp == {"rclone_stats": {"polnd": "logkj"}}
            assert (
                time - datetime.now() - timedelta(seconds=3)
            ).microseconds < 1e6

        for i in range(3):
            await assert_stats()


async def test_update_data_remotes(
    websocket_client: TestClient,
    superuser_token_headers: Dict[str, str],
):
    response = await websocket_client.get(
        "/rclone/data_remotes/",
        headers=superuser_token_headers,
    )

    assert response.status_code == 200
    content = response.json()
    assert len(content["data_remotes"]) == 0

    async with websocket_client.websocket_connect(
        f"/server/ws", headers=superuser_token_headers
    ) as websocket:
        data_remotes_in = [
            {
                "id": 238,
                "name": "my goog drive",
                "remote_type": "Google Drive",
                "owner_id": 3,
                "organization_id": 12,
                "account_email": "jeb@deb.com",
                "account_name": "goobl drive",
                "last_modified": "2023-05-02 13:10:04.606728+00",
            },
            {
                "id": 240,
                "name": "a_bucket_of_things",
                "remote_type": "Dropbox",
                "owner_id": 4003,
                "organization_id": 9,
                "account_email": "admin@oakcity.io",
                "account_name": "admin",
                "last_modified": "2023-05-03 13:10:04.606728+00",
            },
        ]

        response = await websocket_client.patch(
            "/rclone/data_remotes/",
            json=data_remotes_in,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        data_remotes = [
            {
                "id": 238,
                "name": "my goog drive",
                "remote_type": "Google Drive",
                "owner_id": 3,
                "organization_id": 12,
                "account_email": "jeb@deb.com",
                "account_name": "goobl drive",
                "last_modified": "2023-05-02T13:10:04.606728+00:00",
                "path": resolve(settings.ROOT_DIR + "/data/my goog drive"),
            },
            {
                "id": 240,
                "name": "a_bucket_of_things",
                "remote_type": "Dropbox",
                "owner_id": 4003,
                "organization_id": 9,
                "account_email": "admin@oakcity.io",
                "account_name": "admin",
                "last_modified": "2023-05-03T13:10:04.606728+00:00",
                "path": resolve(
                    settings.ROOT_DIR + "/data/a_bucket_of_things"
                ),
            },
        ]

        resp = await wait_for_event(websocket, "data_remotes_update")
        assert resp == {"data_remotes_update": {"data_remotes": data_remotes}}

        response = await websocket_client.get(
            "/rclone/data_remotes/",
            headers=superuser_token_headers,
        )
        assert response.status_code == 200
        content = response.json()
        assert content["data_remotes"] == data_remotes

        # Patching with same data remotes shouldn't trigger websocket event
        response = await websocket_client.patch(
            "/rclone/data_remotes/",
            json=data_remotes_in,
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

        with pytest.raises(AssertionError):
            await wait_for_event(websocket, "data_remotes_update")

        response = await websocket_client.get(
            "/rclone/data_remotes/",
            headers=superuser_token_headers,
        )
        assert response.status_code == 200
        content = response.json()
        assert content["data_remotes"] == data_remotes
