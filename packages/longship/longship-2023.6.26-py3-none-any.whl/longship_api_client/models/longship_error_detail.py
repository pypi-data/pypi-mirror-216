from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="LongshipErrorDetail")


@attr.s(auto_attribs=True)
class LongshipErrorDetail:
    """More details about the error.

    Attributes:
        message (Union[Unset, str]): Explains the error.
        reference_id (Union[Unset, str]): When provided, use when contacting support.
    """

    message: Union[Unset, str] = UNSET
    reference_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        message = self.message
        reference_id = self.reference_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if message is not UNSET:
            field_dict["message"] = message
        if reference_id is not UNSET:
            field_dict["referenceId"] = reference_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        message = d.pop("message", UNSET)

        reference_id = d.pop("referenceId", UNSET)

        longship_error_detail = cls(
            message=message,
            reference_id=reference_id,
        )

        longship_error_detail.additional_properties = d
        return longship_error_detail

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
