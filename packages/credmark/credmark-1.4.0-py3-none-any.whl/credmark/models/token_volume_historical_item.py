from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="TokenVolumeHistoricalItem")


@attr.s(auto_attribs=True)
class TokenVolumeHistoricalItem:
    """
    Attributes:
        start_block_number (float): Start block number. Example: 15384120.
        end_block_number (float): End block number. Example: 15581908.
        start_timestamp (float): Start timestamp. Number of seconds since January 1, 1970. Example: 1661086905.
        end_timestamp (float): End timestamp. Number of seconds since January 1, 1970. Example: 1663765199.
        volume (float): Token volume Example: 16173531.8220335.
    """

    start_block_number: float
    end_block_number: float
    start_timestamp: float
    end_timestamp: float
    volume: float

    def to_dict(self) -> Dict[str, Any]:
        start_block_number = self.start_block_number
        end_block_number = self.end_block_number
        start_timestamp = self.start_timestamp
        end_timestamp = self.end_timestamp
        volume = self.volume

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "startBlockNumber": start_block_number,
                "endBlockNumber": end_block_number,
                "startTimestamp": start_timestamp,
                "endTimestamp": end_timestamp,
                "volume": volume,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        start_block_number = d.pop("startBlockNumber")

        end_block_number = d.pop("endBlockNumber")

        start_timestamp = d.pop("startTimestamp")

        end_timestamp = d.pop("endTimestamp")

        volume = d.pop("volume")

        token_volume_historical_item = cls(
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            volume=volume,
        )

        return token_volume_historical_item
