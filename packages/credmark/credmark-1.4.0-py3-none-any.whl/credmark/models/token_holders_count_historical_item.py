from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="TokenHoldersCountHistoricalItem")


@attr.s(auto_attribs=True)
class TokenHoldersCountHistoricalItem:
    """
    Attributes:
        block_number (float): Block number. Example: 15490034.
        block_timestamp (float): Block timestamp. Number of seconds since January 1, 1970. Example: 1662550007.
        count (float): Total number of holders Example: 42.
    """

    block_number: float
    block_timestamp: float
    count: float

    def to_dict(self) -> Dict[str, Any]:
        block_number = self.block_number
        block_timestamp = self.block_timestamp
        count = self.count

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "blockNumber": block_number,
                "blockTimestamp": block_timestamp,
                "count": count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        block_number = d.pop("blockNumber")

        block_timestamp = d.pop("blockTimestamp")

        count = d.pop("count")

        token_holders_count_historical_item = cls(
            block_number=block_number,
            block_timestamp=block_timestamp,
            count=count,
        )

        return token_holders_count_historical_item
