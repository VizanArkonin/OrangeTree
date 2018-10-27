from enum import Enum


class PacketStatus(Enum):
    """
    Brief enum class to define packet request statuses
    """
    REQUESTED = "requested"
    SUCCESS = "success"
    FAILED = "failed"
    ACCEPTED = "accepted"
    DENIED = "denied"

