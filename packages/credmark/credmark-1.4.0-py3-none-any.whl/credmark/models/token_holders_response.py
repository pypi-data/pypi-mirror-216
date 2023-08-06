from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.token_holder import TokenHolder


T = TypeVar("T", bound="TokenHoldersResponse")


@attr.s(auto_attribs=True)
class TokenHoldersResponse:
    """
    Attributes:
        chain_id (float): Chain ID. Example: 1.
        block_number (float): Block number. Example: 15490034.
        block_timestamp (float): Block timestamp. Number of seconds since January 1, 1970. Example: 1662550007.
        token_address (str): Token address for the price. Example: 0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9.
        scaled (bool): If the holders' balance is scaled by token decimals. Example: True.
        quote_address (str): Quote address is the token/currency of the price units. Example:
            0x0000000000000000000000000000000000000348.
        data (List['TokenHolder']): Paginated list of holders
        total (float): Total number of holders Example: 10.
        cursor (Union[Unset, str]): Cursor to fetch the next page
    """

    chain_id: float
    block_number: float
    block_timestamp: float
    token_address: str
    scaled: bool
    quote_address: str
    data: List["TokenHolder"]
    total: float
    cursor: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        chain_id = self.chain_id
        block_number = self.block_number
        block_timestamp = self.block_timestamp
        token_address = self.token_address
        scaled = self.scaled
        quote_address = self.quote_address
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()

            data.append(data_item)

        total = self.total
        cursor = self.cursor

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "chainId": chain_id,
                "blockNumber": block_number,
                "blockTimestamp": block_timestamp,
                "tokenAddress": token_address,
                "scaled": scaled,
                "quoteAddress": quote_address,
                "data": data,
                "total": total,
            }
        )
        if cursor is not UNSET:
            field_dict["cursor"] = cursor

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.token_holder import TokenHolder

        d = src_dict.copy()
        chain_id = d.pop("chainId")

        block_number = d.pop("blockNumber")

        block_timestamp = d.pop("blockTimestamp")

        token_address = d.pop("tokenAddress")

        scaled = d.pop("scaled")

        quote_address = d.pop("quoteAddress")

        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = TokenHolder.from_dict(data_item_data)

            data.append(data_item)

        total = d.pop("total")

        cursor = d.pop("cursor", UNSET)

        token_holders_response = cls(
            chain_id=chain_id,
            block_number=block_number,
            block_timestamp=block_timestamp,
            token_address=token_address,
            scaled=scaled,
            quote_address=quote_address,
            data=data,
            total=total,
            cursor=cursor,
        )

        return token_holders_response
