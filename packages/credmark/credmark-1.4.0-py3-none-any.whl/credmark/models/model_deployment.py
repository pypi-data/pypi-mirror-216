from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="ModelDeployment")


@attr.s(auto_attribs=True)
class ModelDeployment:
    """
    Attributes:
        name (str): Short identifying name for the model Example: var.
        version (str): The version of the model in this deployment Example: 1.0.0.
        location (str): The location of the model Example: credmark-models-py.
    """

    name: str
    version: str
    location: str

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        version = self.version
        location = self.location

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "version": version,
                "location": location,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        version = d.pop("version")

        location = d.pop("location")

        model_deployment = cls(
            name=name,
            version=version,
            location=location,
        )

        return model_deployment
