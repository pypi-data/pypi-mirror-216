from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, cast

import attr

if TYPE_CHECKING:
    from ..models.position_historical_item import PositionHistoricalItem


T = TypeVar("T", bound="PositionsHistoricalResponse")


@attr.s(auto_attribs=True)
class PositionsHistoricalResponse:
    """
    Attributes:
        chain_id (float): Chain ID. Example: 1.
        start_block_number (float): Start block number. Example: 15384120.
        end_block_number (float): End block number. Example: 15581908.
        start_timestamp (float): Start timestamp. Number of seconds since January 1, 1970. Example: 1661086905.
        end_timestamp (float): End timestamp. Number of seconds since January 1, 1970. Example: 1663765199.
        accounts (List[str]): Account addresses Example: ['0x5291fBB0ee9F51225f0928Ff6a83108c86327636'].
        data (List['PositionHistoricalItem']):
    """

    chain_id: float
    start_block_number: float
    end_block_number: float
    start_timestamp: float
    end_timestamp: float
    accounts: List[str]
    data: List["PositionHistoricalItem"]

    def to_dict(self) -> Dict[str, Any]:
        chain_id = self.chain_id
        start_block_number = self.start_block_number
        end_block_number = self.end_block_number
        start_timestamp = self.start_timestamp
        end_timestamp = self.end_timestamp
        accounts = self.accounts

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
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.position_historical_item import PositionHistoricalItem

        d = src_dict.copy()
        chain_id = d.pop("chainId")

        start_block_number = d.pop("startBlockNumber")

        end_block_number = d.pop("endBlockNumber")

        start_timestamp = d.pop("startTimestamp")

        end_timestamp = d.pop("endTimestamp")

        accounts = cast(List[str], d.pop("accounts"))

        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = PositionHistoricalItem.from_dict(data_item_data)

            data.append(data_item)

        positions_historical_response = cls(
            chain_id=chain_id,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            accounts=accounts,
            data=data,
        )

        return positions_historical_response
