from enum import Enum


class ExecutionState(str, Enum):
    pending = "pending"  # queued for execution
    busy = "busy"
    idle = "idle"
    starting = "starting"
    unknown = "unknown"
