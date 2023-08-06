from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="ModelRuntimeStatistics")


@attr.s(auto_attribs=True)
class ModelRuntimeStatistics:
    """
    Attributes:
        slug (str): Short identifying name for the model Example: var.
        version (str): Version of the model Example: 1.0.
        min (float): Minimum model runtime in milliseconds
        max (float): Maximum model runtime in milliseconds
        mean (float): Mean (average) model runtime in milliseconds
        median (float): Median model runtime in milliseconds
    """

    slug: str
    version: str
    min: float
    max: float
    mean: float
    median: float

    def to_dict(self) -> Dict[str, Any]:
        slug = self.slug
        version = self.version
        min = self.min
        max = self.max
        mean = self.mean
        median = self.median

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "slug": slug,
                "version": version,
                "min": min,
                "max": max,
                "mean": mean,
                "median": median,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        slug = d.pop("slug")

        version = d.pop("version")

        min = d.pop("min")

        max = d.pop("max")

        mean = d.pop("mean")

        median = d.pop("median")

        model_runtime_statistics = cls(
            slug=slug,
            version=version,
            min=min,
            max=max,
            mean=mean,
            median=median,
        )

        return model_runtime_statistics
