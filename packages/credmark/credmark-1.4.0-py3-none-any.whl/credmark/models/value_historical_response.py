from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, cast

import attr

if TYPE_CHECKING:
    from ..models.value_historical_item import ValueHistoricalItem


T = TypeVar("T", bound="ValueHistoricalResponse")


@attr.s(auto_attribs=True)
class ValueHistoricalResponse:
    """
    Attributes:
        chain_id (float): Chain ID. Example: 1.
        start_block_number (float): Start block number. Example: 15384120.
        end_block_number (float): End block number. Example: 15581908.
        start_timestamp (float): Start timestamp. Number of seconds since January 1, 1970. Example: 1661086905.
        end_timestamp (float): End timestamp. Number of seconds since January 1, 1970. Example: 1663765199.
        accounts (List[str]): Account addresses Example: ['0x5291fBB0ee9F51225f0928Ff6a83108c86327636'].
        quote_address (str): Quote address is the token/currency of the price units. Example:
            0x0000000000000000000000000000000000000348.
        data (List['ValueHistoricalItem']):
    """

    chain_id: float
    start_block_number: float
    end_block_number: float
    start_timestamp: float
    end_timestamp: float
    accounts: List[str]
    quote_address: str
    data: List["ValueHistoricalItem"]

    def to_dict(self) -> Dict[str, Any]:
        chain_id = self.chain_id
        start_block_number = self.start_block_number
        end_block_number = self.end_block_number
        start_timestamp = self.start_timestamp
        end_timestamp = self.end_timestamp
        accounts = self.accounts

        quote_address = self.quote_address
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()

            data.append(data_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "chainId": chain_id,
                "startBlockNumber": start_block_number,
                "endBlockNumber": end_block_number,
                "startTimestamp": start_timestamp,
                "endTimestamp": end_timestamp,
                "accounts": accounts,
                "quoteAddress": quote_address,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.value_historical_item import ValueHistoricalItem

        d = src_dict.copy()
        chain_id = d.pop("chainId")

        start_block_number = d.pop("startBlockNumber")

        end_block_number = d.pop("endBlockNumber")

        start_timestamp = d.pop("startTimestamp")

        end_timestamp = d.pop("endTimestamp")

        accounts = cast(List[str], d.pop("accounts"))

        quote_address = d.pop("quoteAddress")

        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = ValueHistoricalItem.from_dict(data_item_data)

            data.append(data_item)

        value_historical_response = cls(
            chain_id=chain_id,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            accounts=accounts,
            quote_address=quote_address,
            data=data,
        )

        return value_historical_response
