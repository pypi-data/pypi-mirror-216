from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.local_token_group_token_post_dto import LocalTokenGroupTokenPostDto


T = TypeVar("T", bound="LocalTokenGroupPostDto")


@attr.s(auto_attribs=True)
class LocalTokenGroupPostDto:
    """
    Attributes:
        oucode (Union[Unset, str]):
        token_group_name (Union[Unset, str]):
        target_ou_codes (Union[Unset, List[str]]):
        tokens (Union[Unset, List['LocalTokenGroupTokenPostDto']]):
        target_chargepoint_ids (Union[Unset, List[str]]):
    """

    oucode: Union[Unset, str] = UNSET
    token_group_name: Union[Unset, str] = UNSET
    target_ou_codes: Union[Unset, List[str]] = UNSET
    tokens: Union[Unset, List["LocalTokenGroupTokenPostDto"]] = UNSET
    target_chargepoint_ids: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
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

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
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

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.local_token_group_token_post_dto import LocalTokenGroupTokenPostDto

        d = src_dict.copy()
        oucode = d.pop("oucode", UNSET)

        token_group_name = d.pop("tokenGroupName", UNSET)

        target_ou_codes = cast(List[str], d.pop("targetOUCodes", UNSET))

        tokens = []
        _tokens = d.pop("tokens", UNSET)
        for tokens_item_data in _tokens or []:
            tokens_item = LocalTokenGroupTokenPostDto.from_dict(tokens_item_data)

            tokens.append(tokens_item)

        target_chargepoint_ids = cast(List[str], d.pop("targetChargepointIds", UNSET))

        local_token_group_post_dto = cls(
            oucode=oucode,
            token_group_name=token_group_name,
            target_ou_codes=target_ou_codes,
            tokens=tokens,
            target_chargepoint_ids=target_chargepoint_ids,
        )

        local_token_group_post_dto.additional_properties = d
        return local_token_group_post_dto

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
