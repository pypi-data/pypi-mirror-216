from .main import app  # noqa: F401
from .version import version as __version__  # noqa: F401

try:
    from . import uvicorn_worker  # noqa: F401
except Exception:
    pass

__all__ = ["app"]
