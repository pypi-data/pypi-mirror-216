import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ChargingPeriodDto")


@attr.s(auto_attribs=True)
class ChargingPeriodDto:
    """
    Attributes:
        timestamp (Union[Unset, datetime.datetime]):
        delta_kwh (Union[Unset, float]):
        absolute_kwh (Union[Unset, float]):
        price (Union[Unset, float]):
    """

    timestamp: Union[Unset, datetime.datetime] = UNSET
    delta_kwh: Union[Unset, float] = UNSET
    absolute_kwh: Union[Unset, float] = UNSET
    price: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        timestamp: Union[Unset, str] = UNSET
        if not isinstance(self.timestamp, Unset):
            timestamp = self.timestamp.isoformat()

        delta_kwh = self.delta_kwh
        absolute_kwh = self.absolute_kwh
        price = self.price

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if delta_kwh is not UNSET:
            field_dict["deltaKwh"] = delta_kwh
        if absolute_kwh is not UNSET:
            field_dict["absoluteKwh"] = absolute_kwh
        if price is not UNSET:
            field_dict["price"] = price

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _timestamp = d.pop("timestamp", UNSET)
        timestamp: Union[Unset, datetime.datetime]
        if isinstance(_timestamp, Unset):
            timestamp = UNSET
        else:
            timestamp = isoparse(_timestamp)

        delta_kwh = d.pop("deltaKwh", UNSET)

        absolute_kwh = d.pop("absoluteKwh", UNSET)

        price = d.pop("price", UNSET)

        charging_period_dto = cls(
            timestamp=timestamp,
            delta_kwh=delta_kwh,
            absolute_kwh=absolute_kwh,
            price=price,
        )

        charging_period_dto.additional_properties = d
        return charging_period_dto

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
