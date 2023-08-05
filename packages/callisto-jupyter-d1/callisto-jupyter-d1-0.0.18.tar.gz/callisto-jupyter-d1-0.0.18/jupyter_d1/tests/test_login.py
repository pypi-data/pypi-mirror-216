from typing import Dict

import pytest  # type: ignore

from .D1TestClient import TestClient


@pytest.mark.asyncio
async def test_get_access_token(client: TestClient) -> None:
    r = await client.get(
        f"/login/access-token", headers={"Authorization": "bogus"}
    )
    assert r.status_code == 401

    r = await client.get(f"/login/access-token")
    assert r.status_code == 401

    r = await client.get(
        f"/login/access-token", headers={"Authorization": "test9token_4"}
    )
    tokens = r.json()["token"]
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


@pytest.mark.asyncio
async def test_use_access_token(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = await client.post(
        f"/login/test-token",
        headers=superuser_token_headers,
    )
    result = r.json()["permission"]
    assert r.status_code == 200
    assert result["id"] == -1
    assert result["user_id"] == -1
    assert result["work_node_id"] == -1
    assert result["read_access"] is True
    assert result["write_access"] is True
