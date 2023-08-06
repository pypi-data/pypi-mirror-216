from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="VideoPublic")


@attr.s(auto_attribs=True)
class VideoPublic:
    """
    Attributes:
        id (str):
        caption (str):
        filename (str):
    """

    id: str
    caption: str
    filename: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        caption = self.caption
        filename = self.filename

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "caption": caption,
                "filename": filename,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        caption = d.pop("caption")

        filename = d.pop("filename")

        video_public = cls(
            id=id,
            caption=caption,
            filename=filename,
        )

        video_public.additional_properties = d
        return video_public

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
