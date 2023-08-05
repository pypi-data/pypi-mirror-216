from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chargepoint_connector_dto import ChargepointConnectorDto


T = TypeVar("T", bound="ChargepointEVSEDto")


@attr.s(auto_attribs=True)
class ChargepointEVSEDto:
    """
    Attributes:
        evse_id (Union[Unset, str]):
        connectors (Union[Unset, List['ChargepointConnectorDto']]):
    """

    evse_id: Union[Unset, str] = UNSET
    connectors: Union[Unset, List["ChargepointConnectorDto"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        evse_id = self.evse_id
        connectors: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.connectors, Unset):
            connectors = []
            for connectors_item_data in self.connectors:
                connectors_item = connectors_item_data.to_dict()

                connectors.append(connectors_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if evse_id is not UNSET:
            field_dict["evse_id"] = evse_id
        if connectors is not UNSET:
            field_dict["connectors"] = connectors

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.chargepoint_connector_dto import ChargepointConnectorDto

        d = src_dict.copy()
        evse_id = d.pop("evse_id", UNSET)

        connectors = []
        _connectors = d.pop("connectors", UNSET)
        for connectors_item_data in _connectors or []:
            connectors_item = ChargepointConnectorDto.from_dict(connectors_item_data)

            connectors.append(connectors_item)

        chargepoint_evse_dto = cls(
            evse_id=evse_id,
            connectors=connectors,
        )

        chargepoint_evse_dto.additional_properties = d
        return chargepoint_evse_dto

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
