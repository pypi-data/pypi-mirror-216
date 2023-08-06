import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.local_token_group_token_get_dto import LocalTokenGroupTokenGetDto


T = TypeVar("T", bound="LocalTokenGroupGetDto")


@attr.s(auto_attribs=True)
class LocalTokenGroupGetDto:
    """
    Attributes:
        id (Union[Unset, str]):
        oucode (Union[Unset, str]):
        token_group_name (Union[Unset, str]):
        target_ou_codes (Union[Unset, List[str]]):
        tokens (Union[Unset, List['LocalTokenGroupTokenGetDto']]):
        target_chargepoint_ids (Union[Unset, List[str]]):
        created (Union[Unset, datetime.datetime]):
        updated (Union[Unset, datetime.datetime]):
    """

    id: Union[Unset, str] = UNSET
    oucode: Union[Unset, str] = UNSET
    token_group_name: Union[Unset, str] = UNSET
    target_ou_codes: Union[Unset, List[str]] = UNSET
    tokens: Union[Unset, List["LocalTokenGroupTokenGetDto"]] = UNSET
    target_chargepoint_ids: Union[Unset, List[str]] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    updated: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        oucode = self.oucode
        token_group_name = self.token_group_name
        target_ou_codes: Union[Unset, List[str]] = UNSET
        if not isinstance(self.target_ou_codes, Unset):
            target_ou_codes = self.target_ou_codes

        tokens: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.tokens, Unset):
            tokens = []
            for tokens_item_data in self.tokens:
                tokens_item = tokens_item_data.to_dict()

                tokens.append(tokens_item)

        target_chargepoint_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.target_chargepoint_ids, Unset):
            target_chargepoint_ids = self.target_chargepoint_ids

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        updated: Union[Unset, str] = UNSET
        if not isinstance(self.updated, Unset):
            updated = self.updated.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if oucode is not UNSET:
            field_dict["oucode"] = oucode
        if token_group_name is not UNSET:
            field_dict["tokenGroupName"] = token_group_name
        if target_ou_codes is not UNSET:
            field_dict["targetOUCodes"] = target_ou_codes
        if tokens is not UNSET:
            field_dict["tokens"] = tokens
        if target_chargepoint_ids is not UNSET:
            field_dict["targetChargepointIds"] = target_chargepoint_ids
        if created is not UNSET:
            field_dict["created"] = created
        if updated is not UNSET:
            field_dict["updated"] = updated

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.local_token_group_token_get_dto import LocalTokenGroupTokenGetDto

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        oucode = d.pop("oucode", UNSET)

        token_group_name = d.pop("tokenGroupName", UNSET)

        target_ou_codes = cast(List[str], d.pop("targetOUCodes", UNSET))

        tokens = []
        _tokens = d.pop("tokens", UNSET)
        for tokens_item_data in _tokens or []:
            tokens_item = LocalTokenGroupTokenGetDto.from_dict(tokens_item_data)

            tokens.append(tokens_item)

        target_chargepoint_ids = cast(List[str], d.pop("targetChargepointIds", UNSET))

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        _updated = d.pop("updated", UNSET)
        updated: Union[Unset, datetime.datetime]
        if isinstance(_updated, Unset):
            updated = UNSET
        else:
            updated = isoparse(_updated)

        local_token_group_get_dto = cls(
            id=id,
            oucode=oucode,
            token_group_name=token_group_name,
            target_ou_codes=target_ou_codes,
            tokens=tokens,
            target_chargepoint_ids=target_chargepoint_ids,
            created=created,
            updated=updated,
        )

        local_token_group_get_dto.additional_properties = d
        return local_token_group_get_dto

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
