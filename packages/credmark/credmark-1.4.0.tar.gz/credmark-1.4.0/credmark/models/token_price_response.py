from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="TokenPriceResponse")


@attr.s(auto_attribs=True)
class TokenPriceResponse:
    """
    Attributes:
        chain_id (float): Chain ID. Example: 1.
        block_number (float): Block number. Example: 15490034.
        block_timestamp (float): Block timestamp. Number of seconds since January 1, 1970. Example: 1662550007.
        token_address (str): Token address for the price. Example: 0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9.
        quote_address (str): Quote address is the token/currency of the price units. Example:
            0x0000000000000000000000000000000000000348.
        price (float): Price of the token in quote units. Example: 82.82911921.
        src (str): Source of the token price. Example: dex or cex.
        src_internal (str): The internal source for tracing Example: db, model, cache, etc..
    """

    chain_id: float
    block_number: float
    block_timestamp: float
    token_address: str
    quote_address: str
    price: float
    src: str
    src_internal: str

    def to_dict(self) -> Dict[str, Any]:
        chain_id = self.chain_id
        block_number = self.block_number
        block_timestamp = self.block_timestamp
        token_address = self.token_address
        quote_address = self.quote_address
        price = self.price
        src = self.src
        src_internal = self.src_internal

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "chainId": chain_id,
                "blockNumber": block_number,
                "blockTimestamp": block_timestamp,
                "tokenAddress": token_address,
                "quoteAddress": quote_address,
                "price": price,
                "src": src,
                "srcInternal": src_internal,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        chain_id = d.pop("chainId")

        block_number = d.pop("blockNumber")

        block_timestamp = d.pop("blockTimestamp")

        token_address = d.pop("tokenAddress")

        quote_address = d.pop("quoteAddress")

        price = d.pop("price")

        src = d.pop("src")

        src_internal = d.pop("srcInternal")

        token_price_response = cls(
            chain_id=chain_id,
            block_number=block_number,
            block_timestamp=block_timestamp,
            token_address=token_address,
            quote_address=quote_address,
            price=price,
            src=src,
            src_internal=src_internal,
        )

        return token_price_response
