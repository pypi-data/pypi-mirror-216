from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.model_runtime_statistics import ModelRuntimeStatistics


T = TypeVar("T", bound="ModelRuntimeStatsResponse")


@attr.s(auto_attribs=True)
class ModelRuntimeStatsResponse:
    """
    Attributes:
        runtimes (List['ModelRuntimeStatistics']):
    """

    runtimes: List["ModelRuntimeStatistics"]

    def to_dict(self) -> Dict[str, Any]:
        runtimes = []
        for runtimes_item_data in self.runtimes:
            runtimes_item = runtimes_item_data.to_dict()

            runtimes.append(runtimes_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "runtimes": runtimes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_runtime_statistics import ModelRuntimeStatistics

        d = src_dict.copy()
        runtimes = []
        _runtimes = d.pop("runtimes")
        for runtimes_item_data in _runtimes:
            runtimes_item = ModelRuntimeStatistics.from_dict(runtimes_item_data)

            runtimes.append(runtimes_item)

        model_runtime_stats_response = cls(
            runtimes=runtimes,
        )

        return model_runtime_stats_response
