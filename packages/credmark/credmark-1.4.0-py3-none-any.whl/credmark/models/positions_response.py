from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, cast

import attr

if TYPE_CHECKING:
    from ..models.position import Position


T = TypeVar("T", bound="PositionsResponse")


@attr.s(auto_attribs=True)
class PositionsResponse:
    """
    Attributes:
        chain_id (float): Chain ID. Example: 1.
        block_number (float): Block number. Example: 15490034.
        block_timestamp (float): Block timestamp. Number of seconds since January 1, 1970. Example: 1662550007.
        accounts (List[str]): Account addresses Example: ['0x5291fBB0ee9F51225f0928Ff6a83108c86327636'].
        positions (List['Position']):
    """

    chain_id: float
    block_number: float
    block_timestamp: float
    accounts: List[str]
    positions: List["Position"]

    def to_dict(self) -> Dict[str, Any]:
        chain_id = self.chain_id
        block_number = self.block_number
        block_timestamp = self.block_timestamp
        accounts = self.accounts

        positions = []
        for positions_item_data in self.positions:
            positions_item = positions_item_data.to_dict()

            positions.append(positions_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "chainId": chain_id,
                "blockNumber": block_number,
                "blockTimestamp": block_timestamp,
                "accounts": accounts,
                "positions": positions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.position import Position

        d = src_dict.copy()
        chain_id = d.pop("chainId")

        block_number = d.pop("blockNumber")

        block_timestamp = d.pop("blockTimestamp")

        accounts = cast(List[str], d.pop("accounts"))

        positions = []
        _positions = d.pop("positions")
        for positions_item_data in _positions:
            positions_item = Position.from_dict(positions_item_data)

            positions.append(positions_item)

        positions_response = cls(
            chain_id=chain_id,
            block_number=block_number,
            block_timestamp=block_timestamp,
            accounts=accounts,
            positions=positions,
        )

        return positions_response
