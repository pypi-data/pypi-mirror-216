from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.image_dto import ImageDto


T = TypeVar("T", bound="BusinessDetailsDto")


@attr.s(auto_attribs=True)
class BusinessDetailsDto:
    """
    Attributes:
        name (Union[Unset, str]):
        website (Union[Unset, str]):
        image (Union[Unset, ImageDto]):
    """

    name: Union[Unset, str] = UNSET
    website: Union[Unset, str] = UNSET
    image: Union[Unset, "ImageDto"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        website = self.website
        image: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.image, Unset):
            image = self.image.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if website is not UNSET:
            field_dict["website"] = website
        if image is not UNSET:
            field_dict["image"] = image

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.image_dto import ImageDto

        d = src_dict.copy()
        name = d.pop("name", UNSET)

        website = d.pop("website", UNSET)

        _image = d.pop("image", UNSET)
        image: Union[Unset, ImageDto]
        if isinstance(_image, Unset):
            image = UNSET
        else:
            image = ImageDto.from_dict(_image)

        business_details_dto = cls(
            name=name,
            website=website,
            image=image,
        )

        business_details_dto.additional_properties = d
        return business_details_dto

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
