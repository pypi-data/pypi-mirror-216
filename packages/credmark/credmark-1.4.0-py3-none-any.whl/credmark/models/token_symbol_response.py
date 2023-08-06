from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="TokenSymbolResponse")


@attr.s(auto_attribs=True)
class TokenSymbolResponse:
    """
    Attributes:
        chain_id (float): Chain ID. Example: 1.
        block_number (float): Block number. Example: 15490034.
        block_timestamp (float): Block timestamp. Number of seconds since January 1, 1970. Example: 1662550007.
        token_address (str): Token address for the price. Example: 0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9.
        symbol (str): Token symbol Example: AAVE.
    """

    chain_id: float
    block_number: float
    block_timestamp: float
    token_address: str
    symbol: str

    def to_dict(self) -> Dict[str, Any]:
        chain_id = self.chain_id
        block_number = self.block_number
        block_timestamp = self.block_timestamp
        token_address = self.token_address
        symbol = self.symbol

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "chainId": chain_id,
                "blockNumber": block_number,
                "blockTimestamp": block_timestamp,
                "tokenAddress": token_address,
                "symbol": symbol,
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

        symbol = d.pop("symbol")

        token_symbol_response = cls(
            chain_id=chain_id,
            block_number=block_number,
            block_timestamp=block_timestamp,
            token_address=token_address,
            symbol=symbol,
        )

        return token_symbol_response
