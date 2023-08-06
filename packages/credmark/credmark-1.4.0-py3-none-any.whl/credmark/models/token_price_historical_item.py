from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="TokenPriceHistoricalItem")


@attr.s(auto_attribs=True)
class TokenPriceHistoricalItem:
    """
    Attributes:
        block_number (float): Block number. Example: 15490034.
        block_timestamp (float): Block timestamp. Number of seconds since January 1, 1970. Example: 1662550007.
        price (float): Price of the token in quote units. Example: 82.82911921.
        src (str): Source of the token price. Example: dex or cex.
        src_internal (str): The internal source for tracing Example: db, model, cache, etc..
    """

    block_number: float
    block_timestamp: float
    price: float
    src: str
    src_internal: str

    def to_dict(self) -> Dict[str, Any]:
        block_number = self.block_number
        block_timestamp = self.block_timestamp
        price = self.price
        src = self.src
        src_internal = self.src_internal

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "blockNumber": block_number,
                "blockTimestamp": block_timestamp,
                "price": price,
                "src": src,
                "srcInternal": src_internal,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        block_number = d.pop("blockNumber")

        block_timestamp = d.pop("blockTimestamp")

        price = d.pop("price")

        src = d.pop("src")

        src_internal = d.pop("srcInternal")

        token_price_historical_item = cls(
            block_number=block_number,
            block_timestamp=block_timestamp,
            price=price,
            src=src,
            src_internal=src_internal,
        )

        return token_price_historical_item
