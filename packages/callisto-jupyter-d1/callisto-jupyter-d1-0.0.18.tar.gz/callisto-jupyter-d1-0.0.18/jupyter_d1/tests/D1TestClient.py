import base64
from typing import Any, Optional, Tuple

from async_asgi_testclient import TestClient as BaseTestClient
from async_asgi_testclient.response import Response


class TestClient(BaseTestClient):
    async def get(
        self, *args: Any, auth: Optional[Tuple[str, str]] = None, **kwargs: Any
    ) -> Response:
        """
        async_asgi_testclient is missing support for the `auth` parameter,
        so intercept it and add the headers manually before calling super()
        """

        if auth is not None:
            (user, password) = auth
            user_and_pass = f"{user}:{password}"
            auth_enc = base64.b64encode(f"{user_and_pass}".encode("utf-8"))
            auth_header = {
                "Authorization": f"Basic {auth_enc.decode('utf-8')}"
            }

            headers = {}
            if "headers" in kwargs.keys():
                headers = kwargs.pop("headers")
            headers.update(auth_header)

            kwargs["headers"] = headers

        return await super().get(*args, **kwargs)

    async def open(
        self, *args: Any, params: Optional[dict] = None, **kwargs: Any
    ) -> Response:
        """
        async_asgi_testclient is uses `query_string` instead of `params` (like
            requests), so intercept and rename
        """
        if params is not None:
            kwargs["query_string"] = params

        return await super().open(*args, **kwargs)
