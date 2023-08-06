from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.token_value import TokenValue


T = TypeVar("T", bound="ValueHistoricalItem")


@attr.s(auto_attribs=True)
class ValueHistoricalItem:
    """
    Attributes:
        block_number (float): Block number. Example: 15490034.
        block_timestamp (float): Block timestamp. Number of seconds since January 1, 1970. Example: 1662550007.
        value (float): Portfolio value in quoted currency. Example: 18990392.724937014.
        positions (List['TokenValue']):
    """

    block_number: float
    block_timestamp: float
    value: float
    positions: List["TokenValue"]

    def to_dict(self) -> Dict[str, Any]:
        block_number = self.block_number
        block_timestamp = self.block_timestamp
        value = self.value
        positions = []
        for positions_item_data in self.positions:
            positions_item = positions_item_data.to_dict()

            positions.append(positions_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "blockNumber": block_number,
                "blockTimestamp": block_timestamp,
                "value": value,
                "positions": positions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.token_value import TokenValue

        d = src_dict.copy()
        block_number = d.pop("blockNumber")

        block_timestamp = d.pop("blockTimestamp")

        value = d.pop("value")

        positions = []
        _positions = d.pop("positions")
        for positions_item_data in _positions:
            positions_item = TokenValue.from_dict(positions_item_data)

            positions.append(positions_item)

        value_historical_item = cls(
            block_number=block_number,
            block_timestamp=block_timestamp,
            value=value,
            positions=positions,
        )

        return value_historical_item
