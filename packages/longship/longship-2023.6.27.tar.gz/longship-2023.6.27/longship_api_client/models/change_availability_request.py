from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.change_availability_request_type import ChangeAvailabilityRequestType

T = TypeVar("T", bound="ChangeAvailabilityRequest")


@attr.s(auto_attribs=True)
class ChangeAvailabilityRequest:
    """
    Attributes:
        connector_id (int):
        type (ChangeAvailabilityRequestType):  Default: ChangeAvailabilityRequestType.INOPERATIVE.
    """

    connector_id: int
    type: ChangeAvailabilityRequestType = ChangeAvailabilityRequestType.INOPERATIVE
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        connector_id = self.connector_id
        type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "connectorId": connector_id,
                "type": type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        connector_id = d.pop("connectorId")

        type = ChangeAvailabilityRequestType(d.pop("type"))

        change_availability_request = cls(
            connector_id=connector_id,
            type=type,
        )

        change_availability_request.additional_properties = d
        return change_availability_request

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
