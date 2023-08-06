import datetime
from io import BytesIO
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, File, FileJsonType, Unset

if TYPE_CHECKING:
    from ..models.entity_tag_header_value import EntityTagHeaderValue


T = TypeVar("T", bound="FileContentResult")


@attr.s(auto_attribs=True)
class FileContentResult:
    """
    Attributes:
        file_contents (Union[Unset, File]):
        content_type (Union[Unset, str]):
        file_download_name (Union[Unset, str]):
        last_modified (Union[Unset, datetime.datetime]):
        entity_tag (Union[Unset, EntityTagHeaderValue]):
        enable_range_processing (Union[Unset, bool]):
    """

    file_contents: Union[Unset, File] = UNSET
    content_type: Union[Unset, str] = UNSET
    file_download_name: Union[Unset, str] = UNSET
    last_modified: Union[Unset, datetime.datetime] = UNSET
    entity_tag: Union[Unset, "EntityTagHeaderValue"] = UNSET
    enable_range_processing: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        file_contents: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.file_contents, Unset):
            file_contents = self.file_contents.to_tuple()

        content_type = self.content_type
        file_download_name = self.file_download_name
        last_modified: Union[Unset, str] = UNSET
        if not isinstance(self.last_modified, Unset):
            last_modified = self.last_modified.isoformat()

        entity_tag: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.entity_tag, Unset):
            entity_tag = self.entity_tag.to_dict()

        enable_range_processing = self.enable_range_processing

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if file_contents is not UNSET:
            field_dict["fileContents"] = file_contents
        if content_type is not UNSET:
            field_dict["contentType"] = content_type
        if file_download_name is not UNSET:
            field_dict["fileDownloadName"] = file_download_name
        if last_modified is not UNSET:
            field_dict["lastModified"] = last_modified
        if entity_tag is not UNSET:
            field_dict["entityTag"] = entity_tag
        if enable_range_processing is not UNSET:
            field_dict["enableRangeProcessing"] = enable_range_processing

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.entity_tag_header_value import EntityTagHeaderValue

        d = src_dict.copy()
        _file_contents = d.pop("fileContents", UNSET)
        file_contents: Union[Unset, File]
        if isinstance(_file_contents, Unset):
            file_contents = UNSET
        else:
            file_contents = File(payload=BytesIO(_file_contents))

        content_type = d.pop("contentType", UNSET)

        file_download_name = d.pop("fileDownloadName", UNSET)

        _last_modified = d.pop("lastModified", UNSET)
        last_modified: Union[Unset, datetime.datetime]
        if isinstance(_last_modified, Unset):
            last_modified = UNSET
        else:
            last_modified = isoparse(_last_modified)

        _entity_tag = d.pop("entityTag", UNSET)
        entity_tag: Union[Unset, EntityTagHeaderValue]
        if isinstance(_entity_tag, Unset):
            entity_tag = UNSET
        else:
            entity_tag = EntityTagHeaderValue.from_dict(_entity_tag)

        enable_range_processing = d.pop("enableRangeProcessing", UNSET)

        file_content_result = cls(
            file_contents=file_contents,
            content_type=content_type,
            file_download_name=file_download_name,
            last_modified=last_modified,
            entity_tag=entity_tag,
            enable_range_processing=enable_range_processing,
        )

        file_content_result.additional_properties = d
        return file_content_result

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
