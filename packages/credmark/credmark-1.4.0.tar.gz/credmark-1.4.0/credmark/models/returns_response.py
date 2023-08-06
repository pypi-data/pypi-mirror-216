from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, cast

import attr

if TYPE_CHECKING:
    from ..models.token_return import TokenReturn


T = TypeVar("T", bound="ReturnsResponse")


@attr.s(auto_attribs=True)
class ReturnsResponse:
    """
    Attributes:
        chain_id (float): Chain ID. Example: 1.
        block_number (float): Block number. Example: 15490034.
        block_timestamp (float): Block timestamp. Number of seconds since January 1, 1970. Example: 1662550007.
        accounts (List[str]): Account addresses Example: ['0x5291fBB0ee9F51225f0928Ff6a83108c86327636'].
        quote_address (str): Quote address is the token/currency of the price units. Example:
            0x0000000000000000000000000000000000000348.
        total_return (float): Total return of the portfolio
        returns (List['TokenReturn']):
    """

    chain_id: float
    block_number: float
    block_timestamp: float
    accounts: List[str]
    quote_address: str
    total_return: float
    returns: List["TokenReturn"]

    def to_dict(self) -> Dict[str, Any]:
        chain_id = self.chain_id
        block_number = self.block_number
        block_timestamp = self.block_timestamp
        accounts = self.accounts

        quote_address = self.quote_address
        total_return = self.total_return
        returns = []
        for returns_item_data in self.returns:
            returns_item = returns_item_data.to_dict()

            returns.append(returns_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "chainId": chain_id,
                "blockNumber": block_number,
                "blockTimestamp": block_timestamp,
                "accounts": accounts,
                "quoteAddress": quote_address,
                "totalReturn": total_return,
                "returns": returns,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.token_return import TokenReturn

        d = src_dict.copy()
        chain_id = d.pop("chainId")

        block_number = d.pop("blockNumber")

        block_timestamp = d.pop("blockTimestamp")

        accounts = cast(List[str], d.pop("accounts"))

        quote_address = d.pop("quoteAddress")

        total_return = d.pop("totalReturn")

        returns = []
        _returns = d.pop("returns")
        for returns_item_data in _returns:
            returns_item = TokenReturn.from_dict(returns_item_data)

            returns.append(returns_item)

        returns_response = cls(
            chain_id=chain_id,
            block_number=block_number,
            block_timestamp=block_timestamp,
            accounts=accounts,
            quote_address=quote_address,
            total_return=total_return,
            returns=returns,
        )

        return returns_response
