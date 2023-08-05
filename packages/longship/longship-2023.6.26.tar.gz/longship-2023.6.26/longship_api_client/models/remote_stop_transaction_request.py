from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="RemoteStopTransactionRequest")


@attr.s(auto_attribs=True)
class RemoteStopTransactionRequest:
    """
    Attributes:
        transaction_id (int):
    """

    transaction_id: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        transaction_id = self.transaction_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "transactionId": transaction_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        transaction_id = d.pop("transactionId")

        remote_stop_transaction_request = cls(
            transaction_id=transaction_id,
        )

        remote_stop_transaction_request.additional_properties = d
        return remote_stop_transaction_request

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
