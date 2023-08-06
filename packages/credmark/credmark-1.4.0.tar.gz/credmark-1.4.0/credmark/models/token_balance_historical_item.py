from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="TokenBalanceHistoricalItem")


@attr.s(auto_attribs=True)
class TokenBalanceHistoricalItem:
    """
    Attributes:
        block_number (float): Block number. Example: 15490034.
        block_timestamp (float): Block timestamp. Number of seconds since January 1, 1970. Example: 1662550007.
        balance (float): Token balance Example: 248367.58266143446.
        value (float): Token value in quoted currency. Example: 18990392.724937014.
    """

    block_number: float
    block_timestamp: float
    balance: float
    value: float

    def to_dict(self) -> Dict[str, Any]:
        block_number = self.block_number
        block_timestamp = self.block_timestamp
        balance = self.balance
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "blockNumber": block_number,
                "blockTimestamp": block_timestamp,
                "balance": balance,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        block_number = d.pop("blockNumber")

        block_timestamp = d.pop("blockTimestamp")

        balance = d.pop("balance")

        value = d.pop("value")

        token_balance_historical_item = cls(
            block_number=block_number,
            block_timestamp=block_timestamp,
            balance=balance,
            value=value,
        )

        return token_balance_historical_item
