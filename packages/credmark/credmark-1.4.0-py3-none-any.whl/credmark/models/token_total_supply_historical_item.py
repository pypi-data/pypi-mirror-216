from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="TokenTotalSupplyHistoricalItem")


@attr.s(auto_attribs=True)
class TokenTotalSupplyHistoricalItem:
    """
    Attributes:
        block_number (float): Block number. Example: 15490034.
        block_timestamp (float): Block timestamp. Number of seconds since January 1, 1970. Example: 1662550007.
        total_supply (float): Token total supply Example: 16000000.
    """

    block_number: float
    block_timestamp: float
    total_supply: float

    def to_dict(self) -> Dict[str, Any]:
        block_number = self.block_number
        block_timestamp = self.block_timestamp
        total_supply = self.total_supply

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "blockNumber": block_number,
                "blockTimestamp": block_timestamp,
                "totalSupply": total_supply,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        block_number = d.pop("blockNumber")

        block_timestamp = d.pop("blockTimestamp")

        total_supply = d.pop("totalSupply")

        token_total_supply_historical_item = cls(
            block_number=block_number,
            block_timestamp=block_timestamp,
            total_supply=total_supply,
        )

        return token_total_supply_historical_item
