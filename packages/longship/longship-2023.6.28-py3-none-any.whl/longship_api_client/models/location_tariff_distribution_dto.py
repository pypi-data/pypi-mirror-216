import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="LocationTariffDistributionDto")


@attr.s(auto_attribs=True)
class LocationTariffDistributionDto:
    """
    Attributes:
        valid_from (datetime.datetime):
        id (Union[Unset, str]):
    """

    valid_from: datetime.datetime
    id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        valid_from = self.valid_from.isoformat()

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "validFrom": valid_from,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        valid_from = isoparse(d.pop("validFrom"))

        id = d.pop("id", UNSET)

        location_tariff_distribution_dto = cls(
            valid_from=valid_from,
            id=id,
        )

        location_tariff_distribution_dto.additional_properties = d
        return location_tariff_distribution_dto

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
