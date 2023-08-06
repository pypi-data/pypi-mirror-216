from enum import Enum


class WebhookPutDtoEventTypesItem(str, Enum):
    CHARGEPOINT_BOOTED = "CHARGEPOINT_BOOTED"
    CONNECTIVITY_STATUS = "CONNECTIVITY_STATUS"
    OPERATIONAL_STATUS = "OPERATIONAL_STATUS"
    PING = "PING"
    SESSION_START = "SESSION_START"
    SESSION_STOP = "SESSION_STOP"
    SESSION_UPDATE = "SESSION_UPDATE"

    def __str__(self) -> str:
        return str(self.value)
