from enum import Enum

import requests

from jupyter_d1.settings import settings


class D1CommandType(str, Enum):
    NOTIFY = "notify"
    HANDLE_IMPORT_ERROR = "handle_import_error"
    CLIENT_COMMAND_URL = "client_command_url"


def execute_d1_notify(title: str, message: str):
    if settings.PUSH_NOTE_SECRET_KEY:
        requests.post(
            f"{settings.MOTHERSHIP_URL}/work_nodes/{settings.WORK_NODE_ID}/push",
            json={
                "secret": settings.PUSH_NOTE_SECRET_KEY,
                "title": title,
                "message": message,
            },
            timeout=30,
        )
    else:
        requests.post(
            f"{settings.MOTHERSHIP_URL}/users/push",
            json={
                "title": title,
                "message": message,
            },
            headers={
                "Authorization": f"Bearer {settings.mothership_auth_token}"
            },
            timeout=30,
        )
