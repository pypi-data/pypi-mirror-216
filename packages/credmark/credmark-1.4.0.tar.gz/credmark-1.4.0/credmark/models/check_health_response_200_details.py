from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.check_health_response_200_details_additional_property import (
        CheckHealthResponse200DetailsAdditionalProperty,
    )


T = TypeVar("T", bound="CheckHealthResponse200Details")


@attr.s(auto_attribs=True)
class CheckHealthResponse200Details:
    """
    Example:
        {'database': {'status': 'up'}}

    """

    additional_properties: Dict[str, "CheckHealthResponse200DetailsAdditionalProperty"] = attr.ib(
        init=False, factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        pass

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.check_health_response_200_details_additional_property import (
            CheckHealthResponse200DetailsAdditionalProperty,
        )

        d = src_dict.copy()
        check_health_response_200_details = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = CheckHealthResponse200DetailsAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        check_health_response_200_details.additional_properties = additional_properties
        return check_health_response_200_details

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "CheckHealthResponse200DetailsAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "CheckHealthResponse200DetailsAdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
