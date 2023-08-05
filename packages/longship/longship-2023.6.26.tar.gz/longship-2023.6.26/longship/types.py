from enum import Enum
from typing import Union

import attr

from longship_api_client.models.chargepoint_dto_connectivity_status import ChargepointDtoConnectivityStatus
from longship_api_client.models.connector_operational_status_dto_operational_status import (
    ConnectorOperationalStatusDtoOperationalStatus,
)


class WebhookPayloadType(str, Enum):
    ChargePointBooted = "ChargePointBooted"
    OperationalStatusChanged = "OperationalStatusChanged"
    ConnectivityStatusChanged = "ConnectivityStatusChanged"
    SessionStart = "SessionStart"
    SessionUpdate = "SessionUpdate"
    SessionStop = "SessionStop"

    def __str__(self) -> str:
        return str(self.value)


class RegistrationStatusType(str, Enum):
    Accepted = "Accepted"
    Pending = "Pending"

    def __str__(self) -> str:
        return str(self.value)


@attr.s(auto_attribs=True)
class ChargePointBootedData:
    registrationstatus: RegistrationStatusType


@attr.s(auto_attribs=True)
class OperationalStatusChangedData:
    status: ConnectorOperationalStatusDtoOperationalStatus
    errorcode: str
    connectornumber: int
    locationid: str
    evseid: str
    statussource: str


@attr.s(auto_attribs=True)
class ConnectivityStatusChangedData:
    # TODO: Longship uses uppercase for the status, but the webhook response uses CamelCase
    status: ChargepointDtoConnectivityStatus


@attr.s(auto_attribs=True)
class SessionStartData:
    chargepointid: str
    connectornumber: int


@attr.s(auto_attribs=True)
class SessionUpdateData:
    chargepointid: str
    connectornumber: int
    totalenergyinkwh: float
    totalduration: str
    totalcosts: float


@attr.s(auto_attribs=True)
class SessionStopData(SessionUpdateData):
    pass


@attr.s(auto_attribs=True)
class WebhookPayload:
    specversion: str
    id: str
    type: WebhookPayloadType
    subject: str
    time: str
    source: str
    datacontenttype: str
    data: Union[
        ChargePointBootedData,
        OperationalStatusChangedData,
        ConnectivityStatusChangedData,
        SessionStartData,
        SessionUpdateData,
        SessionStopData,
    ]

    def __attrs_post_init__(self):
        if self.type == WebhookPayloadType.ChargePointBooted:
            self.data = ChargePointBootedData(**self.data)
        elif self.type == WebhookPayloadType.OperationalStatusChanged:
            self.data = OperationalStatusChangedData(**self.data)
        elif self.type == WebhookPayloadType.ConnectivityStatusChanged:
            self.data['status'] = self.data['status'].upper()
            self.data = ConnectivityStatusChangedData(**self.data)
        elif self.type == WebhookPayloadType.SessionStart:
            self.data = SessionStartData(**self.data)
        elif self.type == WebhookPayloadType.SessionUpdate:
            self.data = SessionUpdateData(**self.data)
        elif self.type == WebhookPayloadType.SessionStop:
            self.data = SessionStopData(**self.data)
